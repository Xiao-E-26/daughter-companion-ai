# XiaoAi Runtime Unification Contract v1

Status: REPAIR CANDIDATE / NON-BEHAVIOR

## Purpose
Unify the live Supabase runtime and GitHub runtime without changing XiaoAi Behavior Logic or removing existing capabilities.

## Frozen boundary
The following remain authoritative and unchanged by this repair:
- `core/XIAOAI_BEHAVIOR_CORE_V1.md`
- `BEHAVIOR_FREEZE_BASELINE_V1.md`
- `BEHAVIOR_MODE_ROUTER_V1.md`
- `runtime/behavior_mode_router.py`

## Canonical responsibility map

### Behavior Logic
Owner: frozen Behavior Core and Behavior Router contract.
Runtime, database, Edge Functions, telemetry, and adapters may consume these rules but must not redefine them.

### Identity and access
Owner: Supabase identity graph (`users`, `daughter_identities`, `companion_access`, `guardians`, `client_connections`).
No conversational phrase grants identity or access.

### Persona session state
Owner: `runtime_sessions` persisted through authenticated runtime adapters.
Activation/deactivation phrases may request state transitions only after identity/access authorization.

### Memory
Durable source of truth: Supabase durable memory layer.
GitHub Python memory code defines runtime eligibility and transformation semantics, not a second authoritative database.
Expired/disputed/deleted memory must never be promoted back into context merely because an adapter can read it.

### Continuity
Owner: `shared_continuity_state` + `continuity_updates`.
Visibility is enforced at the data access layer before content reaches model context.

### Guardian linking
Owner: verified Supabase Auth identity + one-time Guardian invite + atomic claim transaction.
Edge Functions are transport/adapters, not authority owners.

### Live chat orchestration
Current live owner: Supabase `daughter-chat` adapter.
Target architecture: live adapter delegates to the same deterministic decision/context boundaries represented in GitHub runtime.
Do not cut over in one step. Use shadow comparison first.

## Migration path
1. Keep existing `daughter-chat` response path active.
2. Add a shadow-only runtime decision path that receives the same normalized input.
3. Record shadow decision metadata only; do not alter the user-visible reply.
4. Compare live-vs-shadow decisions and investigate mismatches.
5. Add signal generation in shadow mode only.
6. Require regression evidence before any shadow decision is allowed to influence responses.
7. Preserve rollback to the existing response path until production stability is demonstrated.

## Non-goals
- no Behavior Logic rewrite;
- no child-facing personality change;
- no deletion of Memory, Guardian, continuity, device, or multi-entry capabilities;
- no model-provider lock-in;
- no direct production Router activation without shadow evidence.

## Repair invariant
`Reduce duplicate ownership -> keep capability -> keep frozen behavior -> move authority to one canonical layer -> verify before cutover.`
