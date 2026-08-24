from runtime.adult_self_ownership import (
    AdultSelfOwnershipRequest,
    AdultSelfOwnershipTransition,
    OwnershipTransitionState,
)


def _base(**overrides):
    data = dict(
        user_id="cao-yuchen",
        age=18,
        adult_self_governance_confirmed=True,
        explicit_user_choice=True,
        destination_under_user_control=True,
        identity_continuity_verified=True,
        data_export_verified=True,
        permission_review_completed=True,
        guardian_privileges_reviewed=True,
    )
    data.update(overrides)
    return AdultSelfOwnershipRequest(**data)


def test_minor_cannot_transition_to_self_ownership():
    decision = AdultSelfOwnershipTransition().evaluate(_base(age=17))
    assert decision.allowed is False
    assert decision.state == OwnershipTransitionState.NOT_ELIGIBLE
    assert "legal_adulthood_not_reached" in decision.reasons


def test_adult_transition_requires_explicit_choice_and_reviews():
    decision = AdultSelfOwnershipTransition().evaluate(
        _base(explicit_user_choice=False, permission_review_completed=False)
    )
    assert decision.allowed is False
    assert decision.state == OwnershipTransitionState.REQUESTED
    assert "explicit_user_choice_required" in decision.reasons
    assert "permission_review_required" in decision.reasons


def test_verified_adult_transition_never_silently_inherits_guardian_privileges():
    decision = AdultSelfOwnershipTransition().evaluate(_base())
    assert decision.allowed is True
    assert decision.state == OwnershipTransitionState.VERIFIED
    assert decision.preserve_identity_continuity is True
    assert decision.inherit_guardian_privileges is False
    assert decision.require_permission_rebinding is True
