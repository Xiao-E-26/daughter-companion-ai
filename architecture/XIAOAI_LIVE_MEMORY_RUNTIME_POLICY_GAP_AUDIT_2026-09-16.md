# XiaoAi Live Memory Runtime-Policy Gap Audit — 2026-09-16

Status: LIVE AUDIT VERIFIED / NO PRODUCTION MUTATION
Project: `daughter_companion_ai`
Canonical XiaoAi Supabase: `bnxjlbuohnujgvryttzj`

## Verified Live Runtime

Active Edge Function observed through Xiao-E cross-account Supabase execution:

- `xiaoi-memory-runtime` v4
- `verify_jwt=true`
- live bundle read through Xiao-E Provider Executor v4
- binary-safe read verified

Observed live actions:

- `health`
- `bootstrap`
- `recall`
- `save_explicit`
- `safety`

`save_explicit` calls:

`public.request_explicit_memory_save(...)`

with child/session/user utterance/content/memory type/valence/importance/dedupe key.

## Verified Live Save Path

`save_explicit`
-> `request_explicit_memory_save`
-> `memory_candidates(explicit_save=true)`
-> `auto_process_memory_candidates`
-> `promote_memory_candidate`
-> `durable_memories`

### request_explicit_memory_save currently checks

- authenticated guardian
- guardian owns child
- session belongs to child
- original user utterance exists
- content exists
- content length <= 4000
- utterance matches enabled `memory_save_phrases`
- candidate is inserted with `explicit_save=true`

It does **not** currently classify or prove:

- memory class M0-M4
- sensitivity treatment
- minimum-necessary summarization
- scoped visibility
- retention class / review requirement

## Verified Promotion Behavior

`auto_process_memory_candidates` currently promotes:

1. `memory_type='safety'`
2. any `explicit_save=true` when `explicit_save_enabled=true`
3. auto-captured candidates above importance threshold

The table `memory_policy` contains `explicit_save_always_promote`, but the live function does not read or enforce that field.

This is a concrete implementation drift.

`promote_memory_candidate` copies candidate content directly into `durable_memories` and marks the candidate promoted. It does not independently enforce privacy, sensitivity, minimum-necessary, visibility, or retention gates.

## Verified Schema Gap

### memory_candidates
Current relevant fields:

- child_id
- session_id
- content
- memory_type
- valence
- importance
- explicit_save
- status
- processed_at
- dedupe_key

Missing policy metadata includes:

- memory_class
- sensitivity classification
- visibility_scope
- retention class / review semantics
- policy-gate decision/evidence
- minimized/summarized durable representation

### durable_memories
Current relevant fields:

- child_id
- source_candidate_id
- memory_type
- content
- valence
- importance
- confidence
- occurred_at
- expires_at
- is_active

Missing policy metadata includes:

- memory_class
- visibility_scope
- retention class
- review state
- approval/provenance reference for sensitive retention

## Verified RLS

RLS is enabled on:

- `memory_candidates`
- `durable_memories`
- `memory_policy`

Current policies authorize rows through guardian ownership:

`child_profiles.guardian_id = auth.uid()`

This is a real access boundary, but it is **not sufficient to implement the canonical Memory/Privacy visibility model**.

The canonical policy explicitly states that Guardian status must not automatically imply unrestricted visibility into every private child memory, especially M3 sensitive memories.

Therefore:

`RLS exists != visibility policy fully implemented`

## Data-State Impact Check

At audit time:

- `memory_policy` had no rows
- `memory_candidates` had no rows

This means additive schema hardening can be designed without migrating existing candidate data, but production behavior must still be changed carefully.

## Canonical Policy Conflict

`MEMORY_AND_PRIVACY_POLICY_V1.md` requires:

- continuity without surveillance
- M0-M4 memory classes
- selective durable storage
- summary before transcript
- minimum-necessary detail
- stricter treatment for M3 sensitive memory
- purpose-limited M4 safety memory
- scoped visibility rather than one global guardian-visible model
- intentional retention / review / expiry

The current live implementation is materially simpler than this owner policy.

## Safe Closure Direction

Do **not** deploy the earlier hardening migration as-is.

The correct additive closure is:

1. preserve `save_explicit` caller compatibility;
2. keep explicit child save intent as a strong signal, not automatic durable permission;
3. add policy metadata to candidate/durable records;
4. make candidate -> durable promotion require a policy decision;
5. make `explicit_save_always_promote` actually participate in promotion logic;
6. preserve safety events separately from ordinary companion memory;
7. introduce visibility scopes compatible with future child/user ownership, rather than assuming guardian visibility;
8. keep current production data untouched until the compatibility migration and tests are complete.

## Invariants

`Explicit child intent = strong durable intent signal`

`Explicit child intent != bypass privacy/sensitivity/minimum-necessary/visibility gates`

`Guardian ownership != universal visibility entitlement`

`Candidate creation != durable promotion`

`Memory continuity != transcript surveillance`

## Current Decision

`LIVE GAP VERIFIED`

`PRODUCTION HARDENING = HOLD`

`NEXT = ADDITIVE COMPATIBILITY MIGRATION + REGRESSION TESTS`
