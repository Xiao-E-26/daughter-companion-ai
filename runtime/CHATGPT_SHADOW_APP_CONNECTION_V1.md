# ChatGPT Shadow App Connection v1

Status: FRONTEND CONNECTION REQUIRED

## Purpose

Connect ChatGPT Text / native Voice to the already deployed authoritative XiaoAi shadow runtime without touching production v10.

## Shadow MCP endpoint

```text
https://vmegjuceiuplqixizwso.supabase.co/functions/v1/xiaoai-runtime-authoritative-shadow
```

## Tool exposed by shadow runtime

```text
xiaoai_runtime_authoritative
```

## Product role split

- ChatGPT = interface/window only.
- XiaoAi Runtime = authoritative conversational brain.
- GitHub = behavior/policy/code source.
- Supabase = identity/memory/session/continuity/runtime authority.
- MCP = thin transport only.

## Required ChatGPT connection behavior

The ChatGPT app connection must:
1. register the shadow endpoint as the app/tool server;
2. authenticate with the user's Supabase session through the existing protected-resource flow;
3. expose `xiaoai_runtime_authoritative` to ChatGPT;
4. call it for `小爱上线`;
5. call it for every XiaoAi turn while ACTIVE;
6. call it for `小爱下班`;
7. present the returned authoritative reply without locally inventing or rewriting XiaoAi content;
8. fail closed if the tool/runtime is unavailable.

## Acceptance evidence for `小爱上线`

A successful activation must return structured runtime evidence including:
- `ok = true`
- `persona_state = ACTIVE`
- `transition = ->ACTIVE`
- `reply_source = xiaoai_runtime`
- `reply_authoritative = true`
- `chatgpt_role = interface_only`
- verified `daughter_id`
- verified `client_connection_id`
- authoritative `reply`

No verified runtime result means XiaoAi is not online.

## Text / Voice unification test

Run this exact sequence after connection:
1. Text: `小爱上线`
2. Text: ordinary XiaoAi message
3. Switch to native Voice in the same XiaoAi relationship
4. Voice: ordinary XiaoAi message
5. Voice: `小爱下班`
6. Confirm Supabase runtime state is OFF

Pass only if Text and Voice resolve to the same XiaoAi identity/session authority and all final replies come from XiaoAi Runtime.

## Current blocker

The backend shadow runtime is deployed and ACTIVE, but the current ChatGPT account/session does not yet expose a XiaoAi app/tool connection. The connection must be registered on the ChatGPT side before real Text/Voice E2E can run.

Production `xiaoai-mcp-runtime` v10 remains unchanged for rollback.
