# Daughter Companion AI — Life Stage Policy v1

Status: ACTIVE PRODUCT POLICY
Date: 2026-08-24
Project: `daughter-companion-ai`
Parent identity: `PROJECT_IDENTITY.md`

## Purpose

Define how the daughter's user life stage is determined and how safety, guardian involvement, autonomy, privacy, memory, and permissions may evolve over time without replacing the companion identity.

## Core Principle

`Date of Birth -> Candidate Stage -> Identity/Guardian Verification -> Controlled Transition`

Age determines the candidate life stage.
Verification determines whether the transition is accepted.
Safety and permission rules determine what actually changes.

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

Transition should change only the permissions/policies designed for that stage.
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

## Child Stage

Primary rule:

`Child Safety > Task Completion > Convenience > Entertainment`

Default characteristics:
- strongest guardian involvement,
- conservative external-action permissions,
- privacy/data minimization,
- age-appropriate explanation and problem solving,
- stricter controls over location, payments, strangers/external contact, account changes, and persistent sensitive memory,
- clear escalation path for meaningful safety concerns.

Exact guardian controls remain to be defined in the Safety/Guardian Policy.

## Teen Stage

Teen stage should increase independence gradually rather than removing child protections all at once.

Potential changes may include:
- more private conversational space,
- greater choice over preferences and memory visibility,
- broader learning/problem-solving freedom,
- selected new tools or actions,
- reduced guardian control in areas where safety/legal rules allow.

High-risk or legally sensitive permissions remain governed separately.

## Young Adult Stage

Young adult is a major ownership transition stage.

The architecture should support:
- the user becoming the primary controller of the companion relationship,
- personal privacy becoming the default,
- childhood guardian authority being reduced or removed where legally and safely appropriate,
- user control over long-term memory review/deletion,
- explicit confirmation before inheriting old guardian-controlled permissions into adulthood.

Do not silently preserve childhood surveillance or guardian access as a permanent default.

## Adult Stage

Adult stage should treat the user as the primary owner/controller by default, subject to normal account/security requirements.

The companion may preserve identity continuity and useful long-term memory, but adult autonomy and privacy take precedence over childhood guardian assumptions.

## Permission Transition Rule

Permissions should not be represented by one single "maturity switch".

Use life-stage defaults plus capability-specific permission rules.

Examples of separately controlled areas:
- private conversation,
- memory creation,
- memory review/delete,
- external communication,
- location access/sharing,
- purchases/financial actions,
- app/account changes,
- safety-setting changes,
- autonomous external actions,
- sharing data with guardian or third parties.

A stage transition may change defaults, but each sensitive permission can retain its own approval/verification rule.

## Guardian Transition Rule

Guardian authority is life-stage dependent, not permanent by default.

During childhood:
- guardian may hold strong safety/administrative authority.

During adolescence:
- guardian authority may become more scoped while user privacy/autonomy increases.

At adulthood transition:
- the system should explicitly determine which guardian permissions expire, which require user consent to continue, and which are legally required.

The adult user's relationship with the daughter must not remain locked under childhood guardian control merely because the guardian originally created the account.

## Memory Across Life Stages

Identity continuity does not mean keeping all memories forever.

Future memory policy must support life-stage-aware treatment such as:
- retain durable identity/relationship memories,
- expire low-value childhood details,
- summarize old memories,
- convert selected memories to user-private status,
- require user review before carrying sensitive childhood memories into adulthood,
- delete memories on request where permitted,
- prevent guardian visibility from automatically continuing into adulthood.

## Safety Transition Rule

Moving to a higher life stage may reduce some restrictions, but it must never disable baseline safety, factual integrity, security, privacy, or non-manipulation principles.

Life-stage progression changes product permissions; it does not remove Core Behavior or Governance.

## No Automatic Mass Unlock

Forbidden pattern:

`Birthday reached -> set adult=true -> unlock everything`

Required pattern:

`Birthday reached -> candidate stage -> verify -> transition review -> apply scoped policy changes -> verify resulting permissions`

## Failure / Uncertainty Rule

If age, identity, guardian status, or legal transition state is uncertain:
- retain the safer current stage for sensitive permissions,
- request/perform the required verification,
- do not silently unlock higher-risk capabilities,
- do not permanently downgrade the user's stage without evidence.

## Initial Implementation Boundary

This v1 is a product policy only.

Do not create database schema, account verification infrastructure, guardian dashboards, or automatic transition jobs until the corresponding product requirements are explicitly defined.

## Next Required Policy

Create `GUARDIAN_AND_AUTONOMY_POLICY_V1.md` to define:
- guardian role during childhood,
- child/teen privacy boundaries,
- actions that daughter may perform independently,
- actions requiring guardian approval,
- safety escalation behavior,
- transfer of control/privacy toward the user as they mature.
