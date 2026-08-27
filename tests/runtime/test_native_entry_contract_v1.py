from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "runtime" / "XIAOAI_NATIVE_ENTRY_SHADOW_V1.md"


def test_native_entry_is_identity_first_and_runtime_authoritative():
    text = DOC.read_text(encoding="utf-8")
    assert "Identity Resolver" in text
    assert "XiaoAi Runtime" in text
    assert "reply_source = xiaoai_runtime" in text
    assert "reply_authoritative = true" in text


def test_chatgpt_is_io_only_and_mcp_not_user_facing():
    text = DOC.read_text(encoding="utf-8")
    assert "ChatGPT owns only input/output presentation" in text
    assert "user must not configure or understand MCP" in text


def test_native_entry_fails_closed():
    text = DOC.read_text(encoding="utf-8")
    assert "Fail closed" in text
    assert "ChatGPT must not locally generate a XiaoAi replacement" in text
