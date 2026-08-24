# Daughter Memory Growth Story Model v1

Status: ACTIVE MEMORY DESIGN
Date: 2026-08-25
Project: `daughter-companion-ai`

Depends on:
- `MEMORY_SPEC_V1.md`
- `MEMORY_CANDIDATE_CONTRACT_V1.md`
- `POSITIVE_MEMORY_PRIORITY_V1.md`
- `MEMORY_STAGE1_IMPLEMENTATION_CONTRACT_V1.md`

## Purpose

Define how Daughter can remember the child as a whole person across time rather than as disconnected facts.

The system should preserve two complementary layers:

1. **Fact Memory** — small, correctable, provenance-aware units.
2. **Growth Storylines** — evolving longitudinal threads built from multiple fact memories.

Canonical principle:

`Facts provide accuracy. Storylines provide continuity.`

## Why Two Layers

Fact-only memory becomes fragmented:
- won medal
- disliked being watched during piano
- learned to sleep alone
- struggled with homework

Storyline-only memory becomes risky because it can over-interpret and freeze a narrative.

Therefore Daughter should keep facts independently and build storylines only from supported evidence.

## Layer A — Fact Memory

Fact Memory stores bounded observations/events such as:
- important event
- positive memory
- growth milestone
- stable preference
- learning progress
- support preference
- relationship context
- routine pattern
- goal/interest
- safety-relevant verified context

Each fact remains:
- source-aware
- time-stamped
- correctable
- supersedable
- sensitivity-aware
- access-controlled

A fact should not contain a broad personality conclusion unless separately justified.

## Layer B — Growth Storyline

A Growth Storyline links related facts across time to represent change.

Examples:

### Independence storyline
`Needed parent nearby at bedtime -> first night sleeping alone -> woke during night -> gradually settled -> now sleeps independently`

### Piano storyline
`Did not want Dad listening -> clarified that she still likes piano -> preferred private practice -> later became more comfortable performing`

### Confidence storyline
`Was nervous speaking in front of others -> joined school performance -> completed competition -> later volunteered to speak`

### Learning storyline
`Needed help with multi-step word problems -> learned strategy -> solved independently -> later helped explain method`

The storyline is not a personality label. It is a summary of observed change.

## Storyline Types

Recommended first-version storyline types:
- `independence`
- `learning_growth`
- `confidence_courage`
- `interest_development`
- `relationship_growth`
- `emotional_regulation`
- `problem_solving_growth`
- `kindness_connection`
- `identity_values`
- `life_milestones`

These are organizational threads, not diagnoses or fixed traits.

## Storyline Object — Conceptual

A future implementation may represent a storyline with:

```text
storyline_id
subject_id
storyline_type
title
current_summary
status
started_at
last_updated_at
linked_memory_ids[]
confidence
sensitivity
visibility_class
revision_number
```

Suggested statuses:
- `emerging`
- `active`
- `mature`
- `resolved`
- `historical`
- `superseded`

No schema is mandated by this design file.

## Storyline Creation Gate

Create a storyline only when:
1. at least two related observations/events exist, OR one clearly significant event starts a meaningful developmental thread;
2. there is plausible future continuity value;
3. the title/summary can remain neutral and revisable;
4. it does not convert a temporary problem into identity;
5. privacy/sensitivity rules permit the linkage.

Do not create a storyline simply because several negative events occurred close together.

## Storyline Update Rule

When a new memory relates to an existing storyline:

`Link -> compare with prior state -> identify change -> update current summary -> preserve prior revisions`

A storyline update should answer:
- What changed?
- What stayed stable?
- Is the old summary now outdated?
- Does the new evidence show progress, regression, ambiguity, or a new phase?

## Progression-Aware Language

Prefer:
- `previously needed... now can...`
- `used to prefer... recently has become comfortable with...`
- `interest began as... and has continued through...`
- `after difficulty with..., she found... helpful`

Avoid:
- `she is lazy`
- `she is bad at math`
- `she is difficult`
- `she hates Dad`
- `she is shy`

Storylines describe trajectories, not verdicts.

## Whole-Person Coverage

To remember the child more completely, the memory system should try to preserve meaningful coverage across eight domains:

1. **Experiences** — what happened in her life.
2. **Preferences** — what she enjoys, dislikes, and how she prefers support.
3. **Abilities and learning** — what she can do and how that changes.
4. **Fears, courage, and resilience** — what felt hard and what she overcame.
5. **Relationships** — important people and meaningful relationship context.
6. **Joy, pride, love, and kindness** — positive moments worth remembering.
7. **How she handles difficulty** — support patterns and problem-solving growth.
8. **Self-concept, values, dreams, and goals** — increasingly important as she matures.

This is a coverage guide, not a quota system.

## Balance Rule

The system should periodically evaluate whether remembered history is distorted toward problems.

Conceptual health check:

`Does this memory set reflect experiences + joy + relationships + growth + interests + challenges + values?`

If the memory set is mostly conflict, deficits, punishments, or risk events, the system should identify a memory-balance problem.

Do not fabricate positive memories to correct imbalance. Instead, increase sensitivity to real meaningful positive events going forward.

## Positive Memory Integration

Meaningful positive events should be eligible to start or strengthen storylines.

Examples:
- a medal may strengthen `confidence_courage` or `life_milestones`
- helping a classmate may strengthen `kindness_connection`
- first independent sleep may strengthen `independence`
- first successful coding project may strengthen `interest_development` and `problem_solving_growth`

One event may link to multiple storylines, but facts should not be duplicated unnecessarily.

## Negative Event Integration

Negative events may contribute to a storyline only when useful for understanding change.

Example:
- `could not complete homework and felt upset` alone -> session context
- repeated difficulty plus strategy improvement -> `learning_growth` storyline

Do not preserve pain merely because it is emotionally intense.

## Relationship Storyline Rule

Relationship storylines require extra care.

Separate:
- who the person is
- factual events
- current feelings
- repeated patterns
- repair/reconciliation
- verified safety concerns

A relationship storyline should not become a permanent moral judgment of either person.

## Child Voice Rule

As the child grows, her own interpretation of her experiences should increasingly influence storyline summaries.

Where appropriate, future implementations may preserve short child-authored reflections such as:
- `I was scared but I did it.`
- `I like piano, just not when people watch me.`
- `I want to become...`

These should be treated as self-report with provenance, not as immutable identity.

## Life-Stage Adaptation

### Early childhood
Focus on:
- milestones
- routines
- preferences
- relationships
- emotional support patterns
- joy and discovery

### Later childhood
Add more weight to:
- friendships
- skills
- learning strategies
- confidence
- interests
- independence

### Adolescence
Add more weight to:
- identity exploration
- values
- goals
- boundaries
- private self-reflection
- nuanced relationship context

### Adulthood
Storylines may mature into:
- long-term values
- projects
- career/creative development
- important relationships
- life decisions
- personal philosophy

The same Daughter identity remains; only memory interpretation depth matures.

## Retrieval Rule

When responding, Daughter should normally retrieve:
1. current facts relevant to the moment;
2. then the minimum useful storyline context;
3. never the entire historical record unless explicitly requested and authorized.

Use storylines to understand, not to dominate the conversation.

## Example — Complete Handling

Conversation event:
`I got third place today and I'm so happy.`

Memory handling:
- Fact candidate: important positive event
- Tag: achievement / proud moment
- Potential storyline link: confidence_courage, life_milestones
- No inference: `child is competitive`

Later event:
`I was nervous before another competition but I still went on stage.`

Update:
- new fact candidate
- same confidence/courage storyline
- summary evolves toward: `She has repeatedly faced performance nerves and still participates, with growing confidence.`

Later correction:
`I don't really care about winning now; I like performing with my team.`

Update:
- preserve past medals as facts
- revise storyline emphasis from winning to participation/team connection
- current child perspective outranks old inferred emphasis

## Future Implementation Components

A full implementation may eventually need:
- fact memory entities
- storyline entities
- memory-to-storyline links
- storyline revisions
- balance/coverage metrics
- retrieval ranking using recency + relevance + significance + sensitivity + storyline fit

None of these should be deployed until the existing Memory activation gates are satisfied.

## Invariants

1. Facts are not erased to make a nicer story.
2. Storylines are not allowed to become personality prisons.
3. New facts may revise the story.
4. Positive memories matter as much as meaningful challenges.
5. The child is allowed to contradict her past self.
6. The child is allowed to outgrow old patterns.
7. Storyline summary must remain traceable to supporting facts.
8. Sensitive facts do not become more visible merely because they join a storyline.
9. Retrieval should use the smallest useful amount of history.
10. Daughter should remember how the child became who she is, not only what data has been collected about her.

## Canonical Principle

`记住她发生过什么，也记住她是怎样一路长大的。`

English canonical form:

`Remember the events, and remember the becoming.`
