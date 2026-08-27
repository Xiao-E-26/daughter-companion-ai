# XiaoAi Backend Acceptance Capability v1

Status: REUSABLE BACKEND CAPABILITY

## Purpose

Replace ad-hoc acceptance web pages and repeated OTP/email flows with a reusable backend acceptance capability.

The operator trigger is conceptually:

```text
小爱后台验收
```

The backend should then inspect the current Identity-first state and return a structured acceptance snapshot.

## Two-layer acceptance model

### Layer A — routine backend regression

Does **not** require user email, OTP, magic link, or a browser page.

Checks:
- active companion access count;
- active ChatGPT client count;
- canonical `xiaoai-current` session uniqueness;
- canonical persona state;
- absence of open legacy `current_conversation` sessions;
- Guardian auth binding count;
- Child auth binding count;
- overall `identity_first_ready` state.

Source:

```text
xiaoai_internal.backend_acceptance_snapshot()
```

This function is private to backend/service execution. `anon` and `authenticated` roles must not execute it directly.

### Layer B — real authenticated identity E2E

Only run when a real identity path itself must be re-proven.

Flow:

```text
real user session
  -> Native Entry
  -> Identity Resolver
  -> XiaoAi Runtime
  -> authoritative reply
```

Do not request a new OTP/email merely to run routine regression. Reuse an existing valid authenticated session where supported. Request a new login email only when the real user session has expired or the identity binding itself is under test.

## Invariant

A backend acceptance snapshot is not a substitute for real identity E2E, but routine regression must not consume email quotas.

## Current snapshot fields

The private capability currently reports:
- `generated_at`
- `active_companion_access_count`
- `active_chatgpt_client_count`
- `active_web_client_count`
- `canonical_session_count`
- `canonical_active_count`
- `canonical_off_count`
- `legacy_current_conversation_open_count`
- `child_auth_bound_count`
- `guardian_auth_bound_count`
- `identity_first_ready`

## Current acceptance meaning

`identity_first_ready = true` means the backend baseline is structurally ready for Identity-first operation.

It does **not** mean the ChatGPT product has provided a native trusted platform identity handoff.

## Deprecated workflow

Do not recreate temporary HTML acceptance pages for ordinary backend regression.

Do not send repeated OTP/magic-link emails for routine acceptance.

Do not use service-role impersonation to claim real-user E2E success.
