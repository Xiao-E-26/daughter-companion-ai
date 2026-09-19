from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "runtime" / "XIAOAI_BACKEND_ACCEPTANCE_CAPABILITY_V1.md"


def read_doc() -> str:
    return DOC.read_text(encoding="utf-8")


def test_routine_acceptance_is_design_only_not_live_capability():
    text = read_doc()
    assert "REFERENCE / DESIGN — NOT DEPLOYED" in text
    assert "routine backend regression" in text
    assert "not a current capability" in text


def test_real_e2e_cannot_be_faked_by_service_role():
    text = read_doc()
    assert "service-role impersonation" in text
    assert "must not be presented as proof of deployed backend acceptance" in text


def test_backend_acceptance_snapshot_is_target_reference_only():
    text = read_doc()
    assert "xiaoai_internal.backend_acceptance_snapshot()" in text
    assert "A live production database inspection on 2026-09-20 found no deployed" in text
    assert "live implementation evidence" in text
