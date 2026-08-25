# Daughter Memory Runtime Schema & RPC Contract v1

Status: ACTIVE IMPLEMENTATION DESIGN / NOT DEPLOYED
Date: 2026-08-25
Project: `daughter-companion-ai`

## Purpose

Translate the approved Daughter Memory policies into a runtime data model and write-path contract suitable for a future Supabase implementation.

This file is a design contract only.
No Supabase project has been changed.
No durable memory writes are enabled.

## Current Supabase Security Baseline

The runtime design must follow these current Supabase principles:
- enable RLS on every table exposed through the Data API
- grants and RLS are separate controls; both must be reviewed
- `TO authenticated` alone is not authorization
- use ownership/relationship predicates in policies
- UPDATE requires an appropriate SELECT path and should use both `USING` and `WITH CHECK`
- do not use user-editable `user_metadata` for authorization decisions
- do not expose secret/service-role credentials in clients
- avoid `SECURITY DEFINER` as a shortcut around RLS
- if a definer helper is ever genuinely required, keep it out of exposed schemas, restrict EXECUTE, verify caller identity, and audit it
- indexes should exist on columns used heavily by RLS filters

## 1. Runtime Separation

Recommended logical separation:

### Internal durable data
Keep core memory records in an internal/private schema where possible.

Conceptual schema:
`memory_private`

### API surface
Expose only narrowly scoped functions/views required by the runtime.

Conceptual API schema:
`memory_api`

Do not expose raw internal memory tables directly unless a later security review explicitly approves it.

## 2. Core Tables

### 2.1 `memory_subjects`
Represents the child whose autobiographical memory persists across accounts/devices.

Fields:
```text
subject_id uuid pk
status text
created_at timestamptz
updated_at timestamptz
```

Invariant:
`one child continuity = one subject_id`

### 2.2 `memory_accounts`
Maps authenticated application accounts to runtime identities.

Fields:
```text
account_id uuid pk
provider text
provider_user_id text
status text
created_at timestamptz
revoked_at timestamptz null
```

Authentication binding must ultimately resolve to a trusted server/Auth identity, not a client-supplied role string.

### 2.3 `subject_account_links`
Connects accounts to a child subject.

Fields:
```text
link_id uuid pk
subject_id uuid fk
account_id uuid fk
relationship_role text
status text
can_submit_candidates boolean
can_request_correction boolean
can_request_deletion boolean
can_manage_linkage boolean
created_at timestamptz
revoked_at timestamptz null
```

Do not make a guardian account the owner of all child memory rows.

### 2.4 `memory_entities`
Stable logical memory identity and retention state.

Fields:
```text
memory_id uuid pk
subject_id uuid fk
memory_kind text
current_revision_id uuid null
status text
retention_class text
pinned_by_child boolean
significance text
sensitivity text
created_at timestamptz
updated_at timestamptz
superseded_at timestamptz null
deleted_at timestamptz null
```

Suggested `memory_kind` values:
- fact
- event
- preference
- support_preference
- milestone
- storyline_anchor
- child_pinned

Suggested `status` values:
- active
- held
- superseded
- deleted
- protected

Suggested `retention_class` values:
- ordinary
- durable
- child_pinned
- protected

Important:
`memory_entities` answers Retention, not who can see or surface the memory.

### 2.5 `memory_revisions`
Immutable revision history for content and meaning.

Fields:
```text
revision_id uuid pk
memory_id uuid fk
subject_id uuid fk
revision_number bigint
summary text
structured_payload jsonb
meaning_text text null
child_voice_quote text null
confidence text
sensitivity text
revision_reason text
created_by_account_id uuid null
created_by_actor_type text
created_at timestamptz
```

Rule:
- revision rows are append-only
- `current_revision_id` points to effective version
- older revision never overwrites newer revision
- correction must not silently reset retrieval/disclosure rules

### 2.6 `memory_sources`
Provenance for every durable assertion.

Fields:
```text
source_id uuid pk
memory_id uuid fk
revision_id uuid fk
subject_id uuid fk
source_account_id uuid null
source_actor_role text
source_type text
source_ref text null
observed_at timestamptz
source_confidence text
created_at timestamptz
```

Examples:
- child_direct
- guardian_direct
- verified_event
- repeated_pattern
- system_observation
- correction
- migration

Third-party claims must not be rewritten as `child_direct`.

### 2.7 `memory_access_rules`
Separates Retrieval and Disclosure from Retention.

Fields:
```text
access_rule_id uuid pk
memory_id uuid fk
subject_id uuid fk
viewer_account_id uuid null
viewer_role text null
reasoning_use_allowed boolean
proactive_surface_allowed boolean
on_request_allowed boolean
can_disclose boolean
can_modify boolean
can_delete boolean
rule_priority integer
status text
created_at timestamptz
updated_at timestamptz
```

Interpretation:
- `reasoning_use_allowed` = memory may influence internal response planning
- `proactive_surface_allowed` = Daughter may mention the memory without direct user request when context warrants
- `on_request_allowed` = Daughter may surface the memory when the authorized viewer explicitly asks
- `can_disclose` = this viewer may receive the memory content at all

This supports cases such as:
- retain but do not proactively mention
- retain and use internally, but do not surface aloud
- retain but do not disclose to Mum
- self-only
- guardian-safe shared memory

A single `visible` or `can_retrieve` boolean is insufficient.

### 2.8 `memory_tombstones`
Prevents deleted memory from being resurrected by stale clients/sync.

Fields:
```text
tombstone_id uuid pk
memory_id uuid unique
subject_id uuid fk
deleted_by_account_id uuid null
deleted_by_actor_type text
deleted_at timestamptz
delete_reason text null
version bigint
```

Rule:
`newer tombstone > older create/update`

Delete implies:
- Retention = deleted
- Retrieval = blocked
- Disclosure = blocked

### 2.9 `memory_storylines`
Longitudinal growth threads.

Fields:
```text
storyline_id uuid pk
subject_id uuid fk
storyline_type text
title text
current_summary text
status text
confidence text
sensitivity text
revision_number bigint
started_at timestamptz
last_updated_at timestamptz
```

Storyline synthesis must never broaden disclosure beyond the most restrictive relevant source memory.

### 2.10 `memory_storyline_links`
Links facts/events to storylines.

Fields:
```text
storyline_id uuid fk
memory_id uuid fk
relation_type text
created_at timestamptz
primary key (storyline_id, memory_id)
```

### 2.11 `memory_audit_events`
Append-only security/governance trail.

Fields:
```text
audit_id uuid pk
subject_id uuid null
memory_id uuid null
actor_account_id uuid null
actor_type text
action text
decision text
reason_code text
metadata jsonb
created_at timestamptz
```

Audit records must not be ordinary conversational memory.

## 3. Candidate Data

Candidate data may be separate from durable memory.

Suggested table:
`memory_candidates`

Fields align with `MEMORY_CANDIDATE_CONTRACT_V1.md` plus:
```text
intent_class text
child_declared_important boolean
related_memory_id uuid null
created_by_account_id uuid null
requested_retention text null
requested_retrieval_mode text null
requested_disclosure_scope text null
```

Candidates are not durable truth.

## 4. Intent Router Runtime Input

Before any write, runtime supplies:

```text
subject_id
actor_account_id
actor_role_resolved
utterance
conversation_context
intent_class
intent_confidence
source_type
source_ref
requested_retention
requested_reasoning_use
requested_proactive_surface
requested_on_request_surface
requested_disclosure_scope
requested_operation
idempotency_key
```

Supported `intent_class` values:
- long_term_memory_create
- reminder_or_task
- memory_query
- memory_correction
- memory_delete
- ordinary_conversation
- uncertain_memory_intent

Only `long_term_memory_create` can request direct Child-Pinned durable creation.

## 5. RPC/API Write Contract

### 5.1 `create_memory_candidate(...)`
Purpose:
Create a candidate, not durable memory.

Must verify:
- authenticated runtime/account
- active subject-account link
- submit permission
- subject matches caller relationship
- idempotency key

Must not:
- promote automatically
- grant new visibility/disclosure
- create Authority

### 5.2 `pin_child_memory(...)`
Purpose:
Direct durable path for clear child-declared long-term memory intent.

Required conditions:
1. actor is verified child-direct context OR trusted runtime is acting on a verified child-direct utterance
2. router intent = `long_term_memory_create`
3. intent confidence meets threshold
4. no unresolved critical ambiguity
5. privacy/sensitivity handling resolved
6. idempotency key supplied

Writes atomically:
- `memory_entities`
- first `memory_revisions`
- `memory_sources`
- default/explicit `memory_access_rules`
- `memory_audit_events`

Default behavior:
- pinning strengthens Retention only
- pinning does NOT expand Disclosure
- pinning does NOT automatically enable proactive surface

Must never be invoked merely because text contains `记得` or `remember`.

### 5.3 `correct_memory(...)`
Purpose:
Create a new immutable revision and update current pointer.

Required:
- caller authorized to request correction
- target visible/known to caller through allowed path
- reason/provenance recorded
- version check against current revision

Must preserve:
- old revision history
- existing retrieval policy unless explicitly changed
- existing disclosure policy unless explicitly changed

### 5.4 `delete_memory(...)`
Purpose:
Remove memory from active retrieval and create tombstone.

Required behavior:
- validate delete authority
- mark entity deleted
- append audit event
- create/update tombstone with higher monotonic version
- block reasoning retrieval
- block proactive surface
- block on-request surface
- block disclosure
- ensure stale update cannot reactivate it

### 5.5 `set_memory_retrieval_policy(...)`
Purpose:
Change how a retained memory may be used or surfaced without changing retention or disclosure.

Supported controls:
- reasoning use allowed/blocked
- proactive surface allowed/blocked
- on-request surface allowed/blocked

Examples:
- `keep it, but do not bring it up`
- `you may use it to understand me, but don't say it aloud`
- `only tell me if I ask`

Must not:
- delete the memory
- broaden disclosure

### 5.6 `set_memory_disclosure_policy(...)`
Purpose:
Change who may receive memory content without changing retention or retrieval preference.

Examples:
- keep but do not tell Mum
- child only
- Dad and Mum may both know
- restricted sensitive

Must not:
- delete the memory
- automatically enable proactive surface

### 5.7 `retrieve_memories(...)`
Purpose:
Return only memory rows allowed for the current viewer and requested usage mode.

Input must include a retrieval purpose, e.g.:
- `reasoning_context`
- `proactive_surface`
- `explicit_user_query`

Filtering order:
1. authenticated account/session
2. active subject relationship
3. memory Retention status/tombstone
4. viewer Disclosure permission
5. sensitivity restrictions
6. requested Retrieval mode permission
7. relevance/recency/significance/storyline fit
8. current-fact conflict checks
9. only then expose content to response generation

Unauthorized rows must be filtered before model exposure.

## 6. Retention / Retrieval / Disclosure Invariants

1. Retention permission does not imply retrieval permission.
2. Retrieval permission does not imply disclosure to every viewer.
3. Child-pinned does not mean guardian-visible.
4. Guardian-visible does not mean proactive mention is appropriate.
5. Correction does not widen disclosure.
6. Correction does not re-enable proactive surface.
7. Storyline linking does not widen disclosure.
8. Migration must preserve or tighten privacy, never silently broaden it.
9. Missing access metadata must fail closed.
10. Deleted memory is unavailable for normal reasoning, surface, and disclosure.

## 7. Reminder Boundary

`reminder_or_task` never writes to `memory_entities` by default.

Reminder data must live in a separate task/reminder subsystem.

If a reminder later becomes a meaningful event, create a separate memory operation based on the event, not by reusing the task row as autobiographical memory.

## 8. Planned Future Events

If the child pins an event that has not yet occurred:
- store status/meaning as `planned` or `anticipated`
- never represent it later as completed without verification
- actual completion creates/updates a verified event revision

## 9. RLS / Authorization Strategy

Preferred direction:
- raw internal tables not broadly exposed
- authenticated clients should not directly mutate durable memory rows
- narrow API functions or server runtime validates subject relationship and operation intent
- any exposed table must have RLS enabled
- grants must be minimum-required

Authorization data should derive from trusted account/link records or trusted application metadata, never user-editable metadata.

## 10. Index Requirements

At minimum index:
- every `subject_id`
- every `account_id`
- `subject_account_links(account_id, subject_id, status)`
- `memory_entities(subject_id, status)`
- `memory_revisions(memory_id, revision_number)`
- `memory_sources(memory_id)`
- `memory_access_rules(memory_id, viewer_account_id)`
- `memory_tombstones(memory_id)`
- audit lookup fields used by tests

## 11. Migration Rules

Do not hand-invent a migration filename.
When a real Supabase development environment exists:
1. create migration using current Supabase CLI workflow
2. apply first to isolated development/staging only
3. run schema verification
4. run RLS tests
5. run advisors
6. run stress test blocker suite
7. fresh rebuild from migrations
8. compare resulting schema
9. only then consider production activation

## 12. Runtime Activation Gates

Durable memory remains OFF until all are true:
- dedicated Daughter Supabase environment verified
- actual Auth/account model verified
- schema migration applied in staging
- RLS tested with father/mother/child/runtime identities
- child-pinned write path tested
- reminder separation tested
- correction tested
- delete/tombstone tested
- Retention/Retrieval/Disclosure matrix tested
- internal reasoning vs surface-mention split tested
- cross-account sync tested
- privacy/disclosure tested
- 240 life-scenario blocker families translated into executable tests
- security advisors reviewed
- fresh rebuild passes

## Canonical Runtime Principle

`先确认是谁、想做什么、能不能做，再决定要不要保存、什么时候能提起、可以告诉谁。`
