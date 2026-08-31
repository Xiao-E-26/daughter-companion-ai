from __future__ import annotations

from typing import Any, Dict, Protocol

from runtime.durable_memory_bridge import DurableMemoryResult


class SupabaseRpcClient(Protocol):
    def rpc(self, function_name: str, params: Dict[str, Any]) -> Any: ...


class SupabaseDurableMemoryTransport:
    """Narrow transport for child-pinned durable memory.

    This adapter does not enable durable memory by itself. It is only called when
    DurableMemoryBridge is explicitly configured with CHILD_PINNED_ONLY and all
    child-direct intent checks pass.
    """

    RPC_NAME = "pin_child_memory"

    def __init__(self, client: SupabaseRpcClient) -> None:
        self.client = client

    def pin_child_memory(self, payload: Dict[str, Any]) -> DurableMemoryResult:
        response = self.client.rpc(self.RPC_NAME, payload)

        data = getattr(response, "data", response)
        if isinstance(data, dict):
            accepted = bool(data.get("accepted", data.get("memory_id")))
            return DurableMemoryResult(
                accepted=accepted,
                reason=str(data.get("reason", "supabase_rpc_result")),
                memory_id=data.get("memory_id"),
            )

        return DurableMemoryResult(
            accepted=False,
            reason="unexpected_supabase_rpc_response",
        )
