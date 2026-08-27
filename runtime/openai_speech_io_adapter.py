from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Optional

from runtime.speech_io_adapter import (
    SpeechToTextRequest,
    SpeechToTextResult,
    TextToSpeechRequest,
    TextToSpeechResult,
)


class OpenAISpeechIOAdapter:
    """OpenAI-backed STT/TTS adapter for shadow validation.

    This adapter owns transport only. It does not own XiaoAi persona, memory,
    identity, permissions, safety policy, session state, or runtime decisions.

    Required environment for live use:
      OPENAI_API_KEY
      OPENAI_STT_MODEL
      OPENAI_TTS_MODEL
      OPENAI_TTS_VOICE

    Optional environment:
      OPENAI_BASE_URL
      XIAOAI_AUDIO_OUTPUT_DIR

    A client may be injected for tests. No production activation is implied by
    constructing this adapter; callers decide whether it is used in shadow mode.
    """

    provider_name = "openai"

    def __init__(
        self,
        *,
        client: Any | None = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        stt_model: Optional[str] = None,
        tts_model: Optional[str] = None,
        tts_voice: Optional[str] = None,
        output_dir: Optional[str] = None,
    ) -> None:
        self.stt_model = stt_model or os.environ.get("OPENAI_STT_MODEL", "").strip()
        self.tts_model = tts_model or os.environ.get("OPENAI_TTS_MODEL", "").strip()
        self.tts_voice = tts_voice or os.environ.get("OPENAI_TTS_VOICE", "").strip()
        self.output_dir = Path(
            output_dir or os.environ.get("XIAOAI_AUDIO_OUTPUT_DIR", "").strip() or ".xiaoai-audio"
        )

        if not self.stt_model:
            raise RuntimeError("OPENAI_STT_MODEL is required for live XiaoAi STT use.")
        if not self.tts_model:
            raise RuntimeError("OPENAI_TTS_MODEL is required for live XiaoAi TTS use.")
        if not self.tts_voice:
            raise RuntimeError("OPENAI_TTS_VOICE is required for live XiaoAi TTS use.")

        if client is not None:
            self._client = client
            return

        resolved_api_key = api_key or os.environ.get("OPENAI_API_KEY", "").strip()
        resolved_base_url = base_url or os.environ.get("OPENAI_BASE_URL", "").strip() or None
        if not resolved_api_key:
            raise RuntimeError("OPENAI_API_KEY is required for live XiaoAi speech use.")

        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError(
                "The official 'openai' Python package is required for OpenAISpeechIOAdapter."
            ) from exc

        kwargs: dict[str, object] = {"api_key": resolved_api_key}
        if resolved_base_url:
            kwargs["base_url"] = resolved_base_url
        self._client = OpenAI(**kwargs)

    def transcribe(self, request: SpeechToTextRequest) -> SpeechToTextResult:
        audio_path = Path(request.audio_ref)
        if not audio_path.is_file():
            raise RuntimeError("speech_to_text_audio_ref_not_local_file")

        with audio_path.open("rb") as audio_file:
            response = self._client.audio.transcriptions.create(
                model=self.stt_model,
                file=audio_file,
                **({"language": request.language_hint} if request.language_hint else {}),
            )

        text = str(getattr(response, "text", "") or "").strip()
        if not text:
            raise RuntimeError("speech_to_text_empty_transcript")

        return SpeechToTextResult(
            text=text,
            provider=self.provider_name,
            confidence=None,
        )

    def synthesize(self, request: TextToSpeechRequest) -> TextToSpeechResult:
        text = request.text.strip()
        if not text:
            raise RuntimeError("text_to_speech_empty_input")

        self.output_dir.mkdir(parents=True, exist_ok=True)
        output_path = self.output_dir / "shadow-reply.mp3"

        response = self._client.audio.speech.create(
            model=self.tts_model,
            voice=request.voice_profile or self.tts_voice,
            input=text,
        )

        if hasattr(response, "stream_to_file"):
            response.stream_to_file(output_path)
        else:
            content = getattr(response, "content", None)
            if not content:
                raise RuntimeError("text_to_speech_missing_audio")
            output_path.write_bytes(content)

        if not output_path.is_file() or output_path.stat().st_size == 0:
            raise RuntimeError("text_to_speech_missing_audio")

        return TextToSpeechResult(
            audio_ref=str(output_path),
            provider=self.provider_name,
        )
