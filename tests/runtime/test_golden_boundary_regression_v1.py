from __future__ import annotations

from dataclasses import replace

from runtime.decision_engine import DaughterDecisionEngine, DecisionInput


BASE = DecisionInput(
    age=7,
    maturity="child",
    guardian_state="valid",
    daughter_correctness="uncertain",
    child_correctness="uncertain",
    memory_state="reliable",
    model_state="normal",
    authority_state="valid",
    network_state="online",
    embodiment="chat_only",
    emotional_state="stable",
    risk_level="low",
    time_pressure="normal",
    reversibility="reversible",
    domain="general",
    event_type="conversation",
)


def test_revoked_authority_blocks_high_risk_execution():
    result = DaughterDecisionEngine().decide(
        replace(BASE, risk_level="high", authority_state="revoked")
    )
    assert result.decision_class == "BLOCK_PRIVILEGED_EXECUTION_UNTIL_RECONCILED"
    assert result.privileged_execution is False
    assert result.authority_effect == "deny_until_reconciled"


def test_corrupted_memory_requires_current_fact_verification():
    result = DaughterDecisionEngine().decide(replace(BASE, memory_state="corrupted"))
    assert result.decision_class == "VERIFY_CURRENT_FACTS_BEFORE_MEMORY_DEPENDENT_JUDGMENT"
    assert result.privileged_execution is False
    assert result.authority_effect == "no_change"


def test_adult_self_governance_does_not_inherit_childhood_control():
    result = DaughterDecisionEngine().decide(
        replace(BASE, age=25, maturity="adult", guardian_state="none_adult_self_governance")
    )
    assert result.decision_class == "RESPECT_ADULT_SELF_GOVERNANCE"
    assert result.privileged_execution is False
    assert result.authority_effect == "childhood_guardian_authority_not_applied"


def test_critical_unsafe_physical_state_stops_execution():
    result = DaughterDecisionEngine().decide(
        replace(BASE, risk_level="critical", embodiment="robot_damaged")
    )
    assert result.decision_class == "STOP_OR_SAFE_DEGRADED_MODE"
    assert result.privileged_execution is False
    assert result.authority_effect == "no_expansion"


def test_default_path_remains_non_sovereign():
    result = DaughterDecisionEngine().decide(
        replace(
            BASE,
            child_correctness="wrong",
            daughter_correctness="correct",
            risk_level="medium",
        )
    )
    assert result.decision_class == "CONTEXTUAL_JUDGMENT_REQUIRED"
    assert result.privileged_execution is False
    assert result.authority_effect == "no_change"
    assert "preserve_user_agency" in result.actions
