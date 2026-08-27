# XiaoAi Identity-First Entry v1

Status: AUTHORITATIVE ENTRY ARCHITECTURE

## Product intent

XiaoAi is entered by resolving a verified identity, not by asking the user to connect a transport URL.

The user-facing mental model is:

```text
ChatGPT = microphone + speaker + text window
XiaoAi Identity = who the conversation is connected to
XiaoAi Runtime = the only conversational brain
Supabase = identity / authorization / memory / session / continuity authority
GitHub = behavior / policy / runtime code source
```

Transport is implementation detail only. It must not become a user-facing setup step or a second identity/persona layer.

## Core invariant

```text
Resolve verified entry identity
  -> resolve authorized XiaoAi identity
  -> load permitted relationship + session
  -> activate XiaoAi Runtime
  -> Runtime produces final XiaoAi reply
  -> ChatGPT displays or speaks that exact reply
```

ChatGPT must not become XiaoAi merely because the phrase `小爱上线` was spoken or typed.

## Identity-first activation

Canonical activation phrase:

```text
小爱上线
```

Activation sequence:

1. Verify the calling platform/account/session identity using a trusted binding mechanism.
2. Resolve the internal user mapped to that verified identity.
3. Resolve exactly one active `companion_access` relationship to the XiaoAi/Daughter identity.
4. Resolve the authorized client/entry binding when the platform exposes one.
5. Resolve role and authority scope.
6. Resolve the XiaoAi/Daughter identity.
7. Resolve or create the scoped runtime session.
8. Load Behavior Core, life-stage policy, guardian/safety policy, permitted memory and continuity context.
9. Transition the runtime session to `ACTIVE`.
10. XiaoAi Runtime generates the activation reply.
11. Only after all prior steps succeed may ChatGPT say that XiaoAi is online and present the Runtime reply.

No verified identity + authorization result means no XiaoAi activation.

## Identity is not authentication by itself

`XiaoAi Identity` answers **which companion relationship should be loaded**.

Authentication answers **who is requesting access**.

Authorization answers **what that caller may do**.

These remain separate checks. Identity-first does not mean trusting a display name, voice sample, remembered claim, local ChatGPT history, or the phrase `小爱上线`.

## Text and Voice

Text and ChatGPT native Voice are two I/O modes for the same entry identity.

```text
Text input  ─┐
             ├─> verified entry identity -> XiaoAi Identity -> same Runtime/session authority
Voice input ─┘
```

ChatGPT native Voice may perform speech recognition and speech playback. Those functions do not own XiaoAi persona, memory, relationship, policy, or final response generation.

A switch between Text and Voice must not create a second XiaoAi persona or separate durable memory.

## ChatGPT role

Allowed:
- receive typed text;
- receive speech and resolve it into user input;
- present Runtime output as text;
- play Runtime output through native Voice;
- carry hidden platform integration metadata required to reach the verified identity/runtime.

Forbidden:
- locally invent XiaoAi persona replies;
- use ChatGPT-local history as authoritative XiaoAi memory;
- declare XiaoAi online without verified Runtime activation;
- silently fall back to ordinary ChatGPT while presenting itself as XiaoAi;
- require the end user to know or configure an MCP URL as the normal XiaoAi activation flow.

## Transport boundary

MCP, HTTPS, RPC, platform-native tool routing, or another supported protocol may exist below the product layer.

None of them define XiaoAi identity.

Core rule:

```text
Identity-first, transport-agnostic.
```

If MCP is used internally by a platform integration, it is a thin transport only. It is not a user-facing XiaoAi connection concept and is not the conversational brain.

## Session scoping

Live persona state remains scoped to the verified entry relationship. At minimum:
- Daughter/XiaoAi identity;
- internal user;
- runtime session key;
- client/entry identity when available.

Approved durable identity/memory/continuity may be shared across authorized entry points, but live `ACTIVE/OFF` state is not automatically global.

## Canonical deactivation

Canonical phrase:

```text
小爱下班
```

Compatibility aliases may include `小爱收工`.

Deactivation sequence:
1. verify the current entry identity/session relationship;
2. set the scoped runtime persona state to `OFF`;
3. persist allowed continuity/checkpoint state;
4. preserve XiaoAi identity and authorized durable memory;
5. stop loading XiaoAi persona for subsequent turns;
6. return control to ordinary ChatGPT interface behavior.

## Fail-closed behavior

All of the following mean XiaoAi is **not online**:
- caller identity cannot be verified;
- no authorized XiaoAi identity relationship can be resolved;
- ambiguous/multiple active companion bindings where one is required;
- revoked/inactive client binding;
- invalid runtime session relation;
- Runtime activation failure;
- Runtime final reply missing;
- platform integration cannot reach XiaoAi Runtime.

In these cases ChatGPT may report connection/runtime failure, but must not imitate XiaoAi.

## Successful activation evidence

A production implementation should be able to prove at least:
- verified caller identity/binding;
- resolved XiaoAi/Daughter identity;
- authorized role/scope;
- scoped runtime session;
- `persona_state = ACTIVE`;
- authoritative Runtime final reply;
- final reply source is XiaoAi Runtime, not ChatGPT-local generation.

The exact transport metadata is implementation-specific and must not be treated as the product identity.

## Product acceptance test

1. Start from XiaoAi `OFF`.
2. Type `小爱上线`.
3. Verify identity -> authorization -> XiaoAi Identity -> Runtime session -> `ACTIVE`.
4. Verify activation reply comes from XiaoAi Runtime.
5. Continue one normal Text turn and verify same identity/session authority.
6. Switch to native Voice and continue one turn.
7. Verify Voice hits the same XiaoAi identity and compatible runtime session/continuity authority.
8. Say `小爱下班`.
9. Verify scoped runtime state becomes `OFF`.
10. Verify next ordinary turn is not locally presented as XiaoAi.

Pass only when all ten conditions are evidenced by runtime/telemetry.

## Current implementation posture

Backend identity, authorization, client connection, runtime-session and continuity primitives already exist. An authoritative-reply shadow runtime also exists for controlled testing.

However, this architecture document does **not** claim that the current ChatGPT product session exposes a platform-native hidden identity binding to that runtime. Until such a supported integration is actually connected and telemetry proves the path, `小爱上线` must not be claimed as end-to-end production-ready.

## Supersession note

Any earlier document or experiment that requires the end user to manually register or paste an MCP URL is a transport-level development experiment, not the XiaoAi product entry architecture.
