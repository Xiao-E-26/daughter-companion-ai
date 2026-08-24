# Daughter Memory Stage 1 Implementation Contract v1

Status: ACTIVE IMPLEMENTATION CONTRACT
Date: 2026-08-25
Project: `daughter-companion-ai`

Depends on:
- `MEMORY_SPEC_V1.md`
- `MEMORY_CANDIDATE_CONTRACT_V1.md`
- `MEMORY_ADVERSARIAL_TEST_PACK_V1.md`
- `MEMORY_ADVERSARIAL_TEST_V1_RESULTS.md`

## Purpose

Turn the existing Memory policy into a deterministic implementation contract without yet enabling persistent production writes.

Stage 1 objective:

`Conversation/Event -> Candidate Detector -> Deterministic Candidate Decision -> Audit Output`

Stage 1 does NOT include:
- unrestricted durable-memory writes
- sensitive auto-promotion
- production cross-account disclosure
- silent Authority changes
- direct persistence without auditability

## 1. Candidate Detector Input Contract

A detector invocation should receive a bounded input object conceptually containing:

```text
subject_id
actor_id
actor_role
account_context
conversation_or_event_excerpt
source_type
source_ref
observed_at
current_context_summary
relevant_existing_candidates[]
relevant_existing_memories[]
authority_context
```

### Required rules

- `subject_id` identifies whose memory is being considered.
- `actor_id` identifies who supplied or triggered the information.
- `actor_role` is context only and must not automatically imply truth.
- Raw transcript input should be minimized to what is necessary for the decision.
- Existing memory is advisory context, never stronger than current verified facts.
- Authority context is consulted for storage/disclosure permission but must not distort factual judgment.

## 2. Candidate Detector Output Contract

The detector must return one and only one primary decision state:

- `no_candidate`
- `candidate_pending`
- `candidate_hold`
- `candidate_rejected`
- `candidate_corrected`
- `candidate_superseded`

Conceptual output fields:

```text
decision
candidate_id_or_target_id
category
neutral_summary
confidence
sensitivity
stability
promotion_eligibility
reason_codes[]
source_refs[]
related_memory_ids[]
requires_review
visibility_class
revision_intent
audit_note
```

The output must be explainable from deterministic rules plus bounded model judgment.

## 3. Reason Codes

Recommended initial reason codes:

- `LOW_FUTURE_UTILITY`
- `ORDINARY_TRIVIA`
- `ONE_TIME_EMOTION`
- `IDENTITY_LABEL_RISK`
- `SPECULATIVE_DIAGNOSIS`
- `SPECULATIVE_MOTIVE`
- `GUARDIAN_INTERPRETATION_ONLY`
- `CHILD_DIRECT_CORRECTION`
- `VERIFIED_EVENT`
- `REPEATED_PATTERN`
- `EMERGING_PREFERENCE`
- `STABLE_PREFERENCE`
- `LEARNING_PROGRESS`
- `SENSITIVE_CONTEXT`
- `RELATIONSHIP_CONFLICT`
- `SAFETY_CONTEXT`
- `STALE_MEMORY`
- `NEWER_VERIFIED_FACT`
- `DUPLICATE_CANDIDATE`
- `DELETE_REQUEST`
- `AUTHORITY_REQUIRED`
- `VISIBILITY_RESTRICTED`

Reason codes should make test failures diagnosable instead of leaving only free-text explanations.

## 4. Deterministic Decision Rules

### Rule A — No candidate
Return `no_candidate` when the information is ordinary trivia, clearly momentary, or has no plausible future support value.

### Rule B — Reject
Return `candidate_rejected` when candidate formation itself would encode a harmful unsupported generalization, speculative diagnosis, identity label, or interpretation that cannot be neutrally represented.

### Rule C — Hold
Return `candidate_hold` when the information may matter but is sensitive, ambiguous, conflict-related, safety-related, or has insufficient evidence for durable consideration.

### Rule D — Pending
Return `candidate_pending` when the information has plausible future value, adequate provenance, neutral wording, acceptable sensitivity, and enough stability/evidence to deserve later review.

### Rule E — Corrected
Return `candidate_corrected` when a newer source materially clarifies or fixes the wording/factual content of an existing candidate without necessarily replacing the underlying memory identity.

### Rule F — Superseded
Return `candidate_superseded` when a newer verified fact makes the older candidate materially outdated or misleading.

## 5. Provenance Contract

Every candidate-affecting event must preserve provenance.

Minimum provenance fields:

```text
source_type
source_actor_id
source_actor_role
source_ref
observed_at
assertion_scope
verification_state
```

### Assertion scope

Recommended values:
- `self_report`
- `observed_behavior`
- `guardian_report`
- `verified_event`
- `system_inference`
- `correction`
- `outcome`

### Verification state

Recommended values:
- `unverified`
- `partially_verified`
- `verified`
- `disputed`
- `superseded`

No source role automatically grants `verified` state.

## 6. Conflict Contract

When sources conflict:

1. Do not overwrite provenance.
2. Do not flatten conflicting statements into a false consensus.
3. Preserve each assertion with source and scope.
4. Prefer direct statements for internal states such as likes, dislikes, feelings, and intentions when safe and contextually appropriate.
5. Prefer independently verified evidence for external facts.
6. Mark unresolved conflict as `disputed` or `hold`.
7. Current verified facts outrank old memory.

Example:

Guardian: `She hates piano.`
Child: `I like piano; I dislike being watched while practicing.`

Implementation result:
- guardian statement remains provenance-bearing context
- child statement corrects the preference interpretation
- durable candidate should become a support/context preference, not `hates piano`

## 7. Revision Model

Every future persistent candidate/memory must support immutable revision history plus current effective state.

Conceptual fields:

```text
entity_id
revision_id
revision_number
previous_revision_id
revision_type
created_at
created_by
reason_codes[]
content_snapshot
```

Recommended `revision_type` values:
- `create`
- `update`
- `correct`
- `supersede`
- `fade`
- `delete`
- `restore_by_authorized_review`

Normal sync must never create `restore_by_authorized_review` implicitly.

## 8. Tombstone Contract

Deletion must be represented as a durable tombstone/version state rather than physical disappearance alone when synchronization exists.

A tombstone should conceptually contain:

```text
entity_id
deleted_at
deleted_by
deletion_reason
revision_number
replication_state
```

Rules:
- a stale copy with lower revision must not resurrect the entity
- tombstone ordering must participate in conflict resolution
- physical purge, if later required, is separate from logical deletion
- legal/audit retention requirements may constrain purge but not active retrieval

## 9. Version Ordering Contract

A future implementation must use deterministic ordering.

Acceptable strategies may include:
- server-assigned monotonic revision numbers per entity
- globally ordered event sequence
- compare-and-swap using current revision/version

Minimum invariant:

`Older write must not silently overwrite newer effective state.`

Concurrent conflicts must be explicit and auditable.

## 10. Duplicate Consolidation Contract

The system should search relevant active candidates before creating a near-duplicate.

If semantically equivalent:
- strengthen recurrence/evidence
- update `last_seen_at`
- add provenance/source reference
- revise confidence/stability if justified

Do not create parallel memories merely because the same fact was mentioned again.

## 11. Access Boundary Contract

Storage identity and viewer visibility are separate concerns.

Every stored object should conceptually carry or resolve:

```text
subject_id
sensitivity
visibility_class
allowed_viewer_roles_or_policy
origin_account_context
```

Recommended visibility classes:
- `subject_private`
- `shared_guardian_safe`
- `restricted_sensitive`
- `system_only`
- `review_required`

Rules:
- shared backend != universal read access
- guardian role != automatic access to all sensitive child disclosures
- viewer authorization must be enforced server-side
- retrieval must filter before model exposure, not after
- cross-account sync must preserve visibility metadata

## 12. Authority Separation

Memory data must never grant current permission.

Examples:
- `Dad allowed this last month` is historical context, not current authorization.
- `Guardian previously approved device X` does not grant authority to device Y.
- migrated memory does not migrate permission unless Authority independently allows equivalent inheritance.

Canonical invariant:

`Memory != Authority`

## 13. Audit Contract

Every Stage 1 detector decision should produce an audit event conceptually containing:

```text
audit_id
detector_version
policy_version
subject_id
actor_context
input_hash_or_source_ref
decision
reason_codes[]
confidence
sensitivity
target_entity_id
created_at
```

Avoid storing unnecessary raw private transcript in audit logs.

Audit must support answering:
- Why was this candidate created?
- Why was it rejected/held?
- Which rule/version made the decision?
- Which source caused a correction?
- Why did an old memory stop being active?

## 14. Failure Behavior

If the detector is uncertain, malformed input is received, provenance is missing, or policy evaluation fails:

Default to the safer state:
- no durable promotion
- `candidate_hold` or `no_candidate`
- emit auditable error/uncertainty reason

Do not guess missing provenance.
Do not convert failure into automatic memory creation.

## 15. Idempotency

Repeated processing of the same source event should not create duplicated candidate entities.

A future implementation should use an idempotency key or equivalent derived from trusted event/source identity.

Minimum invariant:

`Same event retried -> same logical outcome, not duplicate durable state.`

## 16. Stage 1 Test Requirements

Before any database activation, implementation tests should cover at minimum:
- all 36 adversarial memory cases
- duplicate retries
- correction race
- delete vs stale update race
- conflicting guardian/child assertions
- stale memory vs newer verified fact
- visibility filter before retrieval
- sensitive hold behavior
- malformed provenance
- detector timeout/failure
- version mismatch
- idempotent retry

## 17. Stage 1 Activation State

As of 2026-08-25:

- policy specification: COMPLETE
- candidate contract: COMPLETE
- adversarial policy simulation: 36/36 PASS
- Stage 1 implementation contract: COMPLETE
- runtime candidate detector: NOT IMPLEMENTED
- persistent store: NOT IMPLEMENTED
- RLS/access enforcement: NOT IMPLEMENTED
- auto-promotion: OFF
- durable auto-memory: OFF

## 18. Next Gate

The next safe step is a **data model + RLS design review**, still without production activation.

That review should define the smallest possible schema for:
- memory candidates
- revisions
- provenance/evidence
- tombstones
- access policy mapping

Only after the schema can satisfy this contract and the adversarial test pack should Supabase migrations be written.

## Invariants

1. Candidate != truth.
2. Current verified fact > stale memory.
3. Memory != Authority.
4. Shared storage != shared visibility.
5. Deletion must survive synchronization.
6. Provenance must survive conflict.
7. Retry must not duplicate memory.
8. Failure must not promote memory.
9. Every effective state must be explainable.
10. The child is allowed to change.
