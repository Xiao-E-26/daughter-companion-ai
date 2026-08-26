from runtime.behavior_mode_router import (
    BehaviorFamily,
    BehaviorModeRouter,
    RouterInput,
)


router = BehaviorModeRouter()


def test_s3_overrides_boundary_and_guidance():
    result = router.route(
        RouterInput(
            safety_level="S3",
            needs_boundary=True,
            wants_problem_solving=True,
            mainly_needs_expression=True,
        )
    )
    assert result.family == BehaviorFamily.SAFETY


def test_s2_routes_to_safety():
    result = router.route(RouterInput(safety_level="S2"))
    assert result.family == BehaviorFamily.SAFETY


def test_s1_does_not_automatically_inflate_to_safety():
    result = router.route(
        RouterInput(safety_level="S1", mainly_needs_expression=True)
    )
    assert result.family == BehaviorFamily.COMPANION


def test_boundary_overrides_problem_solving_at_low_risk():
    result = router.route(
        RouterInput(
            safety_level="S0",
            needs_boundary=True,
            wants_problem_solving=True,
        )
    )
    assert result.family == BehaviorFamily.BOUNDARY


def test_problem_solving_routes_to_guide():
    result = router.route(
        RouterInput(safety_level="S0", wants_problem_solving=True)
    )
    assert result.family == BehaviorFamily.GUIDE


def test_expression_routes_to_companion():
    result = router.route(
        RouterInput(safety_level="S0", mainly_needs_expression=True)
    )
    assert result.family == BehaviorFamily.COMPANION


def test_ordinary_default_is_companion():
    result = router.route(RouterInput())
    assert result.family == BehaviorFamily.COMPANION


def test_router_rejects_unknown_safety_level():
    try:
        router.route(RouterInput(safety_level="S9"))
    except ValueError as exc:
        assert "Unsupported safety level" in str(exc)
    else:
        raise AssertionError("Expected ValueError for unsupported safety level")
