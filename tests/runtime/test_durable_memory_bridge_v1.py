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
    }
    values.update(overrides)
    return DurableMemoryIntent(**values)


def test_default_gate_is_off():
    transport = FakeTransport()
    bridge = DurableMemoryBridge(transport=transport)
    result = bridge.submit(make_intent())
    assert result.accepted is False
    assert result.reason == "durable_memory_gate_off"
    assert transport.calls == []


def test_child_pinned_only_allows_verified_child_direct_memory_intent():
    transport = FakeTransport()
    bridge = DurableMemoryBridge(
        gate=DurableMemoryGate.CHILD_PINNED_ONLY,
        transport=transport,
    )
    result = bridge.submit(make_intent())
    assert result.accepted is True
    assert result.memory_id == "memory-1"
    assert transport.calls[0]["retention_class"] == "child_pinned"
    assert transport.calls[0]["pinned_by_child"] is True
    assert transport.calls[0]["proactive_surface_allowed"] is False


def test_ordinary_conversation_never_writes():
    transport = FakeTransport()
    bridge = DurableMemoryBridge(
        gate=DurableMemoryGate.CHILD_PINNED_ONLY,
        transport=transport,
    )
    result = bridge.submit(make_intent(intent_class="ordinary_conversation"))
    assert result.accepted is False
    assert transport.calls == []


def test_guardian_report_cannot_impersonate_child_direct():
    transport = FakeTransport()
    bridge = DurableMemoryBridge(
        gate=DurableMemoryGate.CHILD_PINNED_ONLY,
        transport=transport,
    )
    result = bridge.submit(make_intent(source_type="guardian_reports_child_wants_memory"))
    assert result.accepted is False
    assert transport.calls == []


def test_low_confidence_does_not_write():
    transport = FakeTransport()
    bridge = DurableMemoryBridge(
        gate=DurableMemoryGate.CHILD_PINNED_ONLY,
        transport=transport,
    )
    result = bridge.submit(make_intent(intent_confidence=0.50))
    assert result.accepted is False
    assert transport.calls == []
