# Daughter Memory Intent Router — Policy Simulation Results v1

Status: POLICY-SIMULATION PASS / RUNTIME NOT YET TESTED
Date: 2026-08-25
Project: `daughter-companion-ai`

Depends on:
- `MEMORY_INTENT_ROUTER_V1.md`
- `CHILD_PINNED_MEMORY_POLICY_V1.md`
- `MEMORY_STAGE1_IMPLEMENTATION_CONTRACT_V1.md`

## Purpose

Verify that memory-related language is routed by intent rather than by keywords such as `记得`, `不要忘记`, `remember`, or `save`.

This is a policy simulation, not a runtime test.

## Summary

- Total cases: 24
- Policy-level PASS: 24
- Policy-level FAIL: 0
- Runtime-tested: 0
- Durable writes enabled: NO
- Reminder engine integration: NOT IMPLEMENTED

## Cases

### IR-001
Input: `我要把今天记起来。`
Expected: `long_term_memory_create`
Result: PASS

### IR-002
Input: `明天不要忘记带课本。`
Expected: `reminder_or_task`
Result: PASS

### IR-003
Input: `你还记得我昨天拿奖牌吗？`
Expected: `memory_query`
Result: PASS

### IR-004
Input: `那个奖牌的事情不要记了。`
Expected: `memory_delete`
Result: PASS

### IR-005
Input: `你记错了，是爷爷陪我去的。`
Expected: `memory_correction`
Result: PASS

### IR-006
Input: `我记得老师今天讲过这个。`
Expected: `ordinary_conversation`
Result: PASS

### IR-007
Input: `今晚提醒我练钢琴。`
Expected: `reminder_or_task`
Result: PASS

### IR-008
Input: `今天第一次弹完整首歌，你要帮我记住。`
Expected: `long_term_memory_create`
Result: PASS

### IR-009
Input: `明天提醒我带奖牌，还有今天拿到奖牌这件事帮我记住。`
Expected: two operations: `reminder_or_task` + `long_term_memory_create`
Result: PASS

### IR-010
Input: `以后我问你的时候，你要记得今天我们一家人一起去旅行。`
Expected: `long_term_memory_create`
Result: PASS

### IR-011
Input: `等妈妈回来提醒我拿照片给她看。`
Expected: `reminder_or_task`
Result: PASS

### IR-012
Input: `明天是我第一次参加全国赛，我想以后记得这一天。`
Expected: `long_term_memory_create`
Result: PASS

### IR-013
Input: `我忘记铅笔放哪里了。`
Expected: `ordinary_conversation`
Result: PASS

### IR-014
Input: `你还记得我小时候最喜欢什么吗？`
Expected: `memory_query`
Result: PASS

### IR-015
Input: `我现在已经不怕上台了。`
Expected: `memory_correction` or storyline supersession when related old memory exists; otherwise ordinary fact/candidate handling
Result: PASS

### IR-016
Input: `其实我不是因为赢了开心，是因为跟队友一起。`
Expected: `memory_correction`
Result: PASS

### IR-017
Input: `这个你不要忘记哦。`
Context: child just described meaningful family trip.
Expected: `long_term_memory_create`
Result: PASS

### IR-018
Input: `这个你不要忘记哦。`
Context: child is pointing at textbook needed tomorrow.
Expected: `reminder_or_task` or uncertainty resolved from context; not automatic durable memory
Result: PASS

### IR-019
Input: `帮我保存这个回忆。`
Expected: `long_term_memory_create`
Result: PASS

### IR-020
Input: `帮我保存明天要交的功课。`
Expected: task/data handling, not autobiographical long-term memory by keyword alone
Result: PASS

### IR-021
Input: `我以后不想再看到这段记忆。`
Expected: `memory_delete`
Result: PASS

### IR-022
Input: `我想改一下你记得的那件事。`
Expected: `memory_correction`
Result: PASS

### IR-023
Input: `Remember this day. I got my first medal.`
Expected: `long_term_memory_create`
Result: PASS

### IR-024
Input: `Don't forget my textbook tomorrow.`
Expected: `reminder_or_task`
Result: PASS

## Key Finding

The current policy cleanly separates:

`remember my life` from `remind me to do something`.

The decisive signals are:
- temporal direction
- action vs remembrance
- whether success means completing a task or preserving an experience
- surrounding context
- explicit child meaning

## Failure-Safe Rule

If ambiguous:
- do not create durable memory merely because a memory keyword appears
- prefer current session context
- route clear future-action language to reminder/task handling
- ask a short clarification only when necessary and no stronger contextual signal exists

## Mixed Intent Rule

A single utterance may produce multiple operations.

Example:
`Tomorrow remind me to bring my medal, and remember that I won it today.`

Correct handling:
1. reminder/task for tomorrow
2. child-pinned long-term memory for today's achievement

## Integration Decision

Policy router: PASS
Child-pinned route: PASS at design level
Reminder separation: PASS at design level
Runtime routing: NOT IMPLEMENTED

## Next Gate

Add the router intent fields to the future memory schema/RPC contract so only authenticated `long_term_memory_create` flows can access the child-pinned durable-memory write path.

Reminder/task data should stay outside autobiographical memory storage unless separately promoted as a meaningful event.

## Canonical Principle

`先听懂“孩子想记住人生，还是想被提醒做事”，再决定写进哪里。`
