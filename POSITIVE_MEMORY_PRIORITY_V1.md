# Daughter Positive Memory Priority v1

Status: ACTIVE MEMORY POLICY
Date: 2026-08-25
Project: `daughter-companion-ai`

Depends on:
- `MEMORY_SPEC_V1.md`
- `MEMORY_CANDIDATE_CONTRACT_V1.md`
- `MEMORY_STAGE1_IMPLEMENTATION_CONTRACT_V1.md`

## Purpose

Ensure Daughter's long-term memory does not become biased toward problems, conflict, risk, weakness, or correction.

Daughter should actively preserve meaningful positive experiences so that long-term continuity includes joy, love, achievement, growth, belonging, courage, discovery, and proud moments.

Core principle:

`Do not remember only what went wrong. Remember what made life meaningful too.`

## Positive Memory Priority

Meaningful happy events should receive positive candidate priority.

Examples:
- winning a medal or competition
- receiving recognition at school
- completing something difficult
- first successful performance
- first independent achievement
- a joyful family moment
- a meaningful friendship moment
- a celebration the child values
- a proud learning milestone
- overcoming a fear
- making something the child is proud of
- a memorable trip or experience
- being kind, helping someone, or receiving kindness when the event matters to the child
- a moment the child explicitly says she wants to remember

These should normally become `candidate_pending` when factual, low-risk, and meaningful, even when they are one-time events.

## Important Distinction

A one-time negative emotion is usually temporary and should not become a permanent label.

A one-time positive event may still be a valid durable memory if the event itself is meaningful and historically stable.

Example:

`I won third place in my school competition today.`

This is a one-time event but can still be a strong memory candidate because the event remains true over time and may matter to the child's life story.

Therefore:

`One-time event != low-value event`

The decision should be based on meaning and future remembrance value, not recurrence alone.

## Positive Categories

Add the following positive-memory concepts to candidate handling:

- `happy_memory`
- `achievement`
- `celebration`
- `kindness_moment`
- `connection_moment`
- `courage_moment`
- `discovery_moment`
- `proud_moment`

These may map to existing canonical categories such as `important_event`, `growth_milestone`, or `relationship_context` if schema simplicity is preferred.

The implementation may use tags instead of adding top-level categories.

## Promotion Bias

Low-risk meaningful positive memories should have a lower promotion threshold than ambiguous conflict memories because:
- the event is often factually stable
- privacy risk is usually lower
- future retrieval can strengthen continuity and encouragement
- positive memories help avoid a deficit-focused profile

This does NOT mean all happy moments must auto-promote without governance.

Current rollout still applies:
- candidate detection: allowed by design
- durable auto-write: OFF until activation gates pass

## Child-Declared Importance

If the child says something equivalent to:
- `Remember this.`
- `I never want to forget today.`
- `This was the happiest day.`
- `I am very proud of this.`

Daughter should treat that as a strong `future_value` signal.

Unless sensitive or unsafe, this should normally create a positive memory candidate.

## Ordinary Happy Trivia

Not every pleasant moment needs durable storage.

Examples that can remain session-only unless the child explicitly values them:
- `Ice cream was nice today.`
- `The cartoon was funny.`
- `I am happy because lunch was good.`

The distinction is:

`Pleasant now` vs `worth remembering later`

If the child explicitly asks to remember even a small event, respect that request within privacy and storage policy.

## Retrieval Rule

Positive memories should be retrieved naturally when they can:
- celebrate progress
- remind the child of past capability
- connect a new event to an earlier milestone
- support resilience without minimizing current feelings
- help tell the child's growth story

Do not weaponize positive memory against current sadness.

Bad:
`You won a medal before, so you shouldn't be sad now.`

Good:
`I remember how proud you felt after that competition. Today can still feel hard even though you've had strong moments before.`

## Balance Rule

A healthy long-term memory profile should not over-represent:
- mistakes
- punishments
- conflicts
- weaknesses
- fears
- safety incidents

The system should deliberately preserve enough meaningful positive memories that the child's history reflects a whole person.

Suggested design check:

`Does the memory set describe a growing person, or mostly a list of problems?`

If mostly problems, the system is unhealthy even if each individual memory is technically accurate.

## Never Use Positive Memories as Pressure

Positive memories must not become expectations or emotional debt.

Do not infer:
- `You won once, so you must win again.`
- `You were brave before, so you cannot be scared now.`
- `You helped others before, so you must always be generous.`

Positive memory supports identity continuity; it does not freeze the child into a performance standard.

## Stage 1 Detector Additions

Recommended new reason codes:
- `MEANINGFUL_POSITIVE_EVENT`
- `ACHIEVEMENT_EVENT`
- `GROWTH_MILESTONE_POSITIVE`
- `CHILD_DECLARED_IMPORTANT`
- `POSITIVE_CONNECTION_EVENT`
- `POSITIVE_MEMORY_LOW_RISK`

A meaningful low-risk positive event should generally favor `candidate_pending` unless:
- provenance is too weak
- the event is fabricated/uncertain
- storing it creates unexpected privacy risk
- the child asks not to retain it

## Test Requirements

Future memory tests should include:
1. one-time meaningful achievement -> candidate
2. ordinary happy trivia -> session-only
3. child explicitly says remember this -> strong candidate
4. positive memory retrieved without pressuring child
5. positive memory does not override current sadness
6. positive memory survives normal fading longer than trivial preference data
7. deleted positive memory does not resurrect
8. positive relationship moment does not create unrealistic permanent relationship assumptions
9. repeated successes do not become fixed identity labels
10. long-term memory balance does not become deficit-heavy

## Invariant

`小爱要记得孩子受过的伤，也要记得她笑过、赢过、勇敢过、被爱过、爱过别人，以及第一次做到的那些事情。`

English canonical form:

`Remember meaningful joy, not only meaningful pain.`
