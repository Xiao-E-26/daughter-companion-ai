from pathlib import Path

from tests.conversation.conversational_harness import (
    BoundaryGate,
    FixtureCandidateAdapter,
    FixtureEvaluatorAdapter,
    load_suite,
    run_suite,
)


FIXTURE = Path(__file__).parent / "fixtures" / "golden_conversational_suite_v1.json"


def test_golden_conversational_suite_loads_all_expected_cases():
    scenarios, fixtures = load_suite(FIXTURE)

    assert len(scenarios) == 8
    assert {scenario.scenario_id for scenario in scenarios} == {
        "GR-002",
        "GR-003",
        "GR-004",
        "GR-006",
        "GR-007",
        "GR-008",
        "GR-014",
        "GR-015",
    }
    assert set(fixtures) == {scenario.scenario_id for scenario in scenarios}


def test_fixture_self_check_runs_without_boundary_or_critical_failures():
    scenarios, fixtures = load_suite(FIXTURE)
    report = run_suite(
        scenarios,
        FixtureCandidateAdapter(fixtures),
        FixtureEvaluatorAdapter(fixtures),
        BoundaryGate(),
    )

    assert report["scenarios"] == 8
    assert report["passed"] == 8
    assert report["failed"] == 0
    assert report["critical_failures"] == 0
    assert report["boundary_breaches"] == 0


def test_revoked_permission_case_reaches_deterministic_boundary_gate():
    scenarios, fixtures = load_suite(FIXTURE)
    report = run_suite(
        scenarios,
        FixtureCandidateAdapter(fixtures),
        FixtureEvaluatorAdapter(fixtures),
        BoundaryGate(),
    )

    case = next(item for item in report["cases"] if item["scenario_id"] == "GR-015")
    boundary = case["boundary"]

    assert boundary is not None
    assert boundary["breach"] is False
    assert boundary["expected_boundary"]["decision_class"] == (
        "BLOCK_PRIVILEGED_EXECUTION_UNTIL_RECONCILED"
    )
    assert boundary["candidate_action_intent"]["privileged_execution"] is False
