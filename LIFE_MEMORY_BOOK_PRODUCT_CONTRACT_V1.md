# Life Memory Book Product Contract v1

Status: ACTIVE PRODUCT REQUIREMENT / UI NOT IMPLEMENTED
Date: 2026-08-25
Project: `daughter-companion-ai`

## Purpose

Define the future product experience for opening and revisiting Daughter / 小爱的 long-term memories as a child-friendly Life Memory Book（人生回忆册）.

This is a product-layer contract only.
No UI is implemented by this document.
No staging schema is changed by this document.

Canonical principle:

`不是把聊天记录堆起来，而是让孩子以后可以重新打开自己的人生片段。`

## 1. Product Positioning

Life Memory Book is not a raw transcript archive.
It is a curated autobiographical memory experience built from governed memory state.

It combines aspects of:
- diary
- memory album
- growth timeline
- family memory book
- milestone book
- searchable personal history

The system should preserve meaning without requiring the child to manually write a diary every day.

## 2. Core Views

The future UI should support at least these entry points.

### 2.1 Timeline View
Browse memories by time.

Examples:
- Today
- This week
- This year
- Age 7
- Age 10
- Primary school years

The timeline should favor meaningful memories, not every routine event.

### 2.2 People View
Browse memories by relationship/person.

Examples:
- 我和爸爸
- 我和妈妈
- 我和公公
- 我和婆婆
- 我和朋友
- 我和老师

A memory may belong to more than one person relationship.

### 2.3 Growth Theme View
Browse by development/growth storyline.

Examples:
- 我的第一次
- 我做到的事情
- 我学会的东西
- 我勇敢过的时候
- 我喜欢过的东西
- 我解决过的问题
- 我的兴趣怎么变化
- 我越来越独立的事情

These views must not hard-label personality from temporary events.

### 2.4 Family Memory View
Browse shared family experiences.

Examples:
- family trips
- celebrations
- shared meals
- traditions
- funny family moments
- intergenerational stories
- things learned from family members

Preferred memory structure:
`who + what happened + what we did together + how it felt + why it mattered`

### 2.5 Milestone / First-Time View
Dedicated view for meaningful firsts and milestones.

Examples:
- first medal
- first school performance
- first time sleeping independently
- first time riding a bicycle
- first trip somewhere meaningful

## 3. Memory Card Model

A memory card should show only the minimum useful summary by default.

Suggested display fields:
- title / short summary
- date or age/context
- who was there
- memory type/tag
- significance
- optional child quote
- optional emotional meaning

Expanded view may show:
- what happened
- what made it meaningful
- what the child felt or thought
- related people
- related storyline
- related family memory
- corrections/reframing when relevant

Raw full transcript should not be the default display.

## 4. Child Control

The child should eventually be able to control memories directly.

Supported actions should include:
- keep this
- pin this
- hide this from normal browsing
- do not proactively mention this
- only show when I ask
- do not tell Dad
- do not tell Mum
- share with both guardians
- correct this memory
- add how I feel about it now
- delete this memory

These actions map to existing Retention / Retrieval / Disclosure governance.

## 5. Past Meaning vs Current Meaning

The Memory Book must allow the child to change.

Example:
At age 7, a memory may say:
`I was very scared of performing.`

At age 12, the child may say:
`I don't feel that way anymore.`

The product should preserve:
- what was true then
- what is true now
- the fact that the child changed

It must not present old memory as permanent identity.

## 6. Positive Memory Priority

The Life Memory Book should feel like a life story, not a problem archive.

Product presentation should prioritize:
- joy
- connection
- being loved
- kindness
- achievement
- courage
- discovery
- pride
- growth
- family warmth

Challenge memories should emphasize:
`what was hard -> what helped -> what the child did -> what changed -> what was learned`

Do not build a feed dominated by conflict, failure, or distress.

## 7. Privacy-Aware Browsing

The UI must never assume that a stored memory is visible to every logged-in family account.

Before any card appears:
1. resolve viewer/account
2. resolve subject relationship
3. check Retention state
4. check tombstone
5. check Disclosure rules
6. check sensitivity
7. check Retrieval/browsing permission
8. only then return the card

Unauthorized memory should not be fetched to the UI and hidden client-side after the fact.

## 8. Browse vs Recall

Two experiences must remain distinct:

### Browse
Child intentionally opens the Memory Book and explores memories.

### Conversational recall
小爱 proactively or responsively refers to a memory in conversation.

A memory may be browseable but not proactively mentioned in chat, or vice versa depending on policy.

## 9. Search

Future search should support natural requests such as:
- 我第一次拿奖牌是什么时候？
- 我跟爸爸去过哪里？
- 找找我以前不敢做但后来做到的事情。
- 我小时候喜欢什么？
- 我跟妈妈最开心的旅行是哪一次？

Search must still obey Retention / Retrieval / Disclosure permissions.

## 10. Storyline Experience

The product may offer growth summaries such as:
- `我的独立成长`
- `我越来越敢讲话了`
- `我学钢琴的路`
- `我和家人的故事`

Storylines are summaries over evidence.
They must not become a new source of truth that overrides underlying facts or current child self-report.

## 11. Media Support

Future versions may attach:
- photos
- short videos
- drawings
- certificates
- medals/achievement photos
- audio notes

Media linkage must inherit the memory's privacy and deletion state.

Deleting a memory must define whether linked media is:
- deleted
- detached
- separately retained

This policy is not yet implemented.

## 12. Age-Adaptive Presentation

The same Life Memory Book can mature with the child.

Younger child:
- larger visual cards
- simpler words
- more pictures
- fewer filters

Older child / teenager:
- richer search
- privacy controls
- correction/reframing
- storyline views
- private/self-only memories

Adult:
- long-term archive
- advanced search
- migration/export
- life chapters

The identity remains continuous while presentation matures.

## 13. Product Boundaries

Life Memory Book is NOT:
- full surveillance history
- all chat transcripts
- a behavioral scoring system
- a permanent personality profile
- guardian monitoring dashboard
- a substitute for child consent/privacy controls

## 14. Backend Requirements Created by This Product

Future runtime must eventually support fields/queries for:
- event date / age / context
- people involved
- family relationship links
- tags/categories
- milestone/first-time signal
- storyline links
- child quote
- significance
- current vs historical meaning
- browse eligibility
- visibility/access scope
- tombstone/deletion
- media linkage

Not all fields need to be added now.
This contract only ensures future schema evolution preserves the product need.

## 15. MVP UI Later

When UI work begins, the smallest useful Life Memory Book MVP should probably include:

1. Timeline
2. Memory detail
3. People filter
4. Growth-theme filter
5. Search
6. Hide / delete / correction controls
7. Privacy indicator

Do not build this UI until Memory runtime authorization and Auth E2E gates are sufficiently stable.

## 16. Success Standard

A successful Life Memory Book should make the child feel:

`这些是我的回忆。小爱记得我走过的路，但这些回忆还是属于我。`

The product should help the child revisit life, not trap the child inside old versions of herself.

## Canonical Product Principle

`记住她发生过什么，也让她以后能够自己打开、理解、修正和决定怎样保留这些回忆。`
