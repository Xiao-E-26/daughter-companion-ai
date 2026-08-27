from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Optional

from runtime.read_only_runtime_context import RuntimeContextSnapshot


@dataclass(frozen=True)
class LiveRuntimeSnapshot:
    persona_state: str
    route: str
    child_name: Optional[str]
    daughter_id: Optional[str]
    internal_user_id: Optional[str]
    client_connection_id: Optional[str]


@dataclass(frozen=True)
class ShadowComparison:
    comparable: bool
    state_match: bool
    identity_match: bool
    client_match: bool
    route_consistent: bool
    mismatch_count: int
    reason: Optional[str]
    telemetry_version: str = "shadow-runtime-comparator-v1"

    def telemetry(self) -> dict:
        """Return privacy-safe structured telemetry with no raw message/transcript."""
        data = asdict(self)
        data["contains_raw_message"] = False
        data["contains_transcript"] = False
        return data


class ShadowRuntimeComparator:
    """Compare live runtime facts with a read-only resolver snapshot.

    This comparator never changes response content, never writes state, and never
    accepts raw conversation text. It compares only already-resolved runtime facts.
    """

    def compare(
        self,
        *,
        live: LiveRuntimeSnapshot,
        shadow: RuntimeContextSnapshot,
    ) -> ShadowComparison:
        if not shadow.resolved:
            return ShadowComparison(
                comparable=False,
                state_match=False,
                identity_match=False,
                client_match=False,
                route_consistent=False,
                mismatch_count=0,
                reason=shadow.error_code or "shadow_unresolved",
            )

        state_match = live.persona_state == shadow.persona_state
        identity_match = (
            live.daughter_id == shadow.daughter_id
            and live.internal_user_id == shadow.internal_user_id
            and live.child_name == shadow.child_name
        )
        client_match = live.client_connection_id == shadow.client_connection_id
        expected_route = "xiaoai" if shadow.persona_state == "ACTIVE" else "normal_assistant"
        route_consistent = live.route == expected_route

        flags = [state_match, identity_match, client_match, route_consistent]
        mismatch_count = sum(1 for flag in flags if not flag)

        return ShadowComparison(
            comparable=True,
            state_match=state_match,
            identity_match=identity_match,
            client_match=client_match,
            route_consistent=route_consistent,
            mismatch_count=mismatch_count,
            reason=None if mismatch_count == 0 else "runtime_mismatch",
        )
