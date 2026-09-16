from runtime.memory_policy_gate import MemoryPolicyEvidence, MemoryPolicyGate


def base(**overrides):
    data = dict(
        intent_class='long_term_memory_create',
        source_type='child_direct',
        actor_role_resolved='child',
        explicit_user_intent=True,
        durable_value=True,
        verified_or_explicit=True,
        durable_storage_necessary=True,
        memory_class='M2',
        sensitivity='low',
        visibility_scope='user_and_daughter',
        minimum_necessary=True,
        summary_present=True,
    )
    data.update(overrides)
    return MemoryPolicyEvidence(**data)


def test_allows_low_sensitivity_child_pinned_memory_after_all_gates():
    d = MemoryPolicyGate.evaluate(base())
    assert d.allowed is True
    assert d.reason == 'policy_gates_passed'
    assert d.retention_class == 'child_pinned'
    assert d.privacy_gate_passed is True
    assert d.sensitivity_gate_passed is True
    assert d.minimum_necessary_passed is True
    assert d.visibility_gate_passed is True


def test_ordinary_conversation_never_promotes():
    d = MemoryPolicyGate.evaluate(base(intent_class='ordinary_conversation'))
    assert d.allowed is False
    assert d.reason == 'not_long_term_memory_create'


def test_non_child_direct_never_promotes():
    d = MemoryPolicyGate.evaluate(base(source_type='guardian_report'))
    assert d.allowed is False
    assert d.reason == 'source_not_child_direct'


def test_minimum_necessary_is_required():
    d = MemoryPolicyGate.evaluate(base(minimum_necessary=False))
    assert d.allowed is False
    assert d.reason == 'minimum_necessary_gate_not_passed'


def test_visibility_scope_is_required():
    d = MemoryPolicyGate.evaluate(base(visibility_scope=None))
    assert d.allowed is False
    assert d.reason == 'visibility_gate_not_passed'


def test_sensitive_memory_requires_restricted_sensitivity_and_visibility():
    d = MemoryPolicyGate.evaluate(base(memory_class='M3', sensitivity='low', visibility_scope='guardian_visible'))
    assert d.allowed is False
    assert d.reason == 'sensitivity_gate_not_passed'


def test_sensitive_memory_can_pass_only_with_restricted_visibility():
    d = MemoryPolicyGate.evaluate(base(memory_class='M3', sensitivity='restricted', visibility_scope='user_only'))
    assert d.allowed is True


def test_durable_storage_must_be_necessary():
    d = MemoryPolicyGate.evaluate(base(durable_storage_necessary=False))
    assert d.allowed is False
    assert d.reason == 'durable_storage_not_necessary'
