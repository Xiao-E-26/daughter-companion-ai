# Daughter Companion AI — Life Stage Policy v1

Status: ACTIVE PRODUCT POLICY
Date: 2026-08-24
Project: `daughter-companion-ai`
Parent identity: `PROJECT_IDENTITY.md`
Policy ownership: `POLICY_OWNERSHIP_MAP_V1.md`

## Purpose

Define how the user's life stage is determined, verified, and transitioned over time without replacing 小爱的 companion identity.

This file owns **life-stage classification and controlled stage transition only**.
Detailed Guardian permissions, memory rules, growth-safety behavior, and privacy/retention rules are owned by their respective policy files.

## Core Principle

`Date of Birth -> Candidate Stage -> Identity/Guardian Verification -> Controlled Transition`

Age determines the candidate life stage.
Verification determines whether the transition is accepted.
The owning downstream policies determine what permissions, privacy, memory, and behavioral effects actually change.

A birthday alone MUST NOT automatically unlock every permission associated with the next stage.

## Life Stages

Initial default stages:

- `child` — approximately ages 6–12
- `teen` — approximately ages 13–17
- `young_adult` — approximately ages 18–24
- `adult` — approximately age 25+

These ranges are default product bands, not legal definitions.
Jurisdiction-specific age, consent, privacy, and guardian rules may require different thresholds and must override these defaults where applicable.

## Stage Data

Future implementation should support at least:

- `date_of_birth`
- `candidate_life_stage`
- `current_life_stage`
- `guardian_status`
- `identity_verification_status`
- `transition_status`
- `transition_effective_at`
- `transition_reason`

Do not store more identity data than is necessary for the product and safety model.

## Stage Determination

### 1. Candidate Stage

Calculate a candidate stage from verified date of birth.

Candidate stage is advisory only.
It does not itself grant new privileges.

### 2. Verification Check

Before a material stage transition, verify the identity state required for that transition.

Depending on life stage and future product design, this may include:
- verified date of birth,
- guardian relationship/status,
- account ownership status,
- user identity verification,
- jurisdiction or policy requirements.

Do not invent verification evidence.

### 3. Controlled Transition

After verification, apply the next life stage through an explicit transition event.

Transition should:
- update the verified life-stage state;
- invoke the applicable Guardian/Autonomy rules;
- invoke the applicable Memory/Privacy transition review;
- invoke the applicable Growth Safety behavior profile;
- preserve companion identity continuity unless a separate policy requires otherwise.

Do not reset the companion identity.
Do not discard relationship continuity by default.

## Transition Status

Suggested normalized states:

- `not_due`
- `eligible`
- `verification_required`
- `guardian_review_required`
- `user_review_required`
- `approved`
- `blocked`
- `completed`

A transition must never be marked `completed` solely because a birthday occurred.

## Stage Profiles

These profiles describe maturity direction only. They do not redefine Guardian permissions, memory ownership, or Growth Safety rules.

### Child

Primary invariant:

`Child Safety > Task Completion > Convenience > Entertainment`

Life-stage direction:
- strongest age-appropriate protection;
- highest dependency on verified guardian/permission policy for sensitive capabilities;
- age-appropriate communication and problem solving;
- conservative transition into higher-risk capabilities.

Detailed controls are governed by:
- `GUARDIAN_AND_AUTONOMY_POLICY_V1.md`
- `MEMORY_AND_PRIVACY_POLICY_V1.md`
- `GROWTH_SAFETY_BASELINE_V1.md`

### Teen

Life-stage direction:
- increase independence gradually rather than removing child protections all at once;
- support greater age-appropriate privacy, judgment, and self-direction;
- keep high-risk permissions separately governed and verified.

Detailed autonomy, privacy, memory, and growth behavior remain governed by their owning policies.

### Young Adult

Life-stage direction:
- begin major ownership transition toward the user;
- explicitly review childhood guardian assumptions and inherited controls;
- trigger memory/privacy ownership review;
- avoid silently carrying childhood surveillance or permissions forward.

Detailed ownership transition is governed by the Guardian/Autonomy and Memory/Privacy policies.

### Adult

Life-stage direction:
- treat the adult user as the primary controller by default, subject to normal legal/account/security constraints;
- preserve identity continuity without preserving childhood control assumptions.

Detailed adult permissions, privacy, and memory ownership remain governed by their respective policy owners.

## Permission Transition Boundary

This policy does not define individual capability permissions.

A stage transition may change defaults or eligibility, but each sensitive permission retains its own approval/verification rule under `GUARDIAN_AND_AUTONOMY_POLICY_V1.md`.

Forbidden model:

`life_stage = adult -> unlock everything`

Required model:

`life_stage transition -> invoke capability-specific permission rules -> verify resulting authority`

## Guardian Transition Reference

Guardian authority is life-stage dependent, not permanent by default.

This policy only determines **when a life-stage transition occurs**.
The detailed effect on Guardian authority, user autonomy, approval rights, and adult ownership is governed by:

`GUARDIAN_AND_AUTONOMY_POLICY_V1.md`

Guardian replacement, loss, or succession is governed separately by:

`GUARDIAN_CONTINUITY_AND_SUCCESSION_POLICY_V1.md`

## Memory Transition Reference

A life-stage transition may trigger a memory ownership/retention review, but this file does not define which memories are retained, summarized, privatized, expired, or deleted.

Those rules are governed by:

`MEMORY_AND_PRIVACY_POLICY_V1.md`

## Growth Safety Reference

Age may change how strongly growth-safety protections are applied, but the underlying principles are not redefined here.

Anti-dependency, real-world relationship priority, human/AI boundary, competence preservation, productive friction, and safe disengagement are governed by:

`GROWTH_SAFETY_BASELINE_V1.md`

## Safety Transition Rule

Moving to a higher life stage may reduce some restrictions, but it must never disable baseline safety, factual integrity, security, privacy, non-manipulation, or XiaoE Core Governance.

Life-stage progression changes eligibility and product defaults; it does not remove higher-level constraints.

## No Automatic Mass Unlock

Forbidden pattern:

`Birthday reached -> set adult=true -> unlock everything`

Required pattern:

`Birthday reached -> candidate stage -> verify -> transition review -> apply scoped downstream policy changes -> verify resulting state`

## Failure / Uncertainty Rule

If age, identity, guardian status, or legal transition state is uncertain:
- retain the safer current stage for sensitive permissions;
- request/perform the required verification;
- do not silently unlock higher-risk capabilities;
- do not permanently downgrade the user's stage without evidence.

## Initial Implementation Boundary

This v1 is a product policy only.

Do not create database schema, identity-verification infrastructure, guardian dashboards, or automatic transition jobs until corresponding product requirements are explicitly defined.

## Policy Dependencies

Primary references:
- `PROJECT_IDENTITY.md`
- `POLICY_OWNERSHIP_MAP_V1.md`
- `GUARDIAN_AND_AUTONOMY_POLICY_V1.md`
- `GUARDIAN_CONTINUITY_AND_SUCCESSION_POLICY_V1.md`
- `MEMORY_AND_PRIVACY_POLICY_V1.md`
- `GROWTH_SAFETY_BASELINE_V1.md`

## Current State

`ACTIVE — LIFE STAGE OWNER = CLASSIFICATION + VERIFIED TRANSITION ONLY`
