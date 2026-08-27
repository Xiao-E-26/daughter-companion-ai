# XiaoAi Native Entry Shadow v1

Status: SHADOW / PRE-PRODUCTION

## Purpose

Provide one transport-agnostic JSON entry surface for a future platform-native ChatGPT identity connection.

User-facing architecture:

```text
ChatGPT microphone / speaker / text window
  -> trusted platform identity
  -> XiaoAi Native Entry
  -> Identity Resolver
  -> XiaoAi Runtime
  -> authoritative XiaoAi reply
  -> ChatGPT display / playback
```

The user must not configure or understand MCP. Any JSON-RPC/MCP call used behind this layer is an internal transport detail only.

## Deployed shadow function

`xiaoai-native-entry-shadow`

Security posture:
- `verify_jwt = true`
- accepts only authenticated requests
- requires `message`; optional `session_key`
- fails closed on identity or runtime failure

## Internal stages

1. Receive trusted authenticated caller and message.
2. Call `xiaoai-identity-resolver-shadow` with the same auth context.
3. Require one verified/authorized XiaoAi identity.
4. Call authoritative XiaoAi Runtime internally.
5. Require `reply_source = xiaoai_runtime` and `reply_authoritative = true`.
6. Cross-check that resolved `daughter_id` equals Runtime `daughter_id`.
7. Return the Runtime reply unchanged.

## Identity/Runtime separation

Native Entry owns neither identity nor behavior.

Identity Resolver owns:
- caller identity resolution
- internal user mapping
- companion access resolution
- role/authority scope
- XiaoAi/Daughter identity resolution
- optional entry/session lookup

XiaoAi Runtime owns:
- persona ACTIVE/OFF transitions
- behavior/policy execution
- memory/session context use
- safety logic
- final XiaoAi reply

ChatGPT owns only input/output presentation.

## Required successful response contract

A successful response must prove:
- `identity_verified = true`
- resolved `daughter_id`
- `reply_source = xiaoai_runtime`
- `reply_authoritative = true`
- Runtime `persona_state`
- authoritative `reply`

## Fail closed

Any of these must produce no XiaoAi reply:
- unauthenticated caller
- identity resolver failure
- ambiguous/no companion access
- identity/runtime daughter mismatch
- runtime unavailable
- missing runtime reply
- reply not marked authoritative

ChatGPT must not locally generate a XiaoAi replacement.

## Current limitation

This shadow makes the backend ready for a native platform identity channel, but it does not create that channel inside ChatGPT. A future supported platform integration must pass a trustworthy identity credential/context to this entry or an equivalent production successor.

## Production cutover rule

Do not replace production runtime routing until:
1. platform-native identity handoff is available and verified;
2. Text E2E passes;
3. native Voice E2E passes;
4. both resolve the same XiaoAi identity authority;
5. runtime telemetry proves all final replies come from XiaoAi Runtime;
6. rollback remains available.
