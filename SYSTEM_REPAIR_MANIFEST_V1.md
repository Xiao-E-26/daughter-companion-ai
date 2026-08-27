# XiaoAi System Repair Manifest v1

Status: MERGED BASELINE / ACTIVE REFERENCE
Date: 2026-08-27
Merged through: PR #10 into `main`

## Non-negotiable constraint

Behavior Logic is frozen. The following paths remain protected by CI and must not be changed as part of internal-structure cleanup:

- `core/XIAOAI_BEHAVIOR_CORE_V1.md`
- `BEHAVIOR_FREEZE_BASELINE_V1.md`
- `BEHAVIOR_MODE_ROUTER_V1.md`
- `runtime/behavior_mode_router.py`

## Capability preservation rule

Internal cleanup may remove duplication, narrow unsafe exposure, add constraints, add indexes, add atomic primitives, and clarify source-of-truth ownership. It must not remove XiaoAi capabilities.

## Canonical responsibility map

For the current top-level internal map, see `INTERNAL_STRUCTURE_MAP_V1.md`.

### Behavior
- Canonical owner: Frozen Behavior Core + Behavior Router contract.
- Runtime code may execute these rules but must not silently redefine them.

### Identity / Access
- Canonical runtime authority: Supabase `users`, `daughter_identities`, `companion_access`, `client_connections`, `guardians`.
- Chat wording never grants identity or authority.

### Runtime session / persona
- Canonical state: Supabase `runtime_sessions`.
- Activation remains explicit; OFF does not auto-promote to ACTIVE.

### Durable memory
- Primary policy owner: `MEMORY_AND_PRIVACY_POLICY_V1.md`.
- Durable-memory specialization: `DURABLE_MEMORY_POLICY_V1.md`.
- Runtime 80/20 execution contract: `MEMORY_80_20_RUNTIME_CONTRACT_V1.md`.
- Canonical durable/private memory domain: `memory_private.*`.
- `public.memories` remains a compatibility/runtime-facing memory surface and must not override private canonical revision/tombstone semantics.
- GitHub `MemoryManager` remains provider-neutral runtime abstraction and test contract, not the database source of truth.

### Continuity
- Canonical cross-entry state: `shared_continuity_state` + append-only `continuity_updates` provenance.
- Visibility must be role-aware: shared_runtime / guardian_only / child_only / system_only.

### Guardian linking
- Canonical authority comes from verified Supabase Auth identity + one-time hashed invite + database state.
- `claim_xiaoai_guardian_link_atomic` is the target atomic claim primitive.
- Existing Edge Function remains live until an explicit tested cutover.

### Model provider
- Model provider is replaceable and does not own Behavior, Authority, Guardian, Memory truth, or Identity.

## Applied structural repairs

1. Memory expiry handling in GitHub runtime hardening.
2. Retrieved context marked as non-authority / non-instruction supporting data.
3. Golden CI coverage expanded to runtime/test conversation paths.
4. Cross-account continuity state has explicit visibility.
5. Continuity SELECT policy is role-aware.
6. Hot foreign-key lookup indexes added.
7. Repeated `auth.uid()` RLS calls optimized without changing access semantics.
8. `get_companion_preferred_name()` remains available only to authenticated/service_role and retains its internal access check.
9. Service-role-only atomic Guardian claim primitive added.
10. Behavior Logic freeze CI added.

## Verified current-data health at repair completion

The following checks returned zero issues:

- duplicate runtime session keys;
- active companion access missing `verified_at`;
- expired Guardian invites still pending;
- active clients missing `linked_at`;
- active expired public memories;
- runtime/client user-daughter scope mismatch.

## Explicitly not changed by this repair

- Frozen Behavior Core;
- Behavior Freeze Baseline;
- Behavior Router contract;
- Behavior Router runtime semantics;
- child-facing capabilities;
- current Mother Guardian live binding;
- current `daughter-chat` production behavior;
- current device-chat custom token model.

## Remaining controlled cutovers

These remain separate future work and require regression evidence plus explicit approval before activation:

1. Switch `xiaoai-guardian-link` POST mutation path to `claim_xiaoai_guardian_link_atomic`.
2. Introduce/activate Signal Generator only under controlled Shadow validation.
3. Add durable Shadow telemetry transport.
4. Unify `daughter-chat` with the canonical runtime boundary incrementally, without changing Behavior Logic.
5. Decide and document compatibility lifecycle for `public.memories` versus `memory_private.*`.

## Current rule

This manifest is now a historical/active baseline reference, not an open merge candidate. Any new work should start from current `main` and use a separate branch/PR.
