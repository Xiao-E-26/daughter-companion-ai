
from pathlib import Path

MIGRATION = Path('db/migrations/20260916_identity_foundation_shadow_restore.sql')


def text() -> str:
    return MIGRATION.read_text(encoding='utf-8').lower()


def test_shadow_migration_is_explicitly_not_production_cutover():
    t = text()
    assert 'prepared only. do not apply to production yet' in t


def test_identity_tables_exist_in_shadow_contract():
    t = text()
    for name in ('public.users', 'public.companion_access', 'public.client_connections', 'public.runtime_sessions'):
        assert f'create table if not exists {name}' in t


def test_identity_bindings_default_fail_closed():
    t = text()
    assert "status text not null default 'pending'" in t
    assert "role in ('child','guardian')" in t
    assert "status in ('pending','active','revoked')" in t


def test_runtime_session_requires_user_and_client_binding_columns():
    t = text()
    assert 'user_id uuid not null references public.users(id)' in t
    assert 'client_connection_id uuid references public.client_connections(id)' in t


def test_rls_is_enabled_on_all_identity_tables():
    t = text()
    for name in ('users','companion_access','client_connections','runtime_sessions'):
        assert f'alter table public.{name} enable row level security' in t


def test_shadow_restore_does_not_create_permissive_authenticated_policy():
    t = text()
    assert 'create policy' not in t
    assert 'only service-role workflows may populate/bind these rows' in t
