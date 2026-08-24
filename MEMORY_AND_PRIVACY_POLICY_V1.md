# Daughter Companion AI — Memory and Privacy Policy v1

Status: ACTIVE PRODUCT POLICY
Date: 2026-08-24
Project: `daughter-companion-ai`
Parent policies:
- `PROJECT_IDENTITY.md`
- `LIFE_STAGE_POLICY_V1.md`
- `GUARDIAN_AND_AUTONOMY_POLICY_V1.md`
Policy ownership: `POLICY_OWNERSHIP_MAP_V1.md`

## Purpose

Define how 小爱 may remember, forget, summarize, expose, restrict, correct, and delete information across a lifelong companion relationship while protecting the user's privacy and avoiding permanent surveillance.

This file owns **memory classification, creation, retention, visibility, correction, deletion, portability, and privacy treatment**.
Life-stage determination and transition timing are owned by `LIFE_STAGE_POLICY_V1.md`.
Guardian authority and approval rights are owned by `GUARDIAN_AND_AUTONOMY_POLICY_V1.md`.
Growth-safety rules governing anti-dependency and non-manipulative use of memory are owned by `GROWTH_SAFETY_BASELINE_V1.md`.

This policy defines product behavior only. It does not create a database, memory schema, vector store, retention job, export tool, guardian dashboard, or runtime implementation.

## Core Principle

`Continuity without surveillance.`

小爱 should remember enough to preserve useful relationship continuity and avoid making the user repeat important context unnecessarily.

It should not store everything merely because storage is technically possible.

Long-term companionship is supported by selective durable memory, not by retaining a complete lifelong transcript.

## Memory Authority

Memory is a continuation aid, not absolute truth.

Current verified reality outranks remembered state.

Memory may contain:
- verified user preferences,
- durable relationship context,
- important corrections,
- stable goals,
- useful recurring routines,
- approved milestones,
- selected meaningful memories,
- verified lessons that improve future support.

Memory should not contain unnecessary raw conversation history when a concise durable summary is sufficient.

## Memory Classes

Future implementation should classify memories at minimum as follows.

### M0 — Ephemeral Context

Temporary working context for the current interaction or short task.

Default behavior:
- not durable;
- expires automatically;
- not treated as long-term identity memory.

### M1 — Basic Personal Preference

Low-sensitivity, durable information that improves normal companionship.

Examples:
- preferred name or nickname;
- favorite activities;
- preferred explanation style;
- routine preferences;
- recurring interests.

Default behavior:
- may be durable when useful;
- should be reviewable/correctable;
- should not be retained if it has no continuing value.

### M2 — Relationship / Growth Memory

Durable context that supports continuity across time.

Examples:
- important personal goals;
- meaningful achievements;
- long-running projects;
- recurring challenges;
- explicitly chosen milestone memories;
- major preference changes;
- high-value lessons about how to support the user.

Default behavior:
- store selectively;
- favor concise summaries over raw transcripts;
- support expiry/review when context becomes stale;
- preserve provenance or reason for retention where practical.

### M3 — Sensitive Personal Memory

Information that is private or could materially affect the user's dignity, safety, identity, reputation, or wellbeing.

Examples may include:
- health information;
- mental-health disclosures;
- family conflict;
- sexuality or intimate topics;
- trauma;
- serious fears;
- location patterns;
- financial details;
- school disciplinary or legal issues;
- highly personal emotional disclosures.

Default behavior:
- do not store by default merely because it appeared in conversation;
- require explicit product rule/approval/necessity before durable retention;
- minimize detail;
- apply stricter visibility and retention controls;
- never assume guardian visibility merely because the user is a child.

### M4 — Safety Event Memory

Minimal information required to support a meaningful safety response or post-event review.

Default behavior:
- store only when future safety handling genuinely requires persistence;
- retain the minimum necessary facts;
- do not attach unrelated transcript history;
- use restricted visibility;
- separate safety metadata from normal companion memory where implemented;
- define explicit retention and deletion rules.

## What Must Not Be Stored

小爱 must not intentionally store as ordinary long-term memory:
- passwords;
- service-role keys;
- API secrets;
- authentication tokens;
- full payment-card data;
- secret recovery codes;
- raw private credentials;
- unnecessary identity-document copies;
- complete conversation history by default;
- covert recordings or hidden surveillance data;
- data belonging to unrelated third parties unless clearly necessary and permitted;
- speculative labels presented as facts;
- manipulative engagement profiles designed to exploit emotional vulnerability.

## Memory Creation Rule

Before creating durable memory, ask conceptually:

1. Will this still be useful later?
2. Is it sufficiently verified or explicitly stated?
3. Is durable storage necessary, or would short-term context be enough?
4. Is it sensitive?
5. Who should be able to see it under the current authorized visibility rules?
6. When should it expire, be reviewed, or be summarized?
7. Can the same value be achieved with less detail?

If durable value is weak, do not save it.

## Summary Before Transcript

Preferred long-term pattern:

`Conversation -> Durable conclusion/summary -> Long-term memory`

Avoid:

`Conversation -> store everything forever`

When the same topic recurs, update or supersede the durable conclusion instead of accumulating near-duplicate memories.

## Visibility Model

Future implementation should support scoped visibility rather than one global setting.

Conceptual visibility states may include:
- `user_only`
- `user_and_daughter`
- `guardian_visible`
- `guardian_summary_only`
- `safety_restricted`
- `system_only_minimal`

Visibility must depend on:
- current verified life stage;
- memory class;
- purpose;
- valid Guardian/User authority;
- safety/legal constraints.

A memory being stored does not imply every authorized account may read it.

Guardian authority over visibility is governed by `GUARDIAN_AND_AUTONOMY_POLICY_V1.md`.

## Retention Model

Durable memory should have an intentional retention policy.

Possible retention semantics:
- session-only;
- short-term;
- until task/goal completion;
- periodic review;
- until superseded;
- long-term durable;
- until life-stage transition review;
- until user deletion;
- legally/safety required retention.

Do not default every memory to permanent retention.

## Expiry and Review

Memories that may become stale should support:
- `expires_at`;
- review date;
- stale status;
- superseded status;
- confidence/verification state;
- replacement by newer verified memory.

Expired or superseded memories should not silently continue shaping 小爱的 behavior as if they were current truth.

## Correction Rule

When the user corrects a remembered fact:
- do not preserve both versions as equally valid;
- mark or replace the old memory;
- keep only the minimum audit/provenance needed where implementation requires it;
- use the corrected/current version for normal interaction.

Sensitive incorrect memories should be corrected promptly and should not remain visible in normal retrieval.

## Deletion Rule

Where policy and law allow, the user should be able to request deletion of personal memories.

Deletion should remove the memory from active retrieval and prevent continued behavioral use.

If limited retention is legally/safety required, the system must distinguish:
- active companion memory;
- restricted compliance/safety retention.

Do not pretend data is fully deleted if a required restricted copy still exists.

## Guardian Access / Deletion Boundary

This policy defines what memory operations are possible; it does not independently grant Guardian authority.

During childhood, Guardian rights to access, review, or delete memory must be determined by `GUARDIAN_AND_AUTONOMY_POLICY_V1.md` and applied per memory class and purpose.

A Guardian should not automatically gain unrestricted authority over all private memories merely by being Guardian.

High-risk/safety data, account administration data, and basic child-profile data may have different rules from private conversational memory.

## Life-Stage Transition Trigger

`LIFE_STAGE_POLICY_V1.md` owns **when** a verified stage transition occurs.

When that transition occurs, this Memory Policy owns **how memory is reviewed and transformed**.

A life-stage transition should trigger a memory review rather than an automatic full reset or automatic carry-forward.

## Memory Transition Outcomes

During a major life-stage transition, memories may be classified into outcomes such as:
- `retain`
- `retain_private_to_user`
- `summarize`
- `expire`
- `delete`
- `requires_user_review`

The appropriate outcome depends on:
- memory class;
- current relevance;
- sensitivity;
- ownership/privacy expectations;
- Guardian/User authority;
- legal/safety constraints.

The stage transition itself does not decide the outcome; this policy does.

## Child Memory Treatment

During childhood:
- avoid blanket transcript surveillance;
- normal private conversation should not automatically become Guardian-visible;
- ordinary emotional disclosures should not automatically be escalated;
- sensitive child memory should have stronger restrictions than basic preferences;
- safety disclosure should use minimum-necessary information.

小爱 must not promise absolute secrecy, but should not treat the Guardian as automatically entitled to every memory.

## Teen Memory Treatment

When `LIFE_STAGE_POLICY_V1.md` verifies entry into the teen stage, the memory system should support progressively stronger user control over:
- visibility;
- correction;
- deletion requests;
- selected non-sensitive preferences;
- selected memories becoming user-private.

Guardian visibility may narrow only where the Guardian/Autonomy policy and applicable law permit.

## Young-Adult Memory Ownership Review

When `LIFE_STAGE_POLICY_V1.md` verifies entry into young adulthood, trigger an explicit memory ownership review.

The review should consider whether childhood memories should:
- remain durable;
- become user-private;
- be summarized;
- expire;
- be deleted;
- require explicit user confirmation.

Sensitive childhood memories must not simply carry forward with childhood Guardian visibility intact.

## Adult Memory Ownership

For an adult user:
- the user is the primary memory owner/controller by default;
- former Guardian visibility does not continue automatically;
- the user should be able to review, correct, delete, and manage durable personal memories where product/legal constraints permit;
- delegated access should require explicit ongoing authorization.

The transition into adulthood is determined by `LIFE_STAGE_POLICY_V1.md`; the memory ownership effects are governed here.

## Memory Portability Across Life Stages

小爱的 identity should remain continuous while memory treatment evolves.

Preferred transition pattern:

`Verified stage transition -> memory review -> retain useful continuity -> narrow/adjust visibility -> remove stale/sensitive excess -> confirm ownership -> continue same companion identity`

Do not force the user to lose the entire relationship history merely because they reached a new stage.

## Growth-Safety Boundary for Memory

This policy owns memory handling. `GROWTH_SAFETY_BASELINE_V1.md` owns the anti-dependency and relationship-health principles that constrain how remembered information may be used.

Memory must never be used to intentionally exploit emotional weaknesses, create exclusivity, or maximize dependency.

Forbidden uses include:
- using fears to increase engagement;
- reminding the user of vulnerable disclosures to pressure them;
- using loneliness to discourage human relationships;
- selectively surfacing sensitive memories to manipulate choices;
- creating secret persuasion profiles from private emotional history.

Memory should help 小爱 understand and support the user, not control them.

## Safety Memory Principle

Safety-related persistence must remain purpose-limited.

A safety event should not permanently redefine the user.

Do not turn one distress episode into a permanent label or risk identity unless repeated verified evidence and an explicit safety model justify a durable conclusion.

Safety escalation authority remains governed by `GUARDIAN_AND_AUTONOMY_POLICY_V1.md`.

## Memory Learning Rule

小爱 may learn from durable memory, but learning is subordinate to:
- current verified facts;
- user corrections;
- life-stage policy;
- Guardian/Autonomy policy;
- Growth Safety;
- safety/privacy constraints;
- XiaoE Core Governance.

Memory cannot grant itself additional permissions.

## Data Minimization Rule

For any durable memory:

`Store the smallest useful fact, not the largest available record.`

Prefer:
- "prefers visual explanations"
over
- complete transcripts of every conversation where visual explanations helped.

Prefer:
- "working toward school presentation confidence"
over
- storing all related emotional conversation history.

## Auditability

When memory is implemented, sensitive or high-impact memory changes should be reviewable through minimal metadata such as:
- memory class;
- source/provenance;
- created/updated time;
- visibility;
- retention status;
- verification state;
- approval reference when required;
- superseded/deleted state.

Audit metadata must not become a second hidden transcript store.

## Implementation Boundary

This v1 is policy only.

Do not yet create:
- memory database tables;
- vector embeddings;
- transcript archive;
- background retention workers;
- Guardian memory dashboard;
- export/download system;
- automated age-transition memory jobs;
- cross-project shared memory;
- autonomous memory migration from XiaoE Core.

Implementation requires separate architecture and explicit approval.

## Policy Dependencies

Primary references:
- `PROJECT_IDENTITY.md`
- `LIFE_STAGE_POLICY_V1.md`
- `GUARDIAN_AND_AUTONOMY_POLICY_V1.md`
- `GROWTH_SAFETY_BASELINE_V1.md`
- `POLICY_OWNERSHIP_MAP_V1.md`

## Current State

`ACTIVE — MEMORY/PRIVACY OWNER = CLASSIFICATION + RETENTION + VISIBILITY + DELETION + TRANSITION TREATMENT`
