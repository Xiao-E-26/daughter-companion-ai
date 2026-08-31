from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional, Protocol


class DurableMemoryGate(str, Enum):
    OFF = "off"
    CHILD_PINNED_ONLY = "child_pinned_only"


@dataclass(frozen=True)
class DurableMemoryIntent:
    subject_id: str
    actor_account_id: str
    actor_role_resolved: str
    intent_class: str
    intent_confidence: float
    source_type: str
    summary: str
    idempotency_key: str
    sensitivity: str = "low"
    disclosure_scope: str = "subject_only"


@dataclass(frozen=True)
class DurableMemoryResult:
    accepted: bool
    reason: str
    memory_id: Optional[str] = None


class DurableMemoryTransport(Protocol):
    def pin_child_memory(self, payload: Dict[str, Any]) -> DurableMemoryResult: ...


class DurableMemoryBridge:
    """Dormant bridge for durable autobiographical memory.

    Safety posture:
    - default gate is OFF;
    - ordinary conversation and inferred candidates never persist through this bridge;
    - even when enabled, only verified child-direct long-term memory intent may write;
    - transport implementation is injected separately, so adding this bridge does not
      itself enable Supabase writes.
    """

    def __init__(
        self,
        *,
        gate: DurableMemoryGate = DurableMemoryGate.OFF,
        transport: Optional[DurableMemoryTransport] = None,
        minimum_intent_confidence: float = 0.85,
    ) -> None:
        self.gate = gate
        self.transport = transport
        self.minimum_intent_confidence = minimum_intent_confidence

    def submit(self, intent: DurableMemoryIntent) -> DurableMemoryResult:
        if self.gate == DurableMemoryGate.OFF:
            return DurableMemoryResult(False, "durable_memory_gate_off")

        if self.gate != DurableMemoryGate.CHILD_PINNED_ONLY:
            return DurableMemoryResult(False, "unsupported_gate_state")

        if intent.intent_class != "long_term_memory_create":
            return DurableMemoryResult(False, "not_long_term_memory_create")

        if intent.source_type != "child_direct":
            return DurableMemoryResult(False, "source_not_verified_child_direct")

        if intent.actor_role_resolved != "child":
            return DurableMemoryResult(False, "actor_not_verified_child")

        if intent.intent_confidence < self.minimum_intent_confidence:
            return DurableMemoryResult(False, "intent_confidence_too_low")

        if not intent.idempotency_key.strip():
            return DurableMemoryResult(False, "missing_idempotency_key")

        if self.transport is None:
            return DurableMemoryResult(False, "durable_memory_transport_not_configured")

        payload = {
            "subject_id": intent.subject_id,
            "actor_account_id": intent.actor_account_id,
            "actor_role_resolved": intent.actor_role_resolved,
            "intent_class": intent.intent_class,
            "intent_confidence": intent.intent_confidence,
            "source_type": intent.source_type,
            "summary": intent.summary,
            "idempotency_key": intent.idempotency_key,
            "sensitivity": intent.sensitivity,
            "disclosure_scope": intent.disclosure_scope,
            "retention_class": "child_pinned",
            "pinned_by_child": True,
            "proactive_surface_allowed": False,
        }
        return self.transport.pin_child_memory(payload)
