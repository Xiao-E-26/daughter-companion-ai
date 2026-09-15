# XiaoAi Document Authority Index v1

Date: 2026-09-16
Status: CANONICAL DOCUMENT AUTHORITY INDEX
Project: `daughter_companion_ai`
Repository: `Xiao-E-26/daughter-companion-ai`

## Purpose

Define one authoritative classification for XiaoAi documentation so older status labels, historical scope files, test artifacts, shadow-mode documents, and implementation maps do not compete with current canonical architecture or policy owners.

This file governs document authority classification only. It does not change XiaoAi behavior, runtime logic, policy semantics, backend state, permissions, or production execution.

## Precedence

When document labels or eras conflict, use this precedence:

1. `XIAOAI_CANONICAL_ARCHITECTURE_V1.md`
2. this `DOCUMENT_AUTHORITY_INDEX_V1.md`
3. current canonical policy owner named by `POLICY_OWNERSHIP_MAP_V1.md`
4. current runtime contract / freeze baseline
5. active implementation maps and contracts
6. reference / historical / shadow / evidence documents

A lower document may specialize an owner only when that specialization is explicitly delegated and does not conflict with the higher owner.

Legacy words such as `ACTIVE`, `CANDIDATE`, `READY`, or `CURRENT` inside an older document do not override this index.

## Canonical Entrypoints

### CANONICAL

- `XIAOAI_CANONICAL_ARCHITECTURE_V1.md` — canonical architectural entrypoint.
- `PROJECT_IDENTITY.md` — canonical identity owner.
- `POLICY_OWNERSHIP_MAP_V1.md` — canonical policy-domain ownership map.
- `FOUR_LAYER_ARCHITECTURE_V1.md` — canonical Identity / Behavior / Judgment / Authority mapping.

## Active Owners / Runtime Contracts

### ACTIVE

- `RUNTIME_BEHAVIOR_DECISION_FLOW_V1.md` — active runtime behavior contract; executes policy and does not own policy.
- `BEHAVIOR_FREEZE_BASELINE_V1.md` — active regression/freeze baseline protecting behavioral invariants.
- `MEMORY_AND_PRIVACY_POLICY_V1.md` — active primary memory/privacy owner.
- `GUARDIAN_AND_AUTONOMY_POLICY_V1.md` — active guardian authority/autonomy owner.
- `GUARDIAN_CONTINUITY_AND_SUCCESSION_POLICY_V1.md` — active succession owner.
- `LIFE_STAGE_POLICY_V1.md` — active life-stage owner.
- `GROWTH_SAFETY_BASELINE_V1.md` — active growth-safety/anti-dependency owner.
- `PORTABLE_IDENTITY_AND_EMBODIMENT_POLICY_V1.md` — active portability/embodiment owner.
- `DAUGHTER_PROJECT_PROTOCOL_V1.md` — active project operating boundary / Xiao-E inheritance protocol.

## Implementation Maps / Contracts

### REFERENCE — IMPLEMENTATION MAP

- `INTERNAL_STRUCTURE_MAP_V1.md`

Classification note:
- It remains useful as an implementation responsibility map.
- Its older header `ACTIVE STRUCTURE MAP CANDIDATE` is superseded by this index.
- It is not a second canonical entrypoint.
- If its implementation-state assumptions conflict with later verified runtime/backend state, current verified state wins.

### REFERENCE — IMPLEMENTATION CONTRACT

Implementation-specific contracts may guide a subsystem but do not become global policy owners unless explicitly assigned by `POLICY_OWNERSHIP_MAP_V1.md`.

Examples include:
- `CROSS_ACCOUNT_VISIBILITY_IMPLEMENTATION_CONTRACT_V1.md`
- `GUARDIAN_AUTHORITY_IMPLEMENTATION_CONTRACT_V1.md`
- `MEMORY_80_20_RUNTIME_CONTRACT_V1.md`
- `TEXT_VOICE_CONSISTENCY_CONTRACT_V1.md`

## Historical Product Scope

### HISTORICAL / REFERENCE BASELINE

- `DAUGHTER_V1_PRODUCT_SCOPE.md`

Classification note:
- This is the original minimum-product scope baseline from 2026-08-24.
- Its older header `ACTIVE PRODUCT SCOPE` is superseded by this index.
- It remains useful for understanding original v1 intent and non-goals.
- It must not override later approved architecture, runtime, memory, continuity, multi-device, adapter, provider, or verification contracts.
- Statements such as text-first, voice-later, limited durable memory, or deferred orchestration describe original v1 scope and are not universal current-system constraints.

## Shadow Documents

### SHADOW ONLY

Any document or component explicitly named `SHADOW`, `SHADOW_MODE`, `SHADOW_STAGING`, or otherwise described as observational/non-controlling is classified SHADOW ONLY unless a later explicit production promotion document states otherwise.

This includes, at minimum:
- `BEHAVIOR_ROUTER_SHADOW_MODE_V1.md`
- `BEHAVIOR_MODE_ROUTER_SHADOW_*`
- runtime shadow comparator / telemetry documentation and evidence.

Rules:
- shadow output may observe, compare, measure, or produce evidence;
- shadow output does not own production behavior;
- shadow output does not silently gain authority over responses, memory, permissions, Guardian logic, or tool execution;
- promotion requires a separate explicit production approval and regression proof.

The older `candidate` label inside `BEHAVIOR_ROUTER_SHADOW_MODE_V1.md` does not mean production authority.

## Evidence / Test / Result Files

### EVIDENCE / HISTORICAL

Files whose primary purpose is tests, regression results, stress results, pilots, reports, closure evidence, or migration verification are evidence, not sources of policy truth.

Examples:
- `*_RESULTS.md`
- `*_TEST*.md`
- `*_STRESS*.md`
- `*_REPORT*.md`
- `*_CLOSURE*.md`
- `pilots/**`
- test/workflow evidence under `.github/workflows/**` and `tests/**`

Evidence may prove whether an implementation satisfied an owner; it does not replace the owner.

## Superseded / Legacy Transport

### HISTORICAL / NON-PRIMARY TRANSPORT

Legacy XiaoAi-specific MCP / runtime bridge material remains historical or adapter-level reference where it still exists.

Current project-management/execution orchestration is owned by Xiao-E outside this repository and must not be redefined by legacy XiaoAi transport documentation.

A transport adapter can connect to XiaoAi; it cannot become XiaoAi identity, policy, memory, authority, or project-governance owner.

## Drift Prevention Rules

When adding or modifying documentation:

1. Start from `XIAOAI_CANONICAL_ARCHITECTURE_V1.md`.
2. Identify the existing canonical owner before creating a new rule.
3. Do not create a second document for an already-owned policy domain.
4. Classify the new file as one of:
   - CANONICAL
   - ACTIVE
   - REFERENCE
   - SHADOW ONLY
   - EVIDENCE
   - HISTORICAL
   - SUPERSEDED
5. A test/result/closure file may prove state but may not silently become a policy owner.
6. A runtime/helper/adapter file may implement policy but may not silently redefine it.
7. Current verified runtime/backend state outranks stale implementation assumptions in reference documents.
8. If ownership is ambiguous, stop and resolve ownership before adding more documentation.

## Current Closure

`ONE CANONICAL ARCHITECTURE ENTRYPOINT = YES`

`DOCUMENT AUTHORITY INDEX = ACTIVE`

`INTERNAL_STRUCTURE_MAP_V1 = REFERENCE IMPLEMENTATION MAP`

`DAUGHTER_V1_PRODUCT_SCOPE = HISTORICAL / REFERENCE BASELINE`

`SHADOW DOCUMENTS = SHADOW ONLY`

`TEST / RESULT / CLOSURE DOCUMENTS = EVIDENCE, NOT POLICY`

`LEGACY TRANSPORT DOCS = NON-PRIMARY / HISTORICAL UNLESS EXPLICITLY PROMOTED`

This classification is intended to reduce model drift without deleting useful historical or implementation context.
