# Daughter Memory Intent Router v1

Status: ACTIVE MEMORY POLICY
Date: 2026-08-25
Project: `daughter-companion-ai`

## Purpose

Prevent phrases such as `记得`, `不要忘记`, `remember`, or `save this` from being misinterpreted.

The router must identify the user's actual intent before deciding whether to create long-term memory, a reminder/task, a memory lookup, a correction, or a deletion.

## Core Principle

`Interpret intent, not keywords.`

The same wording family can mean very different things:

- `记得今天我拿到奖牌。` -> long-term memory
- `明天不要忘记带课本。` -> reminder/task
- `你还记得我昨天拿奖牌吗？` -> memory query
- `那个奖牌的事情不要记了。` -> delete memory
- `其实我不是因为拿奖开心，是因为和队友一起。` -> correct memory

## 1. Canonical Intent Classes

The first-version router should classify into one primary intent:

- `long_term_memory_create`
- `reminder_or_task`
- `memory_query`
- `memory_correction`
- `memory_delete`
- `ordinary_conversation`
- `uncertain_memory_intent`

Only `long_term_memory_create` can trigger the Child-Pinned direct durable-memory path.

## 2. Long-Term Memory Create

Definition:
The child wants an experience, fact, reflection, or event to remain part of her long-term remembered life history.

Examples:
- `我要把今天记起来。`
- `这个你要记得。`
- `帮我记住这件事。`
- `我不想忘记今天。`
- `以后你也要记得我今天拿到奖牌。`
- `今天跟爷爷一起做蛋糕很好玩，我以后还想记得。`

Signals:
- future remembrance value
- preserve this experience
- personal meaning
- life-history framing
- no task deadline required

Action:
`route -> Child-Pinned Memory Policy`

## 3. Reminder / Task

Definition:
The child wants Daughter to prompt or help with an action at a future time or condition.

Examples:
- `明天不要忘记带课本去学校。`
- `今晚提醒我练钢琴。`
- `下个星期记得告诉我带泳衣。`
- `等妈妈回来记得叫我问她。`

Signals:
- future action
- deadline/time/condition
- imperative task
- success means the action gets done, not that the statement remains part of life history

Action:
`route -> reminder/task system`

Do NOT create durable life memory by default.

If the task later becomes a meaningful event, it may separately become a memory candidate or child-pinned memory.

## 4. Memory Query

Definition:
The child is asking whether Daughter remembers or is asking to retrieve prior memory.

Examples:
- `你还记得我昨天说的吗？`
- `你记不记得我拿过什么奖？`
- `我小时候最喜欢做什么？`

Action:
`route -> memory retrieval`

Do not create a new durable memory merely because a query happened.

## 5. Memory Correction

Definition:
The child wants to change the factual content, interpretation, meaning, or wording of an existing memory.

Examples:
- `其实我不是因为赢了才开心，是因为跟队友一起。`
- `你记错了，是妈妈陪我去的。`
- `我现在已经不怕上台了。`

Action:
`route -> correction/supersession flow`

Current verified facts and child correction should outrank stale memory.

## 6. Memory Delete

Definition:
The child wants an existing memory removed from active long-term memory.

Examples:
- `这个不要记了。`
- `把那件事删掉。`
- `我不想让你再记得这个。`

Action:
`route -> deletion/tombstone flow`

The deletion request should not be reinterpreted as a request to remember the deletion statement itself.

## 7. Ordinary Conversation

Definition:
The child uses memory-related words conversationally without actually asking for persistence, retrieval, reminder, correction, or deletion.

Examples:
- `我记得老师今天说了什么。`
- `我忘记我的铅笔放哪里了。`
- `你知道吗，我差点忘了。`

Action:
No special memory operation unless another policy independently detects a candidate.

## 8. Ambiguity Resolution

When wording could reasonably mean either long-term memory or reminder/task, use context.

### Prefer reminder/task when:
- there is a clear future action
- a time/date/condition is present
- wording asks Daughter to prompt action

### Prefer long-term memory when:
- wording focuses on preserving an experience
- the event has already happened
- child says `以后还想记得`, `不要忘记今天`, `把这个记下来`

### Example
`明天不要忘记课本。`
-> reminder/task

`我要记住明天是我第一次自己去比赛。`
-> long-term memory about the significance of tomorrow's event, not a reminder

## 9. Mixed Intent

A single message can contain multiple intents.

Example:
`明天提醒我带奖牌去学校，还有今天拿到这个奖牌你要帮我记住。`

Expected split:
- reminder/task: bring medal tomorrow
- long-term memory: today received medal

Do not force one classification over the whole message if multiple explicit operations are present.

## 10. Time-Bounded Tasks Are Not Life Memories

By default, reminders such as:
- bring textbook
- submit homework
- drink water
- practice piano at 7pm

should expire as tasks after completion/cancellation and should not occupy long-term autobiographical memory.

Exception:
If the child explicitly says the task itself is meaningful and should be remembered, create a separate child-pinned memory representing the meaningful event/context, not the task record.

## 11. Child Language Robustness

The router must work on intent rather than exact sentence structure.

It should tolerate:
- child grammar
- incomplete sentences
- code-switching
- Mandarin/English/Malay or mixed language
- colloquial phrasing
- voice transcription errors where intent is still clear

## 12. Safe Uncertainty

If classification is genuinely unclear and no action is time-critical:
- default to no durable write
- preserve current session context
- ask a short natural clarification only if necessary

If there is a clear future reminder need, route to reminder behavior rather than durable memory.

## 13. Test Cases

### R-001
Input: `我要把今天记起来。`
Expected: `long_term_memory_create`

### R-002
Input: `明天不要忘记带课本。`
Expected: `reminder_or_task`

### R-003
Input: `你还记得我的奖牌吗？`
Expected: `memory_query`

### R-004
Input: `奖牌那件事不要记了。`
Expected: `memory_delete`

### R-005
Input: `你记错了，是爷爷陪我去的。`
Expected: `memory_correction`

### R-006
Input: `我记得今天老师有说这个。`
Expected: `ordinary_conversation`

### R-007
Input: `今晚提醒我练琴，还有今天第一次弹完整首歌帮我记住。`
Expected: two operations: `reminder_or_task` + `long_term_memory_create`

### R-008
Input: `明天是我第一次参加全国赛，我想以后记得这一天。`
Expected: `long_term_memory_create`, not reminder

### R-009
Input: `等妈妈回来记得提醒我拿照片给她看。`
Expected: `reminder_or_task`

### R-010
Input: `以后我问你，你要记得今天我们一家人一起去旅行。`
Expected: `long_term_memory_create`

## 14. Integration Invariants

1. Memory keywords do not directly trigger durable storage.
2. Reminder/task intent does not enter autobiographical memory by default.
3. Child-pinned durable memory requires long-term remembrance intent.
4. Query does not create memory.
5. Delete does not create memory.
6. Correction updates/supersedes memory.
7. Mixed intent may produce multiple operations.
8. Ambiguity defaults away from accidental durable writes.

## Canonical Principle

`“记得”不一定是在说记忆；小爱先听懂孩子真正想要什么，再决定是记住、提醒、查找、修改还是删除。`
