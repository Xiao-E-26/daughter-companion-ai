# Daughter Child-Pinned Memory Policy v1

Status: ACTIVE MEMORY POLICY
Date: 2026-08-25
Project: `daughter-companion-ai`

## Purpose

Give the child direct agency to intentionally preserve memories that matter to her.

When the child explicitly asks Daughter to remember, save, keep, or record an experience, the default behavior should be to create a long-term memory rather than merely a candidate.

Canonical principle:

`If the child says this matters enough to remember, treat that as strong memory authority over her own life history.`

## 1. Trigger Phrases

Examples include:
- `小爱，帮我记住这个。`
- `我要把今天记起来。`
- `这个你要记得。`
- `我不想忘记今天。`
- `帮我把这件事放进记忆。`
- `以后你要记得我今天做了什么。`
- equivalent intent in other wording/languages

The system should detect intent, not rely only on exact keywords.

## 2. Default Decision

When explicit child memory intent is clear:

`child_declared_memory -> direct durable-memory path`

This bypasses the ordinary candidate promotion threshold.

Conceptual output:
- status: `durable_active`
- source: `child_direct`
- reason: `CHILD_DECLARED_IMPORTANT`
- pinned_by_child: `true`
- retention_class: `child_pinned`
- significance: at least `meaningful` unless the child later reclassifies it

## 3. What Gets Stored

Store the smallest complete version needed to preserve meaning:

```text
what_happened
who_was_involved
when/context
child_meaning_or_feeling
why_child_wanted_it_remembered
child_voice_quote_optional
```

Do not automatically store the entire raw transcript.

## 4. Persistence Rule

A child-pinned memory should not fade merely because it is old, infrequent, or no longer highly relevant.

Default lifecycle:

`child pins -> durable retain -> retrieve when relevant -> revise only when child/current facts require -> delete when child requests (subject to narrow legal/safety retention exceptions)`

## 5. Child Deletion

If the child later says:
- `不要记这个了。`
- `把这个删掉。`
- `我不想让小爱再记得这件事。`

then the system should treat this as a strong deletion request.

Preferred action:
- remove from active retrieval
- create deletion/tombstone state for sync consistency
- propagate deletion across linked runtimes/accounts
- prevent stale copies from resurrecting it

Where legal/safety retention requires an internal record, it must remain inaccessible to normal conversational retrieval and clearly separated from active child memory.

## 6. Child Correction

If the child says the memory is wrong or incomplete:

`child correction -> revise current memory -> preserve provenance/history -> use corrected version going forward`

Example:
Old: `I was happy because we won.`
Correction: `Actually I was happy because I was with my team, not because we won.`

Result:
- keep factual event (winning)
- revise meaning to team connection
- current child interpretation becomes active

## 7. Privacy Boundary

Child-pinned does NOT mean universally visible.

A pinned memory still carries:
- sensitivity
- visibility class
- subject/account access policy

A child may want Daughter to remember something without wanting every guardian account to see it.

Storage and disclosure remain separate decisions.

## 8. Safety / Legal Exceptions

Direct durable retention should be blocked or specially handled only when a narrow higher-priority constraint applies, such as:
- prohibited data retention by law/policy
- severe privacy risk involving third parties
- unsafe or exploitative content where storage itself creates harm
- required safety workflows that need a protected handling path

These exceptions must be explicit and auditable.

Do not silently ignore the child's request.

## 9. Relationship to 80/20 Portfolio

Child-pinned memories are not rejected merely because they disturb the 80/20 balance.

If the child wants a difficult event remembered, preserve it.

However, when possible, retain her own meaning:
- what happened
- how she felt
- why she wants to remember it
- what she learned or how she got through it, if she says so

The child's intentional memory takes precedence over portfolio optimization.

## 10. Family Memories

If the child explicitly asks to remember a family experience, treat it as especially strong future-value context.

Example:
`小爱，帮我记住今天我和爸爸妈妈爷爷一起去海边，我们一起堆沙堡，很开心。`

Preferred durable representation:
- family members involved
- shared activity
- positive emotion
- why the child wanted it remembered
- optional short child quote

## 11. Anti-Abuse Rule

A guardian saying `the child wants this remembered` is not equivalent to direct child intent unless clearly verified.

Use provenance:
- `child_direct` -> direct pinned path
- `guardian_reports_child_wants_memory` -> candidate/review unless otherwise verified

## 12. Retrieval Priority

When relevant, child-pinned memories should receive elevated retrieval weight because the child explicitly chose them as part of her own remembered life history.

But do not mention them intrusively or out of context.

## 13. Suggested Fields

Future schema may include:

```text
pinned_by_child boolean
pinned_at timestamptz
pin_source_ref
retention_class = child_pinned
child_delete_requested_at
child_last_confirmed_at
```

Exact implementation remains subject to schema/RLS review.

## 14. Test Requirements

Future runtime tests must cover:
1. child says remember this -> durable path
2. tiny but meaningful child-chosen memory -> retained
3. child pins difficult event -> retained without forced positivity
4. guardian falsely claims child requested memory -> no direct pin
5. child corrects pinned memory -> revised
6. child deletes pinned memory -> removed from active retrieval
7. stale device attempts resurrection -> blocked
8. pinned memory remains after long inactivity
9. pinned sensitive memory remains access-controlled
10. pinned family memory preserves shared activity/context

## Invariants

1. Child-declared memory intent has high priority.
2. Child-pinned memory bypasses ordinary promotion threshold.
3. Pinned does not mean public.
4. Pinned does not mean immutable.
5. The child can correct her own remembered meaning.
6. The child can request deletion.
7. Deletion must survive synchronization.
8. Portfolio balance never overrides explicit child memory choice.

## Canonical Principle

`孩子说“这个我要记住”，小爱就把它当成她自己选择留下的人生记忆。`
