from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List


class OwnershipTransitionState(str, Enum):
    NOT_ELIGIBLE = "not_eligible"
    ELIGIBLE = "eligible"
    REQUESTED = "requested"
    VERIFIED = "verified"
    COMPLETED = "completed"
    REVOKED = "revoked"


@dataclass(frozen=True)
class AdultSelfOwnershipRequest:
    user_id: str
    age: int
    adult_self_governance_confirmed: bool
    explicit_user_choice: bool
    destination_under_user_control: bool
    identity_continuity_verified: bool
    data_export_verified: bool
    permission_review_completed: bool
    guardian_privileges_reviewed: bool


@dataclass(frozen=True)
class AdultSelfOwnershipDecision:
    state: OwnershipTransitionState
    allowed: bool
    reasons: List[str]
    preserve_identity_continuity: bool = True
    inherit_guardian_privileges: bool = False
    require_permission_rebinding: bool = True


class AdultSelfOwnershipTransition:
    """Authority-layer contract for optional adult privatization of Daughter.

    This transition changes who controls the deployment, data and credentials.
    It does NOT redefine Daughter's identity, protected purpose or relationship
    principles.

    Core rule:
        identity continuity may transfer;
        authority and credentials must be explicitly rebound.

    Guardian-era privileges never silently become adult-owner privileges.
    """

    def evaluate(self, request: AdultSelfOwnershipRequest) -> AdultSelfOwnershipDecision:
        reasons: List[str] = []

        if request.age < 18:
            reasons.append("legal_adulthood_not_reached")
        if not request.adult_self_governance_confirmed:
            reasons.append("adult_self_governance_not_confirmed")
        if not request.explicit_user_choice:
            reasons.append("explicit_user_choice_required")
        if not request.destination_under_user_control:
            reasons.append("destination_must_be_under_adult_user_control")
        if not request.identity_continuity_verified:
            reasons.append("identity_continuity_verification_required")
        if not request.data_export_verified:
            reasons.append("data_export_verification_required")
        if not request.permission_review_completed:
            reasons.append("permission_review_required")
        if not request.guardian_privileges_reviewed:
            reasons.append("guardian_privilege_review_required")

        if reasons:
            state = (
                OwnershipTransitionState.NOT_ELIGIBLE
                if request.age < 18 or not request.adult_self_governance_confirmed
                else OwnershipTransitionState.REQUESTED
            )
            return AdultSelfOwnershipDecision(
                state=state,
                allowed=False,
                reasons=reasons,
            )

        return AdultSelfOwnershipDecision(
            state=OwnershipTransitionState.VERIFIED,
            allowed=True,
            reasons=["adult_self_ownership_transition_verified"],
        )

    @staticmethod
    def completion_requirements() -> List[str]:
        return [
            "new_repository_or_runtime_controlled_by_adult_user",
            "new_database_or_local_store_controlled_by_adult_user",
            "new_credentials_issued_to_adult_user",
            "guardian_credentials_revoked_or_re-scoped",
            "permissions_rebound_under_adult_authority",
            "identity_and_protected_core_integrity_verified",
            "data_export_import_integrity_verified",
            "rollback_or_recovery_record_created",
        ]
