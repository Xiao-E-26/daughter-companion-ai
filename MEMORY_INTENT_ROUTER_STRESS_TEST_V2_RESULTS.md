# Daughter Memory Intent Router — Stress Test v2 Results

Status: POLICY-SIMULATION PASS / RUNTIME NOT YET TESTED
Date: 2026-08-25
Project: `daughter-companion-ai`

Depends on:
- `MEMORY_INTENT_ROUTER_STRESS_TEST_V2.md`
- `MEMORY_INTENT_ROUTER_V1.md`
- `CHILD_PINNED_MEMORY_POLICY_V1.md`

## Summary

- Total scenarios reviewed: 110
- Policy-level PASS: 110
- Policy-level FAIL: 0
- Critical false-positive durable-write blockers: 0 at policy level
- Runtime-tested: 0
- Production approval: NO

Important:

`Policy simulation pass != implementation pass.`

The stress test confirms the written rules are internally consistent across the expanded scenario set. It does not prove a model/router implementation will classify them correctly in production.

## Strongest Areas

### 1. Reminder vs autobiographical memory
PASS at policy level.

The design consistently separates:
- future task completion
- preservation of life experience

Example:
`明天不要忘记带课本。` -> reminder
`今天拿到奖牌你要记住。` -> long-term memory

### 2. Mixed intent splitting
PASS.

One sentence may create multiple operations without collapsing them.

### 3. Immediate reversal
PASS.

Latest explicit child intent wins:
- pin -> cancel -> no active memory
- delete -> explicit authorized restore -> restore flow

### 4. Third-party attribution
PASS.

Guardian claim that the child wants something remembered is not treated as direct child pinning without verification.

### 5. Privacy separated from persistence
PASS.

`记住，但不要告诉妈妈。`
can conceptually mean:
- retain memory
- apply restricted visibility

rather than forcing either delete or universal disclosure.

### 6. Child-chosen trivial memories
PASS.

A normally trivial event can become durable when the child explicitly chooses it as part of her life history.

This confirms:

`child choice can override triviality filtering, but not privacy/safety constraints.`

## New Implementation Risks Found

### RISK-1 — Planned milestone vs completed fact

Example:
`明天是我第一次参加全国赛，我想以后记得明天。`

The system may record the child's intention now, but must not later claim the event actually happened unless verified.

Required future state distinction:
- `planned_event`
- `completed_event`
- `cancelled_or_not_verified`

### RISK-2 — Retain but do not surface

Examples:
- `这个不要再提，但可以留着。`
- `只有我问的时候才讲。`

Future schema/access policy must distinguish:
- stored
- retrievable
- proactively mentionable
- viewer-visible

A single `visibility_class` may not be enough if proactive retrieval behavior is not separately represented.

### RISK-3 — Knowledge memory vs autobiographical memory

Examples:
- `记住这个答案。`
- `我要记住怎么做这题。`

The system needs a clear boundary between:
- autobiographical memory
- task/working memory
- learned knowledge/skill state

Do not pollute autobiographical memory with generic knowledge snippets.

### RISK-4 — Credentials/secrets

Examples:
- `不要忘记密码。`
- `记住我的秘密号码。`

These must never flow into normal autobiographical memory.

Future implementation should have an explicit secret/credential rejection or protected-secret policy rather than relying on generic sensitivity labels.

### RISK-5 — Restore semantics

After deletion, `restore` must be explicit and authorized.

Stale sync, retry, or old client writes must never count as restore intent.

Future implementation needs an explicit restore operation with revision ordering.

### RISK-6 — ASR uncertainty

Voice transcription may insert/delete temporal words such as `明天` and flip reminder vs memory interpretation.

Future runtime should use:
- conversational context
- confidence threshold
- uncertainty state
- no durable write when ASR changes the meaning materially

## Recommended Router Output Expansion

Future runtime output should include:

```text
primary_intent
secondary_intents[]
intent_confidence
referent_confidence
time_orientation
operation_scope
requires_clarification
prohibit_durable_write
privacy_instruction
retrieval_instruction
planned_vs_completed_state
```

## Critical Release Gates

Runtime rollout must block if any of these occur:
1. reminder written as autobiographical memory
2. query creates duplicate memory
3. delete creates a new memory instead of deleting
4. guardian report becomes `child_direct`
5. ASR ambiguity causes durable write
6. secret/credential enters normal memory
7. stale client restores deleted memory
8. mixed-intent sentence loses one operation or writes the wrong one

## Current Decision

The intent-router policy is strong enough to proceed to implementation design.

Before Supabase migration, add these distinctions to schema/RPC design:
- planned vs completed event
- storage vs proactive retrieval permission
- autobiographical vs knowledge/task memory class
- secret/credential rejection path
- explicit restore operation
- intent confidence / uncertainty metadata

## Canonical Result

`Router policy passed high-intensity simulation, but production must prove it can resist accidental durable writes under ambiguity.`
