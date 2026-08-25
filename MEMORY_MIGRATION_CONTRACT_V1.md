# Daughter Memory Migration Contract v1

Status: ACTIVE MIGRATION DESIGN / NOT EXECUTED
Date: 2026-08-25
Project: `daughter-companion-ai`

## Purpose

Define how Daughter / 小爱 memory moves safely between runtimes, Supabase projects, accounts, devices, future apps, and eventually physical embodiments without losing identity continuity, privacy, deletion state, provenance, or access rules.

Migration is not a raw database copy.
It is a governed transfer of identity-linked memory state.

Canonical principle:

`同一个小爱，可以换环境；同一段记忆，必须连同来源、权限、删除状态和版本一起迁移。`

## 1. Migration Scope

A complete memory migration package must preserve at least:

- `subject_id`
- `memory_entities`
- `memory_revisions`
- `memory_sources`
- `memory_access_rules`
- `memory_tombstones`
- `memory_storylines`
- `memory_storyline_links`
- relevant `subject_account_links`
- required audit/version metadata

Optional/non-authoritative items may include:
- derived caches
- embeddings
- retrieval indexes
- analytics summaries

Derived/cache data may be regenerated.
Authoritative memory state must not be reconstructed from caches alone.

## 2. Identity Continuity

`subject_id` is the continuity anchor.

Rules:
1. The child keeps the same logical `subject_id` across runtime migration.
2. New environment/account/device does not create a new child identity merely because authentication provider identifiers change.
3. Account linkage may change; memory subject identity does not.
4. Migration must preserve provenance showing which original runtime/account produced each source event.

## 3. Secrets Are Never Migrated as Memory

Do not include:
- Supabase secret keys
- service-role credentials
- publishable keys
- JWT signing secrets
- database passwords
- environment secrets
- API tokens
- raw auth session tokens

Target environment receives its own credentials.

`Memory migration != infrastructure-secret migration.`

## 4. Migration Package Manifest

Every export must include a manifest.

Suggested fields:
```text
package_version
schema_version
source_runtime_id
source_environment
source_project_ref_hash_or_alias
subject_id
exported_at
export_mode
record_counts
highest_revision_versions
highest_tombstone_versions
retention_policy_version
access_policy_version
checksum_algorithm
content_checksums
package_checksum
```

Never include raw infrastructure secrets in the manifest.

## 5. Export Modes

### 5.1 Full migration
Used when moving the authoritative memory runtime.

Includes all authoritative memory state required for continuity.

### 5.2 Subject-only migration
Exports one child subject and all dependent authoritative records.

### 5.3 Incremental migration
Transfers only records newer than an agreed checkpoint/version.

Incremental migration must still carry any newer tombstones and access-rule restrictions.

### 5.4 Backup/export
May be non-cutover and read-only.
Must be labeled clearly so it is not accidentally treated as new authority.

## 6. Freeze / Quiesce Rule

For final authoritative cutover, source runtime should enter a controlled migration state.

Preferred sequence:
1. announce migration session internally
2. stop or queue new authoritative memory writes
3. record migration checkpoint/version
4. export authoritative package
5. verify checksums
6. import target
7. run validation
8. switch authority only after validation passes

If a full write freeze is impossible, use versioned dual-run/delta reconciliation, not silent last-write-wins copying.

## 7. Import Order

Recommended dependency-aware import order:

1. validate package manifest/version/checksums
2. establish/verify target `subject_id`
3. import subject/account linkage mappings required for authorization
4. import `memory_entities`
5. import `memory_revisions`
6. import `memory_sources`
7. import `memory_access_rules`
8. import `memory_tombstones`
9. import storylines and storyline links
10. import migration/audit metadata
11. rebuild derived indexes/caches/embeddings
12. run consistency checks

Important:
Even if tombstones are physically inserted after entity rows due to FK dependencies, their versions must win over older active states before retrieval is enabled.

## 8. Tombstone Supremacy

Deletion protection is release-critical.

Rules:
- newer tombstone always outranks older create/update
- deleted memory must not become active because target imported stale active entity state
- stale devices/accounts must not resurrect deleted memory after cutover
- tombstone version/checkpoint must migrate with the memory
- restore is a new explicit authorized operation, not implicit resurrection

Invariant:
`migration must preserve forgetting.`

## 9. Retention / Retrieval / Disclosure Preservation

Migration must preserve all three independently:

### Retention
- active / deleted / protected / pinned state
- retention class
- child-pinned state

### Retrieval
- internal reasoning use
- proactive surface allowance
- on-request allowance

### Disclosure
- subject-only
- specific account restrictions
- guardian-shared rules
- restricted-sensitive rules

Migration must never convert nuanced access rules into a simple `visible=true` default.

If target cannot represent an existing restriction exactly:
- fail closed
- choose the more restrictive safe state
- flag migration for review
- do not silently broaden access

## 10. Account Remapping

Account IDs may differ between source and target.

Therefore:
- do not use target auth account IDs as the child identity
- build an explicit remapping table during migration
- preserve original source account IDs in provenance metadata when useful
- create new target account-link rows only after identity verification

Example:
```text
source father account A -> target father account F2
source mother account B -> target mother account M2
subject_id remains unchanged
```

## 11. Provenance Preservation

Every migrated memory must preserve enough provenance to answer:
- who originally said/reported this?
- when?
- was it child-direct, guardian-direct, system-observed, verified, corrected, or migrated?
- which revision is current?

Migration itself adds provenance; it does not erase old provenance.

Suggested source event:
`source_type = migration`
with link to original source/revision identifiers.

## 12. Revision Integrity

Rules:
- revision numbers remain monotonic
- target must not renumber in a way that loses conflict ordering
- current revision pointer must resolve to the intended effective version
- correction history remains immutable
- duplicate retry must remain idempotent

## 13. Schema Version Compatibility

Migration package and target schema must declare versions.

Possible states:
- compatible same version
- compatible upgrade path
- incompatible / manual transformation required

Do not import blindly across incompatible schema generations.

Every transformation must be:
- versioned
- deterministic
- testable
- auditable

## 14. Validation Before Cutover

At minimum verify:

### Count integrity
- subject count
- entity count
- revision count
- source count
- access-rule count
- tombstone count

### Referential integrity
- every current revision exists
- every source references valid memory/revision
- every access rule references valid subject/memory
- every storyline link resolves

### State integrity
- no deleted memory appears active
- no pinned flag lost
- no privacy rule broadened
- no duplicate subject identity created
- current revisions match expected versions

### Behavioral validation
Run blocker tests for:
- child-only private memory
- guardian restricted memory
- on-request-only memory
- reasoning-only memory
- child-pinned memory
- deleted memory
- corrected memory
- cross-account retrieval

## 15. Cutover Rule

Target becomes authoritative only when:
- import validation passes
- checksums/counts reconcile
- blocker tests pass
- authorization/account mapping passes
- retrieval/disclosure behavior passes
- no stale-resurrection risk remains

Then:
1. mark target authoritative
2. switch clients/runtime endpoints
3. keep source read-only for defined rollback window if policy permits
4. prevent dual-authoritative writes

## 16. Rollback

If cutover fails:
- target remains non-authoritative
- source stays authoritative if safe
- imported target data must not leak into production responses
- retry uses the same or later migration checkpoint
- migration logs record failure reason

Never merge partially validated target writes back into source automatically.

## 17. Dual-Run / Delta Reconciliation

If source cannot freeze completely:
- assign monotonic versions or event sequence IDs
- export checkpoint C
- import up to C
- capture delta > C
- replay delta in order
- apply tombstones/restrictions before activating retrieval
- verify no conflicting dual-authoritative writes

Last-write-wins by timestamp alone is not sufficient for deletion/privacy semantics.

## 18. Staging -> Production

For Daughter staging to production:

Preferred approach:
1. rebuild production schema from GitHub migrations
2. verify RLS/RPC/security first
3. migrate only approved subject memory data
4. remap accounts explicitly
5. validate Retention/Retrieval/Disclosure
6. run blocker suite
7. cut over only after pass

Do not clone staging secrets or experimental auth state into production.

## 19. Future Runtime / Robot Migration

A future device or physical robot may become a new runtime endpoint.

Identity continuity still depends on:
- same logical subject
- compatible memory contract
- preserved provenance
- preserved tombstones
- preserved access/privacy rules
- explicit runtime authorization

Physical embodiment does not automatically gain broader memory authority.

`Capability migration != Authority migration.`

## 20. Migration Blockers

Any of the following blocks migration cutover:

1. subject identity mismatch
2. lost tombstone
3. deleted memory becomes active
4. disclosure broadens silently
5. child-pinned state lost
6. provenance flattened or lost
7. current revision ambiguous
8. duplicate subject identity created
9. target cannot represent required privacy restriction
10. account remapping unresolved
11. checksum/count mismatch unexplained
12. dual-authoritative write risk remains
13. stale client can resurrect old state
14. source/target schema incompatibility unresolved
15. migration requires copying infrastructure secrets

## 21. Migration Test Requirements

Before production migration, executable tests must cover:
- exact subject continuity
- full and incremental export/import
- duplicate import idempotency
- delete before migration
- delete during migration
- correction before migration
- privacy tightening before migration
- account remapping
- revoked account
- stale old client replay
- target rollback
- failed checksum
- missing tombstone
- missing access rule
- incompatible schema version
- storylines with restricted source memories

## Canonical Principle

`迁移不是把资料搬过去，而是把“同一个孩子的记忆状态”完整、可验证、可回滚地交给新的运行环境。`
