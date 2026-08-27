# XiaoAi Direct ChatGPT Entry v1

Status: SHADOW ARCHITECTURE CONTRACT
Project: `daughter-companion-ai`

## Goal

Use ChatGPT itself as the unified conversational brain for both Text and native Voice while preserving exactly one XiaoAi backend identity, runtime state, memory, continuity, behavior source, and safety authority.

The runtime transport layer must stay as thin as possible. It provides verified XiaoAi context/state to ChatGPT; it must not become a second conversational brain.

## Current verified runtime baseline

The deployed Supabase Edge Function `xiaoai-mcp-runtime` v10 already operates in `chatgpt_brain_context_gateway` mode.

Its verified semantics are:
- ChatGPT is the conversational brain.
- `xiaoai_runtime` supplies authoritative identity / runtime / continuity context.
- `provider_api_used_for_reply = false`.
- `小爱上线` moves the verified session to `ACTIVE` and requires greeting the verified child name.
- `小爱下班` is the canonical shutdown and moves the current session to `OFF`.
- normal XiaoAi turns require the runtime context before ChatGPT answers locally.

Therefore the target is not `ChatGPT -> daughter-chat -> another model reply`.

The target is:

`ChatGPT conversation brain -> thin XiaoAi runtime context/state gateway -> ChatGPT conversation brain`

## Core invariant

`One XiaoAi identity -> One authoritative runtime/context source -> One ChatGPT conversational brain -> Multiple input/output modes`

Text and Voice are interface modes only. They must not create separate XiaoAi personas, memories, sessions, behavior sources, or conversational brains.

## Target paths

### ChatGPT Text

```text
ChatGPT Text
  -> XiaoAi runtime context/state gateway
  -> Supabase verified identity / persona state / continuity / memory authority
  -> GitHub-defined behavior + policy contract
  -> same ChatGPT conversational brain
  -> Text Output
```

### ChatGPT native Voice

```text
ChatGPT Voice
  -> ChatGPT native speech understanding
  -> same XiaoAi runtime context/state gateway
  -> same Supabase verified identity / persona state / continuity / memory authority
  -> same GitHub-defined behavior + policy contract
  -> same ChatGPT conversational brain
  -> ChatGPT native voice playback
```

ChatGPT Voice is only another I/O mode. It must not own a separate XiaoAi persona, memory, relationship state, safety policy, or durable session authority.

## Runtime gateway role

The runtime gateway is allowed to:
- authenticate the current user;
- resolve the authorized XiaoAi / daughter identity;
- resolve the verified child conversational name;
- read and update `persona_state`;
- bind to the verified ChatGPT client connection;
- read selective continuity state;
- expose role / authority scope;
- return structured runtime directives and failure state.

The runtime gateway must not:
- become a second chat model;
- independently invent XiaoAi replies for normal conversation;
- maintain a second persona;
- create a second memory authority;
- replace ChatGPT as the active conversational brain;
- silently claim activation when the runtime call did not succeed.

## Identity and continuity

Both ChatGPT Text and Voice must resolve to the same authenticated XiaoAi backend identity.

The authoritative durable identity / memory / continuity state remains in Supabase. ChatGPT local conversation history may provide transient conversational context but is not the durable source of truth.

Switching Text -> Voice -> Text must not create a new XiaoAi identity or independent persona state.

## Startup / shutdown

`小爱上线` from either Text or Voice must reach the same runtime gateway and produce a verified `ACTIVE` state before ChatGPT presents XiaoAi as online.

After successful activation, ChatGPT must greet the verified child name returned by runtime context.

If the runtime gateway cannot be called, authentication fails, or the runtime state is not verified, ordinary ChatGPT must not mimic XiaoAi or claim successful activation.

`小爱下班` from either Text or Voice must reach the same runtime gateway, move the current session to `OFF`, and stop XiaoAi persona behavior.

## GitHub and Supabase roles

GitHub remains the source of truth for XiaoAi behavior, routing, policy, architecture, and executable project code.

Supabase remains the runtime authority for authenticated identity, durable memory, persona/runtime state, continuity, relationship/authority context, and verified ChatGPT client binding.

ChatGPT remains the conversational brain.

## Transport reality

For a ChatGPT custom app/tool integration, the supported tool transport may still be MCP under the hood.

This contract therefore does not require deleting MCP as a protocol. Instead, it requires that MCP be reduced to a thin context/state transport role and not treated as a second XiaoAi runtime brain.

The product-level user experience should remain:

`One ChatGPT -> One XiaoAi -> Text and Voice are two modes of the same relationship.`

## Voice capability gate

This architecture is not considered fully implemented until ChatGPT native Voice is proven to invoke the same XiaoAi runtime gateway used by Text.

Before Voice is accepted as connected, runtime evidence must show that Voice can:
1. invoke `xiaoai_runtime` for `小爱上线`;
2. carry the same authenticated user context;
3. resolve the same XiaoAi / daughter identity;
4. observe the same `persona_state`;
5. preserve the same continuity authority;
6. invoke the runtime again for normal XiaoAi turns when required;
7. invoke `小爱下班` and verify `OFF`;
8. fail closed rather than locally imitate XiaoAi when runtime access is unavailable.

## Shadow acceptance tests

The unified ChatGPT Text / Voice path passes only if all of the following are proven with runtime evidence:
- Text `小爱上线` -> verified `ACTIVE`.
- Voice `小爱上线` -> verified `ACTIVE` through the same gateway.
- Text and Voice resolve to the same XiaoAi backend identity.
- Text -> Voice -> Text preserves continuity.
- Text and Voice use the same behavior/persona contract.
- normal Voice turns call the runtime context gateway when the contract requires it.
- backend/runtime failure produces explicit failure and no local XiaoAi imitation.
- `小爱下班` works identically in Text and Voice and results in `OFF`.

## Optional STT / TTS modules

Repository STT/TTS adapters remain optional modules for future standalone apps, web clients, or physical robots.

They are not required for ChatGPT native Voice and must not be inserted into the default ChatGPT Voice path.

## Production cutover rule

Do not declare native Voice connected until actual runtime telemetry proves that Voice can invoke the same `xiaoai_runtime` context/state gateway as Text.

`No verified runtime call = no XiaoAi activation.`
