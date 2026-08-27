from runtime.authoritative_reply_adapter import AuthoritativeReplyAdapter
from runtime.orchestrator import RuntimeRequest, RuntimeResponse


class StubOrchestrator:
    def __init__(self, text: str):
        self.text = text
        self.calls = []

    def handle(self, request, history=None):
        self.calls.append((request, history))
        return RuntimeResponse(
            text=self.text,
            boundary_decision={"decision_class": "ALLOW"},
            model_provider="runtime-provider",
            model_name="runtime-model",
            memory_candidate=None,
            context_snapshot="verified-context",
            runtime_identity="daughter",
            shadow_behavior_route=None,
        )


def _request():
    return RuntimeRequest(
        user_id="guardian-1",
        session_id="session-1",
        message="今天发生了一件事",
        age=7,
    )


def test_reply_is_exact_runtime_generated_text():
    orchestrator = StubOrchestrator("这是 XiaoAi Runtime 生成的最终回复。")
    adapter = AuthoritativeReplyAdapter(orchestrator)

    result = adapter.reply(_request())

    assert result.text == "这是 XiaoAi Runtime 生成的最终回复。"
    assert result.runtime_identity == "daughter"
    assert result.model_provider == "runtime-provider"
    assert result.model_name == "runtime-model"
    assert len(orchestrator.calls) == 1


def test_missing_runtime_reply_fails_closed():
    orchestrator = StubOrchestrator("   ")
    adapter = AuthoritativeReplyAdapter(orchestrator)

    try:
        adapter.reply(_request())
    except RuntimeError as exc:
        assert str(exc) == "authoritative_xiaoai_reply_missing"
    else:
        raise AssertionError("missing authoritative runtime reply must fail closed")
