# XiaoAi System Repair Manifest v1

Status: REPAIR CANDIDATE
Date: 2026-08-27
Branch: `xiaoai-full-repair-v1`

## Non-negotiable constraint

Behavior Logic is frozen for this repair. The following paths are protected by CI and must not change in this branch:

- `core/XIAOAI_BEHAVIOR_CORE_V1.md`
- `BEHAVIOR_FREEZE_BASELINE_V1.md`
- `BEHAVIOR_MODE_ROUTER_V1.md`
- `runtime/behavior_mode_router.py`

## Capability preservation rule

The repair may remove duplication, narrow unsafe exposure, add constraints, add indexes, add atomic primitives, and clarify source-of-truth ownership. It must not remove XiaoAi capabilities.

## Canonical responsibility map

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

1. Memory expiry handling in GitHub runtime hardening branch.
2. Retrieved context marked as non-authority / non-instruction supporting data.
3. Golden CI coverage expanded to all runtime/test conversation paths.
4. Cross-account continuity state now has explicit visibility.
5. Continuity SELECT policy is role-aware.
6. Hot foreign-key lookup indexes added.
7. Repeated `auth.uid()` RLS calls optimized without changing access semantics.
8. `get_companion_preferred_name()` remains available only to authenticated/service_role and retains its internal access check.
9. Service-role-only atomic Guardian claim primitive added.
10. Behavior Logic freeze CI added.

## Verified current-data health before repair continuation

The following checks returned zero issues:

- duplicate runtime session keys;
- active companion access missing `verified_at`;
- expired Guardian invites still pending;
- active clients missing `linked_at`;
- active expired public memories;
- runtime/client user-daughter scope mismatch.

## Explicitly not changed

- Frozen Behavior Core;
- Behavior Freeze Baseline;
- Behavior Router contract;
- Behavior Router runtime semantics;
- child-facing capabilities;
- current Mother Guardian live binding;
- current `daughter-chat` production behavior;
- current device-chat custom token model.

## Remaining controlled cutovers

These require separate regression evidence before activation:

1. Switch `xiaoai-guardian-link` POST mutation path to `claim_xiaoai_guardian_link_atomic`.
2. Introduce Signal Generator v1 in Shadow-only mode.
3. Add durable Shadow telemetry transport.
4. Unify `daughter-chat` with the canonical runtime boundary incrementally, without changing Behavior Logic.
5. Decide and document compatibility lifecycle for `public.memories` versus `memory_private.*`.

## Merge rule

This branch is not ready to merge until:

- Behavior Logic Freeze CI passes;
- Golden Regression CI passes;
- changed-file review confirms no protected Behavior Logic path changed;
- Supabase post-migration security/data-integrity checks remain clean;
- no production capability regression is detected.
