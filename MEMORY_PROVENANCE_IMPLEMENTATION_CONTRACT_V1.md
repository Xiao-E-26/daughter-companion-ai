# 小爱 / Daughter Companion AI — Memory Provenance Implementation Contract v1

Status: ACTIVE IMPLEMENTATION CONTRACT
Date: 2026-08-24
Project: `daughter-companion-ai`
Policy owner: `MEMORY_AND_PRIVACY_POLICY_V1.md`
Behavior freeze: `BEHAVIOR_FREEZE_BASELINE_V1.md`

## Purpose

Define the minimum implementation metadata and decision rules required for durable memory so that continuity does not become fabrication, surveillance, stale-profile lock-in, or cross-account leakage.

This contract does not change memory policy. It translates policy into implementation requirements.

## Core Rules

`Continuity != fabricated memory`

`Conversation != durable memory`

`Newer statement != automatically more trustworthy`

`Sensitive memory != proof of relationship`

`Remember the smallest useful verified fact`

## Required Memory Record Fields

Every durable memory record must carry, at minimum:

- `memory_id`
- `subject_id`
- `memory_class`
- `content_summary`
- `source_account_id`
- `source_session_id`
- `source_channel`
- `source_timestamp`
- `created_at`
- `updated_at`
- `verification_status`
- `confidence`
- `sensitivity_level`
- `visibility_scope`
- `retention_rule`
- `superseded_by`
- `status`
- `policy_version`

Optional but recommended:
- `source_message_ref`
- `guardian_visibility_override` when policy permits
- `expiry_at`
- `review_after`
- `derived_from_memory_ids`
- `reason_for_storage`

## Verification Status

Use an explicit state, not a boolean:

- `unverified`
- `self_reported`
- `guardian_reported`
- `system_observed`
- `verified`
- `conflicted`
- `superseded`

Runtime must not flatten all sources into the same truth value.

## Sensitivity Levels

Implementation should support at least:

- `M1_LOW` — ordinary preference, harmless continuity fact
- `M2_MODERATE` — relationship or routine context that may matter over time
- `M3_SENSITIVE` — health, family conflict, emotional vulnerability, safety-relevant private information
- `M4_RESTRICTED` — exceptionally sensitive information requiring narrow visibility and strong purpose limitation

Exact mapping remains governed by Memory/Privacy policy.

## Visibility Scope

Every durable memory must declare who may access it.

Minimum scopes:
- `subject_only`
- `shared_companion_runtime`
- `guardian_limited`
- `safety_limited`
- `system_internal_restricted`

Do not use `all_accounts` as a default scope.

## Cross-Account Rule

A memory may be available across linked accounts only when:
1. the identity link is verified;
2. the memory visibility permits shared runtime use;
3. the requesting runtime has legitimate purpose;
4. the memory is not stale/superseded/conflicted without handling;
5. disclosure does not violate Guardian/privacy boundaries.

Cross-account continuity should prefer shared minimal memory over transcript replication.

## Conflict Handling

When two memory records conflict:

`detect conflict -> preserve both provenance chains -> mark conflict -> assess recency/source/verification/context -> ask only if materially needed -> resolve or keep unresolved`

Never silently overwrite a safety-relevant fact merely because a newer account said something different.

Never silently retain a stale harmless preference after the user clearly updates it.

## Supersession

When a current verified fact replaces an older fact:
- do not delete provenance immediately;
- mark older record `superseded` when appropriate;
- link via `superseded_by`;
- prevent ordinary retrieval from treating superseded value as current truth;
- preserve auditability where required.

Example:
`favorite_color = blue` -> later verified `favorite_color = red`

Current response should use red; blue remains historical, not current.

## Retrieval Contract

Memory retrieval must be purpose-limited.

Before returning a memory to Runtime, evaluate:
- relevance to current goal;
- visibility scope;
- sensitivity;
- current status;
- freshness;
- conflict state;
- whether surfacing it is necessary.

Do not retrieve sensitive memories merely to make 小爱 sound familiar.

## Anti-Fabrication Rule

If memory is unavailable, incomplete, or inaccessible:
- say naturally that the detail is not currently available when needed;
- do not invent continuity details;
- do not infer a specific event from relationship familiarity.

## Logging / Audit

Recommended audit events:
- memory_created
- memory_read_sensitive
- memory_updated
- memory_superseded
- memory_visibility_changed
- memory_deleted
- conflict_detected
- conflict_resolved

Audit logs must not themselves become an uncontrolled transcript archive.

## Data Minimization

Prefer:
`useful conclusion -> minimal structured memory`

Avoid:
`raw full transcript -> permanent storage by default`

## Deletion / Correction

Implementation must support:
- correction;
- supersession;
- deletion where policy allows;
- restricted retention where safety/legal requirements apply;
- propagation of deletion/correction to derived indexes or caches where feasible.

## Failure Conditions

Implementation FAIL if:
- memory exists without source provenance;
- stale memory is presented as current despite verified correction;
- sensitive memory is surfaced solely to prove continuity;
- cross-account access ignores visibility scope;
- transcript is treated as default durable memory;
- memory conflict is silently merged into false certainty;
- system fabricates missing memory.

## Current State

`ACTIVE — MEMORY PROVENANCE IMPLEMENTATION CONTRACT V1`
