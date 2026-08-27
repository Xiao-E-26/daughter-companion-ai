import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

import pytest

from runtime.behavior_mode_router import RouterInput
from runtime.behavior_shadow_router import BehaviorShadowRouter
from runtime.model_adapter import ModelRequest, ModelResponse
from runtime.orchestrator import DaughterOrchestrator, RuntimeRequest


FIXTURES = Path(__file__).parent / "fixtures" / "behavior_shadow_staging_v1.json"


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


def load_scenarios():
    return json.loads(FIXTURES.read_text(encoding="utf-8"))


@pytest.mark.parametrize("scenario", load_scenarios(), ids=lambda item: item["id"])
def test_staging_shadow_observes_without_controlling_response(scenario):
    request = RuntimeRequest(
        user_id="staging-shadow-user",
        session_id=f"staging-{scenario['id']}",
        message=scenario["message"],
        age=7,
        risk_level="low",
    )
    baseline_model = CaptureModel()
    shadow_model = CaptureModel()

    baseline = DaughterOrchestrator(baseline_model).handle(request)
    shadow_request = RuntimeRequest(
        **{
            **request.__dict__,
            "behavior_shadow_input": RouterInput(**scenario["signals"]),
        }
    )
    shadow = DaughterOrchestrator(
        shadow_model,
        behavior_shadow_router=BehaviorShadowRouter(),
    ).handle(shadow_request)

    assert shadow.shadow_behavior_route["status"] == "OBSERVED"
    assert shadow.shadow_behavior_route["family"] == scenario["expected_family"]
    assert shadow.shadow_behavior_route["controls_response"] is False
    assert shadow.text == baseline.text
    assert shadow.boundary_decision == baseline.boundary_decision
    assert shadow_model.requests == baseline_model.requests
    assert "shadow_behavior_route" not in shadow_model.requests[0].metadata
    assert "Router" not in shadow_model.requests[0].system_prompt


def test_staging_shadow_invalid_signal_fails_open_for_existing_response_path():
    request = RuntimeRequest(
        user_id="staging-shadow-user",
        session_id="staging-invalid-signal",
        message="我想说说今天发生的事。",
        age=7,
        risk_level="low",
        behavior_shadow_input=RouterInput(safety_level="INVALID"),
    )
    model = CaptureModel()
    response = DaughterOrchestrator(
        model,
        behavior_shadow_router=BehaviorShadowRouter(),
    ).handle(request)

    assert response.text == "UNCHANGED:我想说说今天发生的事。"
    assert response.shadow_behavior_route["status"] == "ERROR"
    assert response.shadow_behavior_route["controls_response"] is False
    assert len(model.requests) == 1
