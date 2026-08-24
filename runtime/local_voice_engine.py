from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Dict

from runtime.voice_input_adapter import (
    SpeakerMatchResult,
    VoiceInputAdapter,
    VoiceSample,
    VoiceSignatureResult,
)


@dataclass(frozen=True)
class StoredVoiceSignature:
    signature_ref: str
    feature_digest: str
    quality_score: float


class LocalVoiceEngine(VoiceInputAdapter):
    """Local-first speaker-recognition implementation scaffold.

    This implementation intentionally avoids claiming real biometric speaker
    recognition before a real local embedding backend is installed. It provides
    the storage/reference lifecycle and deterministic test behavior only.

    Replace `_extract_features` and `_similarity` with a vetted on-device speaker
    embedding backend before production enrollment. No raw audio bytes are stored.
    """

    provider_name = "local-scaffold"

    def __init__(self) -> None:
        self._signatures: Dict[str, StoredVoiceSignature] = {}

    def create_signature(self, sample: VoiceSample) -> VoiceSignatureResult:
        features = self._extract_features(sample)
        signature_ref = "voice:" + hashlib.sha256(features.encode("utf-8")).hexdigest()[:24]
        quality = self._quality_score(sample)
        self._signatures[signature_ref] = StoredVoiceSignature(
            signature_ref=signature_ref,
            feature_digest=features,
            quality_score=quality,
        )
        return VoiceSignatureResult(signature_ref=signature_ref, quality_score=quality)

    def compare(self, sample: VoiceSample, *, signature_ref: str) -> SpeakerMatchResult:
        stored = self._signatures.get(signature_ref)
        if stored is None:
            raise ValueError("Unknown voice signature reference.")
        current = self._extract_features(sample)
        return SpeakerMatchResult(score=self._similarity(stored.feature_digest, current))

    @staticmethod
    def _extract_features(sample: VoiceSample) -> str:
        """Deterministic placeholder; not real speaker biometrics."""
        payload = f"{sample.audio_ref}|{sample.transcript.strip().lower()}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    @staticmethod
    def _quality_score(sample: VoiceSample) -> float:
        return 0.9 if sample.audio_ref.strip() and sample.transcript.strip() else 0.0

    @staticmethod
    def _similarity(reference_digest: str, current_digest: str) -> float:
        return 1.0 if reference_digest == current_digest else 0.0
