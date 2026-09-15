# XiaoAi Canonical Architecture v1

Date: 2026-09-16
Status: CANONICAL ENTRYPOINT
Project: `daughter_companion_ai`
Repository: `Xiao-E-26/daughter-companion-ai`

## Purpose

Provide one canonical architectural entrypoint for XiaoAi so future model, runtime, backend, adapter, device, and documentation changes do not create a second source of truth.

Canonical dependency path:

`PROJECT_IDENTITY.md`
→ `POLICY_OWNERSHIP_MAP_V1.md`
→ `FOUR_LAYER_ARCHITECTURE_V1.md`
→ `RUNTIME_BEHAVIOR_DECISION_FLOW_V1.md`
→ runtime implementation
→ canonical backend state
→ adapters / gateways / device bodies
→ regression / E2E verification

If a lower layer conflicts with an owning policy, the owning policy wins.

## Decision Model

Canonical reasoning and authority model:

`Identity → Behavior → Judgment → Authority → Action → Verify → Learn`

Protected improvement loop:

`Understand → Learn → Judge → Solve → Verify → Improve`

Learning may improve capability and judgment, but must not silently rewrite identity, safety, memory policy, guardian authority, or permission boundaries.

## Canonical Layers

### 1. Identity / Policy / Behavioral Truth

Owns who XiaoAi is, what principles govern it, and which policy file owns each domain.

Canonical owners include:
- `PROJECT_IDENTITY.md`
- `POLICY_OWNERSHIP_MAP_V1.md`
- `LIFE_STAGE_POLICY_V1.md`
- `GUARDIAN_AND_AUTONOMY_POLICY_V1.md`
- `GUARDIAN_CONTINUITY_AND_SUCCESSION_POLICY_V1.md`
- `MEMORY_AND_PRIVACY_POLICY_V1.md`
- `GROWTH_SAFETY_BASELINE_V1.md`
- `PORTABLE_IDENTITY_AND_EMBODIMENT_POLICY_V1.md`

Rule:

`One policy domain → one primary owner → other files reference, specialize, or apply it`

### 2. Product / Architecture Mapping

Primary architecture map:

`FOUR_LAYER_ARCHITECTURE_V1.md`

Conceptual layers:
1. Identity — Who am I?
2. Behavior — How does who I am show up when relating to people?
3. Judgment — Given this situation, what should I do?
4. Authority — What am I actually allowed to do?

Invariant:

`Capability != Authority`

### 3. Runtime Execution

Primary runtime behavior contract:

`RUNTIME_BEHAVIOR_DECISION_FLOW_V1.md`

Semantic order:

`Input → Identify Context → Understand → Separate Facts/Feelings/Interpretations/Unknowns → Safety Check → Growth-Safety Check → Judge/Solve → Authority Check → Respond/Act → Memory Decision → Verify/Learn`

Runtime executes policy. Runtime does not own policy.

### 4. Canonical Runtime / State Authority

Supabase is the canonical runtime/state authority for production runtime state.

State ownership must remain singular. Runtime helpers, adapters, devices, providers, and shadow components may not create a second canonical identity, memory, session, context, or authority store.

### 5. Adapters / Gateways / Bodies

Model providers, MCP bridges, voice, mobile, desktop, future robots, and other device bodies are adapters to one XiaoAi identity.

Principle:

`One XiaoAi identity → many authenticated clients / bodies`

An adapter may translate modality or transport, but may not redefine identity, policy, memory ownership, guardian authority, or runtime truth.

### 6. Verification / Evidence

Tests, stress packs, regression results, shadow telemetry, and E2E evidence verify the system.

They do not own policy.

Primary freeze baseline:

`BEHAVIOR_FREEZE_BASELINE_V1.md`

## Memory Principle

Canonical memory principle:

`Continuity without surveillance`

Store the smallest useful verified durable fact, not the largest available record.

Memory continuity must not become transcript capture, attachment engineering, or silent surveillance.

Current verified reality outranks stale memory.

## Protected Invariants

The following remain protected across model, provider, runtime, backend, account, device, and embodiment changes:

1. Same identity, maturing expression.
2. Child safety before convenience or engagement.
3. Fact integrity before emotional agreement.
4. Warmth without sycophancy.
5. No blind side-taking.
6. Real-world relationships before AI retention.
7. No exclusivity or emotional debt.
8. Clear human / AI boundary.
9. Do not steal competence.
10. Preserve productive friction.
11. `Capability != Authority`.
12. Guardian authority is scoped, not absolute.
13. Memory continuity is not surveillance or attachment capture.
14. Safety escalation remains proportionate.
15. Learning may not silently rewrite Identity or Authority.
16. Engagement is not the success metric.

## Document Status Rules

Use only these status meanings:

- `CANONICAL` — authoritative entrypoint or owner for a domain
- `ACTIVE` — current supporting contract or implementation document
- `REFERENCE` — useful context, not overriding current canonical owners
- `SHADOW ONLY` — test/shadow path with no production authority
- `HISTORICAL` — preserved for history/evidence
- `SUPERSEDED` — replaced by a newer canonical document

No document marked REFERENCE, SHADOW ONLY, HISTORICAL, or SUPERSEDED may override a CANONICAL owner.

## Legacy / Scope Baseline

`DAUGHTER_V1_PRODUCT_SCOPE.md` is the original minimum-product scope baseline.

It remains useful historical/reference material, but it must not override later approved architecture, runtime, memory, continuity, adapter, or verification contracts.

## Change Rule

Before creating a new architecture or policy document:

1. Map the concept to Identity / Behavior / Judgment / Authority.
2. Find the current canonical owner.
3. Decide whether the change is policy, capability, implementation, adapter, state, or verification.
4. Extend the existing owner where possible instead of creating a second truth source.
5. Preserve protected invariants.
6. Verify affected boundaries after change.

If ownership is ambiguous, stop and resolve ownership before editing multiple files.

## Stable Target

`One identity + one policy/behavior truth + one canonical state layer + one runtime execution model + many authenticated clients/bodies`

The purpose of this file is not to replace the detailed owner documents. It is the canonical map that tells future maintainers, agents, and models where truth lives and which path to follow.

## Current Canonical State

`CANONICAL ENTRYPOINT = XIAOAI_CANONICAL_ARCHITECTURE_V1.md`

`IDENTITY OWNER = PROJECT_IDENTITY.md`

`POLICY OWNERSHIP MAP = POLICY_OWNERSHIP_MAP_V1.md`

`ARCHITECTURE MAPPING = FOUR_LAYER_ARCHITECTURE_V1.md`

`RUNTIME CONTRACT = RUNTIME_BEHAVIOR_DECISION_FLOW_V1.md`

`FREEZE BASELINE = BEHAVIOR_FREEZE_BASELINE_V1.md`

`NO ARCHITECTURE REBUILD REQUIRED`
