from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "runtime" / "XIAOAI_BACKEND_ACCEPTANCE_CAPABILITY_V1.md"


def read_doc() -> str:
    return DOC.read_text(encoding="utf-8")


def test_routine_acceptance_does_not_require_email_or_otp():
    text = read_doc()
    assert "Does **not** require user email, OTP, magic link" in text
    assert "routine regression must not consume email quotas" in text


def test_real_e2e_cannot_be_faked_by_service_role():
    text = read_doc()
    assert "Do not use service-role impersonation to claim real-user E2E success" in text


def test_acceptance_is_reusable_backend_capability():
    text = read_doc()
    assert "REUSABLE BACKEND CAPABILITY" in text
    assert "xiaoai_internal.backend_acceptance_snapshot()" in text
    assert "identity_first_ready" in text
