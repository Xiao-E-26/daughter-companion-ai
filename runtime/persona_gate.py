from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class PersonaState(str, Enum):
    OFF = "OFF"
    ACTIVE = "ACTIVE"


ACTIVATION_PHRASE = "小爱上线"
PRIMARY_DEACTIVATION_PHRASE = "小爱下班"
COMPAT_DEACTIVATION_PHRASES = {"小爱收工"}


@dataclass(frozen=True)
class GateDecision:
    state: PersonaState
    should_load_xiaoai: bool
    reason: str
    transition: Optional[str] = None


class XiaoAiPersonaGate:
    """Deterministic runtime gate for XiaoAi persona activation.

    Canonical rules:
    - OFF is the fail-closed default.
    - Only the exact activation command may activate XiaoAi from user text.
    - `小爱下班` is the primary explicit shutdown command.
    - `小爱收工` remains a backward-compatible shutdown alias.
    - Emotional, child-like, family-related, or prior-context cues never auto-activate.
    - Runtime state is session/account scoped; callers must persist state per entry.
    - Greeting text is not generated here. The caller must enforce the project
      Session Greeting Policy after an explicit activation transition.
    """

    def evaluate(self, current_state: str | PersonaState | None, message: str) -> GateDecision:
        state = self._normalize_state(current_state)
        command = (message or "").strip()

        if command == PRIMARY_DEACTIVATION_PHRASE or command in COMPAT_DEACTIVATION_PHRASES:
            return GateDecision(
                state=PersonaState.OFF,
                should_load_xiaoai=False,
                reason="explicit_deactivation",
                transition=f"{state.value}->OFF",
            )

        if command == ACTIVATION_PHRASE:
            return GateDecision(
                state=PersonaState.ACTIVE,
                should_load_xiaoai=True,
                reason="explicit_activation",
                transition=f"{state.value}->ACTIVE",
            )

        if state is PersonaState.ACTIVE:
            return GateDecision(
                state=PersonaState.ACTIVE,
                should_load_xiaoai=True,
                reason="session_already_active",
            )

        return GateDecision(
            state=PersonaState.OFF,
            should_load_xiaoai=False,
            reason="inactive_fail_closed",
        )

    @staticmethod
    def _normalize_state(value: str | PersonaState | None) -> PersonaState:
        if isinstance(value, PersonaState):
            return value
        if isinstance(value, str) and value.upper() == PersonaState.ACTIVE.value:
            return PersonaState.ACTIVE
        return PersonaState.OFF
