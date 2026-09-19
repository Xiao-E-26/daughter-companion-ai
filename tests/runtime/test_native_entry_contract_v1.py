from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
IDENTITY_FIRST = ROOT / "runtime" / "XIAOAI_IDENTITY_FIRST_ENTRY_V1.md"
HANDOFF = ROOT / "runtime" / "XIAOAI_PLATFORM_IDENTITY_HANDOFF_V1.md"


def test_native_entry_is_identity_first_and_runtime_authoritative():
    identity = IDENTITY_FIRST.read_text(encoding="utf-8")
    handoff = HANDOFF.read_text(encoding="utf-8")
    assert "Resolve verified entry identity" in identity
    assert "XiaoAi Runtime = the only conversational brain" in identity
    assert "Runtime generates the final authoritative XiaoAi reply." in handoff


def test_chatgpt_is_io_only_and_transport_not_user_facing():
    identity = IDENTITY_FIRST.read_text(encoding="utf-8")
    assert "ChatGPT = microphone + speaker + text window" in identity
    assert "Identity-first, transport-agnostic." in identity
    assert "require the end user to know or configure an MCP URL" in identity


def test_native_entry_fails_closed():
    identity = IDENTITY_FIRST.read_text(encoding="utf-8")
    assert "Fail-closed behavior" in identity
    assert "must not imitate XiaoAi" in identity
