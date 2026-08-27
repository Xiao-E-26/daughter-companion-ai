from runtime.behavior_mode_router import (
    BehaviorFamily,
    BehaviorModeRouter,
    RouterInput,
)


router = BehaviorModeRouter()


def test_multiconflict_precedence_matrix():
    """Compound policy-derived signals must preserve one stable primary family."""
    cases = [
        ("critical_child_guardian_conflict", RouterInput("S3", True, True, True), BehaviorFamily.SAFETY),
        ("significant_risk_with_memory_uncertainty", RouterInput("S2", True, True, False), BehaviorFamily.SAFETY),
        ("s1_boundary_and_problem_solving", RouterInput("S1", True, True, True), BehaviorFamily.BOUNDARY),
        ("s0_boundary_after_minimization", RouterInput("S0", True, True, True), BehaviorFamily.BOUNDARY),
        ("s1_problem_solving_and_distress", RouterInput("S1", False, True, True), BehaviorFamily.GUIDE),
        ("s0_problem_solving_and_expression", RouterInput("S0", False, True, True), BehaviorFamily.GUIDE),
        ("s1_expression_only", RouterInput("S1", False, False, True), BehaviorFamily.COMPANION),
        ("ordinary_handoff_context", RouterInput("S0", False, False, False), BehaviorFamily.COMPANION),
    ]

    for case_id, value, expected in cases:
        decision = router.route(value)
        assert decision.family == expected, case_id


def test_safety_case_normalization_does_not_change_precedence():
    result = router.route(
        RouterInput(
            safety_level="s3",
            needs_boundary=True,
            wants_problem_solving=True,
            mainly_needs_expression=True,
        )
    )
    assert result.family == BehaviorFamily.SAFETY


def test_context_handoff_does_not_invent_a_stronger_route():
    """Cross-device/session continuity supplies context, not extra authority."""
    result = router.route(
        RouterInput(
            safety_level="S0",
            needs_boundary=False,
            wants_problem_solving=False,
            mainly_needs_expression=True,
        )
    )
    assert result.family == BehaviorFamily.COMPANION


def test_invalid_handoff_safety_state_fails_closed():
    try:
        router.route(RouterInput(safety_level="UNKNOWN"))
    except ValueError as exc:
        assert "Unsupported safety level" in str(exc)
    else:
        raise AssertionError("Unknown cross-session safety state must be rejected")
