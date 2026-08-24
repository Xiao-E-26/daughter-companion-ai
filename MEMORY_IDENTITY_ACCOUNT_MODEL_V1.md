# Daughter Memory Identity & Account Model v1

Status: ACTIVE IMPLEMENTATION DESIGN
Date: 2026-08-25
Project: `daughter-companion-ai`

## Purpose

Define the minimum identity model required before persistent Daughter Memory can safely support multiple ChatGPT accounts, devices, apps, and future embodiments.

Core invariant:

`The child is the memory subject. Accounts are access contexts, not identity containers.`

## 1. Subject Identity

A single stable `subject_id` represents the child whose memory is being stored.

The `subject_id` must remain stable across:
- father ChatGPT account
- mother ChatGPT account
- future child account
- app sessions
- devices
- future robot/embodiment

Accounts must never create separate child identities merely because authentication differs.

## 2. Account Identity

Each connected account receives its own `account_id` and authentication binding.

Conceptual fields:

```text
account_id
provider
provider_user_id
account_role
status
linked_subject_id
linked_at
revoked_at
```

Recommended initial roles:
- `guardian_father`
- `guardian_mother`
- `child_self`
- `system_runtime`
- `review_admin` (future, tightly restricted)

Role names are governance labels, not proof of factual correctness.

## 3. Relationship Mapping

Use a subject-account relationship object rather than embedding ownership into memory rows.

Conceptual mapping:

```text
subject_account_links
- subject_id
- account_id
- role
- can_view_general_memory
- can_view_sensitive_memory
- can_submit_candidates
- can_request_correction
- can_request_deletion
- can_manage_linkage
- status
```

Exact permissions may later be normalized into policies.

## 4. Identity Continuity

The memory identity belongs to the child, not to Dad's account, Mum's account, or ChatGPT.

Therefore:
- moving to another account must not duplicate memory
- revoking an account must not delete the child's memory identity
- adding an account must not expose all memory by default
- embodiment migration must preserve `subject_id`

## 5. Source Identity

Every assertion/event must preserve who supplied it.

Conceptual source fields:

```text
source_actor_id
source_account_id
source_role
source_type
source_ref
observed_at
```

Examples:
- child said something directly on Dad's account
- Mum reported a school event
- Dad reported a family trip
- system observed repeated pattern across sessions

The account through which a statement arrived is provenance, not truth authority.

## 6. Child Self-Report Priority

For internal states such as:
- likes/dislikes
- feelings
- goals
- fears
- preferences
- meaning of an event

child self-report should generally carry the strongest interpretive weight, subject to age, context, safety, and contradictions.

Guardian reports remain important but should not silently overwrite the child's own internal-state report.

## 7. Cross-Account Synchronization

All approved account contexts should resolve to the same `subject_id`.

Sync behavior:
- new memory candidate created on Dad account -> visible to runtime as same subject
- Mum account later adds related event -> same subject, same candidate/storyline space
- duplicates should consolidate
- conflicting sources should retain provenance

## 8. Visibility Boundary

Shared subject identity does NOT imply shared visibility.

Each memory object must be filtered by:
- subject
- viewer account
- viewer role
- sensitivity
- visibility class
- explicit access policy

Recommended visibility classes:
- `subject_private`
- `shared_guardian_safe`
- `restricted_sensitive`
- `system_only`
- `review_required`

## 9. Guardian Separation

Father and mother are separate viewers and sources.

The system must support:
- both linked to same child
- different source provenance
- different disclosure rights if policy requires
- contradictory reports without destructive overwrite

No guardian account should become the technical owner of all memory rows.

## 10. Future Child Account

When a child-facing account is introduced:
- it should bind to the existing `subject_id`
- it should not create a new memory identity
- child privacy settings may evolve with age and governance
- historical memory access may be age/context controlled

The design should allow future rights to increase without rewriting all memory ownership.

## 11. Account Revocation

If an account is removed:
- revoke the subject-account link
- stop retrieval/write from that account
- preserve existing provenance history
- do not rewrite historical source records as if another account supplied them

## 12. Account Replacement / Migration

If Dad or Mum changes ChatGPT account:
- authenticate new account
- verify guardian continuity through governance process
- link new `account_id` to same `subject_id`
- revoke or retain old account according to policy

Memory itself should not be copied into a new subject.

## 13. Device vs Account

Devices are not identity.

A device may carry:
- device_id
- session_id
- account_id

but memory access still resolves through authenticated account + subject relationship.

## 14. Embodiment Migration

A future robot or embodied runtime should receive a runtime identity, not become the memory owner.

`subject_id` remains the child.
`runtime_id` identifies the acting system instance.

Capability migration does not automatically migrate permissions.

## 15. Minimal Initial Model

For a first backend, the smallest identity set is:

1. `memory_subjects`
2. `accounts`
3. `subject_account_links`
4. source/provenance references on memory events

Avoid creating a large IAM framework before actual product roles require it.

## 16. Security Invariants

1. Account != subject.
2. Guardian != owner of child's memory identity.
3. Shared subject != universal visibility.
4. Source role != truth authority.
5. Revoked account loses access without erasing provenance.
6. Migration preserves subject continuity.
7. Memory != permission.
8. Runtime/device identity != child identity.

## Canonical Principle

`小爱的记忆跟着孩子，不跟着某一个 ChatGPT 账号。`
