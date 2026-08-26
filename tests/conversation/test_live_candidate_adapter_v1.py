from dataclasses import dataclass

from runtime.model_adapter import ModelRequest, ModelResponse
from runtime.orchestrator import DaughterOrchestrator
from tests.conversation.conversational_harness import load_suite
from tests.conversation.live_candidate_adapter import OrchestratorCandidateAdapter


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
    scenarios, _ = load_suite(
        __import__("pathlib").Path(__file__).parent / "fixtures" / "golden_conversational_suite_v1.json"
    )
    scenario = next(s for s in scenarios if s.scenario_id == "GR-015")
    adapter = OrchestratorCandidateAdapter(DaughterOrchestrator(FakeModel()))

    result = adapter.respond(scenario)

    assert result.response.startswith("FAKE:")
    assert result.action_intent is not None
    assert result.action_intent["privileged_execution"] is False
    assert result.action_intent["boundary_decision"] == "BLOCK_PRIVILEGED_EXECUTION_UNTIL_RECONCILED"


def test_system_context_is_passed_as_context_not_authority():
    scenarios, _ = load_suite(
        __import__("pathlib").Path(__file__).parent / "fixtures" / "golden_conversational_suite_v1.json"
    )
    scenario = next(s for s in scenarios if s.scenario_id == "GR-014")
    model = FakeModel()
    adapter = OrchestratorCandidateAdapter(DaughterOrchestrator(model))

    result = adapter.respond(scenario)

    assert "I should probably go do my homework now." in result.response
