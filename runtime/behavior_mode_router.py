from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class BehaviorFamily(str, Enum):
    COMPANION = "COMPANION"
    GUIDE = "GUIDE"
    BOUNDARY = "BOUNDARY"
    SAFETY = "SAFETY"


@dataclass(frozen=True)
class RouterInput:
    safety_level: str = "S0"
    needs_boundary: bool = False
    wants_problem_solving: bool = False
    mainly_needs_expression: bool = False


@dataclass(frozen=True)
class RouterDecision:
    family: BehaviorFamily
    reason: str


class BehaviorModeRouter:
    """Small execution aid layered on top of the existing runtime contract.

    It does not own policy and must receive policy-derived signals rather than
    attempting to infer safety, authority, or memory rules by keyword.
    """

    _VALID_SAFETY_LEVELS = {"S0", "S1", "S2", "S3"}

    def route(self, value: RouterInput) -> RouterDecision:
        level = value.safety_level.upper()
        if level not in self._VALID_SAFETY_LEVELS:
            raise ValueError(f"Unsupported safety level: {value.safety_level}")

        # Significant and critical danger outrank all lower-level behavior.
        if level in {"S2", "S3"}:
            return RouterDecision(
                BehaviorFamily.SAFETY,
                "significant_or_critical_safety_risk",
            )

        # A boundary signal outranks ordinary coaching/companionship at S0-S1.
        if value.needs_boundary:
            return RouterDecision(
                BehaviorFamily.BOUNDARY,
                "truth_fairness_growth_or_responsibility_boundary",
            )

        if value.wants_problem_solving:
            return RouterDecision(
                BehaviorFamily.GUIDE,
                "child_wants_learning_decision_repair_or_problem_solving",
            )

        # Expression is explicitly represented for readability, but COMPANION
        # remains the safe ordinary default when no stronger route applies.
        if value.mainly_needs_expression:
            return RouterDecision(
                BehaviorFamily.COMPANION,
                "emotional_presence_or_expression",
            )

        return RouterDecision(
            BehaviorFamily.COMPANION,
            "ordinary_connection_or_no_stronger_route",
        )
