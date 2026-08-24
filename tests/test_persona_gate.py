from runtime.persona_gate import PersonaState, XiaoAiPersonaGate


def test_default_is_off():
    d = XiaoAiPersonaGate().evaluate(None, "hello")
    assert d.state is PersonaState.OFF
    assert d.should_load_xiaoai is False


def test_exact_activation_turns_on():
    d = XiaoAiPersonaGate().evaluate("OFF", "小爱上线")
    assert d.state is PersonaState.ACTIVE
    assert d.should_load_xiaoai is True
    assert d.reason == "explicit_activation"


def test_exact_deactivation_turns_off():
    d = XiaoAiPersonaGate().evaluate("ACTIVE", "小爱收工")
    assert d.state is PersonaState.OFF
    assert d.should_load_xiaoai is False
    assert d.reason == "explicit_deactivation"


def test_child_like_language_does_not_auto_activate():
    d = XiaoAiPersonaGate().evaluate("OFF", "我今天给爸爸骂。")
    assert d.state is PersonaState.OFF
    assert d.should_load_xiaoai is False


def test_emotional_language_does_not_auto_activate():
    d = XiaoAiPersonaGate().evaluate("OFF", "我很难过，你陪我一下")
    assert d.state is PersonaState.OFF
    assert d.should_load_xiaoai is False


def test_family_context_does_not_auto_activate():
    d = XiaoAiPersonaGate().evaluate("OFF", "妈妈今天来接我")
    assert d.state is PersonaState.OFF
    assert d.should_load_xiaoai is False


def test_previous_active_state_stays_active_without_command():
    d = XiaoAiPersonaGate().evaluate("ACTIVE", "今天学校很好玩")
    assert d.state is PersonaState.ACTIVE
    assert d.should_load_xiaoai is True


def test_similar_but_not_exact_activation_phrase_does_not_activate():
    d = XiaoAiPersonaGate().evaluate("OFF", "可以让小爱上线吗")
    assert d.state is PersonaState.OFF
    assert d.should_load_xiaoai is False


def test_unknown_state_fails_closed():
    d = XiaoAiPersonaGate().evaluate("BROKEN", "hello")
    assert d.state is PersonaState.OFF
    assert d.should_load_xiaoai is False


def test_state_is_caller_scoped_not_global():
    gate = XiaoAiPersonaGate()
    dad = gate.evaluate("OFF", "小爱上线")
    mom = gate.evaluate("OFF", "hello")
    assert dad.state is PersonaState.ACTIVE
    assert mom.state is PersonaState.OFF
