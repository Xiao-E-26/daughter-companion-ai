# Daughter Memory RLS Test Matrix v1

Status: ACTIVE SECURITY TEST DESIGN
Date: 2026-08-25
Project: `daughter-companion-ai`

## Purpose

Define authorization tests that must pass before persistent Daughter Memory is deployed.

This matrix tests server-side access boundaries for multiple accounts linked to the same child subject.

Core invariant:

`Shared memory identity does not mean unrestricted shared visibility.`

## Roles Under Test

- Father guardian account
- Mother guardian account
- Child self account
- Daughter runtime/service identity
- Unauthorized external account
- Revoked former guardian account
- Future restricted reviewer/admin

## Data Classes Under Test

- general positive memory
- family shared memory
- learning/growth memory
- child-private memory
- restricted sensitive memory
- safety-relevant memory
- system-only audit data
- deleted/tombstoned memory
- superseded memory revision
- memory candidate not yet promoted

## A. Subject Boundary Tests

### RLS-001 Unauthorized account queries child memory
Expected: zero rows / denied.

### RLS-002 Account linked to another child queries this child
Expected: zero rows / denied.

### RLS-003 Father queries memory for linked child
Expected: only rows allowed by visibility policy.

### RLS-004 Mother queries same child
Expected: only rows allowed by visibility policy.

### RLS-005 Runtime queries subject for response generation
Expected: only data allowed to runtime purpose/context.

## B. General Shared Memory

### RLS-006 Father reads `shared_guardian_safe`
Expected: allowed.

### RLS-007 Mother reads same memory
Expected: allowed.

### RLS-008 Child reads age-appropriate own shared memory
Expected: allowed according to policy.

### RLS-009 Unauthorized viewer reads shared memory
Expected: denied.

## C. Child-Private Memory

### RLS-010 Father reads `subject_private`
Expected: denied unless an explicit policy exception exists.

### RLS-011 Mother reads `subject_private`
Expected: denied unless explicit policy exception exists.

### RLS-012 Child self reads own `subject_private`
Expected: allowed when product policy permits.

### RLS-013 Runtime reads child-private memory
Expected: purpose-limited; only if necessary for the current child interaction and policy allows.

## D. Restricted Sensitive Memory

### RLS-014 Guardian directly queries restricted sensitive row
Expected: denied by default unless explicitly authorized.

### RLS-015 Runtime retrieves sensitive memory for unrelated conversation
Expected: denied/not returned.

### RLS-016 Runtime retrieves sensitive memory for directly relevant support context
Expected: only if policy and purpose permit; access audited.

### RLS-017 Sensitive memory accidentally tagged shared
Expected: test should fail release; policy mismatch detected.

## E. Candidate Write Tests

### RLS-018 Father submits candidate about shared family event
Expected: allowed to submit candidate with father provenance.

### RLS-019 Mother submits candidate about school event
Expected: allowed to submit candidate with mother provenance.

### RLS-020 Child submits self-report candidate
Expected: allowed according to child account policy.

### RLS-021 External account submits candidate for child
Expected: denied.

### RLS-022 Guardian directly marks candidate as durable/promoted
Expected: denied unless reviewed-promotion role explicitly permits.

### RLS-023 Runtime silently self-promotes restricted sensitive candidate
Expected: denied.

## F. Provenance Protection

### RLS-024 Father edits source actor on mother's assertion
Expected: denied.

### RLS-025 Mother rewrites child's self-report provenance
Expected: denied.

### RLS-026 Runtime modifies immutable historical source attribution
Expected: denied except through explicit correction/revision mechanism.

## G. Correction & Revision

### RLS-027 Child requests correction to own internal-state memory
Expected: correction request allowed; original provenance preserved.

### RLS-028 Guardian updates a fact they originally supplied
Expected: new revision/correction path, not destructive overwrite.

### RLS-029 Guardian tries to overwrite another guardian's conflicting report
Expected: denied; add new provenance-bearing assertion instead.

### RLS-030 New verified fact supersedes old memory
Expected: allowed through controlled revision path.

## H. Deletion & Tombstones

### RLS-031 Authorized deletion request
Expected: logical deletion/tombstone created.

### RLS-032 Ordinary viewer reads tombstoned memory
Expected: not returned as active memory.

### RLS-033 Stale client writes old revision after deletion
Expected: rejected; no resurrection.

### RLS-034 Revoked account tries to restore deleted memory
Expected: denied.

### RLS-035 Reviewer accesses tombstone metadata
Expected: only if audit/review role permits.

## I. Revoked Account Tests

### RLS-036 Father account revoked, then reads memory
Expected: denied immediately.

### RLS-037 Revoked account submits candidate
Expected: denied.

### RLS-038 Revoked account remains historical source of prior memories
Expected: provenance preserved, but no active access.

## J. Account Replacement

### RLS-039 New verified father account linked to same subject
Expected: access according to new link policy; no duplicate subject.

### RLS-040 Old father account still active after explicit revoke
Expected: denied.

### RLS-041 Migration creates second child subject accidentally
Expected: release-blocking failure.

## K. Cross-Account Conflict

### RLS-042 Father and mother report contradictory external fact
Expected: both assertions retained; no silent overwrite.

### RLS-043 Guardian contradicts child's internal preference
Expected: both provenance entries may exist, but child self-report should remain primary interpretation for internal state.

### RLS-044 Account A asks runtime what child privately told Account B
Expected: disclosure filtered by visibility/authority; do not reveal solely because same subject is shared.

## L. Family Shared Memory

### RLS-045 Family trip marked `shared_guardian_safe`
Expected: both linked guardians can read.

### RLS-046 Family memory contains unrelated adult-sensitive detail
Expected: adult-sensitive detail excluded or separately restricted.

### RLS-047 Grandpa-related family memory has general positive context
Expected: shared according to family-memory visibility policy.

### RLS-048 Child explicitly marks a family memory private
Expected: future visibility follows child/private governance rules, not default family sharing.

## M. Positive 80/20 Portfolio

### RLS-049 Positive-memory bias attempts to bypass privacy
Expected: denied. Positive priority does not override access control.

### RLS-050 Challenge memory retained for coping/recovery
Expected: visibility still based on sensitivity, not portfolio category.

## N. Runtime / Service Role

### RLS-051 Runtime has direct unrestricted table access
Expected: release-blocking failure unless narrowly justified and separately protected.

### RLS-052 Runtime queries only current subject
Expected: allowed within purpose-bound scope.

### RLS-053 Runtime queries all subjects without explicit operational need
Expected: denied/restricted.

### RLS-054 Runtime writes audit event for memory decision
Expected: allowed with append-only semantics.

### RLS-055 Runtime edits past audit event
Expected: denied.

## O. Review/Admin

### RLS-056 Reviewer reads all raw child conversations
Expected: denied unless an exceptional, explicitly authorized workflow exists.

### RLS-057 Reviewer reads minimum candidate/audit metadata needed for review
Expected: allowed when assigned and logged.

### RLS-058 Reviewer changes memory without trace
Expected: denied; must create auditable revision.

## P. Fail-Closed Behavior

### RLS-059 Missing account-subject link
Expected: deny.

### RLS-060 Missing visibility metadata
Expected: deny/review-required, not public/shared by default.

### RLS-061 Unknown role value
Expected: deny.

### RLS-062 Policy evaluation error
Expected: deny and log.

### RLS-063 Missing provenance on write
Expected: reject write.

### RLS-064 Version mismatch on update
Expected: reject or explicit conflict path; no silent overwrite.

## Release Gate

Before production persistent memory, all critical RLS groups must pass against the real database:
- subject isolation
- guardian separation
- child-private visibility
- restricted sensitive visibility
- provenance immutability
- revision/correction path
- tombstone/no-resurrection behavior
- revoked account denial
- account migration continuity
- cross-account private disclosure
- runtime least privilege
- audit immutability
- fail-closed defaults

Any failure in these groups blocks production memory activation.

## Canonical Principle

`同一个孩子可以有多个入口，但每个入口看到什么、能做什么，必须由权限决定，而不是由“都是家人”来决定。`
