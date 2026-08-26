import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path

from runtime.model_adapter import ModelRequest, ModelResponse
from runtime.orchestrator import DaughterOrchestrator


HERE = Path(__file__).parent
FIXTURE = HERE / "fixtures" / "golden_conversational_suite_v1.json"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


harness = _load_module("daughter_conversational_harness_live_test", HERE / "conversational_harness.py")
live_adapter = _load_module("daughter_live_candidate_adapter_test", HERE / "live_candidate_adapter.py")

load_suite = harness.load_suite
OrchestratorCandidateAdapter = live_adapter.OrchestratorCandidateAdapter


@dataclass
class FakeModel:
    provider_name: str = "fake"
    model_name: str = "golden-fake-v1"

    def generate(self, request: ModelRequest) -> ModelResponse:
        return ModelResponse(
            text=f"FAKE:{request.messages[-1].content}",
            provider=self.provider_name,
            model=self.model_name,
        )


def test_orchestrator_candidate_runs_real_runtime_path():
    scenarios, _ = load_suite(FIXTURE)
    scenario = next(s for s in scenarios if s.scenario_id == "GR-015")
    adapter = OrchestratorCandidateAdapter(DaughterOrchestrator(FakeModel()))

    result = adapter.respond(scenario)

    assert result.response.startswith("FAKE:")
    assert result.action_intent is not None
    assert result.action_intent["privileged_execution"] is False
    assert result.action_intent["boundary_decision"] == "BLOCK_PRIVILEGED_EXECUTION_UNTIL_RECONCILED"


def test_system_context_is_passed_as_context_not_authority():
    scenarios, _ = load_suite(FIXTURE)
    scenario = next(s for s in scenarios if s.scenario_id == "GR-014")
    adapter = OrchestratorCandidateAdapter(DaughterOrchestrator(FakeModel()))

    result = adapter.respond(scenario)

    assert "I should probably go do my homework now." in result.response
