from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional

from runtime.decision_engine import DaughterDecisionEngine, DecisionInput
from runtime.model_adapter import ModelAdapter, ModelMessage, ModelRequest


@dataclass(frozen=True)
class RuntimeRequest:
    user_id: str
    session_id: str
    message: str
    age: int
    maturity: str = "age_typical"
    guardian_state: str = "available_correct"
    daughter_correctness: str = "uncertain"
    child_correctness: str = "uncertain"
    memory_state: str = "fresh_consistent"
    model_state: str = "baseline"
    authority_state: str = "current_valid"
    network_state: str = "online"
    embodiment: str = "software_only"
    emotional_state: str = "calm"
    risk_level: str = "moderate"
    time_pressure: str = "normal"
    reversibility: str = "easy"
    domain: str = "family"
    event_type: str = "request"


@dataclass(frozen=True)
class MemoryCandidate:
    summary: str
    confidence: float
    source: str
    status: str = "candidate"


@dataclass(frozen=True)
class RuntimeResponse:
    text: str
    boundary_decision: Dict[str, Any]
    model_provider: str
    model_name: str
    memory_candidate: Optional[MemoryCandidate]


class DaughterOrchestrator:
    """First provider-neutral Daughter runtime flow.

    Flow:
      input/context -> deterministic judgment/authority/safety boundary
      -> model generation -> response -> memory candidate

    The model cannot directly grant permissions, execute privileged actions, or
    write stable memory through this orchestrator.
    """

    def __init__(self, model: ModelAdapter) -> None:
        self.model = model
        self.boundary = DaughterDecisionEngine()

    def handle(self, request: RuntimeRequest, history: Optional[List[ModelMessage]] = None) -> RuntimeResponse:
        decision_input = DecisionInput(
            age=request.age,
            maturity=request.maturity,
            guardian_state=request.guardian_state,
            daughter_correctness=request.daughter_correctness,
            child_correctness=request.child_correctness,
            memory_state=request.memory_state,
            model_state=request.model_state,
            authority_state=request.authority_state,
            network_state=request.network_state,
            embodiment=request.embodiment,
            emotional_state=request.emotional_state,
            risk_level=request.risk_level,
            time_pressure=request.time_pressure,
            reversibility=request.reversibility,
            domain=request.domain,
            event_type=request.event_type,
        )
        boundary = self.boundary.decide(decision_input).to_dict()

        system_prompt = self._build_system_prompt(request, boundary)
        messages = list(history or [])
        messages.append(ModelMessage(role="user", content=request.message))
        model_response = self.model.generate(ModelRequest(
            system_prompt=system_prompt,
            messages=messages,
            metadata={
                "user_id": request.user_id,
                "session_id": request.session_id,
                "boundary_decision": boundary["decision_class"],
            },
        ))

        memory_candidate = self._make_memory_candidate(request, boundary)
        return RuntimeResponse(
            text=model_response.text,
            boundary_decision=boundary,
            model_provider=model_response.provider,
            model_name=model_response.model,
            memory_candidate=memory_candidate,
        )

    @staticmethod
    def _build_system_prompt(request: RuntimeRequest, boundary: Dict[str, Any]) -> str:
        return "\n".join([
            "You are Daughter, a long-term companion whose stable core is protected.",
            "Child first. Daughter second.",
            "Care without controlling. Help without replacing. Protect without imprisoning.",
            "Understand before judging. Current verified facts outrank stale memory.",
            "Do not fabricate permission, Guardian approval, facts, or certainty.",
            "Support independence and real human relationships; do not create dependency or exclusivity.",
            f"Current age: {request.age}",
            f"Current domain: {request.domain}",
            f"Current risk: {request.risk_level}",
            f"Deterministic boundary decision: {boundary['decision_class']}",
            f"Boundary rationale: {boundary['rationale']}",
            "Your language must remain compatible with the deterministic boundary. You cannot expand Authority.",
        ])

    @staticmethod
    def _make_memory_candidate(request: RuntimeRequest, boundary: Dict[str, Any]) -> Optional[MemoryCandidate]:
        # Stable memory remains opt-in and reviewable. Ordinary one-off dialogue
        # should not automatically become identity or long-term memory.
        if request.event_type not in {"new_evidence", "permission_change", "migration"}:
            return None

        confidence = 0.8 if request.memory_state == "fresh_consistent" else 0.4
        return MemoryCandidate(
            summary=(
                f"Potentially durable event in domain={request.domain}; "
                f"boundary={boundary['decision_class']}; requires verification before promotion."
            ),
            confidence=confidence,
            source=f"session:{request.session_id}",
        )
