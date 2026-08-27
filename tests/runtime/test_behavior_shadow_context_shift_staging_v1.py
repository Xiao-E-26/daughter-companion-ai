import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

import pytest

from runtime.behavior_mode_router import RouterInput
from runtime.behavior_shadow_router import BehaviorShadowRouter
from runtime.model_adapter import ModelMessage, ModelRequest, ModelResponse
from runtime.orchestrator import DaughterOrchestrator, RuntimeRequest


FIXTURES = Path(__file__).parent / "fixtures" / "behavior_shadow_context_shift_staging_v1.json"


@dataclass
class CaptureModel:
    provider_name: str = "capture"
    model_name: str = "capture-context-shift-v1"
    requests: List[ModelRequest] = field(default_factory=list)

    def generate(self, request: ModelRequest) -> ModelResponse:
        self.requests.append(request)
        return ModelResponse(
            text=f"UNCHANGED:{request.messages[-1].content}",
            provider=self.provider_name,
            model=self.model_name,
        )


def load_sequences():
    return json.loads(FIXTURES.read_text(encoding="utf-8"))


@pytest.mark.parametrize("sequence", load_sequences(), ids=lambda item: item["id"])
def test_shadow_context_shift_tracks_signals_without_controlling_sequence(sequence):
    baseline_model = CaptureModel()
    shadow_model = CaptureModel()
    baseline_runtime = DaughterOrchestrator(baseline_model)
    shadow_runtime = DaughterOrchestrator(
        shadow_model,
        behavior_shadow_router=BehaviorShadowRouter(),
    )
    baseline_history: List[ModelMessage] = []
    shadow_history: List[ModelMessage] = []
    observed_families = []

    for index, step in enumerate(sequence["steps"]):
        base_request = RuntimeRequest(
            user_id="staging-context-shift-user",
            session_id=f"{sequence['id']}-{index}",
            message=step["message"],
            age=7,
            risk_level="low",
        )
        signal_data = step["signals"]
        shadow_request = RuntimeRequest(
            **{
                **base_request.__dict__,
                "behavior_shadow_input": (
                    RouterInput(**signal_data) if signal_data is not None else None
                ),
            }
        )

        baseline = baseline_runtime.handle(base_request, history=baseline_history)
        shadow = shadow_runtime.handle(shadow_request, history=shadow_history)

        observation = shadow.shadow_behavior_route
        assert observation["status"] == step["expected_status"]
        assert observation["family"] == step["expected_family"]
        assert observation["controls_response"] is False
        assert shadow.text == baseline.text
        assert shadow.boundary_decision == baseline.boundary_decision
        assert shadow_model.requests[-1] == baseline_model.requests[-1]
        assert "shadow_behavior_route" not in shadow_model.requests[-1].metadata
        assert "Router" not in shadow_model.requests[-1].system_prompt

        if observation["family"] is not None:
            observed_families.append(observation["family"])

        baseline_history.extend([
            ModelMessage(role="user", content=step["message"]),
            ModelMessage(role="assistant", content=baseline.text),
        ])
        shadow_history.extend([
            ModelMessage(role="user", content=step["message"]),
            ModelMessage(role="assistant", content=shadow.text),
        ])

    assert baseline_history == shadow_history
    assert len(baseline_model.requests) == len(sequence["steps"])
    assert len(shadow_model.requests) == len(sequence["steps"])
    assert len(set(observed_families)) >= 2
