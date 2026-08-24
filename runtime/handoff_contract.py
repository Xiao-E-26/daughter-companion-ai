from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Mapping


HANDOFF_SCHEMA = "xiaoe.runtime.handoff.v1"
DAUGHTER_RUNTIME_IDENTITY = "daughter"


@dataclass(frozen=True)
class DaughterHandoff:
    routing_reason: str
    context: Dict[str, str]


def validate_daughter_handoff(packet: Mapping[str, object]) -> DaughterHandoff:
    if packet.get("schema") != HANDOFF_SCHEMA:
        raise ValueError("Unsupported or missing XiaoE handoff schema.")
    if str(packet.get("runtime_identity", "")).strip().lower() != DAUGHTER_RUNTIME_IDENTITY:
        raise ValueError("Handoff is not routed to Daughter.")

    claims = packet.get("claims")
    if not isinstance(claims, Mapping):
        raise ValueError("Handoff claims are required.")
    if claims.get("model_may_change_identity") is not False:
        raise ValueError("Model identity changes are not allowed.")
    if claims.get("model_may_expand_authority") is not False:
        raise ValueError("Model Authority expansion is not allowed.")
    if claims.get("context_is_identity_filtered") is not True:
        raise ValueError("Handoff context must be identity-filtered before Daughter accepts it.")

    raw_context = packet.get("context")
    if not isinstance(raw_context, Mapping):
        raise ValueError("Handoff context must be a mapping.")

    forbidden = {
        "repository_secret",
        "api_key",
        "service_role_key",
        "deployment_secret",
        "internal_governance_notes",
    }
    normalized = {str(k).strip().lower(): str(v) for k, v in raw_context.items()}
    overlap = forbidden & set(normalized)
    if overlap:
        raise ValueError(f"Forbidden cross-context keys in Daughter handoff: {sorted(overlap)}")

    return DaughterHandoff(
        routing_reason=str(packet.get("routing_reason", "")),
        context=normalized,
    )
