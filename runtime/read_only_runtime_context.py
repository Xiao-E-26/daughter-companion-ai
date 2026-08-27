from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Optional


@dataclass(frozen=True)
class RuntimeContextSnapshot:
    resolved: bool
    daughter_id: Optional[str]
    internal_user_id: Optional[str]
    role: Optional[str]
    authority_scope: Optional[str]
    client_connection_id: Optional[str]
    persona_state: Optional[str]
    child_name: Optional[str]
    session_key: str
    continuity_visible: bool
    resolver_version: str = "read-only-runtime-context-v1"
    error_code: Optional[str] = None


class ReadOnlyRuntimeContextSource(Protocol):
    """Read-only data source contract.

    Implementations may query durable stores, but this interface intentionally
    exposes no mutation methods. Message text must never grant identity or authority.
    """

    def resolve_internal_user_id(self, auth_user_id: str) -> Optional[str]: ...

    def resolve_active_access(self, internal_user_id: str) -> Optional[dict]: ...

    def resolve_active_chatgpt_client(self, internal_user_id: str, daughter_id: str) -> Optional[dict]: ...

    def resolve_session(self, internal_user_id: str, daughter_id: str, session_key: str) -> Optional[dict]: ...

    def resolve_child_name(self, daughter_id: str) -> Optional[str]: ...

    def has_visible_continuity(self, internal_user_id: str, daughter_id: str, role: str) -> bool: ...


class ReadOnlyRuntimeContextResolver:
    """Resolves deterministic runtime facts without mutating state or calling a model."""

    def __init__(self, source: ReadOnlyRuntimeContextSource) -> None:
        self.source = source

    def resolve(self, *, auth_user_id: str, session_key: str) -> RuntimeContextSnapshot:
        key = (session_key or "default").strip()[:200] or "default"
        internal_user_id = self.source.resolve_internal_user_id(auth_user_id)
        if not internal_user_id:
            return self._error(key, "identity_not_bound")

        access = self.source.resolve_active_access(internal_user_id)
        if not access:
            return self._error(key, "no_active_companion_access", internal_user_id=internal_user_id)

        daughter_id = str(access.get("daughter_id") or "")
        role = str(access.get("role") or "")
        authority_scope = access.get("authority_scope")
        if not daughter_id or not role:
            return self._error(key, "invalid_access_record", internal_user_id=internal_user_id)

        client = self.source.resolve_active_chatgpt_client(internal_user_id, daughter_id)
        if not client or not client.get("id"):
            return self._error(
                key,
                "no_active_chatgpt_client",
                internal_user_id=internal_user_id,
                daughter_id=daughter_id,
                role=role,
                authority_scope=authority_scope,
            )

        session = self.source.resolve_session(internal_user_id, daughter_id, key)
        persona_state = "ACTIVE" if session and session.get("persona_state") == "ACTIVE" else "OFF"
        child_name = self.source.resolve_child_name(daughter_id)
        continuity_visible = self.source.has_visible_continuity(internal_user_id, daughter_id, role)

        return RuntimeContextSnapshot(
            resolved=True,
            daughter_id=daughter_id,
            internal_user_id=internal_user_id,
            role=role,
            authority_scope=str(authority_scope) if authority_scope is not None else None,
            client_connection_id=str(client["id"]),
            persona_state=persona_state,
            child_name=child_name,
            session_key=key,
            continuity_visible=bool(continuity_visible),
        )

    @staticmethod
    def _error(
        session_key: str,
        error_code: str,
        *,
        internal_user_id: Optional[str] = None,
        daughter_id: Optional[str] = None,
        role: Optional[str] = None,
        authority_scope: Optional[str] = None,
    ) -> RuntimeContextSnapshot:
        return RuntimeContextSnapshot(
            resolved=False,
            daughter_id=daughter_id,
            internal_user_id=internal_user_id,
            role=role,
            authority_scope=str(authority_scope) if authority_scope is not None else None,
            client_connection_id=None,
            persona_state=None,
            child_name=None,
            session_key=session_key,
            continuity_visible=False,
            error_code=error_code,
        )
