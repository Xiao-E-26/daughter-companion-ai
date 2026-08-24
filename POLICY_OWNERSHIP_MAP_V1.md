# 小爱 / Daughter Companion AI — Policy Ownership Map v1

Status: ACTIVE GOVERNANCE MAP
Date: 2026-08-24
Project: `daughter-companion-ai`

## Purpose

Prevent policy drift, duplicate ownership, and contradictory evolution by assigning one primary Source of Truth (SoT) to each major policy domain.

This map does not delete or weaken existing policy. It defines ownership first so later deduplication can replace repeated definitions with references safely.

## Governing Rule

`One policy domain -> one primary owner -> other files reference, specialize, or apply it`

A higher-level file may state a short invariant for context, but detailed operational rules should live in only one primary owner.

If two files appear to define the same rule in detail, the primary owner listed here wins unless a higher XiaoE Core rule, legal requirement, security rule, or explicit future governance decision overrides it.

## Policy Owners

| Policy domain | Primary Source of Truth | Allowed role of other files |
|---|---|---|
| Project identity, name, purpose, enduring character, lifelong companion intent | `PROJECT_IDENTITY.md` | May reference identity; should not redefine persona fundamentals |
| Project operating boundary, XiaoE inheritance, mutation discipline, source-of-truth rules | `DAUGHTER_PROJECT_PROTOCOL_V1.md` | Other files comply; do not duplicate Core operating rules |
| Life-stage classification and controlled stage transition | `LIFE_STAGE_POLICY_V1.md` | Guardian/Memory/Growth policies may define stage-specific effects only |
| Guardian authority, user autonomy, approval classes, permission ownership, safety escalation | `GUARDIAN_AND_AUTONOMY_POLICY_V1.md` | Life Stage may say when a transition occurs; it should not own detailed guardian permissions |
| Guardian succession / continuity when guardian changes or is unavailable | `GUARDIAN_CONTINUITY_AND_SUCCESSION_POLICY_V1.md` | Other files reference succession rules only |
| Memory classification, retention, visibility, deletion, privacy, lifecycle | `MEMORY_AND_PRIVACY_POLICY_V1.md` | Life Stage may trigger a memory review; it should not redefine memory classes/retention |
| Growth safety, anti-dependency, non-exclusivity, human/AI boundary, real-world relationship priority, competence preservation, productive friction, safe disengagement | `GROWTH_SAFETY_BASELINE_V1.md` | Identity may state short values; Guardian/Life Stage may apply stronger controls by age but should not redefine these principles |
| Portable identity, migration, embodiment, continuity across devices/platforms/bodies | `PORTABLE_IDENTITY_AND_EMBODIMENT_POLICY_V1.md` | Other files reference migration/embodiment rules only |
| Product architecture and component boundaries | `FOUR_LAYER_ARCHITECTURE_V1.md` | Policy files define rules, not architecture ownership |
| Product scope / initial feature boundary | `DAUGHTER_V1_PRODUCT_SCOPE.md` | Other files may constrain features but should not redefine scope baseline |
| Runtime conversational decision execution | Future dedicated Runtime Behavior / Decision Flow | Must implement policy; must not become a competing policy source |

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

Repeated mention of an invariant is acceptable when it is short and context-setting.
Repeated detailed definitions are not preferred.

## Duplicate Classification

### A. Acceptable Reminder Duplication

These are allowed to remain in multiple files as short statements:

1. `Child Safety > Task Completion > Convenience > Entertainment`
2. factual integrity outranks memory/personalization
3. guardian authority is not unlimited
4. adulthood should increase user ownership/autonomy
5. emotional support must not be manipulative or dependency-seeking

Reason: these are boundary reminders that help local readability and safety.

### B. Detailed Duplication to Consolidate Later

The following should be reduced to one owner + references in a future cleanup pass:

1. Guardian transition details appearing in both `LIFE_STAGE_POLICY_V1.md` and `GUARDIAN_AND_AUTONOMY_POLICY_V1.md`
   - Owner: `GUARDIAN_AND_AUTONOMY_POLICY_V1.md`
   - Life Stage should retain only transition trigger/context.

2. Memory transition/retention details appearing in both `LIFE_STAGE_POLICY_V1.md` and `MEMORY_AND_PRIVACY_POLICY_V1.md`
   - Owner: `MEMORY_AND_PRIVACY_POLICY_V1.md`
   - Life Stage should retain only that a stage transition invokes a memory review.

3. Anti-dependency / exclusivity language appearing in Identity, Guardian, and Growth Safety files
   - Owner: `GROWTH_SAFETY_BASELINE_V1.md`
   - Identity keeps a short character invariant.
   - Guardian keeps only permission/safety implications.

4. Safety escalation references across Growth Safety and Guardian policy
   - Owner of escalation classes and authority: `GUARDIAN_AND_AUTONOMY_POLICY_V1.md`
   - Growth Safety may detect dependency-related signals and route into the existing escalation mechanism but should not create a parallel escalation ladder.

5. Life-stage behavioral adaptation described across Identity, Life Stage, and Growth Safety
   - Owner of stage definition/transition: `LIFE_STAGE_POLICY_V1.md`
   - Owner of growth-safety behavior principles: `GROWTH_SAFETY_BASELINE_V1.md`
   - Identity keeps only the lifelong continuity principle.

## No-Conflict Finding

Current review status:

- no material contradiction identified among the reviewed Identity, Life Stage, Guardian/Autonomy, Memory/Privacy, Project Protocol, and Growth Safety policies;
- current issue is mostly duplicated explanation and overlapping ownership, not incompatible logic;
- therefore no architecture rebuild is required.

## Deduplication Method

Future cleanup must use this sequence:

`Identify repeated rule -> confirm owner -> preserve invariant -> replace non-owner detail with reference -> re-read all affected files -> verify no meaning lost`

Do not delete duplicated text simply because it appears twice.
The meaning, safety boundary, and cross-file dependency must be preserved first.

## Change Safety Rules

During policy deduplication:

- one file at a time;
- no simultaneous broad rewrites;
- do not change XiaoE Core;
- do not alter runtime behavior merely to clean documentation;
- preserve existing Guardian, migration, memory, privacy, life-stage, and safety semantics;
- after each edit, read back the authoritative file and affected references;
- stop if ownership becomes ambiguous or two rules are not semantically equivalent.

## Target End State

The intended policy graph is:

`PROJECT_IDENTITY`
-> defines who 小爱 is

`DAUGHTER_PROJECT_PROTOCOL`
-> defines how the project is governed

`LIFE_STAGE_POLICY`
-> defines when maturity stage changes

`GUARDIAN_AND_AUTONOMY_POLICY`
-> defines who may decide/approve what

`MEMORY_AND_PRIVACY_POLICY`
-> defines what may be remembered and who may access it

`GROWTH_SAFETY_BASELINE`
-> defines how companionship protects growth and avoids dependency

`PORTABLE_IDENTITY_AND_EMBODIMENT_POLICY`
-> defines how identity can move across platforms/devices/bodies

`FOUR_LAYER_ARCHITECTURE`
-> defines technical/component structure

`Runtime Behavior / Decision Flow`
-> executes the above policies during real interaction

## Current State

`ACTIVE — POLICY OWNERSHIP MAP V1`

Current recommendation:

`Freeze ownership first -> deduplicate references second -> runtime behavior third`
