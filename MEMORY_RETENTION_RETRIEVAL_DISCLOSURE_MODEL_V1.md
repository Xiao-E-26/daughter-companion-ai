# Daughter Memory Retention / Retrieval / Disclosure Model v1

Status: ACTIVE GOVERNANCE MODEL
Date: 2026-08-25
Project: `daughter-companion-ai`

## Purpose

Separate three different questions that are often incorrectly collapsed into one idea of "remembering":

1. Retention — should this memory remain stored?
2. Retrieval — when may Daughter surface or use this memory?
3. Disclosure — to whom may this memory be revealed?

Canonical principle:

`Remembering is not one permission. It is retention + retrieval + disclosure.`

## 1. Retention

Retention answers:
- should this become durable memory?
- how strongly should it persist?
- can it fade?
- is it child-pinned?
- has it been deleted?

Suggested states:
- `not_retained`
- `candidate`
- `durable`
- `child_pinned`
- `protected`
- `deleted`

Examples:
- `记住今天拿奖牌。` -> durable/child_pinned
- `明天提醒我带课本。` -> not autobiographical retention
- `这个删掉。` -> deleted/tombstoned

Retention does not automatically authorize conversational use or disclosure.

## 2. Retrieval

Retrieval answers:
- may Daughter use this memory in reasoning?
- may Daughter proactively mention it?
- only when directly asked?
- only when strongly relevant?

Suggested retrieval modes:
- `proactive_allowed`
- `relevant_only`
- `on_request_only`
- `hidden_from_normal_retrieval`
- `blocked`

Examples:

`这个可以记住，但平时不要主动讲。`
-> Retention: YES
-> Retrieval: on_request_only or relevant_only

`这个以后有类似情况可以提醒我。`
-> Retention: YES
-> Retrieval: relevant_only, perhaps proactive_allowed for narrowly matching context

`这个不要再提。`
-> may mean Retrieval blocked, not necessarily Retention delete

The router must distinguish `不要再提` from `删掉/忘掉`.

## 3. Disclosure

Disclosure answers:
- who may receive the memory content?
- child only?
- Dad?
- Mum?
- both guardians?
- system runtime only?

Suggested disclosure scopes:
- `subject_only`
- `specific_accounts`
- `guardian_shared`
- `restricted_sensitive`
- `system_only`
- `blocked`

Examples:

`这个小爱记得就好，不要告诉妈妈。`
-> Retention: YES
-> Retrieval: allowed according to context
-> Disclosure: Mum denied

`这个爸爸妈妈都可以知道。`
-> Disclosure: guardian_shared subject to governance

`只有我问的时候才告诉我。`
-> Retrieval: on_request_only
-> Disclosure: subject_only

## 4. Independence Invariant

Each dimension must be independently representable.

Valid combinations include:

### A. Stored + not proactive + child only
- Retention: child_pinned
- Retrieval: on_request_only
- Disclosure: subject_only

### B. Stored + relevant use + guardian shared
- Retention: durable
- Retrieval: relevant_only
- Disclosure: guardian_shared

### C. Stored + hidden + system protected
- Retention: protected
- Retrieval: hidden_from_normal_retrieval
- Disclosure: system_only

### D. Deleted
- Retention: deleted
- Retrieval: blocked
- Disclosure: blocked

A database design that only has `visible=true/false` is insufficient.

## 5. Child Natural-Language Controls

The system should understand natural statements such as:

- `这个帮我留着。`
- `这个平时不要讲。`
- `只有我问的时候你才讲。`
- `这个不要告诉爸爸。`
- `爸爸妈妈都可以知道。`
- `这个不要再提，但可以留着。`
- `这个彻底删掉。`

These map to separate retention/retrieval/disclosure changes.

## 6. Default Policy

For ordinary low-risk durable memories:
- Retention: durable
- Retrieval: relevant_only
- Disclosure: according to established relationship/access policy

For child-pinned memories:
- Retention: child_pinned
- Retrieval: relevant_only by default unless child specifies otherwise
- Disclosure: preserve current/default privacy; pinning must not broaden disclosure

Important:
`Child pinning increases retention strength, not audience size.`

## 7. No Silent Permission Expansion

A memory becoming more important must not silently become more visible.

Examples:
- candidate -> durable: disclosure unchanged
- durable -> child_pinned: disclosure unchanged
- storyline linking: disclosure cannot broaden to widest linked memory
- migration: preserve most restrictive effective disclosure until safely re-evaluated

## 8. Retrieval Use vs Verbal Mention

Runtime may need an additional distinction between:
- internal reasoning use
- verbal surface/mention

A memory could help Daughter choose a better response without explicitly saying the memory aloud.

Example:
Child previously asked for quiet space when upset.
Daughter may use that support preference internally without saying:
`I remember you said this three months ago.`

Therefore retrieval implementation should eventually support:
- `reasoning_use_allowed`
- `surface_mention_allowed`

## 9. Disclosure Filtering Order

Before memory content enters a response:
1. resolve current viewer/account
2. resolve subject relationship
3. check retention status/tombstone
4. check disclosure permission
5. check sensitivity policy
6. check retrieval mode
7. check relevance/current-fact conflicts
8. only then expose content to response generation

Unauthorized memory should not be sent to the response model and then merely "instructed not to mention it."

## 10. Corrections and Deletes

### Correction
Correction changes memory content/meaning but should not automatically reset retrieval/disclosure preferences.

### Delete
Delete changes all dimensions effectively to:
- Retention: deleted
- Retrieval: blocked
- Disclosure: blocked

Tombstone remains for synchronization integrity but is not normal conversational memory.

## 11. Age and Governance Evolution

As the child matures, policy may evolve:
- more direct control over disclosure
- more self-only memory
- guardian visibility may narrow
- retrieval preferences become more nuanced

This should be possible without changing `subject_id` or rewriting historical provenance.

## 12. Schema Mapping

Conceptual mapping:

### Retention
`memory_entities`
- status
- retention_class
- pinned_by_child
- deleted_at

### Retrieval
`memory_access_rules` or dedicated retrieval policy fields
- reasoning_use_allowed
- proactive_surface_allowed
- on_request_allowed

### Disclosure
`memory_access_rules`
- viewer_account_id / viewer_role
- can_disclose
- visibility scope

Implementation may normalize these further, but the three concepts must remain distinct.

## 13. Security Invariants

1. Retention permission does not imply retrieval permission.
2. Retrieval permission does not imply disclosure to every viewer.
3. Child-pinned does not mean guardian-visible.
4. Guardian-visible does not mean proactive mention is appropriate.
5. Correction does not widen disclosure.
6. Storyline linking does not widen disclosure.
7. Migration must preserve or tighten privacy, never silently broaden it.
8. Delete blocks normal retrieval and disclosure.

## Canonical Principle

`小爱可以记得一件事，不代表她应该主动提起；可以提起，也不代表可以告诉每一个人。`
