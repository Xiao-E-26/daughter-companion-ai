from __future__ import annotations

from typing import Any, Callable, Dict

from runtime.durable_memory_bridge import DurableMemoryResult


class SupabaseMemoryV2Transport:
    """Thin adapter around a trusted server-side Supabase RPC caller.

    The caller must invoke memory_v2_api.pin_child_memory with service-role or
    equivalent trusted runtime credentials. This adapter never stores secrets.
    """

    def __init__(self, rpc_caller: Callable[[str, Dict[str, Any]], Dict[str, Any]]) -> None:
        self._rpc_caller = rpc_caller

    def pin_child_memory(self, payload: Dict[str, Any]) -> DurableMemoryResult:
        raw = self._rpc_caller("memory_v2_api.pin_child_memory", {"payload": payload})
        return DurableMemoryResult(
            accepted=bool(raw.get("accepted", False)),
            reason=str(raw.get("reason", "unknown")),
            memory_id=(str(raw["memory_id"]) if raw.get("memory_id") else None),
        )
