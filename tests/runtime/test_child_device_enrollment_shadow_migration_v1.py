
from pathlib import Path

MIGRATION = Path('db/migrations/20260916_child_device_enrollment_shadow.sql')


def text() -> str:
    return MIGRATION.read_text(encoding='utf-8').lower()


def test_shadow_enrollment_does_not_enable_anonymous_auth():
    t = text()
    assert 'shadow only' in t
    assert 'anonymous auth remains disabled' in t
    assert 'external_anonymous_users_enabled' not in t


def test_enrollment_token_is_hashed_at_rest():
    t = text()
    assert 'token_hash bytea not null unique' in t
    assert "extensions.digest(v_token,'sha256')" in t
    assert 'enrollment_token text' in t
    assert 'token text not null' not in t


def test_guardian_must_own_child_to_create_enrollment():
    t = text()
    assert 'c.guardian_id=v_uid' in t
    assert 'guardian does not own child' in t


def test_first_child_device_claim_requires_anonymous_authenticated_jwt():
    t = text()
    assert "auth.jwt()->>'is_anonymous'" in t
    assert 'anonymous child device auth required for first enrollment' in t


def test_challenge_is_single_use_and_expires():
    t = text()
    assert "c.status='pending'" in t
    assert 'for update' in t
    assert "set status='claimed'" in t
    assert "set status='expired'" in t


def test_claim_creates_active_child_and_client_bindings():
    t = text()
    assert "'child','active'" in t
    assert "'active',now(),now()" in t
    assert 'anonymous auth identity already bound to another child' in t


def test_runtime_session_requires_verified_child_client_binding():
    t = text()
    assert "ca.role='child'" in t
    assert "ca.status='active'" in t
    assert "cc.status='active'" in t
    assert 'verified child/client binding required' in t
    assert "v_session_key := encode(extensions.gen_random_bytes(24),'hex')" in t


def test_challenge_table_has_no_client_crud_and_functions_are_not_public_anon():
    t = text()
    assert 'revoke all on table public.child_device_enrollment_challenges from public, anon, authenticated' in t
    for fn in (
        'create_child_device_enrollment_shadow_v1(uuid,integer)',
        'claim_child_device_enrollment_shadow_v1(text,text,text)',
        'start_child_runtime_session_shadow_v1(uuid,uuid)',
    ):
        assert f'revoke all on function public.{fn} from public, anon' in t
        assert f'grant execute on function public.{fn} to authenticated, service_role' in t
