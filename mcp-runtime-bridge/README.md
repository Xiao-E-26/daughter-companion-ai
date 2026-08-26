# XiaoAi MCP Runtime Bridge

Primary archetype: **tool-only**.

This bridge lets a ChatGPT app call the existing `daughter-chat` Supabase Edge Function so that `小爱上线` and `小爱收工` become real backend runtime transitions instead of presentation-only persona replies.

## Tools

- `xiaoai_activate` — exact activation route for `小爱上线`
- `xiaoai_deactivate` — exact deactivation route for `小爱收工`
- `xiaoai_message` — forwards normal XiaoAi conversation messages after activation

## Identity model

The bridge does not accept `user_id`, `guardian_id`, or role claims from tool inputs.

It forwards the authenticated Bearer session to `daughter-chat`, which resolves identity through the existing chain:

`auth.users.id -> public.users.auth_user_id -> companion_access -> client_connections`

This means saying "我是妈妈" in chat cannot grant Mother Guardian access.

## Required authentication assumption

The ChatGPT app connection must provide a Supabase Auth Bearer token in the MCP request `Authorization` header. The current bridge intentionally fails closed with `missing_authenticated_supabase_session` when no authenticated Supabase session is present.

For production, configure the ChatGPT app authentication/OAuth path so each connected ChatGPT account authenticates as its own Supabase user. Do not use a service-role token or shared static user token.

## Environment

```bash
SUPABASE_URL=https://vmegjuceiuplqixizwso.supabase.co
PORT=8787
```

No Supabase service-role key is required by this bridge.

## Local development

```bash
npm install
npm run dev
```

Health check:

```bash
curl http://localhost:8787/health
```

MCP endpoint:

```text
http://localhost:8787/mcp
```

For ChatGPT Developer Mode testing, expose the server through a public HTTPS tunnel and connect the app to:

```text
https://<public-host>/mcp
```

## Expected activation verification

After the authenticated Mother Guardian ChatGPT app calls `xiaoai_activate`, Supabase should show:

- one `runtime_sessions` row for Mother Guardian
- `client_connection_id` = the verified Mother ChatGPT connection
- `persona_state = ACTIVE`
- `activation_source = explicit_command`
- no new guardian identity

## Current limitation

This repository now contains the MCP bridge scaffold, but it is **not yet deployed or connected to ChatGPT**. A normal ChatGPT conversation still cannot invoke this code automatically until the MCP server is hosted and added as a ChatGPT app in Developer Mode.
