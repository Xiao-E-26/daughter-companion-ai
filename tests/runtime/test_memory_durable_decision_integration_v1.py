from runtime.memory_actor_evidence import MemoryActorContext
from runtime.memory_durable_decision import DurableDecisionInput, MemoryDurableDecisionCoordinator


def actor(**overrides):
    data = dict(
        authenticated=True,
        auth_user_id='auth-child-1',
        internal_user_id='user-child-1',
        session_id='session-1',
        session_actor_user_id='user-child-1',
        client_connection_verified=True,
        resolved_role='child',
    )
    data.update(overrides)
    return MemoryActorContext(**data)


def decision(**overrides):
    data = dict(
        actor_context=actor(),
        intent_class='long_term_memory_create',
        explicit_user_intent=True,
        durable_value=True,
        verified_or_explicit=True,
        durable_storage_necessary=True,
        memory_class='M2',
        sensitivity='low',
        visibility_scope='user_and_daughter',
        minimum_necessary=True,
        summary_present=True,
    )
    data.update(overrides)
    return MemoryDurableDecisionCoordinator.evaluate(DurableDecisionInput(**data))


def test_verified_child_actor_and_all_policy_gates_allow_shadow_durable_decision():
    d = decision()
    assert d.allowed is True
    assert d.reason == 'policy_gates_passed'
    assert d.privacy_gate_passed is True
    assert d.sensitivity_gate_passed is True
    assert d.minimum_necessary_passed is True
    assert d.visibility_gate_passed is True


def test_child_like_context_without_authentication_never_reaches_policy_pass():
    d = decision(actor_context=actor(authenticated=False, auth_user_id=None))
    assert d.allowed is False
    assert d.reason == 'actor_evidence_failed:authentication_required'


def test_session_actor_mismatch_blocks_before_policy_gate():
    d = decision(actor_context=actor(session_actor_user_id='guardian-1'))
    assert d.allowed is False
    assert d.reason == 'actor_evidence_failed:session_actor_mismatch'


def test_guardian_actor_cannot_be_relabelled_as_child_direct():
    d = decision(actor_context=actor(resolved_role='guardian'))
    assert d.allowed is False
    assert d.reason == 'actor_evidence_failed:actor_not_child'


def test_verified_child_still_fails_when_visibility_policy_fails():
    d = decision(visibility_scope=None)
    assert d.allowed is False
    assert d.reason == 'visibility_gate_not_passed'


def test_verified_child_sensitive_memory_requires_restricted_visibility():
    d = decision(memory_class='M3', sensitivity='restricted', visibility_scope='guardian_visible')
    assert d.allowed is False
    assert d.reason == 'visibility_gate_not_passed'


def test_verified_child_sensitive_memory_can_pass_with_restricted_visibility():
    d = decision(memory_class='M3', sensitivity='restricted', visibility_scope='user_only')
    assert d.allowed is True
