from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, Iterable, List


@dataclass(frozen=True)
class DecisionInput:
    age: int
    maturity: str
    guardian_state: str
    daughter_correctness: str
    child_correctness: str
    memory_state: str
    model_state: str
    authority_state: str
    network_state: str
    embodiment: str
    emotional_state: str
    risk_level: str
    time_pressure: str
    reversibility: str
    domain: str
    event_type: str


@dataclass(frozen=True)
class DecisionOutput:
    decision_class: str
    rationale: str
    actions: List[str]
    privileged_execution: bool
    memory_effect: str
    authority_effect: str
    escalation: str
    protected_invariants: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


UNSAFE_AUTHORITY = {
    "expired",
    "revoked",
    "conflicting_sources",
    "stale_cached_allow",
    "succession_unresolved",
}

UNRELIABLE_MEMORY = {
    "stale",
    "conflicting",
    "corrupted",
    "deleted_but_indexed",
    "wrong_high_confidence",
}

UNSAFE_PHYSICAL = {
    "robot_sensor_conflict",
    "robot_damaged",
}

HIGH_RISK = {"high", "critical"}


class DaughterDecisionEngine:
    """Minimal deterministic runtime for protected Daughter invariants.

    This is not a conversational model. It is the judgment/authority/safety
    boundary that a future model-driven Daughter runtime can call before any
    action. The implementation intentionally encodes only already-approved
    invariants and leaves ambiguous, low-risk cases to contextual judgment.
    """

    def decide(self, state: DecisionInput) -> DecisionOutput:
        # 1. Physical safety is a hard execution gate.
        if state.risk_level == "critical" and state.embodiment in UNSAFE_PHYSICAL:
            return self._out(
                "STOP_OR_SAFE_DEGRADED_MODE",
                "Critical physical uncertainty requires stopping before task completion.",
                ["stop_motion", "stabilize_state", "verify_physical_safety"],
                privileged=False,
                memory_effect="record_verified_safety_event_only",
                authority_effect="no_expansion",
                escalation="critical",
                invariants=["child_first_daughter_second", "physical_safety_gates_motor_action"],
            )

        # 2. High-risk execution requires current valid authority.
        if state.risk_level in HIGH_RISK and state.authority_state in UNSAFE_AUTHORITY:
            return self._out(
                "BLOCK_PRIVILEGED_EXECUTION_UNTIL_RECONCILED",
                "High-risk action cannot rely on stale, revoked, expired, or conflicting authority.",
                ["block_privileged_action", "reconcile_authority", "offer_non_privileged_help"],
                privileged=False,
                memory_effect="no_authority_memory_promotion",
                authority_effect="deny_until_reconciled",
                escalation="high",
                invariants=["capability_does_not_expand_authority", "high_risk_uncertainty_prefers_safe_reversible_action"],
            )

        # 3. Guardian may itself be part of the safety problem.
        if state.guardian_state == "suspected_risk_source" and state.risk_level in HIGH_RISK:
            return self._out(
                "USE_INDEPENDENT_SAFE_ROUTE",
                "A Guardian who may be the source of harm cannot be the automatic escalation target.",
                ["minimize_disclosure", "seek_independent_safe_human_route", "preserve_child_voice"],
                privileged=False,
                memory_effect="store_as_reported_concern_with_uncertainty",
                authority_effect="no_expansion",
                escalation="high",
                invariants=["guardian_is_not_infallible", "child_first_daughter_second"],
            )

        # 4. Unreliable memory can inform but cannot dominate present reality.
        if state.memory_state in UNRELIABLE_MEMORY:
            actions = ["verify_current_facts", "lower_memory_confidence"]
            if state.memory_state == "deleted_but_indexed":
                actions.append("purge_deleted_memory_reference")
            return self._out(
                "VERIFY_CURRENT_FACTS_BEFORE_MEMORY_DEPENDENT_JUDGMENT",
                "Stale, conflicting, corrupted, deleted, or disproven memory is not current verified reality.",
                actions,
                privileged=False,
                memory_effect="quarantine_or_supersede_unreliable_memory",
                authority_effect="no_change",
                escalation="normal",
                invariants=["current_verified_facts_over_stale_memory", "past_must_not_permanently_define_person"],
            )

        # 5. Valid adult self-governance supersedes historical childhood control.
        if state.age >= 18 and state.guardian_state == "none_adult_self_governance":
            return self._out(
                "RESPECT_ADULT_SELF_GOVERNANCE",
                "Valid adult self-governance must not inherit childhood restrictions by habit.",
                ["return_decision_ownership", "offer_context_and_options", "respect_valid_adult_choice"],
                privileged=False,
                memory_effect="retain_history_without_governance_effect",
                authority_effect="childhood_guardian_authority_not_applied",
                escalation="none",
                invariants=["growth_should_increase_autonomy", "child_first_daughter_second"],
            )

        # 6. Low-risk legitimate child choice outranks Daughter preference.
        if state.risk_level == "low" and state.child_correctness in {"correct", "partly_correct"}:
            return self._out(
                "PRESERVE_CHILD_LEGITIMATE_CHOICE",
                "For low-risk choices, Daughter may advise but does not own the child's decision.",
                ["offer_tradeoffs_if_useful", "respect_choice", "remain_available_without_pressure"],
                privileged=False,
                memory_effect="no_negative_trait_label_from_choice",
                authority_effect="no_change",
                escalation="none",
                invariants=["child_first_daughter_second", "relationship_without_dependency"],
            )

        # 7. Higher risk with uncertainty prefers reversible action and help.
        if state.risk_level in HIGH_RISK and (
            state.daughter_correctness == "uncertain" or state.child_correctness == "uncertain"
        ):
            return self._out(
                "TAKE_SMALLEST_SAFE_REVERSIBLE_STEP",
                "High-stakes uncertainty should not produce irreversible guessing.",
                ["clarify_material_facts", "prefer_reversible_step", "seek_qualified_help_if_needed"],
                privileged=False,
                memory_effect="store_uncertainty_not_conclusion",
                authority_effect="no_expansion",
                escalation="high",
                invariants=["understand_before_judging", "smallest_safe_reasonable_action_first"],
            )

        # 8. Default path intentionally stays non-sovereign and contextual.
        return self._out(
            "CONTEXTUAL_JUDGMENT_REQUIRED",
            "No hard invariant dominates this state; continue with contextual judgment and verification.",
            ["understand_context", "compare_options", "preserve_user_agency", "verify_outcome", "learn_from_result"],
            privileged=False,
            memory_effect="candidate_only_until_verified",
            authority_effect="no_change",
            escalation="none",
            invariants=["fact_first", "understand_before_judging", "child_first_daughter_second"],
        )

    @staticmethod
    def _out(
        decision_class: str,
        rationale: str,
        actions: Iterable[str],
        *,
        privileged: bool,
        memory_effect: str,
        authority_effect: str,
        escalation: str,
        invariants: Iterable[str],
    ) -> DecisionOutput:
        return DecisionOutput(
            decision_class=decision_class,
            rationale=rationale,
            actions=list(actions),
            privileged_execution=privileged,
            memory_effect=memory_effect,
            authority_effect=authority_effect,
            escalation=escalation,
            protected_invariants=list(invariants),
        )
