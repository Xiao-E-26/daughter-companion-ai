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
        return DurableMemoryResult(True, "created", "00000000-0000-0000-0000-000000000001")


def valid_intent(**overrides):
    base = dict(
        subject_id="11111111-1111-1111-1111-111111111111",
        actor_account_id="22222222-2222-2222-2222-222222222222",
        actor_role_resolved="child",
        intent_class="long_term_memory_create",
        intent_confidence=0.99,
        source_type="child_direct",
        summary="今天我第一次自己完成了整首歌，我想记住。",
        idempotency_key="session-1:memory-1",
    )
    base.update(overrides)
    return DurableMemoryIntent(**base)


def test_default_gate_is_off():
    transport = FakeTransport()
    bridge = DurableMemoryBridge(transport=transport)
    result = bridge.submit(valid_intent())
    assert result.accepted is False
    assert result.reason == "durable_memory_gate_off"
    assert transport.calls == []


def test_child_pinned_only_allows_verified_child_direct_intent():
    transport = FakeTransport()
    bridge = DurableMemoryBridge(
        gate=DurableMemoryGate.CHILD_PINNED_ONLY,
        transport=transport,
    )
    result = bridge.submit(valid_intent())
    assert result.accepted is True
    assert len(transport.calls) == 1
    assert transport.calls[0]["retention_class"] == "child_pinned"
    assert transport.calls[0]["pinned_by_child"] is True
    assert transport.calls[0]["proactive_surface_allowed"] is False


def test_guardian_cannot_impersonate_child_direct():
    transport = FakeTransport()
    bridge = DurableMemoryBridge(
        gate=DurableMemoryGate.CHILD_PINNED_ONLY,
        transport=transport,
    )
    result = bridge.submit(valid_intent(actor_role_resolved="guardian"))
    assert result.accepted is False
    assert result.reason == "actor_not_verified_child"
    assert transport.calls == []


def test_inferred_candidate_is_not_persisted():
    transport = FakeTransport()
    bridge = DurableMemoryBridge(
        gate=DurableMemoryGate.CHILD_PINNED_ONLY,
        transport=transport,
    )
    result = bridge.submit(valid_intent(source_type="system_inferred"))
    assert result.accepted is False
    assert result.reason == "source_not_verified_child_direct"
    assert transport.calls == []


def test_low_confidence_intent_is_not_persisted():
    transport = FakeTransport()
    bridge = DurableMemoryBridge(
        gate=DurableMemoryGate.CHILD_PINNED_ONLY,
        transport=transport,
    )
    result = bridge.submit(valid_intent(intent_confidence=0.5))
    assert result.accepted is False
    assert result.reason == "intent_confidence_too_low"
    assert transport.calls == []
