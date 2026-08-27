from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from runtime.model_adapter import ModelMessage
from runtime.orchestrator import DaughterOrchestrator, RuntimeRequest, RuntimeResponse


@dataclass(frozen=True)
class AuthoritativeReply:
    """Final XiaoAi reply produced by XiaoAi Runtime, not by the ChatGPT interface."""

    text: str
    runtime_identity: str
    model_provider: str
    model_name: str
    response: RuntimeResponse


class AuthoritativeReplyAdapter:
    """Thin adapter around the existing DaughterOrchestrator.

    Contract:
    - ChatGPT Text / Voice is interface only.
    - This adapter delegates the actual conversational response to XiaoAi Runtime.
    - The returned ``text`` is the authoritative final XiaoAi reply.
    - Callers must not replace or rewrite the reply with a locally invented XiaoAi answer.
    """

    def __init__(self, orchestrator: DaughterOrchestrator) -> None:
        self.orchestrator = orchestrator

    def reply(
        self,
        request: RuntimeRequest,
        history: Optional[List[ModelMessage]] = None,
    ) -> AuthoritativeReply:
        response = self.orchestrator.handle(request, history=history)
        text = response.text.strip()
        if not text:
            raise RuntimeError("authoritative_xiaoai_reply_missing")

        return AuthoritativeReply(
            text=text,
            runtime_identity=response.runtime_identity,
            model_provider=response.model_provider,
            model_name=response.model_name,
            response=response,
        )
