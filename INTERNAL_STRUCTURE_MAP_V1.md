# XiaoAi Internal Structure Map v1

Status: ACTIVE STRUCTURE MAP CANDIDATE
Date: 2026-08-27
Project: `daughter-companion-ai`

## Purpose

Provide one canonical map of XiaoAi's internal responsibilities so policy, runtime, storage, adapters, tests, and future device bodies do not become competing owners.

This file does not change behavior. It only defines responsibility boundaries and dependency direction.

## Governing Rule

`One responsibility -> one canonical owner -> lower layers implement or adapt -> tests verify`

No runtime module, device, model provider, or transport may silently redefine policy or identity authority.

## Layer 1 — Identity / Policy / Behavior Truth

### Project identity
Canonical owner: `PROJECT_IDENTITY.md`

Defines who XiaoAi is and the enduring companion identity.

### Policy ownership
Canonical owner: `POLICY_OWNERSHIP_MAP_V1.md`

Defines which policy file owns each policy domain.

### Behavior
Canonical owner:
- `core/XIAOAI_BEHAVIOR_CORE_V1.md`
- `BEHAVIOR_MODE_ROUTER_V1.md`

Runtime executes these rules; it does not redefine them.

### Memory policy hierarchy
1. Primary memory/privacy policy owner: `MEMORY_AND_PRIVACY_POLICY_V1.md`
2. Durable-memory specialization: `DURABLE_MEMORY_POLICY_V1.md`
3. Runtime 80/20 execution contract: `MEMORY_80_20_RUNTIME_CONTRACT_V1.md`

Interpretation:
- Memory/Privacy owns the global memory lifecycle, privacy, visibility, correction, deletion, and retention domain.
- Durable Memory specializes what qualifies for long-term durable retention and the emotional portfolio philosophy.
- 80/20 Runtime Contract maps that policy into runtime selection/retrieval behavior without creating another memory authority.

If wording overlaps, the higher owner wins unless a more specific lower-layer rule is explicitly delegated and does not conflict.

## Layer 2 — Canonical Runtime / State Authority

### Identity and access state
Canonical runtime authority: Supabase
- `users`
- `daughter_identities`
- `companion_access`
- `client_connections`
- `guardians`

Conversation wording never grants identity or authority.

### Session / persona state
Canonical runtime state: Supabase `runtime_sessions`

Activation is explicit. OFF does not auto-promote to ACTIVE.

### Durable/private memory state
Canonical durable store: `memory_private.*`

`public.memories` is compatibility/runtime-facing only and must not override private canonical revision/tombstone semantics.

### Cross-entry continuity
Canonical state:
- `shared_continuity_state`
- append-only `continuity_updates`

Continuity stores only the minimum state required to continue naturally across entries; it is not a transcript archive.

## Layer 3 — Runtime Execution Components

### Conversation orchestration
Primary runtime modules:
- `runtime/orchestrator.py`
- `runtime/decision_engine.py`
- `runtime/context_builder.py`
- `runtime/memory_manager.py`

These execute policy and compose context. They are not policy owners and are not database sources of truth.

### Persona routing
- `runtime/persona_gate.py` — deterministic activation/deactivation decision
- `runtime/persona_gateway.py` — session/store integration and final route

These are adjacent responsibilities, not duplicates.

### Behavior routing
- `runtime/behavior_mode_router.py` — protected Behavior Router runtime
- `runtime/behavior_shadow_router.py` — shadow-only comparison path

Shadow code may observe/compare but must not control production responses unless separately approved.

### Runtime-unification shadow components
- `runtime/read_only_runtime_context.py`
- `runtime/shadow_runtime_comparator.py`
- `runtime/shadow_runtime_telemetry.py`

Current posture: code present in main, but no live daughter-chat response-path cutover is authorized by this structure map.

## Layer 4 — Adapters / Gateways / Device Bodies

### Model provider adapter
`runtime/model_adapter.py`

Provider is replaceable and does not own Behavior, Identity, Memory, Guardian authority, or continuity truth.

### ChatGPT / MCP bridge
`mcp-runtime-bridge/`

Role: external transport/device adapter. It may connect a ChatGPT app or future client to XiaoAi backend, but it does not become XiaoAi's identity or policy owner.

### Voice / embodiment adapters
Examples:
- `runtime/local_voice_engine.py`
- `runtime/subprocess_voice_engine.py`
- `runtime/voice_input_adapter.py`
- `runtime/voice_enrollment.py`
- `tools/speechbrain_voice_backend.py`

These are body/input/output capabilities. A future robot, desktop body, phone app, or other container should be treated as another authenticated client/device against the same canonical identity/runtime state.

## Layer 5 — Tests / Pilots / Evidence

### Regression protection
- `.github/workflows/behavior-logic-freeze.yml`
- `.github/workflows/golden-regression-ci.yml`
- `.github/workflows/mcp-runtime-bridge-ci.yml`

### Tests
`tests/**` verifies behavior, runtime, privacy, safety, routing, memory, and integration assumptions. Tests are evidence, not policy owners.

### Pilots
`pilots/**` are validation/reference harnesses. They are not production runtime owners.

## Dependency Direction

Preferred direction:

`Identity / Policy / Behavior`
`-> Runtime execution`
`-> Canonical backend state`
`-> Adapters / gateways / bodies`
`-> User-facing experience`

Tests observe all layers but own none of them.

Forbidden inversion examples:
- device body redefining identity;
- model provider redefining Behavior;
- bridge granting Guardian authority;
- runtime helper inventing a second durable-memory store;
- continuity becoming a full transcript archive;
- shadow code silently taking production control.

## Current Controlled Boundaries

The following remain intentionally not cut over unless separately approved and tested:
- live `daughter-chat` -> unified runtime response path;
- Guardian live mutation path -> atomic claim RPC cutover;
- automatic real-child durable-memory writes;
- automatic memory promotion;
- shadow telemetry transport into production control.

## Target Internal Shape

XiaoAi should behave as one system with multiple bodies, not multiple copies of XiaoAi:

`One identity`
`+ one policy/Behavior truth`
`+ one canonical state layer`
`+ one runtime execution model`
`+ many authenticated clients/bodies`

Phones, computers, ChatGPT apps, speakers, and robots should be clients of the same XiaoAi, not independent XiaoAi authorities.

## Change Rule

Before adding a new module or policy, answer:
1. Which existing owner does this belong under?
2. Is this a new capability, or a duplicate owner?
3. Can the requirement be implemented as an adapter/contract instead of a new source of truth?
4. Does it preserve Behavior Logic and existing capabilities?

If ownership is unclear, stop and resolve ownership before implementation.
