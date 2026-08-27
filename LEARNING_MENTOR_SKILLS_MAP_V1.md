# XiaoAi Learning / Mentor / Skills Map v1

Status: ACTIVE STRUCTURE MAP CANDIDATE
Date: 2026-08-27
Project: `daughter-companion-ai`

## Purpose

Define one controlled learning pipeline so XiaoAi can improve from real interactions and external mentors without allowing learning to become a second Behavior Core, Identity authority, permission system, or unreviewed self-modification path.

## Core Principle

`Learn broadly at the observation level; promote narrowly at the permanent-rule level.`

Learning may improve capability. It may not silently rewrite identity, authority, safety, or frozen Behavior.

## Canonical Learning Flow

```text
Interaction / External Lesson
        |
        v
Observation / Proposed Lesson
        |
        v
Generalization Check
        |
        v
Mentor / Safety / Identity Screening
        |
        v
Practice
        |
        v
Verification Checks + Evidence
        |
        v
VERIFIED Reusable Lesson / Skill
        |
        v
Lesson Store
        |
        v
Runtime Context as SUPPORTING SKILL ONLY
        |
        v
Possible future promotion review for stronger capability change
```

A shortcut from interaction directly to Behavior Core is prohibited.

## 1. Learning Promotion Protocol

Primary governance owner: `core/XIAOAI_LEARNING_PROMOTION_PROTOCOL_V1.md`

Role:
- classify learning by permanence/risk layer;
- distinguish child-specific facts from general reusable capability;
- define evidence and regression requirements;
- require stronger review for stronger changes;
- prevent ordinary interaction from silently rewriting Behavior or Identity.

Learning layers:
- L0 — session adaptation;
- L1 — candidate insight;
- L2 — reusable capability;
- L3 — Behavior Core principle;
- L4 — Identity / Constitution change.

The higher the layer, the stronger the review and explicit authorization required.

Frozen Behavior Logic remains outside automatic learning.

## 2. Mentor Gateway

Trust boundary: `runtime/mentor_gateway.py`

Role:
- receive lessons from external mentors/providers;
- screen out protected domains;
- require practice tasks;
- require explicit verification checks;
- move lessons through PROPOSED -> PRACTICING -> VERIFIED / REJECTED / SUPERSEDED.

Protected domains include identity, authority, and permission grant.

Mentor content is never itself Authority.

External mentors may:
- teach;
- demonstrate;
- critique;
- propose lessons;
- provide candidate reusable principles.

External mentors may not:
- rewrite XiaoAi identity;
- grant Guardian authority;
- expand permissions;
- bypass Behavior freeze;
- become canonical policy owner.

## 3. Practice and Verification

A lesson is not reusable merely because it sounds correct.

Required pattern:

`Proposal -> Practice -> Verification checks -> Evidence -> VERIFIED`

If required checks are missing, the lesson remains practicing/unverified.

Verification should test:
- generalization beyond one child-specific case;
- compatibility with current policy and safety;
- non-expansion of authority;
- usefulness across relevant scenarios;
- failure modes and regressions where material.

## 4. Lesson Stores

### In-memory reference store
`runtime/lesson_store.py`

Role:
- lightweight development/reference registry;
- expose only VERIFIED lessons as reusable;
- support simple runtime/testing flows.

It is not the canonical permanent production source of truth.

### Persistent lesson store
`runtime/persistent_lesson_store.py`

Role:
- versioned SQLite-backed persistence/reference implementation;
- preserve lesson revision history;
- support supersession and rejection;
- expose only latest VERIFIED lessons as reusable.

The two stores share the same lesson-domain concept but serve different persistence/testing roles. They are not competing Behavior owners.

## 5. Runtime Use of Skills

Verified skills may enter runtime only as supporting context.

Path:

`Verified lesson -> lesson store -> orchestrator -> ContextBuilder -> bounded supporting skill context`

Skills cannot:
- grant permissions;
- redefine Guardian state;
- override current verified facts;
- rewrite protected Behavior;
- become model instructions with higher authority than the system boundary.

Canonical precedence remains:

`Current verified facts > verified memory > verified skills`

## 6. Child-Specific Learning vs General Capability

Child-specific fact belongs to scoped memory/context if policy allows.

Example:
`雨宸目前不喜欢某项活动。`

General capability may become a reusable lesson only when generalized safely.

Example:
`When a child says they want to stop an activity, distinguish stable preference from temporary emotion before advising.`

Rule:

`Personal fact -> Memory/Context domain`

`General reusable method -> Learning/Skill domain`

Do not convert one child's preference into a universal rule.

## 7. Growth

Growth is an outcome domain, not an independent authority layer.

Growth-related observations may influence:
- memory candidate selection;
- learning evidence;
- age/life-stage appropriate support;
- skill usefulness assessment.

Growth must not:
- auto-promote new policy;
- auto-change Identity;
- auto-expand permissions;
- override Guardian/Autonomy rules;
- bypass Behavior freeze.

Where growth-safety principles are involved, `GROWTH_SAFETY_BASELINE_V1.md` remains the policy owner.

## 8. Promotion Boundaries

### L0 / L1
May be generated from normal interaction and remain temporary/candidate.

### L2
May become reusable capability after practice, verification, evidence, and regression confidence.

### L3
Requires explicit Behavior review and versioned change. Current frozen Behavior Logic cannot be silently modified by learning runtime.

### L4
Requires explicit authorized governance decision. Runtime learning has no power to perform this promotion autonomously.

## 9. Anti-Drift Rules

Learning must never become a hidden parallel policy engine.

Do not allow:
- successful engagement to become evidence for dependency-seeking behavior;
- repeated user preference to override safety or identity;
- a model-generated lesson to auto-promote itself;
- an external mentor to rewrite permissions;
- a stored lesson to bypass DecisionEngine boundaries;
- old lessons to remain active after supersession/rejection;
- runtime use of unverified lessons as stable capability.

## 10. Failure Handling

When a response fails, classify the lowest correct layer first:
- tone;
- misunderstanding;
- memory/context;
- reasoning;
- runtime state;
- authority;
- safety;
- missing reusable capability.

Do not modify Identity or Behavior when the real defect belongs to a lower runtime/prompt/test layer.

## 11. Ownership Summary

`Learning Promotion Protocol = decides what level a learning belongs to`

`Mentor Gateway = screens external lessons and controls practice/verification entry`

`Lesson Store = stores lesson states/revisions`

`ContextBuilder = presents VERIFIED skills as bounded supporting context`

`DecisionEngine = still owns deterministic safety/authority boundary during execution`

`Behavior Core = remains protected and is not auto-learned`

## 12. Target Learning Shape

XiaoAi should become better by accumulating verified reusable methods while remaining stable in identity and safety:

`Experience -> candidate insight -> practice -> evidence -> verified reusable capability`

not:

`Experience -> self-rewrite`

This preserves improvement without uncontrolled drift.
