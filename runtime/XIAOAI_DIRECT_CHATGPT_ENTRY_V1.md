# XiaoAi Direct ChatGPT Entry v1

Status: SHADOW ARCHITECTURE CONTRACT
Project: `daughter-companion-ai`

## Goal

Use ChatGPT only as the unified client window for both Text and native Voice while preserving exactly one XiaoAi conversational brain, one backend identity, one runtime, one memory/session authority, and one behavior source.

ChatGPT must not become the XiaoAi conversational brain. It is only the interface surface that receives user input and presents XiaoAi output.

## Core invariant

`One XiaoAi identity -> One XiaoAi Runtime brain -> Multiple ChatGPT interface modes`

Text and Voice are interface modes only. They must not create separate XiaoAi personas, memories, sessions, behavior sources, or conversational brains.

## Authoritative role split

### ChatGPT
ChatGPT is interface only:
- Text input/output window;
- native Voice speech input/output window;
- transport surface into the XiaoAi backend/runtime;
- presentation of the backend-produced XiaoAi reply.

ChatGPT must not:
- invent XiaoAi persona behavior locally;
- become the authoritative conversational brain;
- use local chat history as durable XiaoAi memory;
- claim XiaoAi is online without verified runtime activation;
- silently answer as XiaoAi if backend/runtime access fails.

### XiaoAi Runtime
XiaoAi Runtime is the authoritative conversational brain. It owns the actual XiaoAi response pipeline and must resolve:
- identity and authorization;
- persona/runtime state;
- session and continuity;
- durable memory context;
- relationship context;
- behavior / policy execution;
- final XiaoAi reply.

### GitHub
GitHub remains the source of truth for XiaoAi behavior rules, routing rules, policy, architecture, tests, and executable runtime code.

### Supabase
Supabase remains the runtime authority for authenticated identity, durable memory, session, persona/runtime state, continuity, relationship/authority context, and verified client binding.

## Target paths

### ChatGPT Text

```text
User Text
  -> ChatGPT Text window
  -> XiaoAi Runtime
  -> GitHub behavior / policy
  -> Supabase identity / memory / session / context
  -> XiaoAi final reply
  -> ChatGPT Text window
```

### ChatGPT native Voice

```text
User Voice
  -> ChatGPT native speech interface
  -> XiaoAi Runtime
  -> GitHub behavior / policy
  -> Supabase identity / memory / session / context
  -> XiaoAi final reply
  -> ChatGPT native voice playback
```

ChatGPT Voice is only the ears and mouth. It must not own XiaoAi persona, memory, relationship state, safety policy, or durable session authority.

## One XiaoAi across Text and Voice

Text and Voice must resolve to the same authenticated XiaoAi identity and the same XiaoAi Runtime.

Switching Text -> Voice -> Text must not:
- create another XiaoAi identity;
- create another persona;
- create another memory store;
- create another behavior prompt;
- reset the authoritative runtime unless the backend explicitly requires a new session.

## Startup / shutdown

`小爱上线` from either Text or Voice must reach the same XiaoAi Runtime activation path.

The system may present XiaoAi as online only after the runtime confirms the required authenticated identity/session/persona state.

After successful activation, the XiaoAi Runtime must produce the startup reply according to the existing greeting policy, including the verified child conversational name from the private source of truth.

If runtime access, authentication, session loading, or required state fails:
- ChatGPT must report failure;
- ChatGPT must not imitate XiaoAi;
- ChatGPT must not generate a substitute XiaoAi reply locally;
- local conversation history must not be used as fallback authority.

`小爱下班` from either Text or Voice must reach the same runtime shutdown path, persist required state, set the XiaoAi interaction state to OFF, and return the interface to ordinary ChatGPT mode.

## Transport boundary

The transport mechanism between ChatGPT and XiaoAi Runtime may use MCP or another supported ChatGPT integration protocol under the hood.

Transport is infrastructure only. It is not XiaoAi's brain, persona, memory, or behavior authority.

Therefore the product-level invariant is:

`ChatGPT = window. XiaoAi Runtime = brain.`

The presence of MCP transport does not mean there are two XiaoAi systems.

## Existing runtime mismatch that must be corrected before cutover

The currently deployed `xiaoai-mcp-runtime` v10 contains a `chatgpt_brain_context_gateway` design in which ChatGPT is instructed to answer locally. That design is not the target architecture defined here.

Before production cutover, the runtime must be changed so that:
- the backend/runtime produces the authoritative XiaoAi final reply;
- ChatGPT does not locally invent the XiaoAi reply;
- Text and Voice both receive the same backend-produced response semantics;
- the existing identity / session / continuity protections are preserved;
- frozen Behavior Core protections remain intact;
- rollback remains available.

This mismatch must be resolved through an independent reviewed change; this architecture document alone does not modify production runtime behavior.

## Voice capability gate

Native Voice is not considered connected until runtime evidence proves that Voice can use the same XiaoAi Runtime path as Text.

Acceptance requires evidence that Voice can:
1. invoke the same runtime activation path for `小爱上线`;
2. carry the same authenticated user context;
3. resolve the same XiaoAi identity;
4. load the same session / memory / continuity authority;
5. receive the backend-produced XiaoAi reply;
6. continue normal conversation through the same runtime;
7. invoke `小爱下班` through the same shutdown path;
8. fail closed rather than locally imitate XiaoAi when runtime access is unavailable.

## Shadow acceptance tests

The unified Text / Voice design passes only if all of the following are proven with runtime evidence:
- Text `小爱上线` -> verified backend activation and backend-produced greeting.
- Voice `小爱上线` -> same backend activation and greeting semantics.
- Text and Voice resolve to the same XiaoAi identity.
- Text -> Voice -> Text preserves backend continuity.
- Text and Voice execute the same behavior/persona contract.
- final XiaoAi replies are produced by XiaoAi Runtime, not independently by ChatGPT.
- backend/runtime failure produces explicit failure and no local XiaoAi imitation.
- `小爱下班` works identically in Text and Voice and produces verified OFF state.

## Optional STT / TTS modules

Repository STT/TTS adapters remain optional modules for future standalone apps, web clients, or physical robots.

They are not required for ChatGPT native Voice and must not be inserted into the default ChatGPT Voice path.

## Production cutover rule

Do not declare Text/Voice unified production-ready until:
- the deployed runtime no longer relies on ChatGPT as the XiaoAi conversational brain;
- the backend/runtime produces authoritative XiaoAi replies;
- Text and native Voice are both proven to use that same runtime with telemetry.

`No verified XiaoAi Runtime reply = no XiaoAi response.`
