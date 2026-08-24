# 小爱 Unified Runtime v1

Status: IMPLEMENTATION DESIGN

## Goal

Create one trusted runtime path for Child, Mother Guardian, web, app, and future robot clients.

`Client -> Runtime Gateway -> Identity/Role -> Policy -> Approved State -> AI -> Audit`

## Source-of-Truth Split

- GitHub: identity, behavior, policy, versioned rules
- Supabase: users, companion identity, guardian relationships, memory, growth state, sessions, safety events, audit logs
- Runtime: resolves who is speaking, what they may access, what context to load, and what may be written back
- ChatGPT/client history: temporary session context only

## Runtime Request Contract

Every request should resolve these fields before model execution:

- `companion_id`
- `user_id`
- `role`
- `client_id`
- `session_id`
- `life_stage`
- `guardian_scope`
- `behavior_version`
- `runtime_version`

No role may be inferred solely from conversational claims.

## Runtime Flow

1. Verify client/account link.
2. Resolve internal user identity.
3. Resolve relationship to the same 小爱 companion identity.
4. Resolve role: CHILD / GUARDIAN / DEVICE / MAINTAINER.
5. Load current growth/life-stage state.
6. Load applicable Guardian and safety rules.
7. Load only authorized durable memories.
8. Build runtime context from GitHub-versioned behavior + Supabase state.
9. Call the AI model.
10. Apply write policy to any memory/state update.
11. Write session/audit/safety events as needed.
12. Return response to the originating client.

## Child Runtime Context

May include:
- 小爱 Behavior Core
- child life stage
- child-approved memories
- relevant growth state
- current safety rules
- current session context

Must exclude by default:
- Guardian private data
- developer secrets
- unrestricted system configuration

## Mother Guardian Runtime Context

May include:
- 小爱 system status/version
- verified Guardian relationship
- Guardian permission scope
- child safety settings permitted by policy
- account/device authorization status
- safety events permitted for Guardian visibility

Must not automatically include:
- full child transcripts
- all private child memories
- secrets or developer credentials

## State Write Rules

Runtime must distinguish:
- session-only context
- candidate memory
- approved durable memory
- safety event
- permission change
- audit event

Conversation text must never be promoted directly into permanent truth without memory-policy checks.

## Failure Mode

If identity, role, or permission resolution fails:
- do not fall back to a more privileged role,
- do not expose shared memory,
- do not perform privileged writes,
- return a limited or unauthenticated interaction mode where appropriate,
- audit the failed privileged attempt when relevant.

## Versioning

Runtime must record both:
- `behavior_version`
- `runtime_version`

This allows rollback and behavioral regression testing.

## Current Target

Runtime v1 should first support:
- one child identity,
- one mother Guardian identity,
- one shared 小爱 companion identity,
- separate sessions,
- role-scoped reads,
- audit logging,
- no automatic transcript sharing.

Do not add broad autonomous actions in v1.
