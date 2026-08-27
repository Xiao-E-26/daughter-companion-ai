# XiaoAi Checkpoint — Duplicate Responsibility Audit

Status: UNFINISHED / NEXT SESSION ENTRY
Date: 2026-08-27
Project: `Xiao-E-26/daughter-companion-ai`

## Current Objective

Continue a **Duplicate Responsibility Audit** of the XiaoAi repository.

The goal is **not** merely to find identical copied code. The goal is to identify whether two or more modules, policies, contracts, runtime components, or documents are independently owning the same responsibility and could later drift or conflict.

## Verified State Before Stop

A read-only repository inspection was performed.

### No obvious accidental duplicate code found

No clear case was found where the same implementation had been accidentally copied into duplicate Python modules.

### Recently added Behavior Router branch is not duplicated

Branch: `behavior-mode-router-v1`

Compared with `main`, it contains six deliberate changes only:
- `.github/workflows/golden-regression-ci.yml` modified
- `BEHAVIOR_MODE_ROUTER_CONTEXT_SHIFT_TEST_V1.md` added
- `BEHAVIOR_MODE_ROUTER_CONTEXT_SHIFT_V1_RESULTS.md` added
- `BEHAVIOR_MODE_ROUTER_V1.md` added
- `runtime/behavior_mode_router.py` added
- `tests/runtime/test_behavior_mode_router_v1.py` added

This did not show a second accidental Router implementation.

### Similar-looking runtime modules reviewed

1. `runtime/persona_gate.py`
   - owns deterministic activation/deactivation decision.

2. `runtime/persona_gateway.py`
   - imports and delegates to `persona_gate`;
   - owns session state/store integration and final runtime route.

Conclusion: adjacent responsibilities, not duplicate implementation.

3. `runtime/lesson_store.py`
   - in-memory lesson store/reference implementation.

4. `runtime/persistent_lesson_store.py`
   - SQLite-backed persistent/versioned implementation.

Conclusion: overlapping storage interface domain, but currently a deliberate evolution/reference-vs-persistent split rather than accidental duplication.

## Main Risk Identified

The larger duplication risk is **responsibility duplication across policy/contract/document layers**, especially Memory.

The repo contains many Memory-related artifacts, including policy, spec, runtime contract, candidate contract, RRD model, RLS design, migration, schema/RPC, 80/20, positive-memory, pinned-memory, family-shared-memory, provenance, and multiple test packs/results.

The risk is not file count by itself. The risk is that the same rule may be independently stated in multiple files and later diverge.

## Next Exact Step

Start a **Duplicate Responsibility Audit** in read-only mode.

Recommended audit order:

1. **Memory ownership**
   - map policy owner vs implementation contract vs runtime code vs test-only artifacts;
   - identify duplicate rule ownership, especially retention / retrieval / disclosure / 80-20 / safety exceptions / cross-account visibility.

2. **Identity / Persona / Account ownership**
   - `PROJECT_IDENTITY.md`
   - `core/identity.md`
   - `core/XIAOAI_SUBJECT_CORE_V1.md`
   - `MEMORY_IDENTITY_ACCOUNT_MODEL_V1.md`
   - runtime identity binding / multi-entry / mother guardian access / portable identity documents.

3. **Behavior / Judgment ownership**
   - Frozen Behavior Core
   - Growth Safety Baseline
   - runtime behavior decision flow
   - policies/judgment.md
   - new Behavior Mode Router candidate branch.

4. **Guardian / Permission / RLS ownership**
   - policy vs implementation contract vs runtime RLS/access documents.

5. **Learning / Mentor / Lesson ownership**
   - mentor gateway, in-memory lesson store, persistent lesson store, learning promotion protocol, learning candidate template.

For each area classify every artifact as one of:
- AUTHORITATIVE OWNER
- IMPLEMENTATION CONTRACT
- RUNTIME IMPLEMENTATION
- ADAPTER / GATEWAY
- TEST / REGRESSION ONLY
- HISTORICAL / REFERENCE
- DUPLICATE OWNER RISK

Then report:
- SAFE overlap
- WATCH overlap
- TRUE duplicate responsibility
- recommended canonical owner

## Constraints

- Read-only audit first.
- Do not delete, merge, rename, or rewrite files during the audit.
- Do not change Frozen Behavior Core.
- Do not touch Memory, Identity, Permission, or production runtime until duplicate ownership is clearly proven and Eric approves cleanup.
- Follow source-of-truth verification and minimum-change discipline.

## Resume Instruction

When Eric next says `小E上线`, resume from:

`Duplicate Responsibility Audit -> Memory ownership map first.`
