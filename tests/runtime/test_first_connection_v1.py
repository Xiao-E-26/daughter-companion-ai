from runtime.first_connection import (
    FIRST_CONNECTION_PHRASE,
    FirstConnectionManager,
    FirstConnectionRequest,
    FirstConnectionState,
)


def test_correct_phrase_connects_daughter():
    result = FirstConnectionManager().connect(
        FirstConnectionRequest(
            user_id="cao-yuchen",
            transcript=FIRST_CONNECTION_PHRASE,
            runtime_identity="daughter",
            guardian_state="verified",
            voice_enrollment_status="enrolled",
        )
    )
    assert result.connected is True
    assert result.record is not None
    assert result.record.state == FirstConnectionState.CONNECTED
    assert result.record.runtime_identity == "daughter"
    assert result.reason == "first_connection_completed"


def test_wrong_phrase_does_not_connect():
    result = FirstConnectionManager().connect(
        FirstConnectionRequest(
            user_id="cao-yuchen",
            transcript="Hi，我是别人，请连接 Daughter。",
            runtime_identity="daughter",
            guardian_state="verified",
        )
    )
    assert result.connected is False
    assert result.record is None
    assert result.reason == "first_connection_phrase_not_matched"


def test_xiaoe_runtime_cannot_complete_daughter_first_connection():
    result = FirstConnectionManager().connect(
        FirstConnectionRequest(
            user_id="cao-yuchen",
            transcript=FIRST_CONNECTION_PHRASE,
            runtime_identity="xiaoe",
            guardian_state="verified",
        )
    )
    assert result.connected is False
    assert result.record is None
    assert result.reason == "runtime_identity_must_be_daughter"
