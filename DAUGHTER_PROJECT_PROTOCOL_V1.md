# Daughter Companion AI — Project Protocol v1

Status: ACTIVE PROJECT PROTOCOL
Date: 2026-08-24
Project: `daughter-companion-ai`
Parent core: `Xiao-E-26/xiaoe-core-md`

## Purpose

Define the daughter project's own operating boundary, scope, source-of-truth rules, verification expectations, and project-specific execution behavior without duplicating or overriding XiaoE Core Behavior.

## Inheritance Rule

This project inherits XiaoE Core's frozen Behavior and active Governance.

Authority order:
1. Security, factual truth, and explicit current user instruction
2. XiaoE Core frozen Behavior Logic
3. XiaoE Core Governance / Policy Gate
4. This Daughter Project Protocol
5. Daughter project state / memory / checkpoints
6. Current-chat assumptions

This file MUST NOT redefine or weaken Core rules such as:
- FACT FIRST
- OWNER FIRST
- SCOPE FIRST
- STABLE PATH LOCK
- ONE CHANGE AT A TIME
- RE-VERIFY
- STOP & REASSESS

If this protocol conflicts with Core Behavior or Governance, Core wins.

## Project Identity

`daughter-companion-ai` is an independent daughter project managed with XiaoE Core methods.

It is not XiaoE Core itself.
It does not own or redefine XiaoE identity.
It may use XiaoE capabilities, reasoning, governance, and project-management patterns while keeping its own code, data, configuration, deployment, and project state separate.

## Isolation Boundary

By default this daughter project must remain independent from XiaoE Core and other daughter/business projects.

Do not create hidden shared dependencies across projects.

Unless separately designed and approved:
- no shared service-role secret,
- no shared database ownership,
- no direct writes into XiaoE Core tables,
- no direct writes into another project's business tables,
- no implicit cross-project runtime dependency,
- no copying Core secrets into this repository.

Any future integration with XiaoE Core or another project should cross an explicit, documented boundary such as a scoped API/service contract.

## Current Source of Truth

Current source-of-truth ownership is:
- GitHub repository: project code, architecture, versioned protocol, configuration templates, migration history
- Daughter Supabase backend: persistent identity, access and shared continuity runtime state
- XiaoE Core: behavior, governance, reusable capability definitions and cross-project operating principles
- Business/application runtime: actual live runtime truth once deployed
- Daughter project memory/checkpoints: continuation aid only, never stronger than current verified source/runtime state

Do not treat XiaoE Core memory as transaction truth for this daughter project.

## Current Backend State

Verified dedicated Supabase project:
- project id: `vmegjuceiuplqixizwso`
- project name: `daughter-companion-ai`
- current health: `ACTIVE_HEALTHY`
- verified core tables:
  - `daughter_identities`
  - `companion_access`
  - `shared_continuity_state`

This backend is the daughter project's own runtime/persistence boundary and must remain separate from XiaoE Core and other projects.

Backend existence does not imply that every planned continuity, cross-account, Guardian, memory, or migration feature is fully deployed. Feature-level status must still be verified from the relevant schema, runtime state, implementation contract, and live behavior before claiming completion.

## Bootstrap Rule

When entering this project, first establish:
- active project = `daughter-companion-ai`
- current user objective
- current repository state
- current dedicated backend identity and health
- current deployment/runtime state if any
- verified project state versus remembered/project-planned state
- immediate scope and risk

If a required project dependency or feature does not yet exist, record it as `not configured` or `not verified` rather than assuming one.

## Development Mode

This project remains lean.

Default rules:
- add only structure needed by a verified requirement,
- prefer reversible and independently testable changes,
- keep project-specific logic here rather than pushing it into XiaoE Core,
- promote a lesson back toward Core only when it is genuinely reusable, verified, and approved through Core learning/governance rules,
- avoid premature queue, agent, provider-router, or infrastructure layers.

## Capability Use

The daughter project may use capabilities registered by XiaoE Core, but capability availability is not project permission.

For each meaningful action:
`Project intent -> Task route -> owning capability -> project boundary -> Governance -> executor -> verification`

The daughter project must not:
- use a Core capability to bypass this project's scope,
- assume a connector/tool is available without checking,
- let an executor widen its own permissions,
- treat a successful tool response as sufficient verification when an authoritative read-back exists.

## Mutation Boundary

Before meaningful writes, identify:
- authoritative owner,
- exact target repository/backend/project,
- expected files/tables/functions/config affected,
- protected invariants,
- rollback/recovery path when persistent or high-risk,
- post-change verification method.

A general instruction such as `继续`, `优化`, `升级`, or `开始` may authorize the next already-defined project step, but it does not authorize:
- modifying XiaoE Core Behavior,
- destructive cross-project changes,
- importing secrets,
- production cutover,
- creating paid infrastructure,
- weakening security boundaries.

## Data and Secret Rule

Never commit:
- service-role keys,
- database passwords,
- JWT signing secrets,
- runtime tokens,
- private API keys,
- customer/private business data.

Use environment/secret stores for runtime credentials.

Store only minimum project data needed for the product.

## Backend Rule

The daughter project has its own dedicated Supabase backend.

Backend rules:
- it must retain its own project identity;
- migrations should be versioned in this daughter repository when schema evolution is performed;
- RLS/authorization must be designed from the actual product roles/data model;
- Core migrations must not be blindly copied unless the daughter genuinely requires the same subsystem;
- fresh-project bootstrap should be tested independently before any production-style rollout;
- current live backend state outranks stale planning text or remembered setup state.

## Behavior Customization Boundary

Project-specific behavior is allowed only at the project level.

Examples of valid daughter-specific behavior:
- product tone/persona rules,
- user workflow rules,
- project-specific approval thresholds,
- product feature constraints,
- domain-specific verification requirements.

These belong in daughter project files and must remain subordinate to Core Behavior/Governance.

Do not create a second `XIAOE_BEHAVIOR_LOGIC` inside this repository.

## Completion Rule

A daughter-project task is complete only when:
- intended result exists in the correct project,
- authoritative state has been verified,
- no unrelated Core/other-project state was changed,
- affected stable paths remain intact,
- durable project state is updated only when useful for future continuation.

## Repository State

Current verified state:
- GitHub repository exists: `Xiao-E-26/daughter-companion-ai`
- repository visibility: public
- default branch: `main`
- project repository contains active identity, policy, architecture, scope, and governance files
- dedicated Supabase project exists and is currently healthy
- verified core backend tables include `daughter_identities`, `companion_access`, and `shared_continuity_state`
- XiaoE Core remains separate and is not modified by this protocol

Historical bootstrap note:
- the repository was empty before this protocol was first added.
