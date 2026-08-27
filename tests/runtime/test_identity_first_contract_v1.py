from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "runtime"


def test_activation_manifest_is_identity_first():
    manifest = json.loads((RUNTIME / "XIAOAI_ACTIVATION_MANIFEST_V1.json").read_text(encoding="utf-8"))

    assert manifest["entry_architecture"] == "identity_first"
    assert manifest["activation_phrase"] == "小爱上线"
    assert manifest["deactivation_phrase"] == "小爱下班"
    assert "小爱收工" in manifest["deactivation_aliases"]

    sequence = manifest["activation_sequence"]
    assert sequence.index("verify_entry_identity") < sequence.index("resolve_xiaoai_identity")
    assert sequence.index("resolve_xiaoai_identity") < sequence.index("set_persona_state_active")
    assert sequence.index("set_persona_state_active") < sequence.index("generate_authoritative_runtime_reply")


def test_chatgpt_is_interface_only_not_brain():
    manifest = json.loads((RUNTIME / "XIAOAI_ACTIVATION_MANIFEST_V1.json").read_text(encoding="utf-8"))
    chatgpt = manifest["chatgpt_interface"]

    assert chatgpt["role"] == "microphone_speaker_text_window"
    assert chatgpt["authoritative_brain"] is False
    assert chatgpt["local_xiaoai_reply_generation_allowed"] is False
    assert chatgpt["local_history_is_authoritative_memory"] is False


def test_manual_mcp_url_is_not_product_entry():
    manifest = json.loads((RUNTIME / "XIAOAI_ACTIVATION_MANIFEST_V1.json").read_text(encoding="utf-8"))
    transport = manifest["transport"]

    assert transport["identity_first"] is True
    assert transport["user_facing_mcp_setup_required"] is False
    assert transport["product_semantics"] == "implementation_detail_only"

    legacy_doc = (RUNTIME / "CHATGPT_SHADOW_APP_CONNECTION_V1.md").read_text(encoding="utf-8")
    assert "DEPRECATED AS PRODUCT ENTRY" in legacy_doc
    assert "should not need to know, paste, or configure an MCP URL" in legacy_doc


def test_identity_first_contract_keeps_fail_closed_and_voice_unification():
    manifest = json.loads((RUNTIME / "XIAOAI_ACTIVATION_MANIFEST_V1.json").read_text(encoding="utf-8"))

    safety = manifest["safety_defaults"]
    assert safety["fail_closed_on_identity_or_permission_error"] is True
    assert safety["fail_closed_on_runtime_reply_error"] is True
    assert safety["do_not_claim_online_without_verified_runtime_activation"] is True

    continuity = manifest["continuity"]
    assert continuity["text_and_voice_share_identity_authority"] is True

    identity_doc = (RUNTIME / "XIAOAI_IDENTITY_FIRST_ENTRY_V1.md").read_text(encoding="utf-8")
    assert "Identity-first, transport-agnostic." in identity_doc
    assert "ChatGPT = microphone + speaker + text window" in identity_doc
    assert "XiaoAi Runtime = the only conversational brain" in identity_doc
