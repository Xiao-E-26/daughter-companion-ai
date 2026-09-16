from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MemoryActorContext:
    authenticated: bool
    auth_user_id: str | None
    internal_user_id: str | None
    session_id: str | None
    session_actor_user_id: str | None
    client_connection_verified: bool
    resolved_role: str


@dataclass(frozen=True)
class MemoryActorEvidence:
    verified: bool
    actor_role_resolved: str
    source_type: str
    actor_account_id: str | None
    reason: str


class MemoryActorEvidenceResolver:
    """Fail-closed resolver for actor evidence used by durable-memory policy.

    Speaker text, display names, child-like language, and remembered context are
    never authentication. A child-direct claim requires a verified authenticated
    user plus a verified session/client binding to the same internal user.
    """

    @staticmethod
    def resolve(ctx: MemoryActorContext) -> MemoryActorEvidence:
        if not ctx.authenticated or not ctx.auth_user_id:
            return MemoryActorEvidence(False, 'unverified', 'unverified', None, 'authentication_required')
        if not ctx.internal_user_id:
            return MemoryActorEvidence(False, 'unverified', 'unverified', None, 'internal_user_binding_required')
        if not ctx.session_id or not ctx.session_actor_user_id:
            return MemoryActorEvidence(False, 'unverified', 'unverified', None, 'session_actor_binding_required')
        if ctx.session_actor_user_id != ctx.internal_user_id:
            return MemoryActorEvidence(False, 'unverified', 'unverified', None, 'session_actor_mismatch')
        if not ctx.client_connection_verified:
            return MemoryActorEvidence(False, 'unverified', 'unverified', None, 'client_binding_required')
        if ctx.resolved_role != 'child':
            return MemoryActorEvidence(False, ctx.resolved_role or 'unverified', 'not_child_direct', ctx.internal_user_id, 'actor_not_child')
        return MemoryActorEvidence(True, 'child', 'child_direct', ctx.internal_user_id, 'verified_child_direct')
