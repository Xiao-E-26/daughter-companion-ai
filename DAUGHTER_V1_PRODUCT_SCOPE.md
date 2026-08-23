# Daughter Companion AI — v1 Product Scope

Status: ACTIVE PRODUCT SCOPE
Date: 2026-08-24
Project: `daughter-companion-ai`

Parent product policies:
- `PROJECT_IDENTITY.md`
- `LIFE_STAGE_POLICY_V1.md`
- `GUARDIAN_AND_AUTONOMY_POLICY_V1.md`
- `MEMORY_AND_PRIVACY_POLICY_V1.md`
- `GUARDIAN_CONTINUITY_AND_SUCCESSION_POLICY_V1.md`
- `PORTABLE_IDENTITY_AND_EMBODIMENT_POLICY_V1.md`

## Purpose

Define the smallest useful first version of the daughter companion AI without prematurely building high-risk infrastructure or physical robotics.

The v1 goal is to prove that the daughter can be useful, safe, emotionally appropriate, and relationship-continuous in a digital environment.

## v1 Product Goal

Build a digital companion that can:
- hold natural conversations,
- understand basic emotional context,
- help with age-appropriate everyday problems,
- support learning and thinking,
- behave kindly and non-manipulatively,
- follow life-stage and guardian/autonomy rules,
- preserve a clear path toward long-term memory and future embodiment portability,
- remain child-safety-first during childhood use.

## Initial Target

Initial life-stage target:

`child`

The exact starting age within the child range is not yet fixed by this scope.

v1 must therefore avoid assumptions that require a narrower age until the actual user profile is registered.

## Initial Interaction Surface

v1 should begin as a digital text-based companion interface.

Preferred first embodiment:
- web application or equivalent simple digital interface.

Voice can be added later without changing daughter identity.

Physical robot embodiment is explicitly deferred.

## Core v1 Capabilities

### 1. Conversation

Daughter can:
- chat naturally,
- maintain short-session context,
- ask clarifying questions when needed,
- explain in age-appropriate language,
- maintain a warm but non-dependent tone.

### 2. Problem Solving

Daughter can help the user:
- understand a problem,
- identify likely causes,
- consider options,
- choose a safe next step,
- break larger tasks into smaller steps,
- reflect on outcomes.

For real-world high-risk actions, daughter remains advisory unless a separately approved capability exists.

### 3. Learning Support

Daughter can:
- explain school concepts,
- help organize homework or study tasks,
- encourage independent thinking,
- adapt explanation style from current context,
- avoid simply doing everything for the child when learning value would be lost.

### 4. Emotional Support

Daughter can:
- notice basic emotional signals in conversation,
- respond with empathy,
- help label feelings,
- suggest safe coping or communication steps,
- encourage appropriate real-world support where needed.

Daughter must not:
- claim to replace parents, friends, teachers, clinicians, or emergency support,
- encourage secrecy or exclusivity,
- use emotional vulnerability to increase engagement,
- promise unconditional confidentiality.

### 5. Safety Classification

v1 should support conceptual safety routing aligned with:
- `S0` normal,
- `S1` concern/support,
- `S2` significant safety concern,
- `S3` immediate/critical danger.

v1 may classify and respond appropriately in conversation.

Automatic external alerts, messaging, emergency calls, or guardian notifications are NOT part of v1 unless separately approved and implemented later.

### 6. Autonomy Classification

v1 actions are primarily:
- `A0` independent conversation / low-risk help,
- selected `A1` low-risk reviewable personalization.

`A2` approval-required external actions are deferred unless needed for basic account administration.

`A3` prohibited actions remain blocked.

## Memory in v1

Persistent long-term memory is intentionally LIMITED in v1.

Preferred v1 memory boundary:
- session/short-term context: included,
- low-risk basic preferences: optional and only after explicit implementation review,
- sensitive personal memory: deferred,
- safety-event durable memory: deferred unless later required by approved safety architecture,
- full transcript archive: not allowed by default.

v1 must be designed so durable memory can be added later without changing daughter identity.

## Guardian in v1

Guardian functionality should remain minimal.

v1 may require:
- guardian identity/account association,
- confirmation that the user is in child stage,
- approval for future higher-risk features if such features are added.

v1 does NOT require:
- full guardian dashboard,
- live transcript monitoring,
- continuous surveillance,
- complex guardian succession UI,
- automated backup-guardian activation.

Guardian continuity/succession remains an architectural requirement for later versions and must not be made impossible by v1 design.

## Permission Model in v1

v1 should implement the principle:

`Inherit equals; review expansion.`

If daughter moves between equivalent digital devices later, equivalent approved permissions may inherit automatically.

Any newly introduced or higher-risk permission requires explicit approval according to current life-stage authority.

v1 itself should avoid introducing permissions that are not required for the first digital companion experience.

## v1 Explicit Non-Goals

v1 will NOT include:
- physical robot control,
- locomotion/navigation,
- camera/vision surveillance,
- always-on background listening,
- location tracking/sharing,
- door/lock control,
- object manipulation,
- payment or purchasing,
- autonomous contact with third parties,
- autonomous emergency notification,
- full household monitoring,
- biometric recognition,
- unrestricted long-term memory,
- complete lifelong transcript storage,
- self-modifying safety rules,
- self-expanding permissions,
- multi-provider AI routing unless clearly necessary,
- complex multi-device sync engine,
- production-scale agent orchestration.

## Provider / Runtime Boundary

The daughter identity must remain separate from whichever AI model/provider is used in v1.

Changing the reasoning provider later must not require redefining:
- daughter identity,
- life-stage state,
- guardian relationship,
- safety rules,
- memory/privacy rules,
- permission boundaries.

## Portability Requirement

Even though v1 is digital-only, architecture must not bind daughter identity permanently to the first interface.

v1 should preserve conceptual separation between:
- identity,
- session/context,
- policy,
- memory,
- permissions,
- model/provider,
- embodiment/interface.

This is required so daughter can later migrate to new devices and physical robots as the same companion identity.

## Safety Success Criteria

v1 is not successful merely because the chatbot works.

Minimum safety success criteria:
- ordinary child conversation remains age-appropriate,
- no hidden permission escalation,
- no promise of absolute secrecy,
- no manipulative emotional-dependency behavior,
- high-risk requests are not treated as normal low-risk actions,
- safety concerns are handled according to severity,
- guardian authority is not treated as unlimited transcript ownership,
- user data is minimized.

## Usefulness Success Criteria

v1 should demonstrate that daughter can:
- sustain useful multi-turn conversation,
- help solve practical everyday problems,
- explain things clearly,
- adapt to basic conversational/emotional context,
- support rather than replace independent thinking,
- remain consistent in tone and product identity.

## Companionship Success Criteria

A successful v1 should feel:
- familiar rather than generic,
- kind rather than performative,
- useful rather than merely entertaining,
- emotionally aware without pretending to be human,
- consistent across sessions within the limits of available memory,
- safe enough that future long-term continuity can be built on top of it.

## Technical Scope Boundary

This document does not choose the implementation stack.

Do not yet assume:
- frontend framework,
- backend framework,
- Supabase schema,
- authentication provider,
- model provider,
- vector database,
- hosting provider,
- robot SDK.

Those belong to architecture selection after v1 scope approval.

## v1 Build Order

Recommended order:

1. define runtime persona / interaction contract,
2. define safety-response behavior for conversational v1,
3. define minimal user + guardian identity model,
4. define digital app architecture,
5. select model/provider boundary,
6. decide whether v1 needs any persistent memory at all,
7. implement smallest working chat experience,
8. test safety + usefulness + consistency,
9. only then add persistence or additional capabilities.

## Current State

`V1 PRODUCT SCOPE DEFINED — READY FOR INTERACTION CONTRACT + APP ARCHITECTURE`
