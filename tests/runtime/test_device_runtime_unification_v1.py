from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "runtime" / "XIAOAI_DEVICE_RUNTIME_UNIFICATION_V1.md"


def read_doc() -> str:
    return DOC.read_text(encoding="utf-8")


def test_device_entry_is_guardian_authorized_child_device():
    text = read_doc()
    assert "guardian_authorized_child_device" in text
    assert "Guardian-authorized device" in text
    assert "without requiring a personal email login" in text


def test_device_does_not_create_second_brain():
    text = read_doc()
    assert "must not contain a second XiaoAi prompt/persona" in text
    assert "one XiaoAi Runtime brain" in text
    assert "reply_source = xiaoai_runtime" in text
    assert "reply_authoritative = true" in text


def test_device_path_fails_closed_and_keeps_production_unchanged():
    text = read_doc()
    assert "Fail closed" in text
    assert "must never fall back to a local device-specific XiaoAi prompt" in text
    assert "existing production `xiaoai-device-chat` unchanged" in text
