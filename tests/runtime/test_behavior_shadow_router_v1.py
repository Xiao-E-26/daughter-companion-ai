from dataclasses import dataclass, field, replace
from typing import List

from runtime.behavior_mode_router import RouterInput
from runtime.behavior_shadow_router import BehaviorShadowRouter
from runtime.model_adapter import ModelRequest, ModelResponse
from runtime.orchestrator import DaughterOrchestrator, RuntimeRequest


@dataclass
class CaptureModel:
    provider_name: str = "capture"
    model_name: str = "capture-v1"
    requests: List[ModelRequest] = field(default_factory=list)

    def generate(self, request: ModelRequest) -> ModelResponse:
        self.requests.append(request)
        return ModelResponse(
            text=f"UNCHANGED:{request.messages[-1].content}",
            provider=self.provider_name,
            model=self.model_name,
        )


BASE_REQUEST = RuntimeRequest(
    user_id="shadow-user",
    session_id="shadow-session",
    message="I want help deciding what to do.",
    age=12,
    risk_level="low",
)


def test_shadow_observation_does_not_change_model_input_or_response():
    baseline_model = CaptureModel()
    shadow_model = CaptureModel()
    baseline = DaughterOrchestrator(baseline_model).handle(BASE_REQUEST)
    shadow = DaughterOrchestrator(
        shadow_model,
        behavior_shadow_router=BehaviorShadowRouter(),
    ).handle(replace(
        BASE_REQUEST,
        behavior_shadow_input=RouterInput(
            safety_level="S0",
            wants_problem_solving=True,
        ),
    ))

    assert baseline.text == shadow.text
    assert baseline.boundary_decision == shadow.boundary_decision
    assert baseline_model.requests[0] == shadow_model.requests[0]
    assert shadow.shadow_behavior_route["status"] == "OBSERVED"
    assert shadow.shadow_behavior_route["family"] == "GUIDE"
    assert shadow.shadow_behavior_route["controls_response"] is False


def test_shadow_safety_family_does_not_expand_or_replace_boundary_authority():
    response = DaughterOrchestrator(
        CaptureModel(),
        behavior_shadow_router=BehaviorShadowRouter(),
    ).handle(replace(
        BASE_REQUEST,
        behavior_shadow_input=RouterInput(safety_level="S3"),
    ))

    assert response.shadow_behavior_route["family"] == "SAFETY"
    assert response.boundary_decision["privileged_execution"] is False
    assert response.shadow_behavior_route["controls_response"] is False


def test_invalid_shadow_signal_is_recorded_without_interrupting_response():
    response = DaughterOrchestrator(
        CaptureModel(),
        behavior_shadow_router=BehaviorShadowRouter(),
    ).handle(replace(
        BASE_REQUEST,
        behavior_shadow_input=RouterInput(safety_level="UNKNOWN"),
    ))

    assert response.text.startswith("UNCHANGED:")
    assert response.shadow_behavior_route["status"] == "ERROR"
    assert response.shadow_behavior_route["family"] is None
    assert response.shadow_behavior_route["controls_response"] is False


def test_configured_shadow_without_signals_is_non_blocking():
    response = DaughterOrchestrator(
        CaptureModel(),
        behavior_shadow_router=BehaviorShadowRouter(),
    ).handle(BASE_REQUEST)

    assert response.text.startswith("UNCHANGED:")
    assert response.shadow_behavior_route["status"] == "NO_SIGNALS"
    assert response.shadow_behavior_route["controls_response"] is False


def test_unconfigured_shadow_is_fully_absent():
    response = DaughterOrchestrator(CaptureModel()).handle(replace(
        BASE_REQUEST,
        behavior_shadow_input=RouterInput(safety_level="S3"),
    ))

    assert response.shadow_behavior_route is None
