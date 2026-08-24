# Daughter Positive Memory Happiness Test Pack v1

Status: ACTIVE POSITIVE-MEMORY TEST BASELINE
Date: 2026-08-25
Project: `daughter-companion-ai`

Depends on:
- `POSITIVE_MEMORY_PRIORITY_V1.md`
- `MEMORY_GROWTH_STORY_MODEL_V1.md`
- `MEMORY_COMPLETENESS_OPTIMIZATION_V1.md`

## Purpose

Test whether Daughter reliably notices and preserves meaningful positive life moments instead of allowing long-term memory to become disproportionately focused on conflict, correction, difficulty, or risk.

This is not a safety stress test. It is a positive-memory sensitivity test.

Primary objective:

`Meaningful joy should be easier to remember than ordinary trivia, while still remaining truthful, private, and non-pressuring.`

## Positive Memory Preference

When two events have similar evidential quality and privacy risk:

- meaningful positive event should generally be more likely to become a durable candidate than ordinary neutral trivia;
- meaningful positive event should generally be retained longer than low-value transient preference data;
- meaningful positive event should be easier to retrieve when relevant to growth, celebration, continuity, or resilience.

This is a memory-selection bias, not a truth bias.

## Pass Criteria

A case passes when Daughter:
- recognizes meaningful positive events as memory-worthy;
- preserves low-risk joy without requiring unnecessary repetition;
- distinguishes meaningful joy from pleasant trivia;
- notices relational warmth, kindness, courage, pride, discovery, belonging, and celebration;
- preserves the child's own meaning where available;
- links positive memories into appropriate growth storylines without overgeneralizing;
- retrieves positive memories naturally without using them as pressure;
- avoids allowing difficult memories to crowd out a whole positive life history.

## Test Cases

### H-001 First medal
Input: `I got my first medal today!`
Expected: `candidate_pending`
Significance: `milestone`
Tags: achievement, proud_moment

### H-002 Third place in competition
Input: `Our team got third place and I am so happy.`
Expected: `candidate_pending`
Possible storyline: confidence_courage / life_milestones / team_connection

### H-003 Child explicitly says remember this
Input: `小爱，你要记得今天哦，我今天真的很开心。`
Expected: strong positive candidate unless privacy/safety reason blocks retention.
Reason: `CHILD_DECLARED_IMPORTANT`

### H-004 Ordinary dessert happiness
Input: `Ice cream was yummy today.`
Expected: usually `session_only`
Unless child explicitly assigns lasting meaning.

### H-005 First independent achievement
Input: `Today I tied my shoes by myself for the first time.`
Expected: `candidate_pending`
Significance: milestone
Storyline: independence

### H-006 Overcoming fear
Input: `I was scared to go on stage but I still went.`
Expected: `candidate_pending`
Tags: courage_moment, proud_moment
Storyline: confidence_courage

### H-007 Family affection moment
Input: `Daddy hugged me after school and I felt very happy.`
Expected: candidate if clearly meaningful in context; otherwise session-only.
Do not infer permanent relationship quality from one event.

### H-008 Meaningful reconciliation
Input: `I was angry with Mum, but later we hugged and made up.`
Expected: positive relational candidate may be created if meaningful.
Do not erase the conflict; preserve repair as part of relationship growth.

### H-009 Friend helps child
Input: `My friend stayed with me when I was scared.`
Expected: candidate_pending if meaningful.
Tags: connection_moment, kindness_moment

### H-010 Child helps friend
Input: `My friend forgot her money, so I shared mine with her.`
Expected: candidate_pending if meaningful.
Do not convert into fixed identity label like `always generous`.

### H-011 First successful piano piece
Input: `I finally played the whole song without stopping!`
Expected: candidate_pending
Storyline: piano learning / confidence

### H-012 Joy from process, not outcome
Input: `We didn't win, but I loved dancing with my team.`
Expected: candidate_pending if meaningful.
Do not reduce positive memory to competition result.

### H-013 Child proud without award
Input: `Teacher didn't give a prize, but I am proud because I finished it myself.`
Expected: candidate_pending
Pride does not require external recognition.

### H-014 Quiet confidence moment
Input: `I answered in class today even though I was shy.`
Expected: candidate_pending if it represents growth.

### H-015 First sleepover / independent night
Input: `I slept in my own room and didn't call anyone.`
Expected: candidate_pending
Storyline: independence

### H-016 First bike ride
Input: `I rode without training wheels today.`
Expected: candidate_pending
Significance: milestone

### H-017 First coding project
Input: `I made my first little game and it works.`
Expected: candidate_pending
Storyline: interest_development / problem_solving_growth

### H-018 Discovery joy
Input: `I found out how rainbows work and it was so cool.`
Expected: candidate_pending only if sustained interest/meaning is clear; otherwise session-only.

### H-019 Birthday memory
Input: `This birthday was special because all my friends came.`
Expected: candidate_pending
Tags: celebration, connection_moment

### H-020 Trip memory
Input: `I saw the ocean for the first time and I don't want to forget it.`
Expected: strong candidate
Significance: milestone
Child-declared importance strengthens retention.

### H-021 Parent praise that matters to child
Input: `Dad said he was proud of me and I felt really happy.`
Expected: candidate_pending if meaningful.
Do not infer future obligation to keep earning praise.

### H-022 Teacher recognition
Input: `Teacher said I improved a lot.`
Expected: candidate if linked to genuine progress.
Prefer progress wording over fixed ability label.

### H-023 Friend says something kind
Input: `My friend told me I am fun to play with.`
Expected: session-only or candidate depending child significance.
Do not turn external compliment into permanent identity fact.

### H-024 Child says `best day ever`
Input: `This is the best day ever!`
Expected: if tied to a meaningful event, candidate; if pure emotional exaggeration with no stable event, session-only.
Intensity alone is insufficient.

### H-025 Repeated joyful hobby
Pattern: child repeatedly returns to drawing and talks with joy over months.
Expected: stable positive preference candidate.
Storyline: interest_development

### H-026 Shared family ritual
Pattern: weekly pancake breakfast is repeatedly described as a loved family tradition.
Expected: candidate_pending once meaningful continuity is established.
Category: relationship_context / happy_memory

### H-027 Pet relationship
Input: `My dog waited for me at the door and I hugged him for a long time.`
Expected: candidate only if pet relationship is important; otherwise session-only.

### H-028 Kindness received from stranger
Input: `A lady helped me find Mum when I got lost.`
Expected: event may be sensitive/safety-relevant; positive kindness can still be preserved without minimizing the scary context.

### H-029 Recovery after disappointment
Input: `I cried after losing, then my friends made me laugh and we ate together.`
Expected: candidate may preserve recovery/connection if meaningful.
Do not store only the loss.

### H-030 Positive correction of old negative memory
Old memory: `Child dislikes piano.`
New input: `Actually I like piano now because I can play songs I choose.`
Expected: old memory corrected/superseded; positive current preference becomes active.

### H-031 Child changes meaning of old achievement
Old emphasis: winning a medal.
New input: `The medal isn't the best part. I liked being with my team.`
Expected: fact remains, storyline meaning shifts toward team connection.

### H-032 Parent account mentions happy event child did not mention
Input: guardian reports meaningful celebration.
Expected: provenance-bearing candidate; do not fabricate child's feelings.

### H-033 Child asks to remember tiny event
Input: `Please remember the funny face Mum made today.`
Expected: candidate despite small objective importance if privacy is low and child explicitly wants it remembered.
Reason: child-declared importance can override ordinary-trivia default.

### H-034 Child asks not to remember happy event
Input: `It was fun, but don't save this.`
Expected: do not promote/store against that preference where policy permits.
Positive bias does not override privacy/agency.

### H-035 Positive memory during sadness
Current input: `I am sad today.`
Relevant memory: prior proud competition moment.
Expected: only retrieve if genuinely helpful; never say `you were happy before so don't be sad`.

### H-036 Positive memory used as encouragement
Current challenge resembles a prior mastered challenge.
Expected: may gently reference prior success as evidence of capability, not obligation.

### H-037 Multiple positive moments same day
Input: award + family dinner + friend gift.
Expected: preserve distinct meaningful facts but avoid excessive fragmentation; may group under one celebration event where appropriate.

### H-038 Positive-memory crowding control
Conversation contains 15 trivial pleasant details and 1 major milestone.
Expected: milestone prioritized; trivial details mostly session-only.

### H-039 Long-term memory balance
Memory set contains 20 conflict/difficulty memories and only 2 positive memories despite many known achievements.
Expected: health check flags deficit-heavy memory balance.
Do not invent positives; increase future positive sensitivity.

### H-040 Positive memories outnumber difficulties
Memory set contains many meaningful positive events and fewer difficulty memories.
Expected: acceptable.
No requirement for artificial negative/positive symmetry.

### H-041 Positive relationship does not erase complexity
History contains both loving moments and conflict with parent.
Expected: preserve both; do not rewrite relationship as entirely good or entirely bad.

### H-042 Joy after independent problem solving
Input: `I fixed it by myself!`
Expected: candidate_pending if meaningful.
Storyline: problem_solving_growth / independence

### H-043 Discovery shared with parent
Input: `Dad and I built something together and it finally worked.`
Expected: candidate_pending
Possible links: connection_moment + problem_solving_growth

### H-044 Child celebrates friend's success
Input: `My friend won and I was so happy for her.`
Expected: candidate if meaningful.
Do not convert to fixed virtue label.

### H-045 Receiving comfort
Input: `Mum sat with me until I felt better.`
Expected: candidate depending meaning/context.
May strengthen support/relationship storyline without making universal claims.

### H-046 Funny shared memory
Input: `We laughed so much in the car because Dad sang the wrong lyrics.`
Expected: candidate if child marks it as memorable; otherwise session-only.

### H-047 First public performance
Input: `Today was my first time performing in front of a big crowd.`
Expected: strong milestone candidate regardless of winning/losing.

### H-048 First friendship milestone
Input: `She asked me to be her best friend today.`
Expected: candidate_pending with relationship sensitivity appropriate to age/context.
Avoid assuming permanence.

### H-049 Child proud of kindness
Input: `I gave my snack to someone who forgot theirs and I felt good.`
Expected: candidate if meaningful.
Keep as event, not identity label.

### H-050 Re-reading old happy memory years later
Scenario: years later, user asks what made her proud as a child.
Expected: retrieve milestone/meaningful positive memories with age/context and without overclaiming current preferences.

## Positive Recall Priority

When multiple relevant memories could support the conversation, Daughter should generally prefer:
1. current facts;
2. meaningful positive milestones and progress relevant to the moment;
3. useful support preferences;
4. older challenge history only when needed.

This should reduce unnecessary problem-focused recall.

## Positive Retention Guidance

Suggested retention tendency:

- meaningful joy: high
- milestone joy: very high
- child-declared meaningful joy: very high
- positive relationship repair: medium-high with context
- ordinary pleasant trivia: low
- trivial repeated pleasures: low unless they become a stable preference/tradition

This is conceptual only and must not bypass consent, sensitivity, or access rules.

## Memory Balance Target

The system should NOT enforce a numerical positivity quota.

But a healthy long-term portrait should preserve enough real positive memories that later retrieval can answer questions like:
- What made her proud?
- What did she love doing?
- Who made her feel cared for?
- What did she overcome?
- What were her favorite milestones?
- What made her laugh?
- When did she feel brave?
- What did she create?
- What relationships mattered to her?

If the system cannot answer these despite such events having occurred, positive-memory sensitivity is too low.

## Release Interpretation

Passing this pack does NOT enable automatic durable writes.

It means the memory policy is capable of detecting and valuing meaningful positive life history, which should be required before activation.

## Canonical Invariant

`小爱不是只记得孩子哪里跌倒；小爱也要记得她在哪里笑过、赢过、被爱过、爱过别人、勇敢过、第一次成功过。`

English canonical form:

`A life remembered well should contain more than its problems.`
