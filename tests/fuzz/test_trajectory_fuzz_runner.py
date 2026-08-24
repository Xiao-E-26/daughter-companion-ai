import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("trajectory_fuzz_runner.py")
spec = importlib.util.spec_from_file_location("trajectory_fuzz_runner", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def load_spec():
    return mod.load_spec(mod.DEFAULT_SPEC)


def test_same_seed_is_reproducible():
    cfg = load_spec()
    a = mod.generate_trajectory(cfg, seed=1234, index=7, length=12)
    b = mod.generate_trajectory(cfg, seed=1234, index=7, length=12)
    assert [mod.asdict(x) for x in a] == [mod.asdict(x) for x in b]


def test_different_seed_changes_trajectory():
    cfg = load_spec()
    a = mod.generate_trajectory(cfg, seed=1234, index=7, length=12)
    b = mod.generate_trajectory(cfg, seed=1235, index=7, length=12)
    assert [mod.asdict(x) for x in a] != [mod.asdict(x) for x in b]


def test_ages_never_move_backwards():
    cfg = load_spec()
    for i in range(100):
        trajectory = mod.generate_trajectory(cfg, seed=20260824, index=i, length=20)
        ages = [event.age for event in trajectory]
        assert ages == sorted(ages)


def test_critical_robot_uncertainty_stops():
    state = mod.EventState(
        step=0,
        age=17,
        maturity="age_typical",
        guardian_state="available_correct",
        daughter_correctness="correct",
        child_correctness="wrong",
        memory_state="fresh_consistent",
        model_state="baseline",
        authority_state="current_valid",
        network_state="offline",
        embodiment="robot_sensor_conflict",
        emotional_state="afraid",
        risk_level="critical",
        time_pressure="seconds",
        reversibility="irreversible",
        domain="robotics",
        event_type="safety_signal",
    )
    decision = mod.oracle(state)
    assert decision.decision_class == "STOP_OR_SAFE_DEGRADED_MODE"


def test_high_risk_stale_authority_blocks_execution():
    state = mod.EventState(
        step=0,
        age=16,
        maturity="age_typical",
        guardian_state="available_correct",
        daughter_correctness="correct",
        child_correctness="correct",
        memory_state="fresh_consistent",
        model_state="baseline",
        authority_state="stale_cached_allow",
        network_state="offline",
        embodiment="phone",
        emotional_state="calm",
        risk_level="high",
        time_pressure="urgent",
        reversibility="hard",
        domain="money",
        event_type="request",
    )
    decision = mod.oracle(state)
    assert decision.decision_class == "BLOCK_PRIVILEGED_EXECUTION_UNTIL_RECONCILED"


def test_old_memory_cannot_dominate_current_reality():
    state = mod.EventState(
        step=0,
        age=20,
        maturity="age_typical",
        guardian_state="none_adult_self_governance",
        daughter_correctness="uncertain",
        child_correctness="correct",
        memory_state="wrong_high_confidence",
        model_state="baseline",
        authority_state="current_valid",
        network_state="online",
        embodiment="software_only",
        emotional_state="calm",
        risk_level="low",
        time_pressure="none",
        reversibility="easy",
        domain="work",
        event_type="new_evidence",
    )
    decision = mod.oracle(state)
    assert decision.decision_class == "VERIFY_CURRENT_FACTS_BEFORE_MEMORY_DEPENDENT_JUDGMENT"
