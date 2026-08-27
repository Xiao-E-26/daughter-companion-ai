from runtime.read_only_runtime_context import RuntimeContextSnapshot
from runtime.shadow_runtime_comparator import LiveRuntimeSnapshot, ShadowRuntimeComparator


def shadow(**overrides):
    base = dict(
        resolved=True,
        daughter_id="daughter-1",
        internal_user_id="user-1",
        role="child",
        authority_scope="{}",
        client_connection_id="client-1",
        persona_state="ACTIVE",
        child_name="雨宸",
        session_key="default",
        continuity_visible=True,
    )
    base.update(overrides)
    return RuntimeContextSnapshot(**base)


def live(**overrides):
    base = dict(
        persona_state="ACTIVE",
        route="xiaoai",
        child_name="雨宸",
        daughter_id="daughter-1",
        internal_user_id="user-1",
        client_connection_id="client-1",
    )
    base.update(overrides)
    return LiveRuntimeSnapshot(**base)


def test_exact_runtime_match_is_zero_mismatch():
    result = ShadowRuntimeComparator().compare(live=live(), shadow=shadow())
    assert result.comparable is True
    assert result.mismatch_count == 0
    assert result.reason is None


def test_persona_state_drift_is_detected_without_controlling_response():
    result = ShadowRuntimeComparator().compare(
        live=live(persona_state="OFF", route="normal_assistant"),
        shadow=shadow(persona_state="ACTIVE"),
    )
    assert result.comparable is True
    assert result.state_match is False
    assert result.route_consistent is False
    assert result.mismatch_count == 2


def test_identity_drift_is_detected():
    result = ShadowRuntimeComparator().compare(
        live=live(child_name="SomeoneElse", daughter_id="daughter-2"),
        shadow=shadow(),
    )
    assert result.identity_match is False
    assert result.mismatch_count == 1


def test_client_scope_drift_is_detected():
    result = ShadowRuntimeComparator().compare(
        live=live(client_connection_id="client-wrong"),
        shadow=shadow(),
    )
    assert result.client_match is False
    assert result.mismatch_count == 1


def test_off_state_requires_normal_assistant_route():
    result = ShadowRuntimeComparator().compare(
        live=live(persona_state="OFF", route="xiaoai"),
        shadow=shadow(persona_state="OFF"),
    )
    assert result.state_match is True
    assert result.route_consistent is False
    assert result.mismatch_count == 1


def test_unresolved_shadow_fails_safe_and_is_not_comparable():
    unresolved = shadow(
        resolved=False,
        daughter_id=None,
        internal_user_id=None,
        role=None,
        authority_scope=None,
        client_connection_id=None,
        persona_state=None,
        child_name=None,
        continuity_visible=False,
        error_code="identity_not_bound",
    )
    result = ShadowRuntimeComparator().compare(live=live(), shadow=unresolved)
    assert result.comparable is False
    assert result.reason == "identity_not_bound"
    assert result.mismatch_count == 0


def test_telemetry_contains_no_raw_message_or_transcript():
    telemetry = ShadowRuntimeComparator().compare(live=live(), shadow=shadow()).telemetry()
    assert telemetry["contains_raw_message"] is False
    assert telemetry["contains_transcript"] is False
    assert "message" not in telemetry
    assert "transcript" not in telemetry
