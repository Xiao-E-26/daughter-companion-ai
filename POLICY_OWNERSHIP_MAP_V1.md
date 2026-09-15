# 小爱 / Daughter Companion AI — Policy Ownership Map v1

Status: ACTIVE GOVERNANCE MAP
Date: 2026-08-24
Updated: 2026-09-16
Project: `daughter-companion-ai`

## Purpose

Prevent policy drift, duplicate ownership, and contradictory evolution by assigning one primary Source of Truth (SoT) to each major policy domain.

This map defines ownership only. It does not itself change runtime behavior, backend state, permissions, or production execution.

## Governing Rule

`One policy domain -> one primary owner -> other files reference, specialize, or apply it`

If two files appear to define the same rule in detail, the primary owner listed here wins unless a higher XiaoE Core rule, legal requirement, security rule, or explicit later governance decision overrides it.

Document status precedence is governed by:
1. `XIAOAI_CANONICAL_ARCHITECTURE_V1.md`
2. `DOCUMENT_AUTHORITY_INDEX_V1.md`
3. this ownership map
4. the named policy owner / runtime contract

## Policy Owners

| Policy domain | Primary Source of Truth | Allowed role of other files |
|---|---|---|
| Project identity, name, purpose, enduring character, lifelong companion intent | `PROJECT_IDENTITY.md` | May reference identity; must not redefine persona fundamentals |
| Project operating boundary, XiaoE inheritance, mutation discipline, source-of-truth rules | `DAUGHTER_PROJECT_PROTOCOL_V1.md` | Other files comply; do not duplicate Core operating rules |
| Life-stage classification and controlled stage transition | `LIFE_STAGE_POLICY_V1.md` | Guardian/Memory/Growth policies may define stage-specific effects only |
| Guardian authority, user autonomy, approval classes, permission ownership, safety escalation | `GUARDIAN_AND_AUTONOMY_POLICY_V1.md` | Other files may apply but not redefine authority |
| Guardian succession / continuity | `GUARDIAN_CONTINUITY_AND_SUCCESSION_POLICY_V1.md` | Other files reference succession rules only |
| Memory classification, creation, retention, visibility, correction, deletion, privacy, lifecycle | `MEMORY_AND_PRIVACY_POLICY_V1.md` | Memory specializations may narrow/apply rules but may not become parallel owners |
| Durable-memory specialization | `DURABLE_MEMORY_POLICY_V1.md` under `MEMORY_AND_PRIVACY_POLICY_V1.md` | Specializes long-term durable memory only |
| Child-declared pinned-memory specialization | `CHILD_PINNED_MEMORY_POLICY_V1.md` under `MEMORY_AND_PRIVACY_POLICY_V1.md` | Strong child intent signal; does not bypass safety/privacy/sensitivity/minimum-necessary gates |
| Family-memory prioritization specialization | `FAMILY_SHARED_MEMORY_PRIORITY_V1.md` under `MEMORY_AND_PRIVACY_POLICY_V1.md` | Prioritization/context completeness only |
| Growth safety, anti-dependency, non-exclusivity, human/AI boundary, real-world relationship priority, competence preservation, productive friction, safe disengagement | `GROWTH_SAFETY_BASELINE_V1.md` | Other files may apply stronger stage-specific controls but must not redefine these principles |
| Portable identity, migration, embodiment, continuity across devices/platforms/bodies | `PORTABLE_IDENTITY_AND_EMBODIMENT_POLICY_V1.md` | Other files reference migration/embodiment rules only |
| Product architecture and component boundaries | `FOUR_LAYER_ARCHITECTURE_V1.md` | Policy files define rules, not architecture ownership |
| Runtime conversational decision execution | `RUNTIME_BEHAVIOR_DECISION_FLOW_V1.md` | Executes policy; must not become a competing policy source |
| Learning promotion governance | `core/XIAOAI_LEARNING_PROMOTION_PROTOCOL_V1.md` | Learning maps/mentor/runtime components implement/support only |

## Historical / Reference Scope

`DAUGHTER_V1_PRODUCT_SCOPE.md` is a HISTORICAL / REFERENCE BASELINE, not a current global product-scope owner.

It preserves original v1 intent and non-goals, but it must not override later approved architecture, runtime, memory, continuity, multi-device, adapter, provider, or verification contracts.

`LEARNING_MENTOR_SKILLS_MAP_V1.md` is an implementation/reference map. Its older `ACTIVE STRUCTURE MAP CANDIDATE` wording does not make it a top-level policy owner.

## Memory Precedence Clarification

The memory domain has one primary owner:

`MEMORY_AND_PRIVACY_POLICY_V1.md`

Specializations operate underneath it.

For explicit child memory intent:

`child says remember this`
`-> strong child-pinned durable intent`
`-> bypass ordinary weak candidate threshold`
`-> still pass safety / privacy / sensitivity / minimum-necessary / visibility gates`
`-> persist durably when allowed`

Therefore:
- `CHILD_PINNED_MEMORY_POLICY_V1.md` may define the strong child-intent specialization;
- `DURABLE_MEMORY_POLICY_V1.md` must defer to that specialization for explicit child-pinned intent;
- neither specialization may bypass the primary Memory/Privacy owner.

## Cross-Cutting Invariants

The following may appear briefly in more than one file because they are global invariants, but detailed rules still have one owner:

- child safety first;
- factual integrity;
- non-manipulation;
- privacy and least privilege;
- controlled learning;
- healthy real-world relationships;
- increasing autonomy with maturity;
- no self-expansion of permissions.

## Duplicate Classification

Acceptable reminder duplication may preserve short global invariants for local readability.

Detailed duplication should be consolidated toward the primary owner while preserving meaning and safety boundaries.

Known ownership examples:
- Guardian transition details -> `GUARDIAN_AND_AUTONOMY_POLICY_V1.md`
- Memory transition/retention details -> `MEMORY_AND_PRIVACY_POLICY_V1.md`
- Anti-dependency / exclusivity -> `GROWTH_SAFETY_BASELINE_V1.md`
- Safety escalation authority -> `GUARDIAN_AND_AUTONOMY_POLICY_V1.md`
- Life-stage definition/transition -> `LIFE_STAGE_POLICY_V1.md`

## Change Safety Rules

During policy deduplication:
- one owner decision at a time;
- no broad behavior rewrites merely to clean docs;
- do not change XiaoE Core;
- preserve Guardian, migration, memory, privacy, life-stage, and safety semantics;
- verify affected references after edits;
- stop if ownership becomes ambiguous.

## Target Policy Graph

`PROJECT_IDENTITY`
-> who 小爱 is

`DAUGHTER_PROJECT_PROTOCOL`
-> project governance

`LIFE_STAGE_POLICY`
-> maturity-stage transitions

`GUARDIAN_AND_AUTONOMY_POLICY`
-> who may decide/approve what

`MEMORY_AND_PRIVACY_POLICY`
-> what may be remembered and who may access it
-> specialized by durable / child-pinned / family-memory rules

`GROWTH_SAFETY_BASELINE`
-> healthy companionship and anti-dependency

`PORTABLE_IDENTITY_AND_EMBODIMENT_POLICY`
-> continuity across platforms/devices/bodies

`FOUR_LAYER_ARCHITECTURE`
-> technical/component structure

`RUNTIME_BEHAVIOR_DECISION_FLOW`
-> executes the above policies during real interaction

## Current State

`ACTIVE — POLICY OWNERSHIP MAP V1 / 2026-09-16 DRIFT-CORRECTED`

`One policy domain -> one owner -> specializations subordinate -> runtime executes`
