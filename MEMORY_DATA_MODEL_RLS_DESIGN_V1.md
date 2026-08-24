# Daughter Memory Data Model + RLS Design v1

Status: DESIGN REVIEW BASELINE — NOT DEPLOYED
Date: 2026-08-25
Project: `daughter-companion-ai`

Depends on:
- `MEMORY_STAGE1_IMPLEMENTATION_CONTRACT_V1.md`
- `MEMORY_SPEC_V1.md`
- `MEMORY_CANDIDATE_CONTRACT_V1.md`

## Purpose

Define the smallest Supabase/Postgres data model capable of supporting governed candidate memory, revisions, provenance, tombstones, and cross-account visibility without enabling production persistence yet.

This file is a design contract only. No migration has been applied.

## Design Goals

The model must support:
- candidate-first memory
- provenance preservation
- correction/supersession
- duplicate consolidation
- logical deletion/tombstones
- version ordering
- cross-account visibility boundaries
- auditability
- future durable promotion

It must NOT assume:
- every guardian can read every child memory
- memory grants Authority
- raw transcripts should be stored wholesale
- one table is enough for all concerns

## Minimal Entities

### 1. `memory_entities`
Represents the logical memory/candidate identity across revisions.

Conceptual columns:

```sql
id uuid primary key
subject_id uuid not null
category text not null
entity_kind text not null -- candidate | durable
current_revision_id uuid null
status text not null -- pending | hold | rejected | promoted | superseded | deleted
sensitivity text not null
visibility_class text not null
created_at timestamptz not null
updated_at timestamptz not null
```

Purpose:
- stable logical identity
- current effective pointer
- top-level filtering metadata

### 2. `memory_revisions`
Immutable snapshots of content changes.

```sql
id uuid primary key
entity_id uuid not null references memory_entities(id)
revision_number bigint not null
previous_revision_id uuid null
revision_type text not null
neutral_summary text null
confidence text null
stability text null
promotion_eligibility text null
reason_codes text[] null
created_by_actor_id uuid null
created_by_role text null
created_at timestamptz not null
is_tombstone boolean not null default false
```

Constraint:
- unique `(entity_id, revision_number)`

Purpose:
- correction history
- supersession
- deletion/tombstone state
- stale-write prevention

### 3. `memory_sources`
Stores provenance/evidence references without requiring full raw transcript retention.

```sql
id uuid primary key
entity_id uuid not null references memory_entities(id)
revision_id uuid null references memory_revisions(id)
source_type text not null
source_actor_id uuid null
source_actor_role text null
source_ref text null
assertion_scope text null
verification_state text not null
observed_at timestamptz null
created_at timestamptz not null
```

Purpose:
- preserve who asserted what
- support disputes/corrections
- avoid flattening conflicting sources

### 4. `memory_access_rules`
Maps viewer contexts to memory visibility.

```sql
id uuid primary key
entity_id uuid not null references memory_entities(id)
viewer_subject_id uuid null
viewer_account_id uuid null
viewer_role text null
access_level text not null -- none | metadata | read | review
created_at timestamptz not null
revoked_at timestamptz null
```

Purpose:
- separate storage from visibility
- allow subject-private / restricted-sensitive behavior

### 5. `memory_audit_events`
Append-only audit trail.

```sql
id uuid primary key
entity_id uuid null
revision_id uuid null
action text not null
actor_id uuid null
actor_role text null
policy_version text null
detector_version text null
reason_codes text[] null
source_ref text null
created_at timestamptz not null
```

Purpose:
- explain why state changed
- debug unexpected promotion/deletion/access

## Why Not One Table

A single-table design would mix:
- logical identity
- mutable current state
- immutable history
- provenance
- access control
- audit events

That would make correction, sync conflict, tombstones, and privacy enforcement harder to reason about and easier to break.

## Current-State Pointer

`memory_entities.current_revision_id` should always point to the effective revision.

State change sequence conceptually:
1. lock/read current entity revision
2. validate expected current revision
3. append new revision
4. update current_revision_id atomically
5. append audit event

This prevents blind last-write-wins updates.

## Version / Concurrency Rule

Use compare-and-swap semantics.

Mutation request should include:

```text
expected_revision_number
```

If the database current revision differs:
- reject with conflict
- caller must reload and reassess

Do not silently overwrite.

## Tombstone Rule

Deletion creates a new revision:
- `revision_type = delete`
- `is_tombstone = true`
- entity status becomes `deleted`

RLS/retrieval must exclude deleted entities from normal reads.

A stale writer with an older expected revision cannot resurrect the entity.

Physical purge is a separate admin/legal-retention operation.

## Duplicate Consolidation

Before candidate creation, runtime should query active relevant candidates for the same subject/category.

Possible supporting index:

```sql
(subject_id, category, status)
```

Semantic duplicate detection remains application logic, but database idempotency should use a trusted event key where available.

Optional future column/table:

```text
source_event_key unique per subject/source namespace
```

## Visibility Classes

Recommended classes:

- `subject_private`
- `shared_guardian_safe`
- `restricted_sensitive`
- `system_only`
- `review_required`

Default should be restrictive, not broad.

## RLS Principles

All memory tables should have RLS enabled.

### Principle 1 — Deny by default
No anonymous broad SELECT/INSERT/UPDATE/DELETE.

### Principle 2 — Subject scope first
Every read/write path must resolve the active subject identity.

### Principle 3 — Viewer scope second
Viewer/account context determines whether a row is visible.

### Principle 4 — Sensitive rows require stronger policy
Guardian role alone is insufficient for unrestricted access to `restricted_sensitive` or `subject_private` memory.

### Principle 5 — Revisions inherit entity visibility
A user must not bypass entity visibility by querying revisions directly.

### Principle 6 — Sources inherit entity visibility
Provenance rows may be more sensitive than the summary and must not be broadly readable.

### Principle 7 — Audit is not ordinary user data
Audit visibility should be restricted to authorized system/admin/review contexts.

## Conceptual RLS — `memory_entities`

Read allowed only when one of these is true:
- viewer is the subject and policy permits subject access
- active `memory_access_rules` grants viewer/account/role read/review
- authorized system service is performing bounded runtime retrieval

Normal guardian visibility should be mediated by explicit rules or safe-class policy, not by `guardian = true` alone.

## Conceptual RLS — `memory_revisions`

Read/write permitted only if corresponding `memory_entities` row is accessible for the required action.

Clients should not directly update immutable revision rows.
Revisions are INSERT-only through a controlled function/RPC/service path.

## Conceptual RLS — `memory_sources`

Source rows require access to parent entity plus sufficient detail permission.

A viewer allowed to read a neutral memory summary may still be denied raw/source-detail access.

## Conceptual RLS — `memory_access_rules`

Ordinary users should not freely create their own access grants.

Writes require appropriate Authority/governance.
Reads should be limited so users cannot enumerate unrelated account permissions.

## Conceptual RLS — `memory_audit_events`

Append from controlled runtime/service only.
Read by authorized admin/reviewer paths only, with child-sensitive redaction where appropriate.

## Controlled RPC / Service Boundary

Recommended future write functions:

- `propose_memory_candidate(...)`
- `revise_memory_entity(...)`
- `delete_memory_entity(...)`
- `grant_memory_access(...)`
- `revoke_memory_access(...)`

Important:
- do not expose unrestricted direct table writes to clients
- RPC must validate subject, actor, expected revision, visibility, sensitivity, and action authorization
- SECURITY DEFINER functions, if used, must hard-code safe `search_path`, validate all identifiers, and never rely on caller-supplied role claims alone

## Service Role Boundary

Service-role keys must never appear in client apps or repository history.

If a backend runtime uses service role:
- it must independently enforce subject/viewer scope
- it must not treat service-role bypass of RLS as authorization
- every privileged path must emit audit records

## Cross-Account Model

Father, mother, child, and future device/app contexts should map to explicit account/viewer identities.

The memory owner is the child/subject identity, not the ChatGPT account itself.

Therefore:

`subject identity != account identity`

Multiple accounts may connect to the same subject while retaining different visibility scopes.

## Sensitive Disclosure Example

Entity:
- subject = child
- sensitivity = high
- visibility = restricted_sensitive

Father account:
- may have no active read grant

Mother account:
- may have review-only or no grant

System safety process:
- may have bounded system access if policy requires it

Shared storage does not change these distinctions.

## Migration Safety

Future migrations must:
- create tables with RLS enabled before exposing APIs
- avoid permissive temporary policies
- test cross-subject isolation
- test cross-account isolation
- test revision direct-query bypass
- test source/audit bypass
- test delete resurrection

## Required RLS Test Matrix

At minimum:

1. Child A cannot read Child B memory.
2. Father A cannot read unrelated child memory.
3. Guardian account cannot automatically read subject-private memory.
4. Safe shared memory can be read only when explicit policy allows it.
5. Restricted-sensitive memory remains hidden without specific access.
6. Revision table cannot bypass entity visibility.
7. Source table cannot bypass entity visibility.
8. Deleted entity not returned in normal retrieval.
9. Stale update rejected by revision mismatch.
10. Direct client UPDATE of revision row rejected.
11. Direct client creation of access grants rejected.
12. Retry with same event key does not duplicate candidate.
13. Service path emits audit record.
14. Revoked access stops subsequent reads.
15. Migration/fresh rebuild produces the same restrictive policies.

## Not Yet Included

This v1 intentionally defers:
- embeddings/vector search
- semantic ranking
- automatic forgetting scheduler
- long-term archival tiers
- encryption beyond platform/database baseline
- legal retention schedules
- parental-consent jurisdiction logic
- production data export UI

These should not be added before the core access/correction/sync model is proven.

## Deployment Gate

Do NOT create Supabase migrations until:
- schema review confirms no missing core invariant
- RLS test plan is accepted
- subject/account identity model is concrete
- runtime caller identity mechanism is known
- project has a dedicated Daughter Supabase backend

## Current State

As of 2026-08-25:
- Data model: DESIGNED
- RLS model: DESIGNED
- Migrations: NOT WRITTEN
- Supabase tables: NOT CREATED
- Runtime detector: NOT IMPLEMENTED
- Auto-memory: OFF

## Invariants

1. Subject identity != account identity.
2. Shared storage != shared visibility.
3. Revisions are immutable history.
4. Current state changes atomically.
5. Stale writers cannot overwrite newer state.
6. Tombstones prevent silent resurrection.
7. Provenance survives conflict.
8. RLS applies to entity, revisions, sources, access rules, and audit.
9. Service-role bypass is not authorization.
10. Memory never grants Authority.
