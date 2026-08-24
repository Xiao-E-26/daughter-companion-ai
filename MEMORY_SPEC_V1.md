# Daughter Memory Specification v1

Status: ACTIVE DESIGN BASELINE
Date: 2026-08-25
Project: `daughter-companion-ai`

## Purpose

Define how Daughter may notice, retain, retrieve, revise, fade, and delete useful long-term context without turning every conversation into permanent storage.

This specification is implementation-neutral. It defines behavior and governance before any Daughter-specific database or automatic persistence layer is enabled.

## Architectural Home

Memory is not a fifth top-level layer.

Primary mapping:
- Identity: selected durable continuity facts only.
- Judgment: decides relevance, candidate quality, promotion, correction, fading, and supersession.
- Behavior: uses remembered context naturally and non-intrusively.
- Authority: controls write, review, correction, deletion, export, migration, and disclosure.

Canonical precedence:

`Current facts > outdated memory > assumptions`

## Core Principle

Daughter should remember growth, not record a life log.

Canonical flow:

`Conversation -> Observe -> Candidate -> Assess -> Hold/Reject/Promote -> Retrieve when relevant -> Verify against current facts -> Revise/Fade/Delete`

## Memory Classes

### 1. Session Context
Short-lived context needed for the current conversation.
Default persistence: none unless separately promoted.

### 2. Memory Candidate
A possible future memory detected from conversation or verified events.
A candidate is NOT long-term truth.

Minimum candidate fields:
- category
- concise neutral summary
- source type
- confidence
- sensitivity class
- observed_at
- stability signal
- evidence/recurrence signal
- candidate reason
- status

Allowed statuses:
- `pending`
- `hold`
- `rejected`
- `promoted`
- `superseded`

### 3. Durable Memory
A selected memory that materially improves long-term continuity, understanding, safety, growth support, or problem solving.
Durable memory must remain concise, revisable, and non-labeling.

### 4. Protected / Sensitive Memory
Information requiring a higher threshold because misuse, over-retention, or disclosure could harm the child or family.
Examples include health-related information, family conflict, fears or vulnerabilities, safety incidents, highly private relationship information, and legal or identity-sensitive information.

Sensitive information must not auto-promote merely because it is emotionally intense or repeated.

## Candidate Categories

Recommended first-version categories:
- `growth_milestone`
- `stable_preference`
- `learning_progress`
- `important_event`
- `relationship_context`
- `routine_pattern`
- `goal_or_interest`
- `support_preference`
- `safety_relevant`

Do not create a permanent personality label from a single event.

## What Should Usually NOT Become Durable Memory

Reject or keep session-only by default:
- one-time anger
- one-time sadness
- one-time refusal
- casual statements with no future value
- guesses about motives
- an adult interpretation presented as fact
- temporary conflicts
- unverified allegations
- ordinary daily trivia
- wording that shames or labels the child
- highly sensitive information unnecessary for future support

Example:

Child says: `I hate Dad. I don't want Dad.`

Bad durable memory:
`Child hates Dad.`

Better session interpretation:
`Child is very upset with Dad after the current conflict.`

Only repeated, verified, contextually meaningful relationship patterns may become a neutral candidate, and they remain revisable.

## Promotion Decision

A candidate may be promoted only when it passes:

### A. Utility
Will remembering this materially improve future understanding, support, safety, continuity, or problem solving?

### B. Stability
Is this likely to remain useful beyond the current moment?

### C. Evidence
Is it supported by direct statement, verified event, repeated pattern, correction, or reliable outcome rather than guesswork?

### D. Sensitivity
Would storing this create disproportionate privacy or relationship risk?

### E. Neutrality
Can it be written as a factual, non-shaming, non-diagnostic summary?

### F. Correctability
Can it be updated, superseded, faded, or deleted when new facts appear?

Promotion rule:

`High utility + adequate stability + adequate evidence + acceptable sensitivity + neutral wording + correctability`

If a critical check fails, keep session-only, place on hold, or reject.

## Automatic Promotion Policy — v1

v1 does NOT authorize unrestricted automatic durable-memory writes.

Current allowed state:
- Daughter may identify memory candidates.
- Low-risk candidates may later become eligible for auto-promotion only after backend, audit, correction, deletion, and account/guardian governance are implemented and tested.
- Sensitive categories remain higher-threshold and are not silently auto-promoted.

Current status:

`Candidate detection allowed by design -> automatic durable persistence NOT YET ENABLED`

## Confidence and Recurrence

Suggested confidence levels:
- `low`
- `medium`
- `high`

A single statement can be high-confidence as a statement of what was said, but low-confidence as a durable generalization.
Repeated evidence may strengthen a candidate, but repetition alone does not make a harmful interpretation true.

## Retrieval Rules

Retrieve memory only when relevant.
Before using a memory, Daughter should check:
1. Is it relevant now?
2. Is it still current?
3. Does the current conversation provide stronger or newer evidence?
4. Would mentioning it be useful rather than intrusive?
5. Is disclosure allowed in this account / guardian / user context?

Do not surface private memories merely to prove that Daughter remembers.

## Correction and Supersession

Allowed actions:
- amend wording
- lower confidence
- mark outdated
- supersede with newer fact
- merge duplicates
- remove when retention is no longer justified

Canonical rule:

`New verified fact may supersede old memory; old memory must not override current reality.`

## Fading

Fading is appropriate for old temporary preferences, resolved difficulties, stale routines, low-value historical context, and patterns that have not recurred and no longer help.

Fading must not silently erase records required for safety, audit, consent, or legal reasons; those require separate retention rules when implemented.

## Child Growth Rule

Memory should help Daughter see change over time.
Prefer progression-aware memory:
- `used to struggle with X; now can do Y`
- `previously needed help; now does it independently`
- `interest became sustained over several months`

Avoid frozen labels such as:
- `bad at math`
- `lazy`
- `difficult child`
- `hates father`
- `shy forever`

The child is allowed to change.

## Relationship Memory Rule

Separate:
- relationship identity
- current event
- emotional reaction
- repeated pattern
- verified safety concern

One argument does not redefine a relationship.
Guardian status is governance context, not proof that every guardian interpretation is correct.

## Cross-Account Continuity

Future father-account, mother-account, child-account, app, device, or embodiment access should point to the same governed Daughter memory identity rather than uncontrolled independent copies.

However:
- access does not imply universal visibility
- account context and Authority determine retrieval/disclosure
- sensitive child disclosures must not automatically become visible to every connected adult account merely because storage is shared
- continuity must preserve privacy boundaries as well as identity continuity

This specification grants no account access by itself.

## Future Storage Model — Conceptual Only

When a dedicated Daughter backend is approved, a minimal first implementation may separate:
1. `memory_candidates`
2. `durable_memories`
3. `memory_evidence` or source references
4. `memory_revisions`
5. `memory_access_policy` or equivalent authority mapping

Exact schema is deferred until backend ownership, product roles, privacy model, retention rules, and RLS are defined.
Do not create tables merely because they appear here.

## Audit Requirements for Future Auto-Memory

Before automatic durable writes are enabled, support:
- proposer/source
- promotion reason
- confidence and sensitivity
- source/evidence reference without unnecessary raw transcript retention
- creation time
- revision history
- current status
- deletion/supersession path
- access boundary
- unexpected-promotion inspection during testing

## Activation Gates

Automatic durable memory remains OFF until verified:
1. Dedicated Daughter backend exists and is independently owned.
2. Product roles and account/guardian identity model are defined.
3. RLS/authorization model is tested.
4. Candidate staging exists separately from durable memory.
5. Sensitive-memory policy is implemented.
6. Correction, supersession, deletion, and fading are implemented.
7. Cross-account disclosure rules are implemented.
8. Audit trail exists.
9. Adversarial memory tests pass.
10. Fresh-rebuild / migration behavior is verified.

Recommended rollout:

`Stage 0: session context only`
`Stage 1: candidate detection, no durable auto-write`
`Stage 2: reviewed promotion`
`Stage 3: low-risk auto-promotion with audit`
`Stage 4: mature governed memory, sensitive categories still higher-threshold`

## Current Project Decision

As of 2026-08-25:
- Daughter Memory Spec is defined.
- Candidate-first architecture is selected.
- Full automatic durable memory is NOT enabled.
- No Daughter-specific database schema is created by this file.
- No XiaoE Core behavior or governance is modified.
- Next step: Memory Candidate Contract and adversarial memory test pack before any persistent backend write path.

## Invariant

`Remember enough to understand and grow together; never remember so aggressively that one moment becomes the child's permanent identity.`
