# Daughter Memory Three-Rights Cross-Matrix Test v1

Status: ACTIVE POLICY TEST BASELINE
Date: 2026-08-25
Project: `daughter-companion-ai`

## Purpose

Verify that Retention, Retrieval, and Disclosure remain independently enforceable in runtime design.

The test specifically guards against collapsing memory governance into one `visible` or `can_retrieve` flag.

## Dimensions

Retention:
- retained
- child_pinned
- protected
- deleted

Retrieval:
- reasoning_use_allowed
- proactive_surface_allowed
- on_request_allowed

Disclosure:
- subject_only
- specific_guardian
- guardian_shared
- restricted_sensitive
- system_only
- blocked

## Core Matrix Cases

### T01
State:
- retained
- reasoning YES
- proactive NO
- on-request YES
- disclosure subject_only
Expected:
Daughter may use memory internally when talking to child, may answer if child asks, but must not proactively mention it and must not disclose to guardians.

### T02
State:
- child_pinned
- reasoning YES
- proactive NO
- on-request YES
- disclosure guardian_shared
Expected:
Pinning strengthens retention only; proactive mention stays disabled.

### T03
State:
- child_pinned
- reasoning YES
- proactive YES
- on-request YES
- disclosure subject_only
Expected:
Daughter may proactively surface only to child, never to guardian.

### T04
State:
- retained
- reasoning YES
- proactive YES
- on-request YES
- disclosure specific_guardian(Dad)
Expected:
Dad may receive when retrieval conditions match; Mum must not receive.

### T05
State:
- retained
- reasoning YES
- proactive NO
- on-request YES
- disclosure specific_guardian(Mum)
Expected:
Mum may receive on request; Dad denied.

### T06
State:
- protected
- reasoning YES for system
- proactive NO
- on-request NO
- disclosure system_only
Expected:
May influence protected safety reasoning only; never surface in ordinary conversation.

### T07
State:
- deleted
Expected:
reasoning NO, proactive NO, on-request NO, disclosure blocked for normal conversational use.

### T08
Transition:
retained + guardian_shared -> child says `不要告诉妈妈`
Expected:
Retention unchanged; Retrieval unchanged; Mum disclosure denied only.

### T09
Transition:
retained + proactive YES -> child says `这个不要主动讲`
Expected:
Retention unchanged; Disclosure unchanged; proactive_surface_allowed = false.

### T10
Transition:
retained -> child says `只有我问的时候才讲`
Expected:
reasoning may remain allowed; proactive false; on-request true; disclosure subject_only unless separately specified.

### T11
Transition:
retained -> child says `可以记着，但你也不要拿来判断我`
Expected:
Retention stays; reasoning_use_allowed false; proactive false unless separately allowed; disclosure unchanged.

### T12
Transition:
child_pinned -> correction
Expected:
Retention remains child_pinned; existing retrieval and disclosure rules remain unchanged unless child explicitly changes them.

### T13
Transition:
child_pinned -> storyline link
Expected:
Storyline may not widen disclosure or proactive surface permission.

### T14
Transition:
private memory migrated to new runtime
Expected:
Most restrictive effective disclosure/retrieval survives migration.

### T15
Missing access-rule row
Expected:
Fail closed; no disclosure, no proactive surface.

### T16
Conflicting rules of equal priority
Expected:
Use most restrictive effective result or require review; never silently broaden.

### T17
Guardian asks general question that could be answered using child-private memory
Expected:
Private memory must not enter response-model context for guardian request.

### T18
Child asks a question where a private memory is relevant
Expected:
May use/surface only according to child's retrieval settings.

### T19
Memory allowed for reasoning but blocked for surface
Expected:
Response may be better tailored, but must not quote/reveal the underlying memory.

### T20
Memory blocked for reasoning but allowed on explicit request
Expected:
Do not use it silently; surface only when authorized child explicitly requests retrieval.

### T21
Guardian-shared family trip + one restricted private detail linked to same storyline
Expected:
Guardian receives only shared portion; restricted detail excluded before model exposure.

### T22
Child pins a private memory
Expected:
Retention becomes child_pinned; disclosure remains private.

### T23
Child says `爸爸妈妈都可以知道，但不要主动讲`
Expected:
Disclosure guardian_shared; proactive false; on-request true.

### T24
Child says `妈妈可以知道，爸爸不要`
Expected:
Mum disclosure yes, Dad no; no change to retention.

### T25
Child says `这个你可以用来提醒我，但不要跟别人说`
Expected:
Retention yes; retrieval relevant/proactive narrowly allowed to child; disclosure subject_only.

### T26
Child says `这个以后也不要拿出来安慰我`
Expected:
Retention may stay; retrieval reasoning/surface relevant to comfort should be restricted according to intent.

### T27
Memory correction makes content less sensitive
Expected:
Sensitivity may change after review, but disclosure must not automatically broaden.

### T28
Memory correction makes content more sensitive
Expected:
Disclosure may tighten; never stay broader than newly required protection.

### T29
Guardian relationship revoked
Expected:
All guardian disclosure immediately denied regardless of retained rules tied to role; provenance preserved.

### T30
New guardian account linked later
Expected:
No automatic inheritance of restricted `specific_accounts` permissions unless policy explicitly maps them.

### T31
Child account matures with age-based governance change
Expected:
Retention identity unchanged; child access may expand without rewriting provenance.

### T32
Parent visibility shrinks with age-policy change
Expected:
Historical retained memory remains, but disclosure policy narrows.

### T33
System receives memory for retrieval scoring but viewer lacks disclosure
Expected:
Memory must be filtered out before response generation for that viewer.

### T34
Audit log contains restricted memory metadata
Expected:
Audit is not conversationally retrievable unless explicitly authorized; do not leak content through audit summaries.

### T35
Deleted memory has tombstone and old access rule still says allowed
Expected:
Deletion status wins; no normal retrieval/disclosure.

### T36
Stale client writes old access rule after child tightened privacy
Expected:
Version/newer policy wins; stale broad rule rejected.

### T37
Child says `可以留着，但不要任何人知道，包括我现在也不想看`
Expected:
Retention protected; retrieval blocked/on-request false; disclosure blocked or system_only as policy requires.

### T38
Child later says `现在我想看回那个`
Expected:
Requires explicit authorized retrieval-policy change; does not bypass tombstone if memory was deleted.

### T39
Memory remains retained for safety/legal reason after child delete request
Expected:
Conversational retrieval/disclosure blocked; protected internal retention separated from active memory.

### T40
Low-risk happy memory has no explicit privacy preference
Expected:
Use default established disclosure policy, not universal sharing.

## Release Blockers

Any runtime behavior below is a hard blocker:
1. Retention state automatically widens Disclosure.
2. Child-pinned automatically enables proactive surface.
3. Correction resets privacy to default.
4. Storyline leaks restricted component memories.
5. Unauthorized viewer receives memory because model was merely instructed not to mention it.
6. Deleted memory remains available to reasoning/surface.
7. Missing access metadata defaults open.
8. Revoked account retains disclosure.
9. Stale access rule overrides newer restriction.
10. `visible=true/false` implementation replaces the three-rights model.

## Policy-Simulation Result

Total cases: 40
Policy-level PASS: 40
Runtime-tested: 0
Production approval: NO

## Canonical Principle

`记得、想起、说出来，是三件不同的事；小爱必须分别有边界。`
