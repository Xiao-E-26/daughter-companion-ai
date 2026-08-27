from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "runtime" / "XIAOAI_PLATFORM_IDENTITY_HANDOFF_V1.md"


def read_doc() -> str:
    return DOC.read_text(encoding="utf-8")


def test_handoff_requires_verifiable_platform_identity():
    text = read_doc()
    assert "verifiable platform identity assertion" in text
    assert "display name" in text
    assert "voiceprint" in text
    assert "conversation memory" in text
    assert "小爱上线" in text


def test_handoff_is_identity_first_and_fail_closed():
    text = read_doc()
    assert "Identity Resolver" in text
    assert "XiaoAi Runtime" in text
    assert "fail closed" in text.lower()
    assert "must not generate a XiaoAi reply locally" in text


def test_chatgpt_role_remains_io_only():
    text = read_doc()
    assert "microphone + speaker + text window" in text
    assert "does not own XiaoAi identity" in text
    assert "does not own XiaoAi final reply" in text
