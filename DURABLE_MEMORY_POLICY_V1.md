# 小爱 / Daughter Companion AI — Durable Memory Policy v1

Status: ACTIVE MEMORY POLICY
Date: 2026-08-26
Project: `daughter-companion-ai`

## Purpose

Define what 小爱 should preserve as long-term durable memory, how memories are classified, how sensitivity and visibility are handled, and how the 80/20 memory balance should work without turning memory into a transcript archive or trauma collection.

Core principle:

`Remember what helps the child cherish life and understand growth; do not collect pain for its own sake.`

## 1. Memory Is Selective

Not every conversation, feeling, complaint, or event should become durable memory.

A candidate should normally meet at least one of these conditions:
- the child explicitly asks to remember it;
- it is a meaningful positive milestone or first-time experience;
- it reflects a stable preference, routine, goal, or identity-relevant fact;
- it captures a resolved or meaningfully processed growth experience;
- it is likely to help future continuity, support, or self-understanding;
- it is important enough that forgetting it would materially reduce useful continuity.

Ordinary transient emotion, repetitive complaints, casual small talk, and unresolved momentary conflict are not durable by default.

## 2. 80/20 Is a Portfolio Bias, Not a Hard Quota

The durable memory portfolio should trend toward approximately:
- 80% positive / cherished / life-giving memories;
- 20% resilience / learning / growth memories.

This is not enforced per day, per week, or per exact batch of ten memories.

Do not:
- invent positive memories to satisfy a ratio;
- discard meaningful growth memories merely because the current ratio exceeds 20%;
- force negative events into memory to fill a growth quota.

Evaluate the balance over a longer window such as the active durable-memory portfolio or a meaningful rolling period.

## 3. Memory Types

### `POSITIVE_GROWTH_MEMORY`
Examples:
- happy family moments;
- achievements and milestones;
- first-time experiences;
- acts of kindness;
- meaningful friendships;
- enjoyable learning;
- moments of courage, pride, belonging, or being loved;
- things the child explicitly says are worth remembering.

### `RESILIENCE_GROWTH_MEMORY`
Only store when there is actual learning, resolution, adaptation, courage, repair, or useful self-understanding.

Examples:
- conflict followed by healthy repair;
- fear followed by successful coping;
- a mistake followed by ownership and correction;
- being treated unfairly followed by safe help-seeking or boundary-setting;
- a setback that led to a new skill or better strategy.

Rule:
`The negative event itself is not the memory value; the growth outcome is.`

### `STABLE_CONTINUITY_FACT`
For low-risk durable facts needed for continuity, such as:
- stable preferences;
- routines;
- long-term goals;
- ongoing interests;
- persistent identity or life-stage facts.

These do not count toward the emotional 80/20 ratio unless they themselves are clearly positive or resilience memories.

## 4. Child-Initiated Pinned Memory

When the child clearly asks 小爱 to remember something, classify it as `PINNED_CANDIDATE` before persistence.

Examples of intent include, but are not limited to:
- “我要把今天记起来。”
- “这个你要记得。”
- “帮我记住这件事。”
- “我不想忘记今天。”
- equivalent natural-language expressions showing clear intent to preserve the memory.

Pinned intent has high priority, but does not bypass:
- safety;
- privacy;
- sensitivity classification;
- minimum-necessary storage;
- visibility rules;
- legal/product restrictions;
- future deletion or supersession rules.

## 5. Save the Meaning, Not the Transcript

Preferred persistence:
`conversation/event -> memory decision -> minimal summary -> metadata -> durable store`

Avoid storing full raw transcript as durable memory by default.

The memory summary should preserve the meaning needed for future continuity while minimizing unnecessary sensitive details.

## 6. Required Memory Metadata

Each durable memory should support at least:
- `memory_id`
- `daughter_id`
- `subject_user_id`
- `memory_type`
- `summary`
- `importance` (1-5)
- `source_type` (`child_explicit`, `system_inferred`, `guardian_provided`, `verified_external`)
- `pinned` (boolean)
- `sensitivity` (`low`, `medium`, `high`, `safety_scoped`)
- `visibility` (`subject_only`, `shared_continuity`, `guardian_scoped`, `safety_scoped`)
- `life_stage`
- `created_at`
- `last_verified_at`
- `retrieval_weight`
- `retrieval_hint`
- `status` (`active`, `superseded`, `archived`, `deleted`)
- `superseded_by`
- `source_ref` or provenance metadata where available

## 7. Sensitivity and Visibility

Memory classification must remain consistent with the project cross-account visibility model.

Default guidance:
- low-risk positive preferences and continuity facts may be eligible for `shared_continuity`;
- family conflict, health, emotional vulnerability, private relationship material, and safety-adjacent events should default to restricted visibility;
- Guardian status does not automatically grant blanket access;
- safety-scoped information should be shared only to the minimum extent required by the safety path.

## 8. Retrieval Rules

Durable memory should not be surfaced simply because it exists.

Before retrieval, consider:
- relevance to the current conversation;
- sensitivity;
- visibility permission;
- freshness;
- whether the memory has been superseded;
- whether surfacing it would help rather than embarrass, pressure, or define the child by the past;
- current life stage.

Do not use old painful memories to prove continuity.

## 9. Growth-Memory Decay

Resolved difficult memories should gradually reduce in active retrieval priority unless they remain materially useful.

Preferred lifecycle:
`event detail -> growth summary -> lower retrieval weight over time`

Example:
Instead of repeatedly retaining and surfacing detailed bullying history, preserve a lower-weight growth summary such as:
“她小时候曾遇到同学冲突，后来逐渐学会求助、表达边界和处理关系。”

Principle:
`Remember the growth; do not freeze the child inside the hurt.`

## 10. Supersession and Change

Children change. Preferences, fears, interests, relationships, and self-understanding can change over time.

When newer verified information conflicts with an older low-risk memory:
- preserve provenance;
- mark the older memory superseded when appropriate;
- prefer current verified self-report;
- do not silently erase safety-relevant history when retention is still justified;
- do not keep presenting stale identity claims as current truth.

## 11. Memory Write Decision

Canonical write flow:

`Candidate -> Worth Remembering? -> Memory Type -> Sensitivity -> Visibility -> Minimum Summary -> Persist -> Verify`

Decision outcomes:
- `save`
- `save_pinned`
- `save_restricted`
- `do_not_save`
- `needs_clarification`
- `safety_scoped_only`

## 12. Memory Retrieval Decision

Canonical retrieval flow:

`Current Need -> Relevant Memory Candidates -> Permission/Visibility -> Freshness/Supersession -> Sensitivity -> Retrieval Weight -> Surface Minimum Useful Context`

## 13. Anti-Patterns

Do not:
- store every chat;
- store every negative event;
- preserve raw emotional venting as permanent identity truth;
- use the 80/20 target as a rigid quota;
- expose sensitive memories across accounts by default;
- treat Guardian status as blanket memory ownership;
- surface old painful memory merely to appear caring or continuous;
- preserve outdated child preferences indefinitely;
- create new top-level rules for every special case.

## 14. Initial Rollout Boundary

This policy defines the memory model and must precede full durable-memory activation.

Initial implementation should be minimal:
- one durable-memory store;
- selective writes only;
- explicit metadata;
- no transcript-wide backfill;
- no automatic migration of all existing continuity data;
- no cross-account expansion beyond existing visibility contracts;
- no autonomous high-sensitivity memory sharing.

## Summary

`80% cherished life memories + 20% meaningful resilience memories, applied as a long-term bias rather than a rigid quota.`

`The system should remember what helps the child feel continuity, belonging, joy, capability, and growth — while preventing memory from becoming a permanent archive of pain.`
