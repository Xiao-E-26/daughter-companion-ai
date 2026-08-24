from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class VoiceIdentityState(str, Enum):
    UNENROLLED = "unenrolled"
    VERIFIED = "verified"
    REVOKED = "revoked"


@dataclass(frozen=True)
class VoiceEnrollmentRequest:
    user_id: str
    enrollment_phrase_transcript: str
    voice_signature_ref: str
    guardian_approved: bool
    child_assented: bool
    retain_raw_audio: bool = False


@dataclass(frozen=True)
class VoiceIdentityRecord:
    user_id: str
    state: VoiceIdentityState
    voice_signature_ref: str
    enrollment_phrase_transcript: str
    raw_audio_retained: bool
    purpose: str = "speaker_recognition_for_companion_context"


class VoiceEnrollmentManager:
    """Privacy-preserving child voice enrollment.

    Voice recognition is supporting identity context only. It must never grant
    permissions, change Guardian state, unlock protected data, or expand Authority.
    Raw audio is not retained by default.
    """

    def enroll(self, request: VoiceEnrollmentRequest) -> VoiceIdentityRecord:
        if not request.guardian_approved:
            raise ValueError("Guardian approval is required for child voice enrollment.")
        if not request.child_assented:
            raise ValueError("Child assent is required for child voice enrollment.")
        if not request.voice_signature_ref.strip():
            raise ValueError("voice_signature_ref is required.")
        if not request.enrollment_phrase_transcript.strip():
            raise ValueError("enrollment_phrase_transcript is required.")

        return VoiceIdentityRecord(
            user_id=request.user_id,
            state=VoiceIdentityState.VERIFIED,
            voice_signature_ref=request.voice_signature_ref.strip(),
            enrollment_phrase_transcript=request.enrollment_phrase_transcript.strip(),
            raw_audio_retained=bool(request.retain_raw_audio),
        )

    @staticmethod
    def recognize(
        record: VoiceIdentityRecord,
        *,
        speaker_match_score: float,
        threshold: float = 0.85,
    ) -> bool:
        if record.state != VoiceIdentityState.VERIFIED:
            return False
        if not 0.0 <= speaker_match_score <= 1.0:
            raise ValueError("speaker_match_score must be between 0 and 1.")
        if not 0.0 <= threshold <= 1.0:
            raise ValueError("threshold must be between 0 and 1.")
        return speaker_match_score >= threshold

    @staticmethod
    def revoke(record: VoiceIdentityRecord) -> VoiceIdentityRecord:
        return VoiceIdentityRecord(
            user_id=record.user_id,
            state=VoiceIdentityState.REVOKED,
            voice_signature_ref=record.voice_signature_ref,
            enrollment_phrase_transcript=record.enrollment_phrase_transcript,
            raw_audio_retained=record.raw_audio_retained,
            purpose=record.purpose,
        )

    @staticmethod
    def identity_context(
        record: Optional[VoiceIdentityRecord],
        *,
        speaker_match_score: Optional[float] = None,
    ) -> str:
        if record is None or speaker_match_score is None:
            return "speaker_identity=unknown"
        if VoiceEnrollmentManager.recognize(record, speaker_match_score=speaker_match_score):
            return "speaker_identity=likely_enrolled_child"
        return "speaker_identity=not_confirmed"
