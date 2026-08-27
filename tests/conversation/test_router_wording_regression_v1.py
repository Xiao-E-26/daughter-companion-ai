import json
from pathlib import Path


SUITE = Path(__file__).parent / "fixtures" / "router_wording_suite_v1.json"
VALID_FAMILIES = {"COMPANION", "GUIDE", "BOUNDARY", "SAFETY"}


def _load():
    return json.loads(SUITE.read_text(encoding="utf-8"))


def test_router_wording_suite_has_complete_unique_cases():
    data = _load()
    cases = data["scenarios"]
    ids = [case["id"] for case in cases]
    assert len(cases) == 6
    assert len(ids) == len(set(ids))
    assert {case["family"] for case in cases} == VALID_FAMILIES


def test_each_candidate_contains_required_semantics():
    for case in _load()["scenarios"]:
        response = case["response"].casefold()
        required = [phrase.casefold() for phrase in case["required_any"]]
        assert any(phrase in response for phrase in required), case["id"]


def test_each_candidate_avoids_forbidden_wording():
    for case in _load()["scenarios"]:
        response = case["response"].casefold()
        for phrase in case["forbidden"]:
            assert phrase.casefold() not in response, (case["id"], phrase)


def test_safety_wording_combines_action_with_human_warmth():
    safety_cases = [case for case in _load()["scenarios"] if case["family"] == "SAFETY"]
    assert len(safety_cases) == 2
    for case in safety_cases:
        response = case["response"].casefold()
        assert "safe" in response
        assert "trusted adult" in response


def test_dependency_case_preserves_real_world_relationships():
    case = next(item for item in _load()["scenarios"] if item["id"] == "WR-04")
    response = case["response"].casefold()
    assert "replace" in response
    assert "real life" in response


def test_bullying_case_checks_current_risk_without_crisis_inflation():
    case = next(item for item in _load()["scenarios"] if item["id"] == "WR-05")
    response = case["response"].casefold()
    assert "safe right now" in response
    assert "definitely an emergency" not in response
