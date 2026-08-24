from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Protocol


@dataclass(frozen=True)
class ModelMessage:
    role: str
    content: str


@dataclass(frozen=True)
class ModelRequest:
    system_prompt: str
    messages: List[ModelMessage]
    metadata: Dict[str, str]


@dataclass(frozen=True)
class ModelResponse:
    text: str
    provider: str
    model: str
    raw_id: Optional[str] = None


class ModelAdapter(Protocol):
    """Provider-neutral language model contract used by Daughter runtime."""

    provider_name: str
    model_name: str

    def generate(self, request: ModelRequest) -> ModelResponse:
        ...


class EchoModelAdapter:
    """Offline development adapter.

    It does not attempt intelligent conversation. Its only purpose is to let the
    runtime pipeline execute without network/API credentials while preserving the
    same adapter contract future providers will implement.
    """

    provider_name = "offline"
    model_name = "echo-dev"

    def generate(self, request: ModelRequest) -> ModelResponse:
        latest = request.messages[-1].content if request.messages else ""
        return ModelResponse(
            text=f"[offline-dev] {latest}",
            provider=self.provider_name,
            model=self.model_name,
        )
