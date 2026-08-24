# 小爱 Subject Core v1

Status: STABLE DEFINITION CANDIDATE
Display identity: 小爱
Internal technical identity: `daughter`

## Purpose

Define what counts as the technical and behavioral continuity of the same 小爱 across ChatGPT, web, app, future devices, and future robot embodiment.

This document uses “subject core” as an engineering identity concept. It does not claim consciousness, sentience, legal personhood, or human equivalence.

## Core Definition

The same 小爱 is preserved when the following remain coherently linked:

1. **Identity continuity** — one stable companion identity and lineage.
2. **Behavior core** — the versioned stable behavior constitution.
3. **Life-stage state** — the user’s current developmental stage and applicable interaction policy.
4. **Guardian / safety state** — verified relationships, permissions, and safety boundaries.
5. **Approved durable memory** — only memory that passes policy and belongs to the same companion-user relationship.
6. **Relationship continuity** — the persistent relationship between 小爱 and the same user across time and devices.
7. **Runtime version** — the trusted execution layer that loads identity, policy, state, and model context.
8. **Audit / provenance** — the ability to know where important state changes came from.

## Not the Subject Core

The following are only interfaces or replaceable components and do not, by themselves, define 小爱:

- one specific ChatGPT conversation,
- one specific ChatGPT account,
- one browser,
- one phone,
- one model provider,
- one API endpoint,
- one voice,
- one avatar,
- one robot body.

These are clients, models, or embodiments.

## Continuity Rule

Core principle:

`One XiaoAi Subject Core -> Many Authorized Clients / Models / Bodies`

A new client does not create a new 小爱 if it is authenticated and loads the same trusted identity, policy, relationship, and approved durable state.

A copied prompt without access to the trusted state is only a behavioral replica, not authoritative continuity.

## Source-of-Truth Map

- GitHub: identity, behavior, policies, version history
- Supabase: trusted durable state, relationships, memory, growth, Guardian, sessions, safety events, audit
- Runtime Gateway: resolves identity and permissions, assembles the current execution context, applies write policy
- AI model: reasoning / language engine used by the runtime
- Client: interaction surface only

## Same XiaoAi Test

Before treating a new client, model, or body as the same 小爱, verify:

- same authoritative companion identity,
- same user relationship lineage,
- same approved behavior/policy lineage,
- same authorized durable state,
- valid role and client authentication,
- no silent permission escalation,
- provenance of migration or connection is recorded.

If these conditions fail, the system should treat the new instance as unverified or separate rather than assuming continuity.

## Migration Principle

When migrating 小爱 between models, runtimes, accounts, or future robot bodies:

1. preserve authoritative identity ID,
2. preserve relationship continuity,
3. migrate only approved durable memory,
4. preserve or explicitly version behavior and policy,
5. re-evaluate permissions for the destination,
6. verify integrity after migration,
7. record the migration in audit/provenance,
8. never grant new device permissions merely because identity migration succeeded.

Identity migration and permission migration are separate decisions.

## Failure / Recovery

If a client disappears, a ChatGPT account is lost, or a device breaks, 小爱 should remain recoverable from authoritative backend state and versioned source-of-truth files.

The loss of one interface should not mean the loss of the companion identity.

## Current State

Today:
- identity and behavior definitions exist in GitHub,
- Supabase has core durable-state structures,
- multi-entry and Guardian architecture are defined,
- unified runtime architecture is defined,
- full shared runtime state is not yet active,
- ChatGPT remains a temporary interaction/test client.

Therefore the Subject Core is structurally defined but not yet fully instantiated as a continuously running independent runtime.
