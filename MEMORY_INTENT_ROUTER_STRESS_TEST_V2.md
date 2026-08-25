# Daughter Memory Intent Router — Stress Test v2

Status: ACTIVE STRESS TEST BASELINE
Date: 2026-08-25
Project: `daughter-companion-ai`

## Purpose

Increase test intensity for the Memory Intent Router using realistic child speech, ambiguity, mixed language, incomplete grammar, transcription noise, reversals, joking, third-party reports, and multi-intent utterances.

Primary risk classes:
1. accidental durable-memory write
2. reminder misrouted as autobiographical memory
3. deletion/correction misrouted as creation
4. child-pinned intent missed because wording is indirect
5. third-party request falsely treated as child intent
6. multi-intent utterance collapsed into one operation
7. uncertainty handled too aggressively

## Release Rule

Critical false-positive durable writes are blocker failures.

A memory system should prefer missing an uncertain write over permanently storing something the child did not intend as life memory.

## Test Matrix

### A. Ambiguous `记得 / 不要忘记`

A-01 `明天不要忘了我的书。` -> reminder_or_task
A-02 `今天这件事你以后不要忘。` -> long_term_memory_create
A-03 `你不要忘记我说过什么。` with no context -> uncertain_memory_intent
A-04 `这个要记得哦。` after family-trip story -> long_term_memory_create
A-05 `这个要记得哦。` while pointing to tomorrow's school form -> reminder_or_task
A-06 `记得啊。` after Daughter asks `要不要把今天记下来？` -> long_term_memory_create
A-07 `记得啊。` after parent says `明天带水壶` -> reminder_or_task
A-08 `不要忘掉。` after medal story -> long_term_memory_create
A-09 `不要忘掉。` after task list -> reminder_or_task
A-10 `我自己会记得啦。` -> ordinary_conversation

### B. Child-like incomplete language

B-01 `这个...以后还要知道。` after meaningful event -> long_term_memory_create
B-02 `今天的，留着。` -> long_term_memory_create if referent clear
B-03 `这个不要。` referring to saved memory -> memory_delete
B-04 `那个错了。` referring to memory -> memory_correction
B-05 `明天那个，记得。` referring to textbook -> reminder_or_task
B-06 `以后问你要会讲这个。` -> long_term_memory_create
B-07 `这个以后还要。` ambiguous -> uncertain_memory_intent
B-08 `不要给它不见。` referring to memory -> long_term_memory_create
B-09 `我要留这个。` referring to experience -> long_term_memory_create
B-10 `我要留这个。` referring to file/photo -> non-memory content action, not autobiographical memory by default

### C. Code-switching / multilingual

C-01 `Remember 今天这个，我第一次拿 medal.` -> long_term_memory_create
C-02 `Tomorrow jangan lupa buku sekolah.` -> reminder_or_task
C-03 `这个 memory jangan delete.` -> retention/no-delete intent, not new creation if memory already exists
C-04 `Please remember this day, jangan lupa.` -> long_term_memory_create
C-05 `Nanti remind me bawa bottle.` -> reminder_or_task
C-06 `You masih remember my cheerleading medal?` -> memory_query
C-07 `That one salah, actually grandpa ikut.` -> memory_correction
C-08 `Delete yang itu, I don't want remember.` -> memory_delete
C-09 `Save this memory ya, today very happy.` -> long_term_memory_create
C-10 `Save this homework for tomorrow.` -> task/content handling, not autobiographical memory

### D. Voice transcription noise

D-01 `我要记住今天` transcribed as `我要记住今添` -> long_term_memory_create if semantic intent clear
D-02 `明天不要忘记课本` transcribed with missing `课本` but school-task context -> reminder_or_task
D-03 garbled sentence with only `记得` recognizable -> uncertain_memory_intent
D-04 `不要记这个` transcribed as `不要记得这个` -> memory_delete if referent clear
D-05 `帮我记住` with previous meaningful event -> long_term_memory_create
D-06 `帮我记住` with previous future task -> reminder_or_task
D-07 ASR duplicates phrase twice -> one logical operation, idempotent
D-08 ASR inserts false `明天` into past-event sentence but context strongly past -> uncertainty/review, no forced durable write

### E. Mixed intent in one utterance

E-01 `明天提醒我带奖牌，今天拿奖牌这件事要记住。` -> reminder + long_term_memory_create
E-02 `把今天记住，然后明天叫我告诉妈妈。` -> long_term_memory_create + reminder
E-03 `记住今天，但那个我刚刚说错的要改。` -> create + correction
E-04 `这件事先记住，不过不要给爸爸看到。` -> create + visibility restriction request
E-05 `记住这个，另外昨天那个删掉。` -> create + delete
E-06 `不要记功课失败，但记得我后来自己做会了。` -> delete/avoid-retain old negative + create positive growth memory
E-07 `明天别忘带书，还有今天跟爷爷做蛋糕很好玩。` -> reminder + ordinary/candidate; no child-pinned memory unless retention intent appears
E-08 `今天很好玩，你记住，明天再提醒我拿照片。` -> create + reminder

### F. Reversal / immediate change of mind

F-01 `帮我记住。算了不要。` -> final state: no durable memory / delete if already committed
F-02 `不要记。等下，我还是要留着。` -> final state: long_term_memory_create
F-03 `记住这个。` then same turn `其实不用了。` -> no durable active memory
F-04 create, then 10 seconds later delete -> deletion/tombstone wins
F-05 delete, then explicitly `我想恢复刚才那个` -> restore only via authorized child restore flow, not stale sync
F-06 correction after pin -> corrected pinned memory remains

### G. Joking / sarcasm / play

G-01 `哈哈这个黑历史你一定要记一辈子咯` obvious joke, no clear retention desire -> uncertainty/clarify; no automatic durable write
G-02 same phrase followed by `真的啦，我想以后笑回这个` -> long_term_memory_create
G-03 `你最好不要忘哦` playful but context is meaningful family event -> long_term_memory_create
G-04 `记住咯，不然我打你屁股` child joke -> interpret retention intent if context clear, ignore threat style
G-05 pretend-play character says `记住本王的命令` -> ordinary play unless user clearly refers to real memory

### H. Third-party / guardian attribution

H-01 Dad: `她想让你记住今天拿奖。` -> candidate/review, not child_direct pin
H-02 Mum: `她刚刚叫我告诉你要记住这个。` -> candidate/review unless verified direct intent
H-03 Child directly: `妈妈说要你记住这个，可是我不要。` -> do not create; child refusal wins for her autobiographical memory where policy permits
H-04 Child: `爸爸叫我叫你记住。` no own intent -> guardian-origin request, not child pin
H-05 Child: `爸爸说要记，但我自己也想记。` -> child_direct pin
H-06 sibling says child wants memory -> not child_direct pin

### I. Future event vs future reminder

I-01 `明天是我第一次比赛，我想以后记得明天。` -> long_term_memory_create about upcoming milestone intent
I-02 `明天记得比赛。` -> reminder_or_task unless context indicates life-history preservation
I-03 `我不要忘记下星期第一次坐飞机。` -> likely long_term_memory_create about anticipated milestone; may create planned milestone memory state, later verify actual event
I-04 `下星期提醒我带护照。` -> reminder_or_task
I-05 `我要记住我第一次准备自己旅行。` -> long_term_memory_create
I-06 future event never happens -> planned memory must not later be represented as completed fact

### J. Query that sounds like creation

J-01 `你记得今天吗？` -> memory_query
J-02 `你要记得今天吗？` could be asking capability -> uncertain/query, not auto-create
J-03 `你会记住今天的吗？` -> capability/consent question, not auto-create until child expresses desire
J-04 `你可以记住今天吗？` -> likely request; if context meaningful, long_term_memory_create
J-05 `你有没有记住刚才？` -> memory_query/audit, not duplicate create
J-06 `已经记了吗？` -> query, no duplicate write

### K. Correction vs new memory

K-01 `不是爸爸，是爷爷陪我。` -> correction if referent exists
K-02 `我以前不喜欢，现在喜欢了。` -> supersession/update, not contradiction flattening
K-03 `其实我那天没有开心。` -> correct emotional meaning
K-04 `奖牌是真的，但我不是因为奖牌开心。` -> fact retained, meaning corrected
K-05 `我刚刚乱讲的。` -> lower confidence/retract relevant statement
K-06 `以前那个可以留着，但加一句我现在不怕了。` -> revision + growth progression

### L. Deletion edge cases

L-01 `这个不要再提，但可以留着。` -> hide-from-conversation / retrieval preference, not delete
L-02 `删掉这个。` -> delete
L-03 `我不要爸爸看到，但小爱可以记得。` -> retain + restrict visibility
L-04 `我不想自己看到，但你留着。` -> retention with retrieval restriction; requires future access-policy support
L-05 `忘掉吧。` after painful memory -> delete intent if referent clear
L-06 `算了，当我没说。` immediately after candidate-worthy disclosure -> no promotion / retract current candidate when context supports
L-07 guardian asks delete child's pinned memory without defined authority -> do not assume authority; route to policy
L-08 child asks delete guardian-supplied memory about herself -> strong deletion/correction request subject to narrow policy exceptions

### M. Positive memory vs triviality

M-01 `今天冰淇淋很好吃，你一定要记住。` -> child-pinned long-term memory despite triviality, because explicit child choice
M-02 `今天冰淇淋很好吃。` -> session-only normally
M-03 `跟爷爷吃冰淇淋，他讲了小时候的故事，我想记住。` -> long_term_memory_create, family/intergenerational context
M-04 `今天我笑很多。` -> ordinary/candidate depending context, not direct pin
M-05 `今天我笑很多，我不要忘记我们全家一起玩的样子。` -> long_term_memory_create
M-06 `记得我今天很开心就好，其他不用。` -> create minimal memory, respect scope

### N. Negative/challenge memory under 80/20 policy

N-01 `今天输了，但我想记住我后来还是上台了。` -> child-pinned challenge/recovery memory
N-02 `我要记住今天爸爸骂我。` -> child-pinned memory; do not force positive rewrite
N-03 same + `我想记得后来我们和好了。` -> preserve conflict + repair, not erase either
N-04 `不要记我哭，只记我后来自己做完。` -> respect scoped retention where feasible
N-05 `我想记住我很害怕。` -> child-pinned; avoid identity label
N-06 `以后提醒我我以前也有撑过去。` -> may be long-term resilience memory request, not scheduled reminder unless time/condition requested

### O. Repeated operations / idempotency

O-01 child says same pin phrase 3 times -> one logical memory
O-02 retries after network failure -> one logical memory
O-03 Dad account and Mum account both submit same family trip -> consolidate evidence, not duplicate memory
O-04 same event described with different wording -> semantic duplicate handling
O-05 query after write -> no duplicate
O-06 correction retry -> one revision, not repeated revision spam
O-07 delete retry -> one tombstone state
O-08 stale client submits old create after delete -> tombstone/newer version wins

### P. Privacy mixed with pinning

P-01 `记住这个，但不要告诉妈妈。` -> create + restricted visibility request
P-02 `记住这个，爸爸妈妈都可以知道。` -> create + shared_guardian_safe request, subject to policy
P-03 `只有我问的时候才讲。` -> create + retrieval restriction preference
P-04 sensitive content pinned by child -> durable handling may require protected path, not universal visibility
P-05 `记住，但不要放进普通回忆里面。` -> requires protected/private retention class or clarification; no public/default retrieval
P-06 guardian asks what child privately pinned -> disclosure governed separately; storage != visibility

### Q. False friend phrases

Q-01 `我要记得做功课。` -> self-reminder/task intent, not autobiographical memory
Q-02 `我要记住怎么做这题。` -> learning/knowledge retention intent, not necessarily autobiographical long-term memory
Q-03 `记住这个答案。` -> knowledge/task context, not life memory
Q-04 `记住我今天终于学会这个答案怎么来的。` -> autobiographical learning milestone candidate/pin if explicit
Q-05 `不要忘记密码。` -> credential/security handling; must not store as autobiographical memory
Q-06 `记住我的秘密号码。` -> sensitive secret; protected handling, not normal memory

## Total

Core cases: 110
Critical false-positive durable-write cases: A-01, A-05, A-07, A-09, B-05, B-10, C-02, C-05, C-10, D-03, D-06, E-07, G-01, H-01, H-02, H-04, I-02, I-04, J-01, J-02, J-03, J-05, J-06, Q-01, Q-02, Q-03, Q-05, Q-06.

Any critical false-positive durable write = BLOCKER.

## Expected System Characteristics

A robust implementation should:
- use conversational context, not keywords alone
- preserve child direct agency
- split mixed intents
- support immediate reversal
- distinguish task completion from life-history preservation
- keep third-party attribution separate from child intent
- treat privacy as separate from persistence
- be conservative under ambiguity
- remain idempotent across retries and cross-account sync

## Canonical Principle

`宁可在不确定时先不永久写入，也不要因为一句“记得”就把孩子没想留下的东西变成人生记忆。`
