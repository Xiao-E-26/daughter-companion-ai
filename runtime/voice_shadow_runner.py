from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from runtime.speech_io_adapter import SpeechToTextAdapter, SpeechToTextRequest, TextToSpeechAdapter, TextToSpeechRequest


@dataclass(frozen=True)
class VoiceShadowResult:
    transcript: str
    candidate_reply: str
    candidate_audio_ref: str


class XiaoAiVoiceShadowRunner:
    """Shadow-only voice path evaluator.

    The runner may exercise STT -> candidate runtime call -> TTS, but it never
    returns or publishes the candidate reply as the production response. The
    caller receives telemetry/test evidence only and remains responsible for the
    authoritative live daughter-chat response path.
    """

    def __init__(
        self,
        *,
        stt: SpeechToTextAdapter,
        tts: TextToSpeechAdapter,
        candidate_runtime: Callable[[str, str], str],
    ) -> None:
        self.stt = stt
        self.tts = tts
        self.candidate_runtime = candidate_runtime

    def run(self, *, audio_ref: str, session_key: str, language_hint: str | None = None) -> VoiceShadowResult:
        transcript = self.stt.transcribe(
            SpeechToTextRequest(audio_ref=audio_ref, language_hint=language_hint)
        ).text.strip()
        if not transcript:
            raise RuntimeError("voice_shadow_empty_transcript")

        candidate_reply = self.candidate_runtime(transcript, session_key).strip()
        if not candidate_reply:
            raise RuntimeError("voice_shadow_empty_candidate_reply")

        rendered = self.tts.synthesize(
            TextToSpeechRequest(text=candidate_reply, language_hint=language_hint)
        )
        if not rendered.audio_ref.strip():
            raise RuntimeError("voice_shadow_missing_audio")

        return VoiceShadowResult(
            transcript=transcript,
            candidate_reply=candidate_reply,
            candidate_audio_ref=rendered.audio_ref,
        )
