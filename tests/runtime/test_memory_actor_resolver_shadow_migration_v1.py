
from pathlib import Path

MIGRATION = Path('db/migrations/20260916_memory_actor_resolver_shadow.sql')


def text() -> str:
    return MIGRATION.read_text(encoding='utf-8').lower()


def test_shadow_resolver_uses_supabase_auth_identity():
    t = text()
    assert 'auth.uid()' in t
    assert "u.status = 'active'" in t


def test_shadow_resolver_requires_active_child_access():
    t = text()
    assert "ca.status = 'active'" in t
    assert "ca.role='child'" in t
    assert "actor_not_child" in t


def test_shadow_resolver_requires_active_session_and_client_binding():
    t = text()
    assert "rs.status = 'active'" in t
    assert "cc.status = 'active'" in t
    assert 'cc.id = rs.client_connection_id' in t
    assert 'active_session_client_binding_required' in t


def test_shadow_resolver_can_only_emit_child_direct_after_all_bindings():
    t = text()
    assert "select true,'child','child_direct'" in t
    assert 'verified_child_direct' in t


def test_shadow_resolver_is_not_public_or_anon_callable():
    t = text()
    assert 'revoke all on function public.resolve_memory_actor_evidence_shadow_v1(uuid,text) from public, anon' in t
    assert 'grant execute on function public.resolve_memory_actor_evidence_shadow_v1(uuid,text) to authenticated, service_role' in t
