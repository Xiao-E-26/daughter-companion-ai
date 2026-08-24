from runtime.persona_gateway import InMemoryPersonaStateStore, XiaoAiRuntimeGateway


D = "daughter-1"
U = "user-1"
S = "session-1"


def test_default_routes_to_normal_assistant():
    gateway = XiaoAiRuntimeGateway(InMemoryPersonaStateStore())
    result = gateway.handle_message(daughter_id=D, user_id=U, session_key=S, message="我今天给爸爸骂")
    assert result.route == "normal_assistant"
    assert result.persona_state.value == "OFF"


def test_explicit_activation_routes_to_xiaoai():
    gateway = XiaoAiRuntimeGateway(InMemoryPersonaStateStore())
    result = gateway.handle_message(daughter_id=D, user_id=U, session_key=S, message="小爱上线")
    assert result.route == "xiaoai"
    assert result.persona_state.value == "ACTIVE"


def test_active_session_stays_xiaoai_until_explicit_shutdown():
    gateway = XiaoAiRuntimeGateway(InMemoryPersonaStateStore())
    gateway.handle_message(daughter_id=D, user_id=U, session_key=S, message="小爱上线")
    result = gateway.handle_message(daughter_id=D, user_id=U, session_key=S, message="今天学校很好玩")
    assert result.route == "xiaoai"


def test_shutdown_returns_to_normal_and_blocks_context_reactivation():
    gateway = XiaoAiRuntimeGateway(InMemoryPersonaStateStore())
    gateway.handle_message(daughter_id=D, user_id=U, session_key=S, message="小爱上线")
    off = gateway.handle_message(daughter_id=D, user_id=U, session_key=S, message="小爱收工")
    after = gateway.handle_message(daughter_id=D, user_id=U, session_key=S, message="我今天给爸爸骂")
    assert off.route == "normal_assistant"
    assert after.route == "normal_assistant"
    assert after.persona_state.value == "OFF"


def test_state_is_session_scoped():
    gateway = XiaoAiRuntimeGateway(InMemoryPersonaStateStore())
    gateway.handle_message(daughter_id=D, user_id=U, session_key="dad-session", message="小爱上线")
    mother = gateway.handle_message(daughter_id=D, user_id=U, session_key="mother-session", message="你好")
    assert mother.route == "normal_assistant"
