from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MULTI = ROOT / "runtime" / "XIAOAI_MULTI_ENTRY_ACCESS_V1.md"
AUTH_HOOK = ROOT / "db" / "migrations" / "20260916_child_device_auth_hook_cutover_v1.sql"


def test_device_entry_requires_verified_authorization():
    text = MULTI.read_text(encoding="utf-8")
    sql = AUTH_HOOK.read_text(encoding="utf-8").lower()
    assert "entry point is a client, not the identity itself" in text
    assert "No entry point gains authority merely by saying `小爱上线`." in text
    assert "xiaoai_enrollment_token" in sql
    assert "valid child-device enrollment is required" in sql


def test_device_does_not_create_second_brain():
    text = MULTI.read_text(encoding="utf-8")
    assert "device-local prompt must not become authoritative shared XiaoAi state" in text
    assert "One XiaoAi Relationship" in text


def test_device_auth_cutover_does_not_claim_persona_runtime_cutover():
    text = MULTI.read_text(encoding="utf-8")
    assert "Production persona persistence: NOT YET" in text
    assert "Live conversational serving: NOT ACTIVE" in text
