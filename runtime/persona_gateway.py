from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from runtime.persona_gate import GateDecision, PersonaState, XiaoAiPersonaGate


class PersonaStateStore(Protocol):
    def get_state(self, *, daughter_id: str, user_id: str, session_key: str) -> str | None: ...

    def set_state(
        self,
        *,
        daughter_id: str,
        user_id: str,
        session_key: str,
        state: PersonaState,
        activation_source: str | None,
    ) -> None: ...


@dataclass(frozen=True)
class GatewayResult:
    persona_state: PersonaState
    should_load_xiaoai: bool
    route: str
    reason: str
    transition: str | None = None


class XiaoAiRuntimeGateway:
    """Single entry gate before any XiaoAi identity/behavior context is loaded.

    The gateway is intentionally model-agnostic. It decides routing first, then the
    caller may build XiaoAi context only when ``should_load_xiaoai`` is true.
    """

    def __init__(self, store: PersonaStateStore, gate: XiaoAiPersonaGate | None = None) -> None:
        self.store = store
        self.gate = gate or XiaoAiPersonaGate()

    def handle_message(
        self,
        *,
        daughter_id: str,
        user_id: str,
        session_key: str,
        message: str,
        activation_source: str = "explicit_command",
    ) -> GatewayResult:
        current = self.store.get_state(
            daughter_id=daughter_id,
            user_id=user_id,
            session_key=session_key,
        )

        decision: GateDecision = self.gate.evaluate(current, message)

        if decision.transition is not None:
            self.store.set_state(
                daughter_id=daughter_id,
                user_id=user_id,
                session_key=session_key,
                state=decision.state,
                activation_source=(activation_source if decision.state is PersonaState.ACTIVE else None),
            )

        return GatewayResult(
            persona_state=decision.state,
            should_load_xiaoai=decision.should_load_xiaoai,
            route="xiaoai" if decision.should_load_xiaoai else "normal_assistant",
            reason=decision.reason,
            transition=decision.transition,
        )


class InMemoryPersonaStateStore:
    """Reference/test store. Production should use an authenticated Supabase adapter."""

    def __init__(self) -> None:
        self._states: dict[tuple[str, str, str], PersonaState] = {}

    def get_state(self, *, daughter_id: str, user_id: str, session_key: str) -> str | None:
        state = self._states.get((daughter_id, user_id, session_key))
        return state.value if state else None

    def set_state(
        self,
        *,
        daughter_id: str,
        user_id: str,
        session_key: str,
        state: PersonaState,
        activation_source: str | None,
    ) -> None:
        self._states[(daughter_id, user_id, session_key)] = state
