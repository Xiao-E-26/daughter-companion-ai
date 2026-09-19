from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "runtime" / "XIAOAI_PLATFORM_IDENTITY_HANDOFF_V1.md"


def read_doc() -> str:
    return DOC.read_text(encoding="utf-8")


def test_handoff_requires_trusted_verifiable_platform_identity():
    text = read_doc()
    assert "trusted assertion" in text
    assert "platform-signed token" in text
    assert "display name" in text
    assert "voice sample alone" in text
    assert "local ChatGPT memory" in text
    assert "`小爱上线`" in text


def test_handoff_is_identity_first_and_fail_closed():
    text = read_doc()
    assert "Identity Resolver" in text
    assert "XiaoAi Runtime" in text
    assert "Fail-closed requirements" in text
    assert "must not imitate XiaoAi" in text


def test_chatgpt_role_remains_io_only():
    text = read_doc()
    assert "microphone + speaker + text window" in text
    assert "The host platform does not become XiaoAi." in text
    assert "ChatGPT remains **I/O only**." in text
    assert "Runtime generates the final authoritative XiaoAi reply." in text
