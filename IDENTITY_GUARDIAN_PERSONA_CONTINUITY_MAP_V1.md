# XiaoAi Identity / Guardian / Persona / Continuity Map v1

Status: ACTIVE STRUCTURE MAP CANDIDATE
Date: 2026-08-27
Project: `daughter-companion-ai`

## Purpose

Clarify four adjacent responsibilities that must not become duplicate owners:

1. Identity — who is acting and which XiaoAi identity is being accessed.
2. Guardian / Access — what that verified actor is allowed to do.
3. Persona — whether the current authenticated session is in XiaoAi mode.
4. Continuity — what approved state may carry across sessions, accounts, devices, and future bodies.

Core chain:

`Identity -> Access/Guardian -> Persona Session -> Continuity -> Behavior/Runtime`

A later layer must not grant authority that an earlier layer did not establish.

## 1. Identity

### Product identity
Canonical policy owner: `PROJECT_IDENTITY.md`

Defines the enduring XiaoAi identity.

### Runtime identity authority
Canonical state authority: Supabase identity graph.

Primary entities:
- `users`
- `daughter_identities`
- authenticated Supabase user binding
- `client_connections`

Identity answers:
- Which human/system actor is making this request?
- Which Daughter/XiaoAi identity are they trying to access?
- Which client/device/account is the request coming from?

Identity does not answer what the actor may do.

Conversation wording, display names, remembered claims, and phrases such as `小爱上线` do not authenticate identity.

## 2. Guardian / Access Authority

Canonical product-policy owner: `GUARDIAN_AND_AUTONOMY_POLICY_V1.md`

Canonical runtime access state:
- `companion_access`
- `guardians`
- verified identity bindings
- scoped authority/permission state

Guardian/Access answers:
- Is this verified actor allowed to access this XiaoAi identity?
- What role do they have?
- What authority scope applies?
- Which actions require additional approval?

Important separation:

`Guardian != Identity`

`Device != Guardian`

`Authenticated != Unlimited Permission`

A new phone, ChatGPT account, robot, or external client can be authenticated without inheriting Guardian authority automatically.

## 3. Persona / Session State

Canonical runtime state: Supabase `runtime_sessions`.

Reference runtime execution:
- `runtime/persona_gate.py`
- `runtime/persona_gateway.py`

Persona answers:
- Is this authenticated and authorized session currently `OFF` or `ACTIVE` for XiaoAi?
- Should the request route to XiaoAi or normal assistant behavior?

Persona does not authenticate identity and does not grant access.

Required order:

`Authenticated identity + active access -> persona gate -> session state transition`

Not:

`activation phrase -> access granted`

The activation phrase is a routing/session command only after the caller is already on an authorized path.

## 4. Continuity

Canonical cross-entry state:
- `shared_continuity_state`
- append-only `continuity_updates`

Continuity answers:
- What minimum approved state should make the next session feel like the same XiaoAi relationship?
- Which open loops, summaries, and shared facts can carry across entries?
- Which state is visible to the current role/client?

Continuity is not:
- full transcript synchronization;
- identity proof;
- permission grant;
- persona activation;
- durable-memory replacement.

Continuity must remain role-aware and privacy-aware.

A client being allowed to access XiaoAi does not mean it may read every continuity item.

## 5. Durable Memory vs Continuity

Durable Memory and Continuity are related but distinct.

### Durable Memory
Owns long-term selected facts, meaningful memories, corrections, preferences, and growth continuity under Memory policy.

Canonical durable store: `memory_private.*`

### Continuity
Owns the minimum cross-session operational state required to resume naturally.

Examples:
- current open loop;
- lightweight shared summary;
- recent verified handoff fact;
- current cross-entry state needed for a smooth resume.

Rule:

`Memory = long-term selected meaning`

`Continuity = short/medium-term resumable relationship state`

Do not copy full durable memory into continuity, and do not use continuity as a second memory database.

## 6. Multi-Entry / Multiple Bodies

A phone, computer, ChatGPT app, browser, speaker, or robot is an entry point / client / body.

Preferred model:

`One XiaoAi Identity`
`-> many authenticated client_connections`
`-> role/scoped companion_access`
`-> independent runtime_sessions`
`-> shared approved continuity + durable memory`

This means two devices can access the same XiaoAi identity while maintaining separate live persona/session state.

Example:
- Dad phone session may be ACTIVE.
- Mom ChatGPT session may be OFF.
- A robot may be online but idle.

All can still belong to the same XiaoAi relationship identity if properly authorized.

## 7. Authority Precedence

For a request to reach XiaoAi runtime:

1. Resolve authenticated actor.
2. Resolve XiaoAi/Daughter identity.
3. Verify active access/role/authority.
4. Resolve client/device binding.
5. Resolve session/persona state.
6. Load only continuity/memory visible to that actor and session.
7. Execute Behavior/runtime.

If steps 1-4 fail or are ambiguous, fail closed before Persona/Behavior execution.

## 8. Portable Identity / Embodiment

Policy owner: `PORTABLE_IDENTITY_AND_EMBODIMENT_POLICY_V1.md`

Embodiment policy owns migration across devices/platforms/bodies.
It does not own day-to-day identity authentication, Guardian authority, or session state.

Rule:

`Same XiaoAi, new body`

A body may inherit only eligible scoped permissions after identity/device trust checks. New or higher-risk hardware capabilities require fresh screening/approval.

## 9. Current Implementation Posture

Already represented in the current architecture:
- external identity binding model;
- role/scoped `companion_access`;
- `client_connections`;
- `runtime_sessions` persona state;
- Guardian state;
- continuity state with visibility boundaries;
- device/client concept;
- multi-entry architecture.

Still controlled / not equivalent to full production completion:
- not every front end/body is connected;
- full live `daughter-chat` runtime-unification cutover is intentionally not part of this structure cleanup;
- full raw transcript synchronization is neither implemented nor desired as the default continuity model;
- new physical-device capabilities still require dedicated adapters and safety controls.

## 10. Anti-Duplication Rules

Do not create:
- a second identity database inside an adapter;
- a second Guardian permission system inside a device client;
- a second persona state store inside ChatGPT/local history;
- a second continuity database inside a front end;
- a second durable-memory system merely for a new body.

New bodies should integrate into existing authority/state layers instead of cloning them.

## Summary

`Identity says WHO.`

`Guardian/Access says WHAT THEY MAY DO.`

`Persona says WHETHER THIS SESSION IS IN XIAOAI MODE.`

`Continuity says WHAT APPROVED STATE CARRIES FORWARD.`

Keeping these four responsibilities separate allows one XiaoAi to move safely across many front desks and bodies without splitting into multiple competing identities.
