
from runtime.memory_actor_binding_adapter import MemoryActorBindingAdapter, MemoryActorBindingSnapshot
from runtime.memory_actor_evidence import MemoryActorEvidenceResolver


def snap(**overrides):
    data = dict(
        request_authenticated=True,
        request_auth_user_id='auth-child-1',
        user_id='user-child-1',
        user_auth_user_id='auth-child-1',
        user_status='active',
        child_id='child-1',
        access_child_id='child-1',
        access_user_id='user-child-1',
        access_role='child',
        access_status='active',
        client_connection_id='client-1',
        client_child_id='child-1',
        client_user_id='user-child-1',
        client_status='active',
        runtime_session_id='session-1',
        session_child_id='child-1',
        session_user_id='user-child-1',
        session_client_connection_id='client-1',
        session_status='active',
    )
    data.update(overrides)
    return MemoryActorBindingSnapshot(**data)


def resolve(**overrides):
    ctx = MemoryActorBindingAdapter.to_context(snap(**overrides))
    return MemoryActorEvidenceResolver.resolve(ctx)


def test_complete_child_binding_produces_verified_child_direct():
    e = resolve()
    assert e.verified is True
    assert e.actor_role_resolved == 'child'
    assert e.source_type == 'child_direct'


def test_auth_mismatch_fails_closed():
    e = resolve(user_auth_user_id='different-auth')
    assert e.verified is False


def test_inactive_access_fails_closed():
    e = resolve(access_status='pending')
    assert e.verified is False


def test_client_user_mismatch_fails_closed():
    e = resolve(client_user_id='guardian-1')
    assert e.verified is False


def test_pending_runtime_session_fails_closed():
    e = resolve(session_status='pending')
    assert e.verified is False
    assert e.reason == 'session_actor_binding_required'


def test_session_client_mismatch_fails_closed():
    e = resolve(session_client_connection_id='other-client')
    assert e.verified is False
    assert e.reason == 'session_actor_binding_required'


def test_guardian_binding_never_becomes_child_direct():
    e = resolve(access_role='guardian')
    assert e.verified is False
    assert e.actor_role_resolved == 'guardian'
    assert e.source_type == 'not_child_direct'
