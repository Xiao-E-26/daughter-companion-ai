import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MAPPING = ROOT / "tests" / "golden" / "golden_regression_mapping_v1.json"

ALLOWED_MODES = {
    "deterministic",
    "deterministic_contract",
    "conversational",
    "hybrid",
    "policy_contract",
    "structured",
    "governance_contract",
}


def _load_mapping():
    return json.loads(MAPPING.read_text(encoding="utf-8"))


def test_mapping_routes_all_16_golden_cases_once():
    data = _load_mapping()
    ids = [case["id"] for case in data["cases"]]
    assert len(ids) == 16
    assert len(set(ids)) == 16
    assert ids == [f"GR-{n:03d}" for n in range(1, 17)]


def test_mapping_has_explicit_owner_and_supported_mode():
    for case in _load_mapping()["cases"]:
        assert case["route"].strip()
        assert case["owner"].strip()
        assert case["mode"] in ALLOWED_MODES


def test_decision_engine_not_used_as_universal_owner():
    engine_owned = [
        case for case in _load_mapping()["cases"]
        if case["owner"] == "runtime/decision_engine.py"
    ]
    assert [case["id"] for case in engine_owned] == ["GR-015"]
