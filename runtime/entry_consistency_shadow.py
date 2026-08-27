from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Optional


@dataclass(frozen=True)
class EntryRuntimeSnapshot:
    entry_mode: str
    runtime_path: str
    persona_state: str
    daughter_id: Optional[str]
    session_key: str
    behavior_source: str
    response_style_signature: str


@dataclass(frozen=True)
class EntryConsistencyComparison:
    comparable: bool
    same_runtime_path: bool
    same_persona_state: bool
    same_identity: bool
    same_session: bool
    same_behavior_source: bool
    same_style_signature: bool
    mismatch_count: int
    reason: Optional[str]
    telemetry_version: str = "entry-consistency-shadow-v1"

    def telemetry(self) -> dict:
        data = asdict(self)
        data["contains_raw_message"] = False
        data["contains_transcript"] = False
        data["contains_reply_text"] = False
        return data


class EntryConsistencyShadowComparator:
    """Observation-only Text/Voice consistency comparator.

    It never changes user-visible output and never accepts raw transcript/reply text.
    It compares normalized runtime metadata and a precomputed privacy-safe style signature.
    """

    def compare(
        self,
        *,
        text: EntryRuntimeSnapshot,
        voice: EntryRuntimeSnapshot,
    ) -> EntryConsistencyComparison:
        if text.entry_mode != "text" or voice.entry_mode != "voice":
            return EntryConsistencyComparison(
                comparable=False,
                same_runtime_path=False,
                same_persona_state=False,
                same_identity=False,
                same_session=False,
                same_behavior_source=False,
                same_style_signature=False,
                mismatch_count=0,
                reason="invalid_entry_pair",
            )

        same_runtime_path = text.runtime_path == voice.runtime_path
        same_persona_state = text.persona_state == voice.persona_state
        same_identity = text.daughter_id == voice.daughter_id
        same_session = text.session_key == voice.session_key
        same_behavior_source = text.behavior_source == voice.behavior_source
        same_style_signature = text.response_style_signature == voice.response_style_signature

        flags = [
            same_runtime_path,
            same_persona_state,
            same_identity,
            same_session,
            same_behavior_source,
            same_style_signature,
        ]
        mismatch_count = sum(1 for flag in flags if not flag)

        return EntryConsistencyComparison(
            comparable=True,
            same_runtime_path=same_runtime_path,
            same_persona_state=same_persona_state,
            same_identity=same_identity,
            same_session=same_session,
            same_behavior_source=same_behavior_source,
            same_style_signature=same_style_signature,
            mismatch_count=mismatch_count,
            reason=None if mismatch_count == 0 else "entry_consistency_mismatch",
        )
