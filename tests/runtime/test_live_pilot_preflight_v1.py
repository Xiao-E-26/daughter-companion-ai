import json
import os

import pytest

from pilots.first_live_gpt_pilot_v1 import run_preflight


def _handoff_packet() -> str:
    return json.dumps({
        "schema": "xiaoe.runtime.handoff.v1",
        "runtime_identity": "daughter",
        "routing_reason": "child_facing_companion_responsibility",
        "context": {
            "request_text": "Help me learn coding.",
            "user_id": "pilot-child",
            "session_id": "pilot-live-001",
            "age": "7",
            "domain": "coding",
            "risk_level": "low",
        },
        "dropped_context_keys": ["api_key"],
        "claims": {
            "model_may_change_identity": False,
            "model_may_expand_authority": False,
            "context_is_identity_filtered": True,
        },
    })


def test_preflight_rejects_missing_required_environment(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    monkeypatch.delenv("XIAOE_HANDOFF_JSON", raising=False)

    result = run_preflight()

    assert result.ready is False
    assert any("OPENAI_API_KEY is missing" in item for item in result.errors)
    assert any("OPENAI_MODEL is missing" in item for item in result.errors)
    assert any("XIAOE_HANDOFF_JSON is missing" in item for item in result.errors)


def test_preflight_never_prints_or_returns_api_key_value(monkeypatch):
    secret = "sk-test-secret-value"
    monkeypatch.setenv("OPENAI_API_KEY", secret)
    monkeypatch.setenv("OPENAI_MODEL", "test-model")
    monkeypatch.setenv("XIAOE_HANDOFF_JSON", _handoff_packet())

    result = run_preflight()
    combined = "\n".join(result.checks + result.errors)

    assert secret not in combined
    assert "OPENAI_API_KEY: present (value hidden)" in result.checks


def test_preflight_rejects_wrong_runtime_identity(monkeypatch):
    packet = json.loads(_handoff_packet())
    packet["runtime_identity"] = "xiaoe"

    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.setenv("OPENAI_MODEL", "test-model")
    monkeypatch.setenv("XIAOE_HANDOFF_JSON", json.dumps(packet))

    result = run_preflight()

    assert result.ready is False
    assert any("XIAOE_HANDOFF_JSON invalid" in item for item in result.errors)
