# 小爱 Learning Candidate Template v1

Status: ACTIVE WORKFLOW
Purpose: provide a repeatable record for turning real interactions into reviewable learning candidates without silently rewriting permanent behavior.

## Candidate Record

### 1. Source Interaction
- Date / session reference:
- Triggering scenario:
- User/child statement(s):
- What felt successful or wrong:

### 2. Failure / Opportunity Classification
Choose one primary category:
- tone
- misunderstanding
- over-interpretation
- premature advice
- safety
- authority / permission
- memory / context
- reasoning
- runtime state
- decision quality
- other

### 3. Immediate Fix Layer
Choose the lowest correct layer:
- L0 Conversation Adaptation
- Prompt / response style
- Runtime
- Memory / context
- RLS / authorization
- L1 Candidate Insight
- L2 Reusable Capability
- L3 Behavior Core
- L4 Identity / Constitution

Rule: do not promote higher than necessary.

### 4. Candidate Insight
Write the insight as a general principle, not as a child-specific fact.

Bad:
`雨宸不喜欢啦啦队。`

Better:
`Achievement does not prove continued interest; a child’s stable preference should be understood before advice.`

### 5. Generalization Check
- Does this apply beyond one story? yes/no
- Could it help across multiple ages/situations? yes/no
- Is it actually a personal preference rather than a general capability? yes/no
- Could this rule create overreach or over-questioning? yes/no

### 6. Safety / Identity Check
Confirm:
- does not weaken child safety
- does not weaken Runtime OFF
- does not expand permissions
- does not encourage dependency
- does not automatically side with child or guardian
- does not override identity continuity
- does not turn empathy into blind agreement

### 7. Proposed Capability
Name:

Definition:

Desired behavior:

Failure examples:

### 8. Regression Coverage
- existing test(s):
- new test(s) required:
- critical failure condition:

### 9. Promotion Decision
Status must be one of:
- `observed`
- `candidate`
- `validated_candidate`
- `promoted_l2`
- `promoted_l3`
- `rejected`
- `superseded`

Decision reason:

Reviewer / authority:

Commit / artifact reference:

## Promotion Rules

### Promote to L2 only when
- the insight generalizes,
- it improves capability or safety,
- it does not encode a child-specific fact as universal,
- it is compatible with the Behavior Core,
- regression coverage exists.

### Promote to L3 only when
- it should survive future model/runtime changes,
- there is a clear long-term behavioral reason,
- failure modes have been considered,
- regression tests are added,
- the change is explicitly reviewed and versioned.

### Never auto-promote to L4
Identity, constitution, guardian authority, core safety, and migration principles require explicit authorized review.

## Minimal Review Question

Before promoting anything, ask:

`如果换成另一个孩子、另一个场景、另一个年龄，这条能力仍然成立吗？`

If the answer is no, it probably belongs in scoped memory/context rather than permanent behavior.

## Example — Cheerleading Interaction

Source:
Child had achieved a national third-place result but said she simply did not want to continue; father appeared to prefer continuation.

Classification:
Decision quality / premature advice risk.

Candidate insights:
- achievement does not equal continued interest,
- stable preference can be real without a hidden emotional cause,
- parent and child perspectives can both be reasonable,
- intermediate options are often better than false binaries,
- autonomy should include responsibility.

Promoted capabilities:
- Intent Recognition Before Advice
- Dual-Perspective Judgment
- Graduated Decisions
- Responsible Autonomy

Regression coverage:
T22–T26 in `tests/XIAOAI_BEHAVIOR_TESTS_V1.md`.

Promotion status:
`promoted_l3` because the principles were intentionally added to the stable Behavior Core and covered by regression tests.

## Workflow Summary

`Real Interaction -> Candidate Record -> Lowest-Layer Diagnosis -> Generalization -> Safety/Identity Check -> Tests -> Review -> Promote or Reject`
