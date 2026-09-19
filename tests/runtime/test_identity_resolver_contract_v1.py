from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HANDOFF = ROOT / "runtime" / "XIAOAI_PLATFORM_IDENTITY_HANDOFF_V1.md"
BINDING = ROOT / "runtime" / "XIAOAI_IDENTITY_BINDING_AND_RLS_V1.md"


def _handoff() -> str:
    return HANDOFF.read_text(encoding="utf-8")


def _binding() -> str:
    return BINDING.read_text(encoding="utf-8")


def test_identity_resolver_requires_trusted_authenticated_subject():
    text = _handoff()
    assert "Verify the platform assertion issuer and signature/channel." in text
    assert "stable platform subject" in text
    assert "Forbidden identity substitutes" in text


def test_identity_resolver_is_not_xiaoai_brain():
    text = _handoff()
    assert "Platform identity assertion proves **who is calling**." in text
    assert "Runtime determines **how XiaoAi thinks and replies**." in text
    assert "ChatGPT remains **I/O only**." in text


def test_phrase_is_not_authentication():
    text = _binding()
    assert "phrases such as `小爱上线` must never grant Authority" in text


def test_current_identity_resolution_chain_uses_live_entities():
    text = _binding()
    for item in (
        "`users`",
        "`child_profiles`",
        "`companion_access`",
        "`client_connections`",
        "`runtime_sessions`",
    ):
        assert item in text
    assert "There is no live `public.daughter_identities` table." in text
