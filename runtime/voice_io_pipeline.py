from __future__ import annotations

from dataclasses import dataclass

from runtime.speech_io_adapter import (
    SpeechToTextAdapter,
    SpeechToTextRequest,
    TextToSpeechAdapter,
    TextToSpeechRequest,
)


@dataclass(frozen=True)
class VoicePipelineInput:
    audio_ref: str
    session_key: str
    language_hint: str | None = None


@dataclass(frozen=True)
class VoicePipelineOutput:
    transcript: str
    reply_text: str
    audio_ref: str


class DaughterChatClient:
    """Minimal runtime boundary implemented by the live daughter-chat adapter."""

    def send_message(self, *, message: str, session_key: str) -> str:  # pragma: no cover - protocol-like scaffold
        raise NotImplementedError


class XiaoAiVoiceIOPipeline:
    """Voice I/O wrapper around the same live XiaoAi text runtime.

    Flow:
      audio -> STT -> daughter-chat -> text reply -> TTS -> audio

    This class deliberately owns no persona, memory, identity, safety policy,
    permission logic, or durable runtime state. Those remain in the shared
    XiaoAi runtime / daughter-chat authority.
    """

    def __init__(
        self,
        *,
        stt: SpeechToTextAdapter,
        tts: TextToSpeechAdapter,
        daughter_chat: DaughterChatClient,
    ) -> None:
        self.stt = stt
        self.tts = tts
        self.daughter_chat = daughter_chat

    def handle(self, request: VoicePipelineInput) -> VoicePipelineOutput:
        stt_result = self.stt.transcribe(
            SpeechToTextRequest(
                audio_ref=request.audio_ref,
                language_hint=request.language_hint,
            )
        )
        transcript = stt_result.text.strip()
        if not transcript:
            raise RuntimeError("speech_to_text_empty_transcript")

        reply_text = self.daughter_chat.send_message(
            message=transcript,
            session_key=request.session_key,
        ).strip()
        if not reply_text:
            raise RuntimeError("daughter_chat_empty_reply")

        tts_result = self.tts.synthesize(
            TextToSpeechRequest(
                text=reply_text,
                language_hint=request.language_hint,
            )
        )
        if not tts_result.audio_ref.strip():
            raise RuntimeError("text_to_speech_missing_audio")

        return VoicePipelineOutput(
            transcript=transcript,
            reply_text=reply_text,
            audio_ref=tts_result.audio_ref,
        )
