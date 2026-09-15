from runtime.durable_memory_bridge import (
    DurableMemoryBridge,
    DurableMemoryGate,
    DurableMemoryIntent,
    DurableMemoryResult,
)


class FakeTransport:
    def __init__(self):
        self.calls = []

    def pin_child_memory(self, payload):
        self.calls.append(payload)
        return DurableMemoryResult(True, "ok", "memory-1")


def make_intent(**overrides):
    values = {
        "subject_id": "child-1",
        "actor_account_id": "account-1",
        "actor_role_resolved": "child",
        "intent_class": "long_term_memory_create",
        "intent_confidence": 0.99,
        "source_type": "child_direct",
        "summary": "A meaningful memory",
        "idempotency_key": "session-1:turn-1",
        "privacy_gate_passed": True,
        "sensitivity_gate_passed": True,
        "minimum_necessary_passed": True,
        "visibility_gate_passed": True,
    }
    values.update(overrides)
    return DurableMemoryIntent(**values)


def make_bridge(transport):
    return DurableMemoryBridge(
        gate=DurableMemoryGate.CHILD_PINNED_ONLY,
        transport=transport,
    )


def test_default_gate_is_off():
    transport = FakeTransport()
    bridge = DurableMemoryBridge(transport=transport)
    result = bridge.submit(make_intent())
    assert result.accepted is False
    assert result.reason == "durable_memory_gate_off"
    assert transport.calls == []


def test_child_pinned_only_allows_verified_child_direct_memory_intent_after_policy_gates():
    transport = FakeTransport()
    result = make_bridge(transport).submit(make_intent())
    assert result.accepted is True
    assert result.memory_id == "memory-1"
    payload = transport.calls[0]
    assert payload["retention_class"] == "child_pinned"
    assert payload["pinned_by_child"] is True
    assert payload["proactive_surface_allowed"] is False
    assert payload["privacy_gate_passed"] is True
    assert payload["sensitivity_gate_passed"] is True
    assert payload["minimum_necessary_passed"] is True
    assert payload["visibility_gate_passed"] is True


def test_ordinary_conversation_never_writes():
    transport = FakeTransport()
    result = make_bridge(transport).submit(make_intent(intent_class="ordinary_conversation"))
    assert result.accepted is False
    assert transport.calls == []


def test_guardian_report_cannot_impersonate_child_direct():
    transport = FakeTransport()
    result = make_bridge(transport).submit(
        make_intent(source_type="guardian_reports_child_wants_memory")
    )
    assert result.accepted is False
    assert transport.calls == []


def test_low_confidence_does_not_write():
    transport = FakeTransport()
    result = make_bridge(transport).submit(make_intent(intent_confidence=0.50))
    assert result.accepted is False
    assert transport.calls == []


def test_empty_summary_fails_closed():
    transport = FakeTransport()
    result = make_bridge(transport).submit(make_intent(summary="   "))
    assert result.accepted is False
    assert result.reason == "empty_summary"
    assert transport.calls == []


def test_privacy_gate_is_required():
    transport = FakeTransport()
    result = make_bridge(transport).submit(make_intent(privacy_gate_passed=False))
    assert result.accepted is False
    assert result.reason == "privacy_gate_not_passed"
    assert transport.calls == []


def test_sensitivity_gate_is_required():
    transport = FakeTransport()
    result = make_bridge(transport).submit(make_intent(sensitivity_gate_passed=False))
    assert result.accepted is False
    assert result.reason == "sensitivity_gate_not_passed"
    assert transport.calls == []


def test_minimum_necessary_gate_is_required():
    transport = FakeTransport()
    result = make_bridge(transport).submit(make_intent(minimum_necessary_passed=False))
    assert result.accepted is False
    assert result.reason == "minimum_necessary_gate_not_passed"
    assert transport.calls == []


def test_visibility_gate_is_required():
    transport = FakeTransport()
    result = make_bridge(transport).submit(make_intent(visibility_gate_passed=False))
    assert result.accepted is False
    assert result.reason == "visibility_gate_not_passed"
    assert transport.calls == []
