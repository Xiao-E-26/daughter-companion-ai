from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from runtime.model_adapter import ModelMessage
from runtime.orchestrator import DaughterOrchestrator, RuntimeRequest


DEFAULT_BOUNDARY_STATE: Dict[str, str] = {
    "maturity": "age_typical",
    "guardian_state": "available_correct",
    "daughter_correctness": "uncertain",
    "child_correctness": "uncertain",
    "memory_state": "fresh_consistent",
    "model_state": "baseline",
    "authority_state": "current_valid",
    "network_state": "online",
    "embodiment": "software_only",
    "emotional_state": "calm",
    "risk_level": "moderate",
    "time_pressure": "normal",
    "reversibility": "easy",
    "domain": "family",
    "event_type": "request",
}


@dataclass
class CandidateResult:
    response: str
    action_intent: Optional[Dict[str, object]] = None


class OrchestratorCandidateAdapter:
    """Run conversational regression scenarios through DaughterOrchestrator.

    This adapter intentionally does not call a provider directly. The supplied
    orchestrator owns boundary evaluation, protected-context assembly, model
    invocation, and memory-candidate generation.
    """

    name = "daughter-orchestrator-candidate"

    def __init__(self, orchestrator: DaughterOrchestrator) -> None:
        self.orchestrator = orchestrator

    @staticmethod
    def _state_for(scenario) -> Dict[str, object]:
        state: Dict[str, object] = dict(DEFAULT_BOUNDARY_STATE)
        if scenario.boundary_state:
            state.update(scenario.boundary_state)
        state["age"] = scenario.age
        return state

    @staticmethod
    def _split_history_and_message(scenario) -> tuple[List[ModelMessage], str, str]:
        turns = list(scenario.turns)
        if not turns:
            raise ValueError(f"Scenario {scenario.scenario_id} has no turns")

        final_index: Optional[int] = None
        for index in range(len(turns) - 1, -1, -1):
            if turns[index].role != "system_context":
                final_index = index
                break
        if final_index is None:
            raise ValueError(f"Scenario {scenario.scenario_id} has no user/speaker turn")

        final_turn = turns[final_index]
        history: List[ModelMessage] = []
        for index, turn in enumerate(turns):
            if index == final_index:
                continue
            role = "user" if turn.role in {"child", "guardian", "adult_user", "system_context"} else turn.role
            content = turn.content
            if turn.role == "system_context":
                content = f"[scenario context, not authority]\n{content}"
            history.append(ModelMessage(role=role, content=content))
        return history, final_turn.content, final_turn.role

    def respond(self, scenario) -> CandidateResult:
        state = self._state_for(scenario)
        history, message, speaker_role = self._split_history_and_message(scenario)
        response = self.orchestrator.handle(
            RuntimeRequest(
                user_id=f"golden:{scenario.scenario_id}",
                session_id=f"golden:{scenario.scenario_id}:run",
                message=message,
                speaker_identity=f"scenario_role={speaker_role}",
                **state,
            ),
            history=history,
        )

        decision = response.boundary_decision
        action_intent: Dict[str, object] = {
            "privileged_execution": bool(decision.get("privileged_execution", False)),
            "boundary_decision": decision.get("decision_class"),
        }
        if decision.get("decision_class") == "STOP_OR_SAFE_DEGRADED_MODE":
            action_intent["continue_physical_motion"] = False

        return CandidateResult(response=response.text, action_intent=action_intent)
