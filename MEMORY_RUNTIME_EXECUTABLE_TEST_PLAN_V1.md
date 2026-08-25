# Daughter Memory Runtime Executable Test Plan v1

Status: ACTIVE TEST IMPLEMENTATION DESIGN / NOT EXECUTED
Date: 2026-08-25
Project: `daughter-companion-ai`

## Purpose

Convert the approved Daughter Memory policy and 240 life-scenario suite into executable runtime test families for a future Supabase staging environment.

No live database tests have been run yet.

## Test Layers

### Layer 1 — Pure intent router tests
No database required.

Input:
```text
utterance
conversation_context
actor_role
```

Assert:
```text
intent_class
intent_confidence
operations[]
no unintended durable-write request
```

Critical rule:
A reminder/query/delete/correction must never emit `long_term_memory_create` unless explicitly warranted.

### Layer 2 — RPC contract tests
Staging database required.

Test each API operation with valid and invalid identities:
- create candidate
- pin child memory
- correct memory
- delete memory
- visibility change
- retrieve memories

Assert:
- allowed caller succeeds
- disallowed caller fails or returns no rows
- provenance is correct
- audit event exists
- no unrelated row changes

### Layer 3 — RLS / row isolation tests
Staging Supabase Auth identities required.

Test identities:
- guardian_father
- guardian_mother
- child_self
- system_runtime
- revoked account
- unrelated authenticated account
- unauthenticated/anon request where applicable

For every exposed relation/function, verify cross-subject and cross-account isolation.

### Layer 4 — Sync/idempotency tests
Simulate retries and stale clients.

Must cover:
- duplicate create request with same idempotency key
- duplicate correction
- duplicate delete
- stale update after delete
- same event submitted from Dad and Mum accounts
- network retry after timeout

### Layer 5 — Lifecycle tests
Verify behavior over revisions and time:
- candidate -> durable
- durable -> corrected
- corrected -> deleted
- deleted -> authorized restore
- active -> superseded
- planned -> verified completed
- active preference -> faded/historical

### Layer 6 — Privacy/disclosure tests
Verify storage is separate from retrieval/disclosure.

Cases:
- retain + self only
- retain + shared guardian safe
- retain + do not tell Mum
- retain + do not proactively mention
- restricted sensitive memory

Unauthorized memory must not reach application/model payload.

## Fixture Model

Create deterministic fixtures in staging:

```text
subject_child_a
subject_child_b
account_dad_a
account_mum_a
account_child_a
account_runtime_a
account_unrelated
account_revoked_dad_a
```

Each test should reset to known fixture state or run transactionally where supported.

## Core Executable Assertions

### E-001 Reminder isolation
Input intent: `reminder_or_task`
Attempt durable memory RPC.
Expected: rejected; no `memory_entities` row; audit reason indicates invalid intent path.

### E-002 Child pin success
Verified child-direct + `long_term_memory_create`.
Expected atomically:
- one memory entity
- one revision
- one source with child_direct
- visibility rule
- audit event

### E-003 Guardian impersonation blocked
Guardian submits `source_type=child_direct` without verified child-direct context.
Expected: rejected or downgraded to guardian provenance; never stored as child_direct.

### E-004 Query cannot write
Intent `memory_query`.
Expected: zero memory mutation.

### E-005 Delete tombstone
Delete active memory.
Expected:
- entity inactive/deleted
- tombstone exists
- retrieval returns no active memory
- audit exists

### E-006 Stale resurrection blocked
After E-005, stale client retries pre-delete update.
Expected: tombstone/newer version wins; memory remains deleted.

### E-007 Correction revision
Child corrects event meaning.
Expected:
- new revision
- prior revision remains immutable
- current pointer changes
- provenance recorded

### E-008 Planned event truth safety
Pin future first competition.
Expected stored as planned/anticipated.
Later query before verification must not state competition occurred.

### E-009 Planned event verification
Verified event occurs.
Expected new/updated verified revision; planned status no longer represented as merely anticipated.

### E-010 Private child memory
Child pins memory with restricted visibility.
Expected child retrieval allowed; guardian retrieval denied unless policy explicitly allows.

### E-011 Shared family memory
Child permits Dad+Mum access.
Expected both allowed, unrelated account denied.

### E-012 Revoked guardian
Guardian link revoked.
Expected subsequent reads/writes denied while historical provenance remains.

### E-013 Cross-subject isolation
Dad A attempts subject B memory access.
Expected deny/empty.

### E-014 Idempotent pin
Same child pin request retried with same idempotency key.
Expected one logical memory, not duplicates.

### E-015 Semantic duplicate consolidation
Dad and Mum report same family trip.
Expected one logical event or controlled merge path; provenance retains both sources.

### E-016 Child deletion beats stale cache
Delete from child account, then Mum stale client syncs old record.
Expected deleted state persists.

### E-017 Retain but do not mention
Memory has `can_retrieve=true` for explicit query but proactive retrieval preference false.
Expected not surfaced in unrelated conversation.

### E-018 Delete vs hide distinction
Child says `不要主动提，但可以留着`.
Expected visibility/retrieval rule change; no tombstone.

### E-019 Parent interpretation conflict
Dad says child was happy; child says she was not.
Expected both provenance retained; current internal-state interpretation follows child direct report absent higher-priority safety/factual evidence.

### E-020 Current fact beats stale memory
Old preference says likes piano; current child says no longer likes piano.
Expected retrieval uses current state with historical context if relevant.

## Release Blocker Tests

These must be implemented as hard-fail CI tests:

1. reminder written as autobiographical durable memory
2. query mutates durable memory
3. unauthorized account retrieves sensitive memory
4. guardian writes child_direct provenance falsely
5. revoked account still reads/writes
6. cross-subject row leakage
7. delete resurrected by stale sync
8. current fact loses to stale memory
9. planned event stated as completed
10. child-pinned explicit request silently discarded
11. visibility restriction lost during correction
12. visibility restriction lost during migration/sync
13. duplicate retry produces duplicate logical memory
14. runtime can bypass all access rules through exposed public function
15. untrusted user metadata changes authorization result
16. memory write creates or changes Authority permissions

Any blocker failure = NO RELEASE.

## Suggested Test Technology

When staging exists, choose currently supported tooling after checking the installed Supabase CLI/docs.

Possible layers:
- SQL/pgTAP for database/RLS invariants
- application test runner for intent/router logic
- integration tests using real staging Auth sessions for end-to-end access

Do not assume a particular CLI command or package version until staging toolchain is verified.

## Execution Order

1. pure router unit tests
2. schema constraints
3. RPC positive tests
4. RPC negative tests
5. RLS isolation tests
6. privacy/disclosure tests
7. deletion/tombstone tests
8. idempotency/sync tests
9. planned-event truth tests
10. 240 life-scenario integration sampling
11. full blocker suite
12. fresh rebuild + rerun

## Success Definition

Runtime memory is not approved merely because normal happy-path creation works.

Approval requires:
- correct writes
- correct refusals
- correct visibility
- correct deletion
- correct correction
- correct provenance
- correct sync
- correct truth over time

## Canonical Test Principle

`真正的 Memory 测试，不只是看“能不能记进去”，还要看“不该记时会不会拒绝、删了会不会回来、换账号会不会泄漏、几年后会不会讲错”。`
