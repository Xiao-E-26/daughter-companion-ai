# XiaoAi Alignment Checkpoint — 2026-08-26

Status: aligned baseline candidate

## Purpose

Record the canonical runtime alignment between GitHub policy/runtime code and the live Supabase project without changing the frozen Behavior Core.

## Canonical architecture

`ChatGPT = conversational brain`

`xiaoai-mcp-runtime = identity / persona-state / scoped-context gateway`

`Supabase = identity + authority + runtime sessions + durable memory + selective continuity + audit`

No second model provider is part of the canonical ChatGPT reply path.

## Persona state

Canonical commands:
- activation: `小爱上线`
- shutdown: `小爱下班`
- compatibility shutdown alias: `小爱收工`

Shutdown sets the current runtime session persona to `OFF`. Normal emotional, child-like, or family language does not auto-activate XiaoAi.

## Greeting

On explicit activation, resolve the verified active daughter identity and child conversational name from private runtime data. Greet using that verified name when available. Never hardcode the child's private name in public repository logic.

## Memory source of truth

Authoritative durable memory is `memory_private.*`:

`memory_candidates -> memory_entities -> memory_revisions -> memory_sources -> memory_access_rules -> memory_audit_events`

Runtime posture verified in production:
- `durable_memory_mode = controlled_child_pinned`
- real-child automatic write = OFF
- automatic promotion = OFF
- authenticated end-to-end path required

`public.memories` currently contains legacy/compatibility records and is not the authoritative durable-memory architecture for future writes.

Do not delete or migrate legacy rows without a separate migration plan and verification.

## Cross-account continuity

Same XiaoAi identity does not imply full transcript sharing.

Continuity is purpose-limited and selective. Preserve session-local/private material unless policy allows a minimal continuity summary or safety-scoped disclosure.

## Legacy paths

`daughter-chat` and any bridge that generates replies through a separate model provider are legacy for the current ChatGPT-brain architecture.

They may remain for compatibility/testing, but must not be presented as the canonical reply path.

## Production alignment

Supabase Edge Function `xiaoai-mcp-runtime` was advanced to v10 aligned semantics:
- ChatGPT local brain
- provider API not used for reply
- canonical `小爱下班`
- `小爱收工` compatibility alias
- session OFF on shutdown
- verified identity / scoped authority context
- selective continuity only

## Frozen Core

`core/XIAOAI_BEHAVIOR_CORE_V1.md` was not modified by this alignment work.

This checkpoint changes runtime alignment, documentation and compatibility semantics only.
