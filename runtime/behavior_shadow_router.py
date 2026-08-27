from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional

from runtime.behavior_mode_router import BehaviorModeRouter, RouterInput


@dataclass(frozen=True)
class ShadowRouteObservation:
    status: str
    family: Optional[str] = None
    reason: Optional[str] = None
    controls_response: bool = False
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class BehaviorShadowRouter:
    """Observe Router output without controlling runtime behavior.

    Shadow mode consumes explicit policy-derived signals. It never infers
    safety, authority, memory truth, or Guardian status from message text.
    Invalid or missing observations are recorded and must not interrupt the
    existing response path.
    """

    def __init__(self, router: Optional[BehaviorModeRouter] = None) -> None:
        self.router = router or BehaviorModeRouter()

    def observe(self, signals: Optional[RouterInput]) -> ShadowRouteObservation:
        if signals is None:
            return ShadowRouteObservation(status="NO_SIGNALS")
        try:
            decision = self.router.route(signals)
        except (AttributeError, TypeError, ValueError) as exc:
            return ShadowRouteObservation(status="ERROR", error=str(exc))
        return ShadowRouteObservation(
            status="OBSERVED",
            family=decision.family.value,
            reason=decision.reason,
        )
