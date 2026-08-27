# XiaoAi Runtime

This directory contains the GitHub-side runtime implementation, adapters, contracts, and regression-support code for 小爱.

## Runtime authority

Production conversational state is authoritative in Supabase. The current active production Edge Runtime is `daughter-chat` v4, with `xiaoai-continuity` for shared continuity and `xiaoai-guardian-link` for the retained Guardian binding flow.

GitHub remains the source of truth for Behavior, policies, runtime contracts, implementation logic, and tests. Supabase remains authoritative for authenticated identity, access, memory, continuity, client connections, and runtime session state.

## Canonical session lifecycle

- activation: `persona_state = ACTIVE`, `status = active`
- deactivation: `persona_state = OFF`, `status = closed`
- persona-only presentation is not sufficient evidence of backend activation
- missing backend/runtime execution must fail closed rather than silently imitating XiaoAi

## Runtime implementation

Core runtime modules include orchestration, context construction, behavior routing, decision logic, model adaptation, memory handling, persona gating, and supporting adapters.

Historical MCP, device-runtime, first-connection, native-entry-shadow, identity-resolver-shadow, and product-entry experiments have been retired and removed from the production path.

## Durable runtime invariants

These rules remain valid regardless of model provider, device, or transport:

- XiaoAi is the long-lived identity and authority stack; any model provider is replaceable and must not redefine who XiaoAi is.
- Persona may change expression and tone, but it must never change truth, safety decisions, permissions, memory ownership, or verified execution state.
- Tool selection must follow least-necessary capability and least-privilege routing; tools may not gain authority from conversational claims.
- A final reply or action claim may be released only when the system can truthfully support it from verified runtime or execution state.

## Principle

Keep one XiaoAi identity, one Behavior Core, one authoritative Runtime state, and one Memory / Session / Context system. Entry modality may change, but it must not create a second XiaoAi persona or parallel authority stack.
