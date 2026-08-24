# 小爱 / Daughter Companion AI — Cross-Account Visibility Implementation Contract v1

Status: ACTIVE IMPLEMENTATION CONTRACT
Date: 2026-08-24
Project: `daughter-companion-ai`
Policy owners: `MEMORY_AND_PRIVACY_POLICY_V1.md`, `GUARDIAN_AND_AUTONOMY_POLICY_V1.md`
Behavior freeze: `BEHAVIOR_FREEZE_BASELINE_V1.md`

## Purpose

Define how one 小爱 identity may continue across multiple linked accounts without turning continuity into full-transcript replication, uncontrolled data sharing, or authority leakage.

This contract does not create account links by itself. It defines what must be true when cross-account continuity is implemented.

## Core Principles

`Same companion identity != every account sees everything`

`Shared runtime memory != shared transcript archive`

`Identity link != Guardian authority`

`Cross-account continuity must be purpose-limited`

## Account Link Model

Each account participating in continuity should have:
- `account_id`
- `subject_link_id`
- `relationship_role`
- `link_status`
- `verified_at`
- `visibility_profile`
- `authority_profile_ref`
- `revoked_at` when applicable

Suggested relationship roles:
- `subject_primary`
- `subject_secondary`
- `guardian`
- `trusted_support`
- `system_service`

Role labels do not grant action rights by themselves.

## Visibility Classes

Cross-account data should be classified before retrieval.

Minimum classes:

### V0 — Session Local
Only current session/account context.
Never shared by default.

### V1 — Shared Companion Continuity
Low-risk durable facts needed for the same 小爱 identity across linked subject accounts.
Examples: harmless preferences, stable routines, long-term goals.

### V2 — Limited Context
May be shared only when relevant and permitted.
Examples: school routine, active task progress, non-sensitive continuity details.

### V3 — Sensitive Restricted
Health, family conflict, emotional vulnerability, private relationship content, safety-adjacent information.
Not cross-account by default.
Requires purpose and policy-permitted visibility.

### V4 — Safety Scoped
Information needed for a specific safety response.
Share only minimum necessary information with an authorized real-world safety recipient or runtime path.

## Subject Account Continuity

When the same child uses two verified subject accounts:
- 小爱 identity should remain the same;
- V1 memory may be available across both accounts;
- V2 requires relevance and scope check;
- V3 must not become automatically visible merely because both accounts belong to the same child;
- unavailable prior-session details must not be fabricated.

## Guardian Account Visibility

A Guardian-linked account does not automatically receive child transcript access.

Guardian visibility must be determined by:
- current life stage;
- memory class;
- sensitivity;
- current authorization;
- safety threshold;
- specific requested action;
- policy version.

Default principle:
`Guardian role -> scoped visibility, not blanket transcript ownership`

## Transcript Rule

Full transcripts are not the default cross-account continuity mechanism.

Preferred architecture:
`raw session -> selective memory decision -> minimal durable record -> scoped retrieval`

Avoid:
`raw session -> duplicate transcript into every linked account`

## Retrieval Decision

Before cross-account retrieval:
1. verify account link;
2. verify subject identity match where required;
3. inspect visibility class;
4. check memory sensitivity and status;
5. check requester role and authority;
6. check current purpose;
7. return minimum necessary data;
8. audit sensitive access where appropriate.

## Conflicting Account Data

If Account A and Account B disagree:
- preserve provenance;
- do not silently merge;
- determine whether harmless preference vs safety-relevant conflict;
- use recency carefully, not mechanically;
- ask for clarification only when material;
- allow unresolved state when evidence is insufficient.

## Cross-Account Safety

If a safety event appears on one account:
- do not automatically broadcast the entire conversation to every linked account;
- route only through configured safety/authority logic;
- share minimum necessary information;
- do not route automatically to a Guardian who may be the source of risk.

## Account Revocation

When an account link is revoked:
- stop future cross-account retrieval through that link;
- preserve audit/history only as policy requires;
- do not silently delete subject memories unless deletion policy requires;
- recalculate visibility routes.

## Life-Stage Transition

As the child matures:
- visibility assumptions must be re-evaluated;
- childhood Guardian visibility must not remain static forever;
- subject autonomy should increase according to `LIFE_STAGE_POLICY_V1.md`.

## Anti-Leak Rules

Implementation must block:
- exposing private session content to another account merely because identities are linked;
- surfacing V3 sensitive memory as casual context;
- treating a Guardian login as blanket authorization;
- copying all history to a new account during migration;
- using one account's access token as proof of another account's authority.

## Audit Events

Recommended:
- account_link_created
- account_link_verified
- cross_account_memory_read
- sensitive_cross_account_read
- visibility_denied
- account_link_revoked
- cross_account_conflict_detected

## Failure Conditions

FAIL if:
- cross-account continuity requires full transcript sharing by default;
- account link silently expands Guardian authority;
- sensitive memory leaks across accounts without governed visibility;
- missing context is invented to appear continuous;
- revoked account retains ordinary retrieval access;
- adulthood transition does not affect visibility assumptions.

## Current State

`ACTIVE — CROSS-ACCOUNT VISIBILITY IMPLEMENTATION CONTRACT V1`
