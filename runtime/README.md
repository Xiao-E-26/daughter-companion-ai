# XiaoAi Runtime

This directory contains the GitHub-side runtime implementation, adapters, contracts, and regression-support code for 小爱.

## Runtime authority

GitHub is the source of truth for XiaoAi Behavior, policies, runtime contracts, implementation logic, and tests.
Supabase is authoritative for authenticated identity, access, memory, continuity, client connections, runtime session state, and deployed Edge Function state.

### Live production Edge inventory — verified 2026-09-20

Canonical XiaoAi Supabase project: `bnxjlbuohnujgvryttzj`.

Active Edge Functions discovered through Xiao-E cross-account Supabase execution:
- `xiaoi-memory-runtime` v5 — ACTIVE — `verify_jwt=true`
- `xiaoi-ui-preview` v3 — ACTIVE — `verify_jwt=false`

No active `daughter-chat` Edge Function was present in the verified live project inventory at the time of this check.

Therefore, older documentation describing `daughter-chat v4` as the active production conversational runtime must be treated as historical/stale unless a later live deployment re-establishes it.

Do not infer that `xiaoi-memory-runtime` is the full conversational brain merely because it is active. Its exact production responsibilities must be established from live source or verified execution evidence.

## Session / persona posture

- `runtime_sessions` exists as the current session substrate.
- The verified live schema does not currently contain a production `persona_state` column.
- `ACTIVE/OFF` persona persistence is therefore not yet productionized.
- Persona-only presentation is not sufficient evidence of backend activation.
- Missing backend/runtime execution must fail closed rather than silently imitating XiaoAi.

## Runtime implementation

Core runtime modules include orchestration, context construction, behavior routing, decision logic, model adaptation, memory handling, persona gating, and supporting adapters.

Historical MCP, device-runtime, first-connection, native-entry-shadow, identity-resolver-shadow, and product-entry experiments are not authoritative merely because they remain documented.

The current canonical architecture and document authority index determine which runtime artifacts are active, reference-only, shadow, historical, or superseded.

## Durable runtime invariants

These rules remain valid regardless of model provider, device, or transport:

- XiaoAi is the long-lived identity and authority stack; any model provider is replaceable and must not redefine who XiaoAi is.
- Persona may change expression and tone, but it must never change truth, safety decisions, permissions, memory ownership, or verified execution state.
- Tool selection must follow least-necessary capability and least-privilege routing; tools may not gain authority from conversational claims.
- A final reply or action claim may be released only when the system can truthfully support it from verified runtime or execution state.
- Child-pinned durable memory is a strong child-intent path, not a bypass around privacy, sensitivity, minimum-necessary, visibility, or safety gates.

## Principle

Keep one XiaoAi identity, one Behavior Core, one authoritative Runtime state, and one Memory / Session / Context system. Entry modality may change, but it must not create a second XiaoAi persona or parallel authority stack.
