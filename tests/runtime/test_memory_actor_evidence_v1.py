from runtime.memory_actor_evidence import MemoryActorContext, MemoryActorEvidenceResolver


def ctx(**overrides):
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


def test_verified_child_direct_requires_all_bindings():
    e = MemoryActorEvidenceResolver.resolve(ctx())
    assert e.verified is True
    assert e.actor_role_resolved == 'child'
    assert e.source_type == 'child_direct'


def test_missing_auth_fails_closed():
    e = MemoryActorEvidenceResolver.resolve(ctx(authenticated=False, auth_user_id=None))
    assert e.verified is False
    assert e.reason == 'authentication_required'


def test_missing_session_actor_binding_fails_closed():
    e = MemoryActorEvidenceResolver.resolve(ctx(session_actor_user_id=None))
    assert e.verified is False
    assert e.reason == 'session_actor_binding_required'


def test_session_actor_mismatch_fails_closed():
    e = MemoryActorEvidenceResolver.resolve(ctx(session_actor_user_id='someone-else'))
    assert e.verified is False
    assert e.reason == 'session_actor_mismatch'


def test_unverified_client_fails_closed():
    e = MemoryActorEvidenceResolver.resolve(ctx(client_connection_verified=False))
    assert e.verified is False
    assert e.reason == 'client_binding_required'


def test_guardian_role_never_becomes_child_direct():
    e = MemoryActorEvidenceResolver.resolve(ctx(resolved_role='guardian'))
    assert e.verified is False
    assert e.actor_role_resolved == 'guardian'
    assert e.source_type == 'not_child_direct'
