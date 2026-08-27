# XiaoAi Runtime Production Reply Wiring v1

Status: SHADOW / PRE-PRODUCTION

## Goal

Replace the current `chatgpt_local` reply behavior with an authoritative XiaoAi Runtime reply path while keeping ChatGPT Text and native Voice as interface-only surfaces.

## Product invariant

`ChatGPT = window. XiaoAi Runtime = brain.`

ChatGPT may transport input and present output. It must not invent, rewrite, complete, or substitute XiaoAi replies locally.

## Target runtime path

```text
ChatGPT Text / Voice
  -> XiaoAi transport entry
  -> authenticated identity + runtime/session resolution
  -> XiaoAi Brain Core
      -> intent / safety / memory / behavior planning
      -> provider/model adapter
      -> authoritative final reply
  -> transport returns exact final reply
  -> ChatGPT displays / speaks exact reply
```

## Existing assets to reuse

- `runtime/orchestrator.py` is the existing protected runtime brain boundary.
- `runtime/authoritative_reply_adapter.py` enforces authoritative reply ownership on the Python runtime side.
- `xiaoai-brain-core-test` demonstrates intent/safety/memory/response planning plus provider invocation.
- `xiaoai-brain-gateway-test` demonstrates provider-backed reply generation.
- Current `xiaoai-mcp-runtime` v10 already contains useful authenticated identity/session/continuity resolution, but its `chatgpt_local` reply mode is not the target.

## Required production behavior

For each XiaoAi turn after activation:
1. authenticate the calling ChatGPT connection;
2. resolve the existing authorized daughter identity;
3. resolve the same runtime session and continuity state used by Text and Voice;
4. load only authorized memory/context;
5. invoke the authoritative XiaoAi Brain Core;
6. require a non-empty backend `reply`;
7. return that exact reply as the tool result;
8. mark metadata as backend-authoritative;
9. prohibit a local ChatGPT XiaoAi fallback.

## Required structured result

A successful runtime result must include at least:

```json
{
  "ok": true,
  "reply_source": "xiaoai_runtime",
  "reply_authoritative": true,
  "persona_state": "ACTIVE",
  "daughter_id": "...",
  "session_key": "...",
  "reply": "..."
}
```

Optional telemetry may include provider/model IDs, runtime version, checkpoint stage, memory candidate state, or continuity version, but must not expose private secrets.

## Fail-closed rules

If any required stage fails, the transport must return an explicit error and no XiaoAi reply.

Failure cases include:
- authentication missing/invalid;
- identity/access conflict;
- runtime session conflict;
- persona not ACTIVE for a normal XiaoAi turn;
- Brain Core unavailable;
- provider unavailable;
- provider returns empty output;
- authoritative reply missing;
- behavior/safety boundary failure.

In all such cases:

`No authoritative runtime reply = no XiaoAi response.`

ChatGPT must not generate a substitute XiaoAi answer.

## Activation / shutdown

`小爱上线` and `小爱下班` remain runtime state transitions.

Activation must be verified before the startup reply is presented. Shutdown must set the current session OFF before ordinary ChatGPT behavior resumes.

The startup/shutdown reply may be deterministic inside XiaoAi Runtime, but it is still runtime-owned and must not be locally invented by the ChatGPT interface.

## Text / Voice unification

Text and Voice must call the same runtime path and resolve to the same:
- daughter identity;
- authenticated user;
- client connection;
- session authority;
- memory authority;
- continuity state;
- behavior/safety rules;
- final reply pipeline.

Only presentation differs: Text displays the runtime reply; Voice speaks the same runtime reply.

## Shadow migration plan

1. Keep current production `xiaoai-mcp-runtime` v10 unchanged.
2. Create a separately named shadow Edge Function for authoritative reply wiring.
3. Reuse the existing v10 identity/session protections.
4. Route shadow normal turns to a secured Brain Core endpoint.
5. Require `reply_authoritative=true` and `reply_source=xiaoai_runtime`.
6. Run Text/Voice-equivalent payload regression against the shadow function.
7. Compare activation, normal turn, failure, continuity, and shutdown behavior.
8. Only after all regression passes may production v10 be replaced or versioned forward.

## Security requirements for Brain Core endpoint

The production Brain Core endpoint must not be publicly callable without authentication/authorization.

If implemented as a service-to-service Edge Function, require an internal secret/header and never expose service-role credentials in ChatGPT or client-visible payloads.

## Cutover gate

Production cutover is forbidden until all are true:
- Behavior Freeze CI passes;
- Golden Regression CI passes;
- authoritative reply tests pass;
- shadow Edge Function returns backend-owned replies;
- failure paths are fail-closed;
- Text and Voice resolve to the same XiaoAi identity/runtime;
- rollback to current v10 remains available.
