# ChatGPT Runtime Bridge v1

## Goal
Connect both the primary ChatGPT account and Mother Guardian ChatGPT account to the same XiaoAi backend runtime without duplicating identity, memory, or companion state.

## Current verified state
- Mother Guardian Supabase Auth identity is verified.
- Mother Guardian is bound to the existing guardian placeholder.
- `companion_access` is active for role `guardian`.
- `client_connections` contains one active `chatgpt` connection labelled `Mother ChatGPT - verified`.
- `daughter-chat` already supports explicit activation with `小爱上线` and deactivation with `小爱收工`, and persists `runtime_sessions`.
- Plain ChatGPT conversation currently does not automatically invoke `daughter-chat`; therefore a persona response inside ChatGPT is not proof of backend activation.

## Bridge contract

### Trigger
When a bound ChatGPT entry receives the exact activation command:

`小爱上线`

it MUST invoke the XiaoAi backend before presenting XiaoAi as active.

When it receives:

`小爱收工`

it MUST invoke the backend deactivation route before presenting XiaoAi as offline.

### Identity resolution
The bridge must never trust a conversational statement such as "我是妈妈".
Identity must come from the authenticated connector/tool session and map to:

`auth.users.id -> public.users.auth_user_id -> companion_access -> client_connections`

Only one active companion access row and one active ChatGPT client connection are accepted for a runtime call.

### Runtime activation
For `小爱上线`, call `daughter-chat` with:

```json
{
  "message": "小爱上线",
  "session_key": "<stable ChatGPT conversation/session key>"
}
```

Expected response:

```json
{
  "ok": true,
  "route": "xiaoai",
  "persona_state": "ACTIVE",
  "transition": "->ACTIVE"
}
```

Only after this response may the UI say XiaoAi is online.

### Runtime deactivation
For `小爱收工`, call `daughter-chat` with the same stable `session_key`.
Expected state: `persona_state = OFF`.

### Continuity
After runtime activation, the bridge may load continuity through the existing continuity layer subject to role and visibility policy. Guardian entry must not receive child-private raw conversation merely because the guardian account is authenticated.

### Safety and privacy
- Never expose service-role keys, Supabase secrets, or raw auth tokens to the client.
- No conversational phrase can grant or upgrade guardian access.
- No duplicate guardian identity creation.
- Do not fabricate a `runtime_session` when the backend call was not made.
- Preserve V0-V4 / minimum-necessary cross-account visibility rules.

## Verification checklist
A successful Mother Guardian activation test must show all of the following:

1. Mother `client_connections.status = active`.
2. A `runtime_sessions` row exists for the Mother Guardian user.
3. `runtime_sessions.client_connection_id` equals the verified Mother ChatGPT connection.
4. `persona_state = ACTIVE` after `小爱上线`.
5. `activation_source = explicit_command`.
6. No new guardian identity was created.
7. Continuity read/write, if any, respects guardian visibility rules.

## Important limitation
A normal ChatGPT chat session cannot call this backend merely because the user typed `小爱上线`. A tool/app/MCP bridge must be registered with ChatGPT and invoked for activation. Until that bridge is installed, XiaoAi-style replies in a normal chat are presentation-layer behavior only, not backend runtime activation.
