# 小爱 / Daughter Companion AI — Memory 80/20 Runtime Contract v1

Status: ACTIVE RUNTIME CONTRACT
Date: 2026-08-26
Project: `daughter-companion-ai`
Authoritative memory store: `memory_private.*`
Primary memory/privacy policy owner: `MEMORY_AND_PRIVACY_POLICY_V1.md`
Durable-memory specialization: `DURABLE_MEMORY_POLICY_V1.md`

## Purpose

Turn the 80/20 durable-memory philosophy into an executable decision model without creating a second memory system or a second memory policy authority.

This file is a runtime execution contract. It does not own the global memory/privacy policy domain. Where policy interpretation is required, `MEMORY_AND_PRIVACY_POLICY_V1.md` is primary; `DURABLE_MEMORY_POLICY_V1.md` specializes durable-memory selection; this contract maps those rules into runtime behavior.

Core principle:

`记住快乐，记住成长，不收藏创伤。`

Equivalent operating rule:

`Prefer cherished life memories; preserve difficult experiences only when the durable value is the child's learning, resilience, repair, courage, or self-understanding.`

## 1. Existing Memory Core Is Authoritative

Do not create a parallel public durable-memory store.

Use the existing private memory flow:

`memory_candidates -> memory_entities -> memory_revisions -> memory_sources -> memory_access_rules -> memory_audit_events`

Related lifecycle support:
- `memory_tombstones`
- `memory_subjects`
- `memory_accounts`
- `subject_account_links`
- `memory_runtime_config`

The current runtime mode remains controlled unless separately approved.

## 2. Current Runtime Boundary

Current expected runtime posture:
- durable memory mode: `controlled_child_pinned`
- real-child automatic write: OFF
- automatic promotion: OFF
- authenticated end-to-end path required

This means the 80/20 contract currently governs classification and review behavior, not blanket automatic persistence.

## 3. Candidate Detection

A conversation/event may become a candidate when at least one of these is true:
- child explicitly asks to remember it;
- meaningful positive milestone or cherished experience;
- stable preference, routine, goal, identity or support preference;
- difficult event has reached a meaningful learning/repair/growth outcome;
- recurring fact is useful for continuity;
- verified outcome materially improves future support.

Do not create a candidate merely because an event is emotionally intense.

## 4. Candidate Classification

Every candidate should be classified conceptually as one of:

### A. Positive / Cherished
Examples:
- joy
- belonging
- family warmth
- achievement
- first-time experience
- kindness
- courage
- pride
- enjoyable learning

Recommended existing-field mapping:
- `category`: positive/cherished semantic label
- `intent_class`: positive_memory
- `memory_kind` on promotion: usually `event`, `milestone`, `storyline_anchor`, `preference`, or `child_pinned`
- `significance`: ordinary / meaningful / milestone according to actual importance

### B. Resilience / Growth
Use only when there is actual growth value.

Examples:
- conflict -> repair
- fear -> coping
- mistake -> ownership/correction
- unfair treatment -> help-seeking/boundary setting
- setback -> new strategy/skill

Recommended mapping:
- `intent_class`: resilience_growth
- `source_type`: `outcome` when the growth is evidenced by an outcome
- `memory_kind`: usually `event`, `milestone`, or `storyline_anchor`

Rule:
`Do not preserve pain as the durable meaning when the meaningful durable value is the growth.`

### C. Stable Continuity Fact
Examples:
- preferences
- routines
- goals
- interests
- support preferences

Recommended mapping:
- `intent_class`: continuity_fact
- `memory_kind`: `fact`, `preference`, or `support_preference`

Stable continuity facts are outside the emotional 80/20 balance unless they clearly represent a cherished or resilience memory.

## 5. 80/20 Portfolio Bias

The 80/20 target is a long-run portfolio bias:
- approximately 80% cherished/positive emotional memories;
- approximately 20% resilience/growth emotional memories.

Do not enforce it as an exact per-session or per-ten-memory quota.

Do not:
- generate positive memories to fix the ratio;
- suppress meaningful resilience memories only because the current ratio is above 20%;
- promote negative events merely to fill a growth quota.

The ratio should guide memory selection pressure, not distort factual truth.

## 6. Child-Pinned Priority

If the child clearly asks to remember something:
- set `child_declared_important = true` at candidate level;
- prefer `child_pinned` as the durable memory kind where appropriate;
- preserve `pinned_by_child = true` after promotion;
- retain minimum necessary summary rather than raw transcript;
- still classify sensitivity and access.

Pinned intent increases retention priority but does not bypass safety, privacy, visibility, correction, or deletion rules.

## 7. Difficult Event Handling

For a difficult event, use this sequence:

`Acknowledge current feeling -> determine whether event is still unresolved -> if unresolved, do not prematurely convert to growth -> if resolved/processed, identify actual learning/outcome -> create growth-focused candidate`

Examples:

Bad durable summary:
`She was bullied by classmates and felt helpless.`

Preferred later growth summary when supported by facts:
`She learned to seek help, express boundaries, and handle peer conflict more confidently.`

If no growth outcome exists yet, keep the experience session-local or candidate-held rather than forcing a resilience narrative.

## 8. Promotion Gate

A candidate should not be promoted automatically merely because it fits the 80/20 philosophy.

Promotion requires consideration of:
- source confidence;
- stability;
- recurrence or significance;
- sensitivity;
- child-declared importance;
- whether the memory is current and accurate;
- whether a related active memory already exists;
- whether the summary is minimal and non-stigmatizing;
- applicable access/disclosure rules.

Current runtime posture keeps automatic promotion OFF.

## 9. Revision and Supersession

When the child changes:
- create a new revision or supersede stale content as appropriate;
- preserve provenance;
- prefer current verified self-report for low-risk preferences and identity facts;
- do not keep outdated labels active merely because they were once true.

For difficult memories, revision should progressively emphasize durable meaning and reduce unnecessary incident detail when safe and appropriate.

## 10. Retrieval Weighting

Retrieval should favor:
1. relevant current positive continuity;
2. child-pinned meaningful memories;
3. current stable preferences/goals;
4. resilience memories only when genuinely useful to the present situation.

Do not proactively surface painful history just to demonstrate that 小爱 remembers.

Resolved difficult memories should generally receive lower proactive-surface priority over time unless still materially useful.

## 11. Access and Disclosure

Use existing `memory_access_rules` rather than inventing a second visibility system.

Distinguish:
- reasoning use;
- proactive surface;
- on-request access;
- disclosure;
- modification;
- deletion.

Guardian relationship alone does not mean blanket disclosure.

## 12. Auditability

Material memory actions should be auditable through `memory_audit_events` where the runtime path supports it.

Important events include:
- candidate creation
- child pin
- promotion
- correction
- supersession
- deletion
- disclosure-policy change
- retrieval-policy change

## 13. Runtime Decision Summary

Canonical memory flow:

`Conversation/Event`
`-> Candidate?`
`-> Positive / Resilience / Continuity Fact`
`-> Sensitivity + Stability + Confidence`
`-> Child-Pinned?`
`-> Hold / Reject / Review / Promote`
`-> Entity + Revision + Source`
`-> Access Rules`
`-> Retrieval by relevance and current need`
`-> Correct / Supersede / Delete when life changes`

## 14. Anti-Duplication Rule

Do not introduce another durable-memory table, identity layer, visibility model, promotion engine, or memory policy owner unless the existing architecture is proven insufficient.

New requirements should first be mapped onto the existing Memory Core and policy hierarchy.

## Summary

`多记幸福，少记伤痛；如果困难值得留下，就留下孩子从中长出来的力量。`

This contract implements the 80/20 philosophy as selection and retrieval bias on top of the existing private Memory Core, while keeping automatic real-child writes and automatic promotion disabled until separately verified and approved.
