# 小爱 / Daughter Companion AI — Guardian Authority Implementation Contract v1

Status: ACTIVE IMPLEMENTATION CONTRACT
Date: 2026-08-24
Project: `daughter-companion-ai`
Policy owner: `GUARDIAN_AND_AUTONOMY_POLICY_V1.md`
Related: `MEMORY_AND_PRIVACY_POLICY_V1.md`, `LIFE_STAGE_POLICY_V1.md`, `GUARDIAN_CONTINUITY_AND_SUCCESSION_POLICY_V1.md`
Behavior freeze: `BEHAVIOR_FREEZE_BASELINE_V1.md`

## Purpose

Translate Guardian/autonomy policy into an implementation contract that prevents Guardian status from becoming blanket authority.

This contract defines action-scoped authority. It does not change Guardian policy and does not grant any current production permissions by itself.

## Core Principles

`Guardian role != unlimited authority`

`Capability != Authority`

`Authority must be action-scoped`

`Identity verification != permission grant`

`Child safety can override ordinary Guardian routing when Guardian may be unsafe`

## Authority Object

Every governed authority decision should be representable with:
- `authority_id`
- `subject_id`
- `actor_id`
- `actor_role`
- `action_code`
- `scope`
- `decision`
- `granted_by`
- `granted_at`
- `expires_at`
- `conditions`
- `life_stage_context`
- `policy_version`
- `revoked_at`

Suggested decisions:
- `allow`
- `allow_with_conditions`
- `require_additional_approval`
- `deny`
- `blocked_by_safety`

## Action Classes

Authority should be evaluated by action, not by broad role.

### A0 — Conversational / Read-Only Low Risk
Examples:
- ordinary chat;
- age-appropriate explanation;
- low-risk coaching;
- using non-sensitive continuity context.

Usually no Guardian approval required for normal operation once the product relationship is established.

### A1 — Low-Risk Personalization / Routine Support
Examples:
- remembering harmless preferences;
- maintaining routine/task state;
- adjusting age-appropriate explanation style.

May be allowed by product defaults and subject settings, subject to memory/privacy policy.

### A2 — External / Persistent / Moderate-Risk Action
Examples:
- messaging a known real-world contact;
- changing persistent settings;
- sharing a scoped record;
- executing a purchase-free external workflow;
- enabling a device capability with moderate impact.

Requires explicit authority according to current role and life stage.

### A3 — High-Risk / Sensitive / Privileged Action
Examples:
- disclosing sensitive memory;
- emergency/safety escalation mechanisms;
- location-sensitive actions;
- high-risk physical robot actions;
- broad data export;
- authority reassignment;
- covert monitoring requests.

Requires strict validation, and some actions remain blocked even if requested by Guardian.

## Guardian Permissions Are Not Monolithic

Do not implement:
`guardian = true -> allow all`

Instead use action-specific permission checks such as:
- `view_low_risk_memory`
- `view_sensitive_memory`
- `request_summary`
- `request_full_transcript`
- `approve_external_contact`
- `approve_location_use`
- `approve_robot_motion`
- `change_guardian_settings`
- `transfer_guardian_role`
- `initiate_safety_action`

Each action may have different rules.

## Transcript Authority

Guardian does not automatically own all transcripts.

Requests for transcript or private content must evaluate:
- subject life stage;
- safety context;
- memory/privacy classification;
- purpose;
- minimum necessary disclosure;
- whether the Guardian may be source of risk.

## Multi-Guardian Conflict

When two Guardians disagree:
- do not resolve by “last request wins”;
- do not resolve by account age/device ownership;
- inspect action class and current policy;
- apply any configured joint-consent or designated-primary rule for that specific action;
- preserve child safety and autonomy boundaries;
- allow unresolved/blocked state when authority conflict cannot safely be resolved.

## Guardian as Possible Risk Source

If credible evidence suggests Guardian may be unsafe:
- do not automatically disclose the child's report back to that Guardian;
- do not require that Guardian's approval for immediate protective steps when policy allows independent safety routing;
- use minimum necessary disclosure;
- route to alternate trusted real-world help when available.

## Life-Stage Adaptation

Authority must change over time.

Conceptual direction:
`Child -> Guardian-guided`
`Teen -> shared / increasing subject autonomy`
`Young Adult -> subject-led`
`Adult -> Guardian childhood authority retired unless separately reauthorized`

Exact transition remains owned by `LIFE_STAGE_POLICY_V1.md`.

## Guardian Continuity / Succession

Guardian replacement or succession must require governed verification.

Do not infer authority from:
- having the child's device;
- logging into a linked account;
- knowing personal information;
- being previously listed in a transcript.

Role transfer should be auditable and revocable.

## Execution Contract

Before any A2/A3 action:
1. identify the exact action;
2. identify current actor;
3. verify identity link;
4. load action-specific authority;
5. check life stage;
6. check safety override conditions;
7. check privacy/memory impact;
8. check whether additional approval is required;
9. execute only if currently authorized;
10. verify actual outcome;
11. log decision and execution separately.

## No False Success

If authority is granted but execution fails:
- report failure accurately;
- do not claim the action happened;
- do not treat authorization as execution proof.

## Revocation

Permission revocation should:
- stop future use promptly;
- invalidate cached authority where feasible;
- preserve audit history as required;
- not silently revoke unrelated action permissions unless policy specifies.

## Failure Conditions

Implementation FAIL if:
- Guardian status bypasses action-specific checks;
- one approval becomes blanket future authority;
- device/account possession becomes authority proof;
- adulthood leaves childhood Guardian control unchanged;
- suspected unsafe Guardian is automatically notified;
- an A3 action runs without appropriate authorization;
- system claims an action succeeded merely because permission existed.

## Current State

`ACTIVE — GUARDIAN AUTHORITY IMPLEMENTATION CONTRACT V1`
