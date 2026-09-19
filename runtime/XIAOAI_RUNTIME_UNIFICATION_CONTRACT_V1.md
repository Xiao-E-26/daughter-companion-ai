# XiaoAi Runtime Unification Contract v1

Status: REFERENCE / HISTORICAL REPAIR CONTRACT

## Purpose

Preserve the earlier runtime-unification repair intent without allowing stale implementation assumptions to override current verified production state.

## Frozen boundary

The following remain unchanged by runtime maintenance:
- `core/XIAOAI_BEHAVIOR_CORE_V1.md`
- `BEHAVIOR_FREEZE_BASELINE_V1.md`
- `BEHAVIOR_MODE_ROUTER_V1.md`
- `runtime/behavior_mode_router.py`

## Current verified production posture — 2026-09-20

Active Edge Functions:
- `xiaoi-memory-runtime` v5 — ACTIVE — `verify_jwt=true`
- `xiaoi-ui-preview` v3 — ACTIVE

No active `daughter-chat` Edge Function exists.

Therefore any older wording that names `daughter-chat` as the current live conversational owner is historical and must not be treated as current truth.

## Current responsibility map

### Behavior
Owned by canonical behavior/policy sources and runtime decision contracts.

### Identity / session substrate
Supabase contains the identity/session primitives, but current live identity/session rows are empty and persona-state persistence is not productionized.

### Memory
Memory V2 protected production path is deployed and enabled in `child_pinned_only` mode. This does not imply current real-user usage.

### Conversational brain
GitHub contains `DaughterOrchestrator` and `AuthoritativeReplyAdapter` as the canonical conversational brain implementation boundary.

### Live conversational serving
Not currently active.

## Historical migration note

Earlier migration steps that referenced keeping `daughter-chat` active and comparing a shadow runtime describe a retired transition plan. Do not recreate `daughter-chat` merely to satisfy this historical document.

## Current repair invariant

`Reduce duplicate ownership -> preserve capability -> preserve frozen behavior -> keep one canonical state authority -> verify before cutover`.

## Non-goals

- no Behavior Core rewrite;
- no child-facing personality reset;
- no permission expansion;
- no restoration of retired shadow transport;
- no live-serving cutover unless explicitly approved and evidenced.
