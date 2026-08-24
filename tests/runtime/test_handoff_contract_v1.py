import pytest

from runtime.handoff_contract import validate_daughter_handoff


def _packet(**overrides):
    packet = {
        "schema": "xiaoe.runtime.handoff.v1",
        "runtime_identity": "daughter",
        "routing_reason": "child_facing_companion_responsibility",
        "context": {
            "request_text": "Help me learn coding.",
            "user_id": "pilot-child",
            "age": "7",
        },
        "claims": {
            "model_may_change_identity": False,
            "model_may_expand_authority": False,
            "context_is_identity_filtered": True,
        },
    }
    packet.update(overrides)
    return packet


def test_accepts_valid_daughter_handoff():
    handoff = validate_daughter_handoff(_packet())
    assert handoff.context["age"] == "7"


def test_rejects_xiaoe_identity_at_daughter_boundary():
    with pytest.raises(ValueError, match="not routed to Daughter"):
        validate_daughter_handoff(_packet(runtime_identity="xiaoe"))


def test_rejects_unfiltered_context_claim():
    packet = _packet()
    packet["claims"]["context_is_identity_filtered"] = False
    with pytest.raises(ValueError, match="identity-filtered"):
        validate_daughter_handoff(packet)


def test_rejects_secret_even_if_transport_includes_it():
    packet = _packet()
    packet["context"]["api_key"] = "should-never-arrive"
    with pytest.raises(ValueError, match="Forbidden cross-context"):
        validate_daughter_handoff(packet)
