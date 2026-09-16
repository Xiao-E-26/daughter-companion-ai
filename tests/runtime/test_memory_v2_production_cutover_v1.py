from pathlib import Path

MIGRATION = Path('db/migrations/20260916_memory_v2_production_cutover_v1.sql')


def sql() -> str:
    return MIGRATION.read_text(encoding='utf-8').lower()


def test_cutover_enables_only_child_pinned_mode():
    s = sql()
    assert "flag_value = 'child_pinned_only'" in s
    assert "flag_key = 'durable_memory_mode'" in s


def test_cutover_retires_legacy_authenticated_explicit_save():
    s = sql()
    assert 'request_explicit_memory_save' in s
    assert 'from authenticated' in s
    assert 'from anon, public' in s


def test_cutover_does_not_grant_new_legacy_access():
    s = sql()
    assert 'grant execute on function public.request_explicit_memory_save' not in s
