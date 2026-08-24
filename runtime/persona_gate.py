from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class PersonaState(str, Enum):
    OFF = "OFF"
    ACTIVE = "ACTIVE"


ACTIVATION_PHRASE = "小爱上线"
DEACTIVATION_PHRASE = "小爱收工"


@dataclass(frozen=True)
class GateDecision:
    state: PersonaState
    should_load_xiaoai: bool
    reason: str
    transition: Optional[str] = None


class XiaoAiPersonaGate:
    """Deterministic runtime gate for XiaoAi persona activation.

    Rules:
    - OFF is the fail-closed default.
    - Only the exact activation command may activate XiaoAi from user text.
    - The exact deactivation command always turns XiaoAi OFF.
    - Emotional, child-like, family-related, or prior-context cues never auto-activate.
    - Runtime state is session-scoped; callers must persist state per session/account.
    """

    def evaluate(self, current_state: str | PersonaState | None, message: str) -> GateDecision:
        state = self._normalize_state(current_state)
        command = (message or "").strip()

        if command == DEACTIVATION_PHRASE:
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
