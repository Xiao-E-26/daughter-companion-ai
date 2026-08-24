from __future__ import annotations

import os
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


class OpenAIResponsesAdapter:
    """Live OpenAI adapter using the official Responses API.

    The provider is replaceable. Daughter's protected core, Authority boundary,
    memory rules and verified skills remain outside the model provider.

    Required environment:
      OPENAI_API_KEY
      OPENAI_MODEL

    Optional environment:
      OPENAI_BASE_URL

    No API credential is stored in source control.
    """

    provider_name = "openai"

    def __init__(
        self,
        *,
        model_name: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> None:
        self.model_name = model_name or os.environ.get("OPENAI_MODEL", "").strip()
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "").strip()
        self.base_url = base_url or os.environ.get("OPENAI_BASE_URL", "").strip() or None

        if not self.model_name:
            raise RuntimeError("OPENAI_MODEL is required for live Daughter model use.")
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is required for live Daughter model use.")

        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError(
                "The official 'openai' Python package is required for OpenAIResponsesAdapter."
            ) from exc

        client_kwargs = {"api_key": self.api_key}
        if self.base_url:
            client_kwargs["base_url"] = self.base_url
        self._client = OpenAI(**client_kwargs)

    @staticmethod
    def _render_input(messages: List[ModelMessage]) -> str:
        """Render provider-neutral history into a bounded textual conversation.

        Role markers are data for the provider call; they do not alter Daughter's
        protected system instructions or grant Authority.
        """
        rendered: List[str] = []
        for message in messages:
            role = message.role.strip().lower() or "unknown"
            rendered.append(f"[{role}]\n{message.content}")
        return "\n\n".join(rendered)

    def generate(self, request: ModelRequest) -> ModelResponse:
        response = self._client.responses.create(
            model=self.model_name,
            instructions=request.system_prompt,
            input=self._render_input(request.messages),
        )
        text = getattr(response, "output_text", "") or ""
        raw_id = getattr(response, "id", None)
        return ModelResponse(
            text=text,
            provider=self.provider_name,
            model=self.model_name,
            raw_id=raw_id,
        )
