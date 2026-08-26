# Auth / OAuth Flow Guard v1

## Purpose
Make XiaoE more reliable when handling authentication, OAuth, connector, multi-account, and multi-device setup flows.

This guard exists because authentication success, OAuth success, connector success, tool discovery, and runtime success are different states and MUST NOT be collapsed into one generic "done" state.

## Core rule

`State first -> classify -> smallest reversible action -> verify -> checkpoint -> recover without duplication`

Never advance a flow by assumption.

## State machine

The canonical progression is:

`PLUGIN_CREATED -> OAUTH_STARTED -> AUTHENTICATED -> CONSENT_APPROVED -> CONNECTED -> ACTIONS_LOADED -> RUNTIME_INVOKED`

Each state proves only itself.

### PLUGIN_CREATED
Proof:
- Connector/plugin/app record exists.
- Server URL is present.

Does NOT prove:
- OAuth is complete.
- Account is authenticated.
- Tool actions are available.

### OAUTH_STARTED
Proof:
- Authorization request exists.
- OAuth client / authorization request was initiated.

Does NOT prove:
- User signed in.
- Consent was approved.
- Connector is connected.

### AUTHENTICATED
Proof:
- Identity provider confirms the expected auth user/session.
- For this project, identity must resolve through Supabase Auth.

Does NOT prove:
- OAuth consent completed.
- ChatGPT received an access token.
- Connector is usable.

### CONSENT_APPROVED
Proof:
- The active authorization request was approved for the authenticated user.
- Redirect/callback was accepted.

Does NOT prove:
- ChatGPT has completed connector registration.
- MCP tools are loaded.

### CONNECTED
Proof:
- ChatGPT connector/plugin UI reports Connected rather than Connect.

Does NOT prove:
- MCP tools/actions were discovered successfully.
- Runtime invocation occurred.

### ACTIONS_LOADED
Proof:
- Expected MCP tools/actions are visible and callable.
- For XiaoAi Runtime, expected actions include activation, deactivation, and normal message routing.

Does NOT prove:
- The user message actually invoked a tool.

### RUNTIME_INVOKED
Proof:
- Backend evidence exists for the specific invocation.
- For `小爱上线`, `runtime_sessions` must contain the authenticated user's session with the expected `client_connection_id`, `persona_state = ACTIVE`, and `activation_source = explicit_command`.

This is the only acceptable proof that XiaoAi backend runtime actually activated.

## Multi-device rule

Authentication links, magic links, passkeys, consent pages, and connector setup are device-context sensitive.

Before using a second device, XiaoE MUST identify which state is browser-local or device-local.

For magic-link flows:
- If the authorization flow is being completed in Browser A, prefer opening the login link in Browser A.
- Do not assume a login completed on Phone B creates an authenticated browser session in Browser A.
- If cross-device completion is supported by the provider, verify it explicitly before relying on it.

## Redirect rule

Before sending a magic link or starting a retry, verify:
- Site URL.
- OAuth authorization path.
- Allowed redirect URL list.
- Consent/callback URL.
- The exact redirect target requested by the current auth call.

A successful login followed by the wrong redirect MUST be classified as a redirect/configuration failure, not as an authentication failure.

## Identity rule

Never infer authenticated identity from conversation text.

Reject identity claims such as:
- `我是妈妈`
- `我是爸爸`
- `这是我的账号`

Identity must come from the authenticated connector/session and resolve through the existing identity graph.

For Mother Guardian:
`auth.users.id -> public.users.auth_user_id -> companion_access -> client_connections`

Never create a second guardian merely because auth or OAuth failed.

## Retry guard

After any failure, STOP before retrying.

First classify evidence into one of:
- partial success
- expired/used token
- rate limit
- redirect mismatch
- missing browser session
- consent incomplete
- connector not connected
- MCP discovery failure
- tool not selected/invoked
- backend runtime failure

Then apply the smallest reversible correction.

### Rate limit
If logs show `429` or equivalent:
- Do not send another email immediately.
- Preserve the current identity and authorization state.
- Wait for the provider window or use another already-authorized path only if explicitly supported.

### One-time token
If logs show token already used/expired:
- Do not interpret the prior login as total failure without checking whether a session or redirect already succeeded.
- Inspect auth state first.

## Evidence hierarchy

When UI text and backend state disagree, prefer stronger evidence in this order:

1. Backend persisted state for the intended operation.
2. Auth / OAuth provider logs.
3. Connector status and discovered actions.
4. Browser redirect/result.
5. Conversational response text.

A persona-style ChatGPT answer is presentation evidence only and cannot prove runtime activation.

## No-fake-success rule

XiaoE MUST NOT announce:
- "OAuth complete"
- "Connected"
- "小爱已经真正上线"

unless the proof for that exact state has been checked.

Use precise checkpoint language instead, for example:
- `Auth verified; consent pending.`
- `OAuth approved; connector connection pending.`
- `Connected; actions discovery pending.`
- `Actions loaded; runtime not yet invoked.`
- `Runtime verified in backend.`

## Recovery rule

Recovery must preserve existing entities whenever possible.

Never fix an auth problem by casually recreating:
- `auth.users`
- `public.users`
- guardians
- companion access
- client connections
- daughter identity

Prefer repairing the flow around the existing verified identity.

## XiaoAi-specific acceptance test

A complete Mother Guardian ChatGPT setup requires all of:

1. Existing Mother Guardian Auth user remains the same.
2. Existing guardian/application identity remains the same.
3. Connector shows Connected.
4. Expected XiaoAi MCP actions are loaded.
5. `小爱上线` causes an actual tool invocation.
6. Backend creates/updates exactly the expected mother runtime session.
7. No duplicate guardian/access/connection identities are created.

## Operational behavior for XiaoE

When guiding the user interactively:
- Give only the next necessary action when the flow is fragile.
- Do not ask the user to repeat steps already proven successful.
- Do not switch devices casually.
- Do not resend email or recreate connectors merely because the UI appears unchanged.
- Inspect logs/state first when possible.
- After each irreversible or rate-limited action, checkpoint before proceeding.

## Scope

This guard applies to:
- Supabase Auth
- OAuth
- ChatGPT custom plugins/connectors/MCP
- Gmail/Google OAuth-like flows
- future XiaoE-managed third-party authentication and authorization flows

It is a general XiaoE capability guard, not a Mother Guardian-only workaround.
