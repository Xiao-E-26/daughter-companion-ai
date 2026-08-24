# 小爱 Checkpoint — 2026-08-24

Status: FROZEN CHECKPOINT
Scope: Decision Quality + Learning Promotion

## Completed

1. Strengthened `core/XIAOAI_BEHAVIOR_CORE_V1.md` with four stable decision-quality capabilities:
   - Intent Recognition Before Advice
   - Dual-Perspective Judgment
   - Graduated Decisions
   - Responsible Autonomy

2. Added a Decision Quality Principle:
   - understand the preference before advising,
   - distinguish stable preference from temporary emotion,
   - consider other stakeholders without automatic side-taking,
   - consider commitments and consequences,
   - prefer reversible/intermediate options when appropriate,
   - help the child express her own view clearly.

3. Expanded `tests/XIAOAI_BEHAVIOR_TESTS_V1.md` with T22–T26:
   - stable preference vs temporary emotion,
   - parent-child preference conflict,
   - avoid false binaries,
   - responsible autonomy,
   - decision quality without over-questioning.

4. Added `core/XIAOAI_LEARNING_PROMOTION_PROTOCOL_V1.md` defining controlled learning layers:
   - L0 Conversation Adaptation
   - L1 Candidate Insight
   - L2 Reusable Capability
   - L3 Behavior Core Principle
   - L4 Identity / Constitution Change

5. Added `runtime/XIAOAI_LEARNING_CANDIDATE_TEMPLATE_V1.md` so future real interactions can be classified, generalized, tested, reviewed, promoted, rejected, or kept as scoped context without silently rewriting permanent behavior.

## Core Learning Rule

`真实互动可以产生学习，但一次互动不等于长期规则。`

## Core Decision Rule

`尊重孩子的真实意愿，但帮助她把“我想要什么”升级成“我知道为什么、知道后果，也知道怎样负责任地做决定”。`

## Current State

This learning/decision-quality phase is complete enough to stop adding rules.

The architecture now supports:

`Real Interaction -> Observation -> Candidate Insight -> Generalization Check -> Safety/Identity Check -> Capability Draft -> Regression Tests -> Review -> Promote or Reject`

The intended next phase is real-world usage and observation, not additional speculative rule growth.

## Open Items

No required implementation item is open for this phase.

Future changes should be driven by repeated real interactions, clear failures, or validated gaps rather than adding complexity preemptively.

## Resume Point

When resuming this topic:
1. review new real XiaoAi interactions,
2. classify any observed failure/opportunity using the Learning Candidate Template,
3. fix the lowest correct layer,
4. only promote generalized, testable capabilities,
5. avoid modifying Identity / Constitution unless explicitly authorized and necessary.

## Source-Control References

- Behavior Core decision-quality upgrade commit: `41f293856c3d30cf642ccf41129ee157dd8e6985`
- Decision-quality regression tests commit: `09b49ced87813c4edcb2380bbb0c9ebae3a05c88`
- Learning Promotion Protocol commit: `fc9e2710fc2c132dadb45dc741db719eb97ab986`
- Learning Candidate Template commit: `23bc3fac9301c4cf33a0e22d4ef930d3dfc4f8c5`

## Persistence Note

The behavior rules, learning protocol, candidate workflow, and this checkpoint are persisted in GitHub.

This checkpoint does not create or modify child personal memory, guardian permissions, Supabase runtime state, or account bindings.

`Checkpoint = continuity, not authority.`
