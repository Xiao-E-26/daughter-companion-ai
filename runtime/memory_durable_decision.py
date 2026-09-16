from __future__ import annotations

from dataclasses import dataclass

from runtime.memory_actor_evidence import (
    MemoryActorContext,
    MemoryActorEvidenceResolver,
)
from runtime.memory_policy_gate import (
    MemoryPolicyDecision,
    MemoryPolicyEvidence,
    MemoryPolicyGate,
)


@dataclass(frozen=True)
class DurableDecisionInput:
    actor_context: MemoryActorContext
    intent_class: str
    explicit_user_intent: bool
    durable_value: bool
    verified_or_explicit: bool
    durable_storage_necessary: bool
    memory_class: str
    sensitivity: str
    visibility_scope: str | None
    minimum_necessary: bool
    summary_present: bool


class MemoryDurableDecisionCoordinator:
    """Canonical orchestration point for actor evidence -> durable policy decision.

    This class does not write, queue, promote, or transport memory. It resolves
    actor evidence first, then feeds only verified actor facts into the canonical
    MemoryPolicyGate. Unverified actor identity always fails closed before a
    durable-memory policy PASS can be produced.
    """

    @staticmethod
    def evaluate(i: DurableDecisionInput) -> MemoryPolicyDecision:
        actor = MemoryActorEvidenceResolver.resolve(i.actor_context)
        if not actor.verified:
            return MemoryPolicyDecision(
                False,
                f'actor_evidence_failed:{actor.reason}',
                False,
                False,
                False,
                False,
            )

        return MemoryPolicyGate.evaluate(
            MemoryPolicyEvidence(
                intent_class=i.intent_class,
                source_type=actor.source_type,
                actor_role_resolved=actor.actor_role_resolved,
                explicit_user_intent=i.explicit_user_intent,
                durable_value=i.durable_value,
                verified_or_explicit=i.verified_or_explicit,
                durable_storage_necessary=i.durable_storage_necessary,
                memory_class=i.memory_class,
                sensitivity=i.sensitivity,
                visibility_scope=i.visibility_scope,
                minimum_necessary=i.minimum_necessary,
                summary_present=i.summary_present,
            )
        )
