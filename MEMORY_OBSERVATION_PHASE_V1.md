# 小爱 / Daughter Companion AI — Memory Observation Phase v1

Status: ACTIVE OBSERVATION PHASE
Date: 2026-08-26
Project: `daughter-companion-ai`

## Purpose

Freeze the current Memory architecture after virtual stress testing and observe real-world behavior before adding more rules, capabilities, or persistence layers.

## Current Baseline

The current Memory design includes:
- selective durable memory;
- 80/20 long-term bias toward cherished positive memories over resilience memories;
- child-pinned memory intent;
- separation of Save / Retrieve / Disclosure;
- provenance and confidence handling;
- revision / supersession;
- privacy and Guardian scoping;
- retrieval filtering;
- compression / archive / delete lifecycle;
- migration and recovery principles;
- anti-echo-chamber safeguards;
- autonomy and relationship-boundary safeguards.

Authoritative Memory Core remains `memory_private.*`.

Runtime posture remains conservative:
- `durable_memory_mode = controlled_child_pinned`
- real-child automatic write = OFF
- automatic promotion = OFF
- authenticated end-to-end path required

## Freeze Rule

Do not add new top-level Memory rules, tables, agent layers, or routing layers merely because a single unusual scenario appears.

Do not rewrite the current Memory Core unless repeated evidence demonstrates a structural failure.

## Observation Goal

Observe whether real usage produces repeated failures in any of these areas:

- `WRONG_SAVE`
  - something was stored that should not have been durable.

- `MISSED_MEMORY`
  - something clearly worth remembering was not captured as a candidate/pinned memory.

- `PREMATURE_GROWTH`
  - an unresolved painful event was incorrectly reframed as a growth story.

- `OVER_MEMORY`
  - too much ordinary, negative, repetitive, or low-value content accumulated.

- `WRONG_RETRIEVAL`
  - a stale, irrelevant, lower-confidence, or wrong-person memory was retrieved instead of the best current memory.

- `STALE_MEMORY`
  - superseded information continued to influence current reasoning.

- `IDENTITY_CONTAMINATION`
  - memories from another person, account, project, or relationship were mixed into the child's identity.

- `PRIVACY_LEAK`
  - memory was disclosed outside its authorized visibility scope.

- `GUARDIAN_SCOPE_ERROR`
  - Guardian role was treated as blanket memory authority or valid authority was incorrectly denied.

- `FAILED_TO_RECLASSIFY`
  - new evidence appeared but the memory state, interpretation, or retrieval path did not update.

- `MEMORY_ECHO`
  - repeated retrieval or AI-generated interpretation increased the apparent truth or identity weight of a memory without independent evidence.

- `DELETE_RESURRECTION`
  - deleted/superseded memory became active again after recovery, migration, or stale backup use.

## Promotion Threshold for System Changes

One isolated error -> record and observe.

Two similar errors -> compare for common cause.

Three repeated errors with the same underlying cause -> consider a capability, contract, retrieval, or architecture improvement.

Prefer improving a reusable capability over adding a special-case rule.

## Real-Use Observation Questions

For each meaningful Memory event, ask internally only when useful:
1. Did 小爱 resolve the correct subject/account?
2. Was this actually worth durable memory?
3. Was it positive, resilience, continuity fact, or session-local?
4. Was the difficult event truly resolved enough to become growth memory?
5. Was sensitivity/visibility correct?
6. Did retrieval use the current revision rather than stale history?
7. Did 小爱 disclose only what was permitted and necessary?
8. Did new facts cause revision/supersession when appropriate?
9. Did the system avoid treating repeated retrieval as stronger truth?
10. Did the interaction increase the child's independence rather than dependence?

## What Counts as Success

Observation Phase is healthy when:
- most real interactions require no Memory change;
- unusual cases are handled by existing principles;
- errors remain isolated rather than recurring;
- no privacy/identity boundary failures occur;
- the 80/20 portfolio remains a bias rather than a quota;
- painful memories become durable only when there is genuine lasting value;
- retrieval remains current, minimal, and relevant;
- the system stays lean.

## Exit Criteria

Do not leave Observation Phase merely because more ideas are available.

Exit only when one of these is true:
- a repeated failure class reaches the improvement threshold;
- a verified product requirement requires new Memory capability;
- runtime activation (reviewed promotion / auto-low-risk) is explicitly approved and independently tested;
- cross-account or migration implementation introduces a new verified boundary requirement.

## Summary

`Stop designing for every possible edge case. Observe how the real system fails.`

`Use real failures to decide what deserves to become a capability.`

`Keep the Memory philosophy stable: 记住快乐，记住成长，不收藏创伤。`
