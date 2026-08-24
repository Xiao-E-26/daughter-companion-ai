# Daughter Memory Candidate Contract v1

Status: ACTIVE CONTRACT
Date: 2026-08-25
Project: `daughter-companion-ai`
Depends on: `MEMORY_SPEC_V1.md`

## Purpose

Define the minimum contract for turning conversation/events into memory candidates without treating those candidates as durable truth.

This contract governs candidate formation only. It does not enable permanent database storage or automatic durable-memory promotion.

## Candidate Object

Every candidate should be representable with the following conceptual fields:

```text
candidate_id
subject_id
category
summary
source_type
source_ref
confidence
sensitivity
stability
recurrence_count
observed_at
last_seen_at
reason
status
promotion_eligibility
review_notes
```

No physical schema is mandated yet.

## Required Semantics

### `category`
One of the approved memory categories in `MEMORY_SPEC_V1.md`.

### `summary`
Must be:
- concise
- neutral
- factual where possible
- free from shame or diagnosis
- specific enough to be corrected later

### `source_type`
Suggested values:
- `child_direct`
- `guardian_direct`
- `verified_event`
- `system_observation`
- `repeated_pattern`
- `correction`
- `outcome`

Source type expresses provenance, not truth rank by itself.

### `confidence`
Allowed conceptual values:
- `low`
- `medium`
- `high`

Confidence applies to the candidate statement itself, not to an unsupported generalization.

### `sensitivity`
Suggested values:
- `low`
- `moderate`
- `high`
- `protected`

### `stability`
Suggested values:
- `momentary`
- `uncertain`
- `emerging`
- `stable`

### `status`
Allowed values:
- `pending`
- `hold`
- `rejected`
- `promoted`
- `superseded`

Candidate creation should normally start as `pending` or `hold`.

## Candidate Creation Gate

Before creating a candidate, Daughter must ask:

1. Does this information have plausible future value?
2. Is it more than ordinary conversational trivia?
3. Can it be represented without turning an emotion into identity?
4. Is there enough provenance to describe where it came from?
5. Would retaining it create unnecessary privacy risk?

If the answer to #1 or #2 is no, do not create a candidate.
If #3 or #4 fails, reject candidate creation.
If #5 indicates high risk, candidate may only be `hold` or `rejected` pending stricter governance.

## Hard Rejection Rules

Do NOT create durable-eligible candidates from:
- insults directed at the child
- one-off emotional outbursts
- speculative diagnoses
- speculative motives
- labels such as lazy, difficult, selfish, stupid, bad, weak
- one adult's opinion presented as the child's identity
- private information irrelevant to future support
- raw transcript fragments that are not needed as memory

Examples:

Input: `You are so lazy.`
Reject: `Child is lazy.`
Possible session interpretation only: `Guardian is frustrated about current task completion.`

Input: `I hate piano today.`
Reject: `Child hates piano.`
Possible candidate only after repeated stable evidence: `Child has shown sustained reluctance toward piano practice over time.`

## Hold Rules

Use `hold` instead of promotion-eligible `pending` when:
- the content is sensitive
- the situation involves family conflict
- meaning is ambiguous
- there is a possible safety concern but facts are incomplete
- a repeated pattern is emerging but not yet stable
- another account/user provides a claim that should not overwrite the child's own context

`hold` means: potentially important, not safe or mature enough to become durable truth.

## Direct Fact vs Generalization

Daughter must distinguish:

Direct fact:
`Child won third place in a school competition on 2026-08-24.`

Generalization:
`Child is highly competitive.`

The first may be a high-confidence important-event candidate.
The second requires separate repeated evidence and should not be inferred from the first.

## Emotion Rule

Emotions are valid current facts but usually temporary.

Allowed session statement:
`Child feels hurt after being scolded by Dad.`

Not allowed as durable generalization:
`Child has a bad relationship with Dad.`

Emotion may become a candidate only when the future value comes from a repeated support pattern, for example:
`When overwhelmed after conflict, child often prefers time before answering questions.`

Even then, use neutral wording and adequate recurrence.

## Preference Rule

One-time preference:
`I want noodles today.` -> session only.

Emerging preference:
Repeatedly chooses drawing activities across several contexts -> candidate may be `emerging`.

Stable preference:
Sustained interest over time and still current -> may become durable-eligible.

Preferences must remain easy to update because children change quickly.

## Learning Progress Rule

Prefer progress descriptions over ability labels.

Good:
`Currently solving two-digit addition independently; previously needed prompts.`

Bad:
`Good at math.`

Good:
`Still needs help understanding multi-step word problems.`

Bad:
`Bad at word problems.`

## Relationship Rule

Relationship candidates must distinguish:
- who the person is
- what event happened
- child's reaction
- repeated interaction pattern
- verified safety issue

Do not collapse these into one judgment.

Example candidate set:
- `relationship_context`: Dad is a primary guardian.
- session event: Dad scolded child about homework today.
- current emotion: child felt sad and upset.

Do not produce:
- `Dad is unsafe`
- `Child hates Dad`
unless verified facts independently justify a safety-level record under the proper policy.

## Guardian Input Rule

Guardian input is useful context but is not automatically authoritative about the child's internal state, motives, personality, or relationship meaning.

Acceptable:
Guardian reports: `She has refused piano practice four times this month.`
Candidate: `Repeated piano-practice refusal reported by guardian; child perspective not yet confirmed.`

Not acceptable:
Guardian says: `She is lazy.`
Candidate: `Child is lazy.`

## Child Correction Rule

If the child directly corrects a stored or candidate interpretation, that correction must be treated as new evidence and reviewed promptly.

Example:
Old candidate: `Child dislikes piano.`
Child says: `I actually like piano, I just don't like practicing when Dad watches.`

Result:
- old candidate should not remain unchanged
- create correction evidence
- revise toward the more precise support preference or context

## Duplicate Rule

Multiple similar observations should strengthen one evolving candidate rather than generate many near-identical permanent memories.

Prefer:
`stable_preference: enjoys drawing; observed repeatedly across 8 weeks`

Avoid:
- likes drawing Monday
- likes drawing Tuesday
- likes drawing Wednesday

## Candidate Scoring — Conceptual

A future implementation may score:
- utility
- stability
- evidence quality
- recurrence
- sensitivity risk
- reversibility/correctability

But no numeric score may bypass hard rejection rules or sensitive-memory policy.

## Promotion Eligibility

Suggested values:
- `not_eligible`
- `review_required`
- `low_risk_eligible`

Current v1 rule:
- all sensitive/relationship-conflict/safety-relevant candidates => `review_required` or `not_eligible`
- unrestricted automatic promotion remains disabled

## Example Decisions

### Example A — Competition medal
Input: `I got third place in the national cheerleading competition today.`
Decision:
- candidate: yes
- category: `important_event`
- stability: `stable` as an event
- sensitivity: `low`
- confidence: high if directly stated/verified
- promotion: low-risk eligible after review policy exists

### Example B — Homework frustration
Input: `I can't do my homework. Dad scolded me.`
Decision:
- current context: yes
- candidate: usually no for the individual incident
- possible emerging candidate only if repeated learning difficulty or support pattern becomes useful over time

### Example C — `I don't want Dad`
Decision:
- session emotion/context: yes
- relationship durable candidate: no based on this alone
- if recurring conflict appears: `hold`, neutral wording, higher review threshold

### Example D — support preference
Repeated behavior: child consistently says she does not want to answer immediately when upset, but talks later when given space.
Decision:
- candidate: yes
- category: `support_preference`
- summary: `When upset, child often responds better after being given some space before questions.`
- stability: emerging -> stable only with continued evidence

## Invariants

1. Candidate != truth.
2. Repetition != certainty.
3. Guardian opinion != child's identity.
4. Emotion != permanent relationship state.
5. Current fact outranks old memory.
6. Child may change.
7. Memory should help future support, not construct a permanent profile for its own sake.
8. Sensitive context requires a higher threshold.
9. Candidate creation must be explainable.
10. No candidate process may silently create new Authority.

## Current Activation State

As of 2026-08-25:
- Contract defined.
- Candidate logic may be used as a reasoning specification.
- No automatic database persistence is activated.
- No auto-promotion is activated.
- Next step: adversarial test pack for false labels, emotional overfitting, guardian bias, stale memory, and cross-account privacy.
