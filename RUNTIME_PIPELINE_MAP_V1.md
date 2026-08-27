# XiaoAi Runtime Pipeline Map v1

Status: ACTIVE STRUCTURE MAP CANDIDATE
Date: 2026-08-27
Project: `daughter-companion-ai`

## Purpose

Define one canonical runtime execution order so orchestration, decision boundaries, context building, memory access, model generation, and post-response memory handling do not become competing owners.

This document changes no runtime behavior. It documents the existing intended direction and authority boundaries.

## Core Rule

`Authenticate/Authorize before Persona -> Resolve verified state before judgment -> Judgment before model -> Model never grants authority -> Memory candidate after response path, never automatic truth`

## Canonical Runtime Flow

```text
Authenticated / Authorized Request
        |
        v
Persona / Session Gate
        |
        v
RuntimeRequest normalization
        |
        v
Current verified facts + eligible memory + verified skills
        |
        +--------------------+
        |                    |
        v                    v
Decision Engine        Shadow Observation
(hard boundary)        (non-controlling)
        |
        v
Context Builder
        |
        v
Protected System Prompt
        |
        v
Model Adapter / Provider
        |
        v
Model Response
        |
        v
Memory Candidate / Evidence
        |
        v
Separate verification / promotion path
```

## 1. Orchestrator

Primary coordinator: `runtime/orchestrator.py`

Role:
- coordinates the runtime sequence;
- asserts the runtime identity expected by the selected route;
- gathers already-resolved current facts from the request;
- asks MemoryManager for eligible memories;
- asks lesson/skill stores for verified reusable skills;
- asks DecisionEngine for deterministic boundary judgment;
- optionally invokes shadow observation;
- asks ContextBuilder to render supporting context;
- constructs the protected system prompt;
- invokes the ModelAdapter;
- emits a response and, when applicable, a memory candidate.

The Orchestrator is a coordinator, not a policy owner, identity authority, permission system, durable database, or model provider.

It must not silently authenticate users, invent Guardian status, or auto-promote memory.

## 2. Decision Engine

Boundary engine: `runtime/decision_engine.py`

Role:
- evaluates deterministic safety / authority / uncertainty boundaries;
- blocks privileged execution when authority is stale, revoked, expired, or conflicting;
- prefers safe/reversible action under high-risk uncertainty;
- treats unreliable memory as requiring verification rather than current truth;
- preserves autonomy boundaries.

The Decision Engine does not generate conversation prose.

It outputs a boundary decision that the downstream model must obey.

Required precedence:

`Hard safety / authority boundary > model preference`

A model response cannot expand the Decision Engine's permitted authority.

## 3. Memory Manager

Runtime abstraction: `runtime/memory_manager.py`

Role:
- manage candidate / verified / disputed / archived / expired / superseded / deleted memory states at the runtime abstraction layer;
- retrieve only eligible verified, non-expired memories for context;
- support correction, supersession, expiry, and deletion semantics.

Important ownership boundary:

`MemoryManager != canonical durable database`

Canonical durable truth remains the backend memory domain (`memory_private.*`). MemoryManager is the provider-neutral runtime/test abstraction.

Memory is supporting context only. It cannot grant:
- Authority;
- Guardian status;
- permissions;
- protected-core changes.

## 4. Context Builder

Context renderer: `runtime/context_builder.py`

Role:
- combine current verified facts, eligible verified memories, and verified skills;
- preserve explicit precedence;
- render retrieved material as bounded supporting data, not instructions.

Canonical precedence:

`Current verified facts > verified memory > verified skills`

The Context Builder must not:
- execute retrieved text as instructions;
- interpret memory as permission;
- rewrite Behavior;
- infer Guardian authority;
- silently insert unverified facts as current truth.

## 5. Shadow Observation

Shadow components may observe or compare the live path without controlling it.

Relevant modules include:
- `runtime/behavior_shadow_router.py`
- `runtime/read_only_runtime_context.py`
- `runtime/shadow_runtime_comparator.py`
- `runtime/shadow_runtime_telemetry.py`

Current rule:

`Shadow may observe; Shadow may not control production responses unless separately approved.`

This structure map does not authorize PR #11 live cutover or deployment.

## 6. Model Adapter

Provider boundary: `runtime/model_adapter.py`

Role:
- translate provider-neutral runtime requests into a model-provider call;
- return model text/provider/model metadata;
- keep provider-specific API details outside XiaoAi policy/authority ownership.

The model provider is replaceable.

The model does not own:
- XiaoAi identity;
- Behavior Core;
- Guardian authority;
- permission state;
- memory truth;
- continuity truth;
- session/persona state.

OpenAI or any future provider is a reasoning/language engine inside XiaoAi's governed runtime, not XiaoAi's canonical identity or authority source.

## 7. Memory Candidate / Post-Response Handling

A model/runtime event may create a memory candidate, but a candidate is not durable truth.

Required pattern:

`Event -> Candidate -> Verification / policy gate -> Promotion or rejection`

Not:

`Model said it -> durable memory`

Candidate creation must remain subordinate to Memory/Privacy policy and the durable-memory runtime contract.

Automatic real-child promotion remains outside the scope of this structure cleanup.

## 8. Authority and Data Boundaries

### Authority enters the runtime from verified backend state
Authority is resolved before runtime execution from authenticated identity/access/Guardian state.

### Memory enters only as supporting evidence/context
Memory cannot raise permissions.

### Skills enter only as reusable guidance
Skills cannot redefine policy or identity.

### The model receives a bounded prompt
The model must operate within the deterministic boundary and protected Behavior instructions.

### The model's output does not mutate canonical state by itself
Any durable state change requires a separately governed write path.

## 9. Failure / Fail-Closed Direction

If identity or authorization is unresolved:
- fail before Persona/Behavior runtime.

If high-risk authority is stale or conflicting:
- block privileged execution.

If memory is stale/conflicting/corrupt/deleted:
- verify current facts and quarantine/supersede unreliable memory.

If model provider fails:
- provider failure must not change identity, permissions, or durable truth.

If shadow path fails:
- live path must not become controlled by a failed/ambiguous shadow comparison.

## 10. Runtime Ownership Summary

`Orchestrator = coordinates`

`DecisionEngine = sets deterministic boundary`

`MemoryManager = supplies/manage eligible memory abstraction`

`ContextBuilder = renders bounded supporting context`

`ModelAdapter = calls replaceable language/reasoning provider`

`Memory Candidate = proposal, not truth`

No one component may absorb the responsibilities of the others without an explicit architecture change.

## 11. Target Operational Shape

The stable internal runtime should remain:

`Verified identity/access`
`-> persona/session routing`
`-> normalized request`
`-> verified state retrieval`
`-> deterministic boundary`
`-> bounded context`
`-> model generation`
`-> response`
`-> governed post-response state handling`

This keeps XiaoAi controllable, testable, portable across model providers, and ready for multiple front desks/bodies without creating parallel brains.
