# XiaoAi Direct ChatGPT Entry v1

Status: SHADOW ARCHITECTURE CONTRACT
Project: `daughter-companion-ai`

## Goal

Use ChatGPT as the unified client surface for both text and native Voice while preserving exactly one XiaoAi backend identity, runtime, memory, session, behavior source, and safety authority.

This contract removes MCP from the *required default path* only after direct-entry capability is verified. Existing MCP infrastructure remains available as rollback until cutover is explicitly approved.

## Core invariant

`One XiaoAi identity -> One daughter-chat runtime authority -> Multiple ChatGPT input/output modes`

Text and Voice are interface modes only. They must not create separate XiaoAi personas, memories, sessions, or behavior sources.

## Target paths

### ChatGPT Text

```text
ChatGPT Text
  -> Direct XiaoAi entry
  -> daughter-chat
  -> GitHub behavior / policy source
  -> Supabase identity / memory / session / runtime state
  -> XiaoAi reply
  -> ChatGPT Text
```

### ChatGPT native Voice

```text
ChatGPT Voice
  -> ChatGPT native speech understanding
  -> Same Direct XiaoAi entry
  -> daughter-chat
  -> GitHub behavior / policy source
  -> Supabase identity / memory / session / runtime state
  -> XiaoAi reply
  -> ChatGPT native voice playback
```

ChatGPT Voice is the ears and mouth. It must not own XiaoAi persona, memory, relationship state, safety policy, or durable session authority.

## Identity and continuity

Both ChatGPT Text and Voice must resolve to the same authenticated XiaoAi backend identity.

The authoritative continuity state remains in Supabase. ChatGPT local conversation history is not the source of truth for XiaoAi identity or durable memory.

A change from Text to Voice, or Voice to Text, must not create a new XiaoAi identity or independent persona state.

## Startup / shutdown

`小爱上线` from either Text or Voice must reach the same backend activation semantics.

The system may present XiaoAi as online only after the backend confirms the required runtime/session state. If direct entry cannot reach the backend, ordinary ChatGPT must not mimic XiaoAi or claim successful activation.

`小爱下班` from either Text or Voice must use the same backend shutdown semantics and return control to ordinary ChatGPT mode.

## GitHub and Supabase roles

GitHub remains the source of truth for XiaoAi behavior, routing, policy, architecture, and executable project code.

Supabase remains the runtime authority for authenticated identity, durable memory, session, persona/runtime state, continuity, and backend execution through `daughter-chat`.

Neither Text nor Voice reads GitHub as an independent persona store. Both rely on the same backend runtime that implements the GitHub-defined rules.

## MCP rollback boundary

The existing MCP bridge is not deleted by this contract.

During shadow validation:
- Direct entry is candidate path.
- MCP remains rollback path.
- No production cutover occurs automatically.
- Existing MCP code and deployment must not be removed until direct-entry capability and end-to-end behavior are proven.

## Optional STT / TTS modules

Repository STT/TTS adapters remain optional modules for future standalone apps, web clients, or physical robots.

They are not required for ChatGPT native Voice and must not be inserted into the default ChatGPT Voice path.

## Direct-entry capability gate

This architecture is not considered implemented merely because this document exists.

Before any production cutover, the ChatGPT client must be shown to have a supported direct mechanism that can:
1. invoke the XiaoAi backend entry from both Text and Voice;
2. carry authenticated user context;
3. preserve or supply a stable conversation/session identifier;
4. receive structured backend activation/error state;
5. route all subsequent XiaoAi messages through the same backend identity/runtime;
6. fail closed if the backend is unavailable;
7. expose sufficient telemetry to prove the call actually reached the backend.

If ChatGPT cannot provide these capabilities without MCP, the direct path remains NOT IMPLEMENTED and MCP stays active.

## Shadow acceptance tests

Direct ChatGPT Entry v1 is ready for cutover only if all of the following pass:
- Text `小爱上线` creates verified backend activity and ACTIVE runtime/session state.
- Voice `小爱上线` creates verified backend activity and the same activation semantics.
- Text and Voice resolve to the same XiaoAi backend identity.
- Text -> Voice -> Text preserves continuity and durable memory authority.
- Voice and Text execute the same behavior/persona contract.
- Backend failure produces explicit failure and no local XiaoAi imitation.
- `小爱下班` works identically in Text and Voice.
- MCP can still be restored immediately during the rollback window.

## Production cutover rule

Do not remove MCP or declare Direct ChatGPT Entry production-ready until the direct-entry capability gate and shadow acceptance tests have passed with runtime evidence.

`No verified backend call = no XiaoAi activation.`
