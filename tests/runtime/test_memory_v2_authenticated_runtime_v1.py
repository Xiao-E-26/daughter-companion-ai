from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MIGRATION = ROOT / 'db/migrations/20260916_memory_v2_authenticated_runtime_api_v1.sql'
EDGE = ROOT / 'supabase/functions/xiaoi-memory-runtime/index.ts'


def test_authenticated_runtime_api_is_fail_closed_and_child_bound():
    sql = MIGRATION.read_text(encoding='utf-8')
    assert 'request_child_pinned_memory_v2' in sql
    assert 'retrieve_child_pinned_memories_v2' in sql
    assert 'resolve_memory_actor_evidence_shadow_v1' in sql
    assert "actor_role_resolved,'') <> 'child'" in sql
    assert "source_type,'') <> 'child_direct'" in sql
    assert 'explicit_user_intent_required' in sql
    assert 'durable_value_not_established' in sql
    assert 'verification_not_established' in sql
    assert 'durable_storage_not_necessary' in sql
    assert 'sensitivity_gate_not_passed' in sql
    assert 'minimum_necessary_gate_not_passed' in sql
    assert 'visibility_gate_not_passed' in sql
    assert 'memory_v2_api.pin_child_memory' in sql
    assert 'to authenticated' in sql
    assert 'from public, anon, service_role' in sql


def test_edge_v5_uses_memory_v2_and_never_legacy_explicit_save():
    ts = EDGE.read_text(encoding='utf-8')
    assert "version:'5.0'" in ts
    assert "mode:'verified-child-pinned-memory-v2'" in ts
    assert "rpc(auth,'request_child_pinned_memory_v2'" in ts
    assert "rpc(auth,'retrieve_child_pinned_memories_v2'" in ts
    assert 'request_explicit_memory_save' not in ts
    assert "if (!b.session_key)" in ts
    assert "p_explicit_user_intent:b.explicit_user_intent === true" in ts
    assert "p_minimum_necessary:b.minimum_necessary === true" in ts
    assert "p_durable_storage_necessary:b.durable_storage_necessary === true" in ts


def test_edge_does_not_use_service_role_secret():
    ts = EDGE.read_text(encoding='utf-8')
    assert 'SUPABASE_SERVICE_ROLE_KEY' not in ts
    assert "Deno.env.get('SUPABASE_ANON_KEY')" in ts
    assert 'Authorization: auth' in ts
