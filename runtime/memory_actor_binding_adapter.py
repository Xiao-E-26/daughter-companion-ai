
from __future__ import annotations

from dataclasses import dataclass

from runtime.memory_actor_evidence import MemoryActorContext


@dataclass(frozen=True)
class MemoryActorBindingSnapshot:
    request_authenticated: bool
    request_auth_user_id: str | None
    user_id: str | None
    user_auth_user_id: str | None
    user_status: str | None
    child_id: str | None
    access_child_id: str | None
    access_user_id: str | None
    access_role: str | None
    access_status: str | None
    client_connection_id: str | None
    client_child_id: str | None
    client_user_id: str | None
    client_status: str | None
    runtime_session_id: str | None
    session_child_id: str | None
    session_user_id: str | None
    session_client_connection_id: str | None
    session_status: str | None


class MemoryActorBindingAdapter:
    """Convert verified identity/session database rows into actor context.

    This adapter is deliberately fail-closed. It does not infer identity from text,
    display names, child-like wording, memory, or model output. A child actor context
    is produced only when auth, user, access, client, and session bindings all match
    and are active.
    """

    @staticmethod
    def to_context(s: MemoryActorBindingSnapshot) -> MemoryActorContext:
        if not s.request_authenticated or not s.request_auth_user_id:
            return MemoryActorContext(False, None, None, None, None, False, 'unverified')
        if not s.user_id or not s.user_auth_user_id or s.user_status != 'active':
            return MemoryActorContext(True, s.request_auth_user_id, None, None, None, False, 'unverified')
        if s.request_auth_user_id != s.user_auth_user_id:
            return MemoryActorContext(True, s.request_auth_user_id, None, None, None, False, 'unverified')
        if not s.child_id:
            return MemoryActorContext(True, s.request_auth_user_id, s.user_id, None, None, False, 'unverified')
        if (
            s.access_status != 'active'
            or s.access_user_id != s.user_id
            or s.access_child_id != s.child_id
            or s.access_role not in {'child', 'guardian'}
        ):
            return MemoryActorContext(True, s.request_auth_user_id, s.user_id, None, None, False, 'unverified')
        if (
            not s.client_connection_id
            or s.client_status != 'active'
            or s.client_user_id != s.user_id
            or s.client_child_id != s.child_id
        ):
            return MemoryActorContext(True, s.request_auth_user_id, s.user_id, None, None, False, s.access_role)
        if (
            not s.runtime_session_id
            or s.session_status != 'active'
            or s.session_user_id != s.user_id
            or s.session_child_id != s.child_id
            or s.session_client_connection_id != s.client_connection_id
        ):
            return MemoryActorContext(
                True,
                s.request_auth_user_id,
                s.user_id,
                s.runtime_session_id,
                None,
                True,
                s.access_role,
            )
        return MemoryActorContext(
            True,
            s.request_auth_user_id,
            s.user_id,
            s.runtime_session_id,
            s.session_user_id,
            True,
            s.access_role,
        )
