# XiaoAi Memory v2 Legacy Compatibility Contract

Status: ACTIVE ARCHITECTURE CONTRACT
Purpose: rebuild long-term memory as an independent v2 system while preserving compatibility with useful legacy memory semantics.

## 1. Core decision

Memory v2 is the only future primary memory system.
Legacy memory is not a runtime dependency.

Canonical runtime path:

`XiaoAi Runtime -> Memory v2 Bridge -> Memory v2 API -> Memory v2 Store`

Forbidden future runtime path:

`XiaoAi Runtime -> Legacy Memory -> Memory v2`

## 2. Legacy memory role

Legacy memory may only be used as:
- read-only migration source;
- historical reference during migration review;
- compatibility input for field mapping;
- rollback evidence during the migration window.

Legacy memory must not be required for:
- new writes;
- ordinary retrieval;
- child-pinned storage;
- runtime identity;
- authorization;
- safety decisions;
- current response generation after v2 cutover.

## 3. Compatibility principle

Compatibility means preserving useful meaning, not preserving old implementation coupling.

Where legacy records provide equivalent concepts, Memory v2 should preserve or map:
- summary / human-readable meaning;
- category or memory kind;
- source / provenance;
- confidence;
- sensitivity;
- status;
- timestamps;
- daughter/subject relationship where verifiable.

Memory v2 may add stronger fields that did not exist previously, including:
- child_pinned;
- retention_class;
- disclosure scope;
- retrieval policy;
- immutable revisions;
- tombstones;
- audit trail;
- supersession links;
- idempotency protection.

## 4. Migration direction is one-way

Allowed:
`Legacy -> reviewed mapping -> Memory v2`

Not allowed:
`Memory v2 -> Legacy`

Not allowed:
- dual-write as the default architecture;
- automatic synchronization back into legacy tables;
- fallback to legacy when v2 has no result;
- silent merge of conflicting legacy and v2 records.

## 5. Legacy access after v2 cutover

After v2 is verified:
- legacy memory becomes `retired_read_only`;
- no new legacy writes;
- legacy records are excluded from normal XiaoAi context assembly;
- migration tools may access legacy only through an explicit migration path;
- runtime must continue functioning if legacy storage is unavailable.

## 6. Memory v2 activation posture

Initial v2 state remains:

`durable_memory_mode = off`

Future first enabled mode:

`durable_memory_mode = child_pinned_only`

In `child_pinned_only` mode, a durable write requires all of:
- verified child-direct source;
- intent class `long_term_memory_create`;
- sufficiently clear intent;
- valid subject/account relationship;
- privacy and sensitivity checks;
- idempotency key;
- active Memory v2 transport.

Ordinary conversation and inferred candidates do not become durable memory automatically.

## 7. Migration safety

No legacy record is migrated merely because it exists.

Each migrated record should be one of:
- accepted_as_is;
- normalized;
- corrected;
- superseded;
- rejected;
- held_for_review.

Migration should preserve provenance and must not rewrite a guardian/system statement as `child_direct`.

## 8. Independence test

Memory v2 is considered independent only when all of the following are true:
- XiaoAi can start with legacy storage unavailable;
- child-pinned writes do not touch legacy tables;
- v2 retrieval does not query legacy tables;
- correction and deletion operate only on v2 records;
- v2 permission checks do not depend on legacy memory rows;
- disabling legacy access does not break XiaoAi runtime;
- all future migrations target v2 only.

## 9. Decommission rule

Legacy memory must not be deleted during initial cutover.

Recommended lifecycle:
`active_legacy -> read_only_legacy -> retired_read_only -> archived_or_removed_later`

Deletion, if ever chosen, is a separate explicit operation after migration verification and backup/recovery review.

## Canonical rule

`兼容旧记忆的意义，不依赖旧记忆的系统。`
