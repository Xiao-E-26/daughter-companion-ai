# Supabase Persona State Adapter v1

Status: SHADOW / REFERENCE CONTRACT

## Purpose

Define the target contract for persisting XiaoAi persona state per authorized runtime session without allowing the language model to self-activate.

This document does **not** claim that production persona-state persistence is currently deployed.

## Verified live database posture — 2026-09-20

Current production table: `public.runtime_sessions`.

Verified live columns:
- `id`
- `child_id`
- `user_id`
- `client_connection_id`
- `session_key`
- `status`
- `started_at`
- `ended_at`
- `created_at`
- `updated_at`

The live table currently does **not** contain:
- `persona_state`
- `activation_source`
- `activated_at`
- `deactivated_at`
- `last_active_at`

The only verified session-start RPC is `start_child_runtime_session_shadow_v1`.

Therefore:
- session substrate exists;
- persona-state persistence remains shadow/design-only;
- production `ACTIVE/OFF` persistence is not yet closed.

## Command contract

Canonical activation command: `小爱上线`

Canonical shutdown command: `小爱下班`

Compatibility aliases:
- `小爱收工`
- `小愛收工`
- `小愛下班`

The deterministic gate in `runtime/persona_gate.py` owns command interpretation. Conversation context, emotional wording, child-like language, remembered state, or family context must never auto-activate XiaoAi.

## Security contract

1. Default state is fail-closed.
2. Identity, authorization, client binding, session state, and persona state remain separate concerns.
3. Do not expose service-role credentials to any client.
4. Do not add broad authenticated RLS merely to make persona persistence work.
5. The model must never write persona state directly.
6. A future production adapter must require a verified caller binding and authorized session before persisting `ACTIVE/OFF`.
7. Missing or unreadable persona persistence must not be presented as successful activation.

## Target adapter interface

A production implementation may satisfy the `PersonaStateStore` protocol from `runtime/persona_gateway.py`:

```python
get_state(child_id, user_id, session_key) -> str | None
set_state(child_id, user_id, session_key, state, activation_source) -> None
```

This is a target interface, not evidence of a live production adapter.

## Current blocker

Production contains no bound live identities or live runtime sessions. Verified counts for `auth.users`, `users`, `companion_access`, `client_connections`, and `runtime_sessions` are all zero.

Until a real verified identity/session path exists and a production persona-state store is deployed, this contract remains SHADOW / REFERENCE and activation persistence must fail closed.
