# XiaoAi Checkpoint — Duplicate Responsibility Audit

Status: COMPLETED / INCORPORATED INTO INTERNAL STRUCTURE CLEANUP
Date: 2026-08-27
Project: `Xiao-E-26/daughter-companion-ai`

## Objective

Audit XiaoAi for duplicate responsibility across modules, policies, contracts, runtime components, and documentation—not merely identical copied code.

## Final Findings

### 1. No obvious accidental duplicate runtime implementation

No clear case was found where the same live responsibility had been accidentally copied into two active Python runtime modules.

### 2. Persona modules are adjacent, not duplicate

- `runtime/persona_gate.py` owns deterministic activation/deactivation decisions.
- `runtime/persona_gateway.py` owns session/store integration and final runtime route.

### 3. Lesson stores are reference vs persistent implementations

- `runtime/lesson_store.py` is an in-memory/reference implementation.
- `runtime/persistent_lesson_store.py` is a SQLite-backed persistent/versioned implementation.

These overlap in domain but do not currently represent accidental duplicate ownership.

### 4. Main duplication risk is policy/document ownership drift

Memory is the clearest example. Multiple files discuss classification, retention, visibility, 80/20, and durable memory. The correct hierarchy is now explicitly defined as:

1. `MEMORY_AND_PRIVACY_POLICY_V1.md` — primary memory/privacy policy owner.
2. `DURABLE_MEMORY_POLICY_V1.md` — durable-memory specialization under the primary owner.
3. `MEMORY_80_20_RUNTIME_CONTRACT_V1.md` — runtime execution contract implementing the durable-memory philosophy.

This follows `POLICY_OWNERSHIP_MAP_V1.md` and is recorded in `INTERNAL_STRUCTURE_MAP_V1.md`.

### 5. Identity / access / runtime state ownership is already separable

- Project identity/purpose: `PROJECT_IDENTITY.md`
- Policy ownership: `POLICY_OWNERSHIP_MAP_V1.md`
- Runtime identity/access authority: Supabase identity/access graph
- Session/persona state: Supabase `runtime_sessions`
- Durable/private memory: `memory_private.*`
- Cross-entry continuity: `shared_continuity_state` + `continuity_updates`

### 6. Behavior remains frozen and singular

Canonical Behavior ownership remains:
- `core/XIAOAI_BEHAVIOR_CORE_V1.md`
- `BEHAVIOR_MODE_ROUTER_V1.md`

Runtime executes these rules. It must not silently redefine them.

### 7. MCP and device/voice components are adapters, not XiaoAi owners

`mcp-runtime-bridge/`, voice engines, future robot bodies, phone clients, and other containers are entry/output adapters against the same canonical XiaoAi identity/runtime state. They must not create independent identity, Behavior, Memory, or Guardian authority.

## Cleanup Result

No production/runtime code was deleted as part of this audit because no file was proven to be capability-free dead code.

The primary corrective action is responsibility clarification, not code removal.

## Canonical Follow-On Reference

Use `INTERNAL_STRUCTURE_MAP_V1.md` as the current top-level internal responsibility map.

## Constraints Preserved

- Behavior Logic unchanged.
- PR #11 live runtime-unification cutover remains untouched.
- No production Edge Function deployment or cutover.
- No Memory/Identity/Permission semantics removed.
- No XiaoAi capability removed.

## Current State

`COMPLETED — DUPLICATE RESPONSIBILITY AUDIT CLOSED; INTERNAL STRUCTURE MAP IS THE CONTINUATION POINT`
