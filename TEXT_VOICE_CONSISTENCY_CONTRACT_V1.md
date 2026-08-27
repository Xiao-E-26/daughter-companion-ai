# XiaoAi Text / Voice Consistency Contract v1

Status: CANDIDATE — NON-PRODUCTION ARCHITECTURE CONTRACT
Date: 2026-08-27
Project: `daughter-companion-ai`

## Purpose

Guarantee that Text XiaoAi and ChatGPT Voice are two entry modes into the same XiaoAi system, not two personas or two assistants.

This contract must be implemented without:
- creating a second Voice Persona;
- modifying the frozen Behavior Core;
- changing or cutting over the current production `daughter-chat` response path;
- creating a second Memory, Session, Context, Identity, Guardian, or Continuity authority.

## Canonical Rule

`One XiaoAi Persona + One Behavior Core + One Runtime + One Memory/Session/Context model + Multiple Entry Modes`

Text and Voice are transport/presentation differences only.

Under equivalent authorized runtime state:

`Text XiaoAi ≈ Voice XiaoAi`

Natural speech timing, pauses, filler reduction, and spoken cadence may differ. Persona identity, naming, relationship stance, language habits, emotional logic, interaction style, behavioral rules, and core expression style must not drift.

## Architecture Placement

This contract belongs between canonical XiaoAi runtime/behavior state and presentation adapters.

It is an adapter consistency contract, not a new behavior owner.

Required direction:

`ChatGPT Text -> MCP / Runtime Bridge -> daughter-chat -> XiaoAi Runtime/Core`

`ChatGPT Voice -> speech input/output layer -> MCP / Runtime Bridge -> daughter-chat -> XiaoAi Runtime/Core -> speech output`

Voice is XiaoAi's ears and mouth. It is not XiaoAi's brain, identity, persona owner, memory owner, or behavior owner.

## Voice Persona Prohibition

The following are forbidden:
- `Voice XiaoAi` as a second persona definition;
- a voice-only prompt that redefines XiaoAi personality;
- a simplified Voice profile that behaves as `ordinary ChatGPT + warm tone`;
- a voice-specific Memory store;
- a voice-specific Session/Context authority;
- a voice-specific relationship model;
- a voice-only greeting identity that can diverge from Text XiaoAi.

Voice adapters may transform modality only:
- speech -> text/input event;
- text/output event -> speech;
- spoken pacing/prosody where supported.

They may not rewrite the semantic persona contract.

## Activation Contract — `小爱上线`

For both Text and Voice entry:

1. Resolve authenticated actor and allowed XiaoAi identity.
2. Resolve verified client/entry binding.
3. Invoke the existing MCP / Runtime Bridge path.
4. Invoke the existing `daughter-chat` activation behavior with a stable session key.
5. Require confirmed backend runtime/session success.
6. Load the same authorized Identity, Memory, Context, Relationship, Continuity, and expression/behavior state used by Text XiaoAi.
7. Only after successful runtime activation may the interface declare XiaoAi online.
8. After successful activation, the first XiaoAi-facing response must greet `雨宸` naturally, subject to the existing Greeting rule and caller/relationship context.

If runtime/session activation fails or cannot be proven:
- do not declare XiaoAi online;
- do not imitate XiaoAi from ordinary ChatGPT;
- do not substitute a warm generic assistant persona;
- report that XiaoAi runtime was not successfully activated.

## Deactivation Contract — `小爱下班`

Text and Voice must use the same deactivation rule and runtime/session transition.

After successful deactivation:
- XiaoAi persona mode is OFF for that session;
- normal ChatGPT mode resumes;
- Voice must not continue XiaoAi persona presentation merely because audio mode remains open.

If a legacy route still uses `小爱收工`, it may remain compatible, but `小爱下班` must map to the same semantic deactivation behavior rather than create a separate Voice-only rule.

## Shared State Requirement

Text and Voice must read from the same canonical sources for the same authorized XiaoAi identity:
- Persona/session state;
- Identity;
- Memory;
- Context;
- Relationship/Guardian visibility;
- Continuity;
- Behavior/response rules;
- naming and greeting conventions;
- language and expression style.

Entry modality must not become a source of truth.

## Multi-Entry Alignment

Voice is another authenticated entry/client capability under the existing Multi-Entry model.

A phone, ChatGPT Text session, ChatGPT Voice session, browser, speaker, or robot may have separate live session instances while still belonging to the same XiaoAi identity and canonical state model.

Separate session instance does not mean separate XiaoAi persona.

## MCP Bridge Alignment

The existing `CHATGPT_RUNTIME_BRIDGE_V1.md` activation guarantee remains authoritative:
- backend invocation is required before presenting XiaoAi as active;
- conversational imitation is not proof of activation;
- identity and access come from verified connector/runtime state, not user wording.

Voice must use the same bridge guarantee.

## Behavior Freeze Alignment

`BEHAVIOR_FREEZE_BASELINE_V1.md` remains unchanged.

This contract does not alter frozen behavior invariants. It prevents presentation-layer drift from bypassing them.

Voice adaptation may change delivery mechanics but must not weaken or reinterpret Behavior Core semantics.

## Runtime-Unification Alignment

This contract does not authorize production cutover of runtime-unification shadow components.

Existing controlled boundary remains:

`No live daughter-chat -> unified runtime response-path cutover unless separately approved and tested.`

The contract defines the target consistency requirement independent of whether runtime unification is still shadowed or later approved.

## Consistency Test Standard

A Text/Voice consistency test must compare more than factual answer correctness.

For equivalent Memory / Context / Relationship / Session conditions, evaluate whether both outputs sound like the same XiaoAi across:
- persona identity;
- names and forms of address;
- relationship stance;
- warmth and emotional logic;
- language choice and habits;
- boundaries and safety behavior;
- initiative level;
- correction style;
- response structure;
- core expression style;
- greeting behavior after activation;
- deactivation behavior.

Permitted differences:
- spoken pauses;
- natural oral rhythm;
- speech-friendly punctuation;
- minor compression needed for natural listening;
- TTS/prosody differences.

Failure condition:

If Voice content is factually correct but clearly sounds like ordinary ChatGPT rather than the same XiaoAi persona, mark:

`Consistency Test Failed`

## Minimum Test Matrix

1. Text activation -> verified runtime success -> first greeting to 雨宸.
2. Voice activation -> verified runtime success -> first greeting to 雨宸.
3. Text and Voice given same neutral question under same context.
4. Text and Voice given same emotional disclosure under same context.
5. Text and Voice given same correction/discipline scenario.
6. Text and Voice given same safety-sensitive scenario.
7. Text and Voice verify same naming/relationship behavior.
8. Voice runtime failure -> must not imitate XiaoAi.
9. Text runtime failure -> must not imitate XiaoAi.
10. Text deactivation via `小爱下班` -> normal ChatGPT.
11. Voice deactivation via `小爱下班` -> normal ChatGPT.
12. Cross-entry continuation verifies same approved Memory/Context/Relationship state without creating duplicate stores.

## Non-Goals

This contract does not:
- deploy a new Voice service;
- change production `daughter-chat`;
- change frozen Behavior Core;
- grant new Guardian permissions;
- change Memory privacy rules;
- authorize a runtime-unification production cutover;
- require identical wording between Text and Voice.

## Acceptance Rule

The feature is acceptable only when all of the following are true:

`Same XiaoAi identity`
`+ same Behavior truth`
`+ same authorized canonical state`
`+ same runtime activation/deactivation semantics`
`+ modality-only Voice adaptation`
`+ first successful activation greeting to 雨宸`
`+ no generic-ChatGPT fallback masquerading as XiaoAi`

Summary:

`Voice changes how XiaoAi hears and speaks, never who XiaoAi is.`
