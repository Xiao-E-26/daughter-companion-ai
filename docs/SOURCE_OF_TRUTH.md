# Daughter Source of Truth

Status: pre-freeze consolidation

When documents or runtime behavior appear to conflict, use this precedence order:

1. `core/constitution.md` — constitutional principles
2. `core/identity.md` — identity continuity and role
3. `policies/` — current policy definitions
4. `runtime/src/` — executable implementation of current policy
5. `runtime/tests/` — executable invariants and regression expectations
6. `docs/` — architecture and explanatory material
7. legacy root-level `*_V1.md` policy/protocol files — historical/reference material only unless explicitly re-promoted

## Runtime conflict precedence

Safety → Fact Integrity → Permission / Guardian → Relationship Health → Growth → Problem Solving → Memory / Learning.

## Change rule

A lower-precedence layer must never silently override a higher-precedence layer. If implementation cannot satisfy a higher-precedence rule, treat it as a blocking design conflict and update the design explicitly before changing behavior.

## Freeze rule

`core/constitution.md` remains a FROZEN CANDIDATE until executable tests covering the critical invariants pass. After freeze, changes to constitutional behavior require explicit versioning and review rather than silent mutation.
