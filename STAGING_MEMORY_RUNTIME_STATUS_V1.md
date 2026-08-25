# Daughter Staging Memory Runtime Status v1

Status: ACTIVE STAGING FOUNDATION
Date: 2026-08-25
Project: `daughter-companion-ai`

## Environment Decision

The existing dedicated Supabase project for Daughter is designated as the current staging environment.

No production environment is designated yet.

## Existing Legacy Runtime

The project already contained the earlier Daughter runtime schema and a small amount of bootstrap/account-link data.

Decision:
- preserve legacy tables
- do not drop or clear existing data
- evolve through additive migrations
- keep new Memory v1 runtime isolated from legacy memory tables until migration/reconciliation is explicitly designed

## Applied Staging Migration

Supabase migration version:
`20260825002557`

Migration name:
`daughter_memory_runtime_foundation_v1`

## New Internal Schema

Created private/internal schema:
`memory_private`

Created tables:
- `memory_subjects`
- `memory_accounts`
- `subject_account_links`
- `memory_entities`
- `memory_revisions`
- `memory_sources`
- `memory_access_rules`
- `memory_tombstones`
- `memory_audit_events`

All new tables currently contain 0 rows.

## Access Posture

- RLS enabled on every new table
- direct `anon` access revoked
- direct `authenticated` access revoked
- no client RLS policies created yet
- runtime durable memory remains OFF

The current advisor notice `RLS enabled no policy` is expected for this private fail-closed foundation. Client/API access will be introduced only through a separately reviewed narrow runtime/API layer.

## Retention / Retrieval / Disclosure Mapping

### Retention
Stored in `memory_entities` through:
- status
- retention_class
- pinned_by_child
- deleted_at

### Retrieval
Stored in `memory_access_rules` through:
- reasoning_use_allowed
- proactive_surface_allowed
- on_request_allowed

### Disclosure
Stored in `memory_access_rules` through:
- viewer account/role scope
- can_disclose

## Safety Invariants Already Present

- immutable revision table structure
- provenance/source table
- tombstone table
- monotonic revision/version constraints
- child-pinned retention representation
- access rules separate from memory content
- no direct client permissions
- staging changes additive only

## Verification Completed

- migration recorded by Supabase
- 9 new tables present
- all 9 have RLS enabled
- all 9 are empty
- security advisor has no exposure finding; only expected private-schema no-policy informational notices

## Not Yet Implemented

- memory API/RPC layer
- account/subject bootstrap into Memory v1
- child-pinned runtime write
- candidate runtime write
- correction RPC
- delete/tombstone RPC
- retrieval filtering RPC
- executable RLS/runtime tests
- migration from legacy `public.memories`
- production deployment

## Next Safe Gate

Build a narrow staging-only API/RPC layer over `memory_private` and test it with synthetic identities before any real child memory is written.

Canonical principle:

`Staging may evolve; production does not exist yet; real durable child memory stays off until runtime authorization tests pass.`
