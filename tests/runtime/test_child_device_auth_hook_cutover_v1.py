
from pathlib import Path

MIGRATION = Path('db/migrations/20260916_child_device_auth_hook_cutover_v1.sql')


def text() -> str:
    return MIGRATION.read_text(encoding='utf-8').lower()


def test_non_anonymous_signup_is_unchanged():
    t = text()
    assert 'if not v_is_anonymous then' in t
    assert "return '{}'::jsonb" in t


def test_anonymous_signup_requires_high_entropy_enrollment_and_client_type():
    t = text()
    assert 'xiaoai_enrollment_token' in t
    assert 'client_type' in t
    assert '^[0-9a-fa-f]{64}$' in t
    assert 'valid child-device enrollment is required' in t


def test_auth_hook_checks_hash_pending_and_expiry():
    t = text()
    assert "extensions.digest(v_token,'sha256')" in t
    assert "c.status='pending'" in t
    assert 'c.expires_at>now()' in t


def test_auth_hook_is_auth_admin_only_and_has_rls_read_policy():
    t = text()
    assert 'grant execute on function public.hook_xiaoai_child_enrollment_before_user_created_v1(jsonb) to supabase_auth_admin' in t
    assert 'from authenticated,anon,public,service_role' in t
    assert 'supabase_auth_admin_read_child_device_enrollment_challenges' in t
    assert 'to supabase_auth_admin' in t
    assert 'using(true)' in t


def test_after_insert_trigger_only_handles_anonymous_auth_users():
    t = text()
    assert 'after insert on auth.users' in t
    assert 'when (new.is_anonymous is true)' in t
    assert 'finalize_xiaoai_anonymous_child_enrollment_v1' in t


def test_finalizer_locks_and_claims_one_time_challenge():
    t = text()
    assert 'for update' in t
    assert "set status='claimed'" in t
    assert 'claimed_auth_user_id=new.id' in t


def test_finalizer_creates_verified_identity_bindings():
    t = text()
    assert 'insert into public.users(auth_user_id,status)' in t
    assert 'insert into public.companion_access(child_id,user_id,role,status,verified_at)' in t
    assert "'child','active'" in t
    assert 'insert into public.client_connections' in t


def test_plaintext_enrollment_token_is_scrubbed_from_auth_metadata():
    t = text()
    assert "raw_user_meta_data=coalesce(raw_user_meta_data,'{}'::jsonb)-'xiaoai_enrollment_token'" in t


def test_finalizer_has_no_client_or_service_role_execute():
    t = text()
    assert 'revoke all on function public.finalize_xiaoai_anonymous_child_enrollment_v1()' in t
    assert 'from public,anon,authenticated,service_role' in t


def test_parallel_client_claim_path_is_retired():
    t = text()
    assert 'revoke execute on function public.claim_child_device_enrollment_shadow_v1(text,text,text)' in t
    assert 'from authenticated,service_role,anon,public' in t


def test_migration_does_not_enable_anonymous_provider_by_itself():
    t = text()
    assert 'external_anonymous_users_enabled' not in t
    assert 'hook_before_user_created_enabled' not in t
