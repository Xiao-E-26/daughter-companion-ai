from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "runtime" / "XIAOAI_IDENTITY_RESOLVER_SHADOW_V1.md"


def _text() -> str:
    return DOC.read_text(encoding="utf-8")


def test_identity_resolver_requires_authenticated_subject():
    text = _text()
    assert "verify_jwt = true" in text
    assert "accepts only authenticated requests" in text
    assert "never authenticates from a phrase" in text


def test_identity_resolver_is_not_xiaoai_brain():
    text = _text()
    assert "does **not** generate XiaoAi replies" in text
    assert "does **not** activate the XiaoAi persona" in text
    assert "Identity Resolver does not own" in text
    assert "response generation" in text


def test_legacy_first_connection_is_not_authentication():
    text = _text()
    assert "daughter-first-connection" in text
    assert "must never be used as authentication" in text
    assert "A successful phrase match" in text


def test_identity_first_resolution_chain_is_explicit():
    text = _text()
    order = [
        "verified Supabase Auth subject",
        "public.users(auth_user_id)",
        "exactly one active companion_access",
        "active daughter_identities row",
        "optional active client_connections entry",
        "optional scoped runtime_sessions row",
        "result for XiaoAi Runtime",
    ]
    positions = [text.index(item) for item in order]
    assert positions == sorted(positions)
