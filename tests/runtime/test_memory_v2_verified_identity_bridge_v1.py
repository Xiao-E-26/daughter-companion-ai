from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MIGRATION = ROOT / "db" / "migrations" / "20260916_memory_v2_verified_identity_bridge_v1.sql"


def _sql() -> str:
    return MIGRATION.read_text(encoding="utf-8")


def test_bridge_requires_verified_live_child_identity_and_session():
    sql = _sql()
    assert "ca.role = 'child'" in sql
    assert "ca.status = 'active'" in sql
    assert "ca.verified_at is not null" in sql
    assert "u.status = 'active'" in sql
    assert "u.auth_user_id is not null" in sql
    assert "rs.status = 'active'" in sql
    assert "cc.status = 'active'" in sql
    assert "rs.client_connection_id" in sql


def test_bridge_maps_memory_account_to_public_user_and_supabase_auth():
    sql = _sql()
    assert "p_account_id,'supabase_auth',v_auth_user_id::text" in sql
    assert "relationship_role='child'" in sql
    assert "can_submit_child_pinned=true" in sql
    assert "verified_child_identity_binding_required" in sql


def test_pin_remains_fail_closed_on_all_policy_gates():
    sql = _sql()
    for token in (
        "durable_memory_gate_off",
        "not_long_term_memory_create",
        "source_not_verified_child_direct",
        "actor_not_verified_child",
        "intent_confidence_too_low",
        "missing_idempotency_key",
        "empty_summary",
        "privacy_gate_not_passed",
        "sensitivity_gate_not_passed",
        "minimum_necessary_gate_not_passed",
        "visibility_gate_not_passed",
    ):
        assert token in sql


def test_private_helper_is_not_exposed_to_client_or_service_role():
    sql = _sql()
    assert "revoke all on function memory_v2_private.ensure_verified_child_link(uuid,uuid)" in sql
    assert "from public, anon, authenticated, service_role" in sql
    assert "grant execute on function memory_v2_api.pin_child_memory(jsonb) to service_role" in sql
    assert "revoke all on function memory_v2_api.pin_child_memory(jsonb) from public, anon, authenticated" in sql


def test_identity_bridge_does_not_enable_durable_mode():
    sql = _sql()
    assert "update memory_v2_private.runtime_flags" not in sql.lower()
    assert "insert into memory_v2_private.runtime_flags" not in sql.lower()
