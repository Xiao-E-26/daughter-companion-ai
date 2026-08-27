from runtime.entry_consistency_shadow import EntryConsistencyShadowComparator, EntryRuntimeSnapshot


def snap(entry_mode: str, **overrides):
    base = dict(
        entry_mode=entry_mode,
        runtime_path="mcp-runtime-bridge->daughter-chat->xiaoai-runtime",
        persona_state="ACTIVE",
        daughter_id="daughter-1",
        session_key="shared-session",
        behavior_source="frozen-behavior-core-v1",
        response_style_signature="xiaoai-style-v1",
    )
    base.update(overrides)
    return EntryRuntimeSnapshot(**base)


def test_text_voice_same_runtime_and_style_passes():
    result = EntryConsistencyShadowComparator().compare(
        text=snap("text"),
        voice=snap("voice"),
    )
    assert result.comparable is True
    assert result.mismatch_count == 0
    assert result.reason is None


def test_voice_generic_chatgpt_style_fails_consistency():
    result = EntryConsistencyShadowComparator().compare(
        text=snap("text"),
        voice=snap("voice", response_style_signature="generic-chatgpt-warm"),
    )
    assert result.same_style_signature is False
    assert result.mismatch_count == 1
    assert result.reason == "entry_consistency_mismatch"


def test_voice_second_runtime_path_fails_consistency():
    result = EntryConsistencyShadowComparator().compare(
        text=snap("text"),
        voice=snap("voice", runtime_path="voice-persona-local"),
    )
    assert result.same_runtime_path is False
    assert result.mismatch_count == 1


def test_voice_separate_behavior_source_fails_consistency():
    result = EntryConsistencyShadowComparator().compare(
        text=snap("text"),
        voice=snap("voice", behavior_source="voice-persona-v1"),
    )
    assert result.same_behavior_source is False
    assert result.mismatch_count == 1


def test_session_or_identity_drift_is_detected():
    result = EntryConsistencyShadowComparator().compare(
        text=snap("text"),
        voice=snap("voice", daughter_id="daughter-2", session_key="voice-only-session"),
    )
    assert result.same_identity is False
    assert result.same_session is False
    assert result.mismatch_count == 2


def test_invalid_entry_pair_is_not_comparable():
    result = EntryConsistencyShadowComparator().compare(
        text=snap("voice"),
        voice=snap("voice"),
    )
    assert result.comparable is False
    assert result.reason == "invalid_entry_pair"


def test_telemetry_contains_no_raw_content():
    telemetry = EntryConsistencyShadowComparator().compare(
        text=snap("text"),
        voice=snap("voice"),
    ).telemetry()
    assert telemetry["contains_raw_message"] is False
    assert telemetry["contains_transcript"] is False
    assert telemetry["contains_reply_text"] is False
    assert "message" not in telemetry
    assert "transcript" not in telemetry
    assert "reply" not in telemetry
