# XiaoAi RLS Coverage Policy v1

## Goal

Document which public tables are intentionally client-accessible and which are intentionally fail-closed/server-only. A Supabase advisor warning about missing policies must never be resolved by broadly opening access without an explicit product need.

## Client-accessible with scoped RLS

### users
Authenticated users may access only their own internal user mapping via `users.auth_user_id = auth.uid()`.

### daughter_identities
Read access is limited to the authenticated subject mapping already defined by the project.

### companion_access
Authenticated users may read only access rows belonging to their mapped internal user. Runtime authorization additionally requires `status = 'active'`.

### client_connections
Authenticated users may read only their own client connections. Runtime control additionally requires an active matching client.

### runtime_sessions
Authenticated users may read/write only runtime rows for a Daughter to which they have active companion access. Any attached client connection must belong to the same user/Daughter pair and be active. Persona state is session scoped.

### relationships
Authenticated users with active companion access may read the relationship row for the authorized Daughter.

### shared_continuity_state
Authenticated active companions may read continuity state for their authorized Daughter. Only child/guardian roles may insert or update, and writes must identify the authenticated internal user as the actor.

### continuity_updates
Only authenticated child/guardian actors with active companion access may insert updates for the authorized Daughter and valid subject relationship.

### audit_logs
Only authenticated child/guardian actors may insert audit events that identify themselves as the actor for the authorized Daughter.

### guardians
Read-only self access. A guardian may read their own guardian row when either `guardians.auth_user_id = auth.uid()` or the linked internal `users` row maps to `auth.uid()`. No self-service mutation policy is granted.

## Explicit server-only tables

The following tables intentionally use deny-all RLS policies for the `authenticated` role. They are not client APIs.

### memories
Contains long-term memory content, sensitivity, confidence, source, and fact-status metadata. Raw memory rows must not be directly exposed to clients. Access should occur only through a purpose-built, filtered server/runtime interface.

### experience_memories
Contains internal problem patterns, hypotheses, actions, outcomes, lessons, and confidence. This is an internal reasoning/learning store and remains server-only.

### safety_events
Contains risk levels, safety summaries, guardian-conflict markers, actions taken, and open/closed safety state. Direct client access is intentionally denied. Any future guardian-facing safety view must use a dedicated, redacted API with its own review.

### guardian_link_requests
Contains `token_hash`, claim state, expiry, and linkage metadata. Direct authenticated-table access is intentionally denied. Guardian linking must be performed through a dedicated server flow that never exposes token hashes.

## Why explicit deny-all policies are used

RLS enabled with no policy already fails closed, but an explicit deny-all policy documents the intended boundary and avoids future maintainers "fixing" an advisor message by creating overly broad access.

Example intent:

```sql
create policy memories_server_only
on public.memories for all
to authenticated
using (false)
with check (false);
```

This does not make the table public; it records that direct authenticated access is forbidden.

## Non-negotiable rules

- Never authorize with `user_metadata`.
- Never use service-role access in client-facing runtime functions merely to bypass RLS.
- Never expose guardian-link token hashes.
- Never expose raw safety events or raw memory tables directly to clients.
- `小爱上线` is a persona command, not authentication.
- Memory/continuity access does not imply runtime persona-control permission.
- Shared identity/memory does not imply shared session ACTIVE/OFF state.

## Verification status

After applying the scoped-access and explicit server-only policies, the Supabase Security Advisor returned zero security lints for the project.
