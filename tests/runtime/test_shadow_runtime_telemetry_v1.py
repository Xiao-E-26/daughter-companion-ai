from runtime.shadow_runtime_comparator import ShadowComparison
from runtime.shadow_runtime_telemetry import build_shadow_telemetry


def comparison():
    return ShadowComparison(
        comparable=True,
        state_match=True,
        identity_match=True,
        client_match=True,
        route_consistent=True,
        mismatch_count=0,
        reason=None,
    )


def test_telemetry_excludes_direct_identifiers_and_conversation_content():
    envelope = build_shadow_telemetry(
        comparison=comparison(),
        resolver_version="resolver-v1",
        session_key="session-sensitive",
        daughter_id="daughter-sensitive",
        latency_ms=12,
    ).as_dict()

    serialized = str(envelope)
    assert "session-sensitive" not in serialized
    assert "daughter-sensitive" not in serialized
    assert "child_name" not in serialized
    assert "message" not in serialized
    assert "transcript" not in serialized
    assert "authority_scope" not in serialized
    assert len(envelope["correlation_hash"]) == 64


def test_negative_latency_is_clamped_to_zero():
    envelope = build_shadow_telemetry(
        comparison=comparison(),
        resolver_version="resolver-v1",
        session_key="s",
        daughter_id="d",
        latency_ms=-5,
    )
    assert envelope.latency_ms == 0
