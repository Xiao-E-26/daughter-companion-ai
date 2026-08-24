# Supabase Persona State Adapter v1

## Purpose

Persist XiaoAi persona state per authorized runtime session without allowing the language model to self-activate.

## Current database contract

Table: `public.runtime_sessions`

Required fields used by the gateway:

- `daughter_id`
- `user_id`
- `session_key`
- `persona_state` (`OFF` | `ACTIVE`)
- `activation_source`
- `activated_at`
- `deactivated_at`
- `last_active_at`

`status` remains the lifecycle status of the runtime session and MUST NOT be reused as persona activation state.

## Security contract

1. Default state is `OFF`.
2. Missing, malformed, unauthorized, or unreadable state must resolve to `OFF`.
3. Persona state is scoped by `(daughter_id, user_id, session_key)`.
4. Memory continuity may be shared across authorized clients, but persona runtime state is not implicitly shared.
5. The model never writes directly to `runtime_sessions`.
6. Do not expose a service-role key to a ChatGPT client, browser, mobile client, or robot client.
7. Do not add a broad authenticated RLS policy merely to make the gateway work.
8. Production writes require a verified caller identity mapped to `public.users.auth_user_id` and authorized access in `public.companion_access`.
9. Activation/deactivation must be persisted by the trusted gateway after `XiaoAiPersonaGate` decides the transition.
10. The exact command `小爱收工` persists `OFF`; subsequent emotional or child-like content cannot reactivate XiaoAi.

## Production adapter interface

The adapter must implement the `PersonaStateStore` protocol from `runtime/persona_gateway.py`:

```python
get_state(daughter_id, user_id, session_key) -> str | None
set_state(daughter_id, user_id, session_key, state, activation_source) -> None
```

## Activation flow

```text
Client message
  -> authenticate caller
  -> resolve internal user + daughter access
  -> read session persona_state
  -> XiaoAiPersonaGate.evaluate(...)
  -> persist transition when present
  -> ACTIVE: load XiaoAi identity/behavior/memory context
  -> OFF: route to normal assistant without XiaoAi persona context
```

## Blocker before production persistence

The current Supabase project contains no rows in `users`, `client_connections`, or `companion_access`. Therefore there is not yet a verified caller-to-user-to-daughter mapping to authorize production state writes safely. Until that mapping exists, the production adapter must remain fail-closed rather than introducing a permissive RLS/RPC shortcut.
