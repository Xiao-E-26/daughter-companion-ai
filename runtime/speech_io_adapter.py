from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class SpeechToTextRequest:
    audio_ref: str
    language_hint: str | None = None


@dataclass(frozen=True)
class SpeechToTextResult:
    text: str
    provider: str
    confidence: float | None = None


@dataclass(frozen=True)
class TextToSpeechRequest:
    text: str
    voice_profile: str | None = None
    language_hint: str | None = None


@dataclass(frozen=True)
class TextToSpeechResult:
    audio_ref: str
    provider: str


class SpeechToTextAdapter(Protocol):
    """Provider-neutral speech-to-text I/O boundary.

    STT converts audio into text only. It must not own XiaoAi identity,
    persona, memory, safety policy, permissions, or runtime state.
    """

    provider_name: str

    def transcribe(self, request: SpeechToTextRequest) -> SpeechToTextResult:
        ...


class TextToSpeechAdapter(Protocol):
    """Provider-neutral text-to-speech I/O boundary.

    TTS renders an already-produced XiaoAi text reply into audio only. It must
    not rewrite, reinterpret, or independently generate XiaoAi behavior.
    """

    provider_name: str

    def synthesize(self, request: TextToSpeechRequest) -> TextToSpeechResult:
        ...
