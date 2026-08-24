from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class VoiceSample:
    audio_ref: str
    transcript: str


@dataclass(frozen=True)
class VoiceSignatureResult:
    signature_ref: str
    quality_score: float


@dataclass(frozen=True)
class SpeakerMatchResult:
    score: float


class VoiceInputAdapter(Protocol):
    """Provider-neutral contract for future microphone/speaker-recognition engines.

    The implementation may be local/on-device or external. This contract never
    grants Authority; it only produces voice-signature and match evidence.
    """

    provider_name: str

    def create_signature(self, sample: VoiceSample) -> VoiceSignatureResult:
        ...

    def compare(self, sample: VoiceSample, *, signature_ref: str) -> SpeakerMatchResult:
        ...
