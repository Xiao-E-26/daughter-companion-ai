from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


ALLOWED_VISIBILITY = {
    'user_only',
    'user_and_daughter',
    'guardian_visible',
    'guardian_summary_only',
    'safety_restricted',
    'system_only_minimal',
}
SENSITIVE_CLASSES = {'M3', 'M4'}


@dataclass(frozen=True)
class MemoryPolicyEvidence:
    intent_class: str
    source_type: str
    actor_role_resolved: str
    explicit_user_intent: bool
    durable_value: bool
    verified_or_explicit: bool
    durable_storage_necessary: bool
    memory_class: str
    sensitivity: str
    visibility_scope: Optional[str]
    minimum_necessary: bool
    summary_present: bool


@dataclass(frozen=True)
class MemoryPolicyDecision:
    allowed: bool
    reason: str
    privacy_gate_passed: bool
    sensitivity_gate_passed: bool
    minimum_necessary_passed: bool
    visibility_gate_passed: bool
    retention_class: Optional[str] = None


class MemoryPolicyGate:
    """Canonical fail-closed decision point for durable-memory promotion.

    This gate owns only the durable-memory policy decision. It does not write,
    queue, promote, transport, or mutate memory. All production callers must
    consume this decision rather than independently deciding promotion.
    """

    @staticmethod
    def evaluate(e: MemoryPolicyEvidence) -> MemoryPolicyDecision:
        if e.intent_class != 'long_term_memory_create':
            return MemoryPolicyDecision(False, 'not_long_term_memory_create', False, False, False, False)
        if e.source_type != 'child_direct':
            return MemoryPolicyDecision(False, 'source_not_child_direct', False, False, False, False)
        if e.actor_role_resolved != 'child':
            return MemoryPolicyDecision(False, 'actor_not_verified_child', False, False, False, False)
        if not e.explicit_user_intent:
            return MemoryPolicyDecision(False, 'explicit_user_intent_required', False, False, False, False)
        if not e.summary_present:
            return MemoryPolicyDecision(False, 'summary_required', False, False, False, False)
        if not e.durable_value:
            return MemoryPolicyDecision(False, 'durable_value_not_established', False, False, False, False)
        if not e.verified_or_explicit:
            return MemoryPolicyDecision(False, 'verification_not_established', False, False, False, False)
        if not e.durable_storage_necessary:
            return MemoryPolicyDecision(False, 'durable_storage_not_necessary', False, False, False, False)

        privacy = True
        minimum = bool(e.minimum_necessary)
        visibility = e.visibility_scope in ALLOWED_VISIBILITY

        memory_class = e.memory_class.upper().strip()
        sensitivity = e.sensitivity.lower().strip()
        if memory_class in SENSITIVE_CLASSES:
            sensitivity_ok = sensitivity in {'restricted', 'high'}
            visibility_ok = e.visibility_scope in {'user_only', 'safety_restricted', 'system_only_minimal'}
            sensitivity = sensitivity_ok
            visibility = visibility and visibility_ok
        else:
            sensitivity = sensitivity in {'low', 'normal', 'moderate'}

        if not sensitivity:
            return MemoryPolicyDecision(False, 'sensitivity_gate_not_passed', privacy, False, minimum, visibility)
        if not minimum:
            return MemoryPolicyDecision(False, 'minimum_necessary_gate_not_passed', privacy, True, False, visibility)
        if not visibility:
            return MemoryPolicyDecision(False, 'visibility_gate_not_passed', privacy, True, minimum, False)

        return MemoryPolicyDecision(
            True,
            'policy_gates_passed',
            True,
            True,
            True,
            True,
            retention_class='child_pinned',
        )
