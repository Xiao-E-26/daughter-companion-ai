from __future__ import annotations

from typing import Any, Callable, Dict

from runtime.durable_memory_bridge import DurableMemoryResult


class SupabaseMemoryV2Transport:
    """Thin adapter for the rebuilt XiaoAi V2 memory runtime.

    The injected caller is responsible for authenticated transport to the V2
    Supabase runtime. This adapter stores no secrets and keeps memory failure
    non-authoritative: conversation may continue even when memory is degraded.
    """

    def __init__(self, rpc_caller: Callable[[str, Dict[str, Any]], Dict[str, Any]]) -> None:
        self._rpc_caller = rpc_caller

    def pin_child_memory(self, payload: Dict[str, Any]) -> DurableMemoryResult:
        child_id = str(payload.get("subject_id", "")).strip()
        summary = str(payload.get("summary", "")).strip()
        dedupe_key = str(payload.get("idempotency_key", "")).strip()
        if not child_id or not summary or not dedupe_key:
            return DurableMemoryResult(False, "invalid_v2_memory_payload")

        raw = self._rpc_caller(
            "enqueue_memory_candidate_v2",
            {
                "p_child_id": child_id,
                "p_session_id": payload.get("session_id"),
                "p_content": summary,
                "p_memory_type": "event",
                "p_valence": int(payload.get("valence", 1)),
                "p_importance": int(payload.get("importance", 5)),
                "p_explicit_save": True,
                "p_dedupe_key": dedupe_key,
            },
        )

        if raw.get("degraded") or raw.get("continue_chat"):
            return DurableMemoryResult(False, "memory_degraded_continue_chat")

        memory_id = raw.get("candidate_id") or raw.get("data") or raw.get("id")
        if isinstance(memory_id, list):
            memory_id = memory_id[0] if memory_id else None
        if isinstance(memory_id, dict):
            memory_id = memory_id.get("id") or memory_id.get("candidate_id")

        return DurableMemoryResult(
            accepted=bool(raw.get("ok", memory_id is not None)),
            reason=str(raw.get("reason", "candidate_enqueued" if memory_id else "memory_write_failed")),
            memory_id=(str(memory_id) if memory_id else None),
        )
