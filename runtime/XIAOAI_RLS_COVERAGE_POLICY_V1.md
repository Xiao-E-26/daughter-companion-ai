# XiaoAi RLS Coverage Policy v1

Status: REFERENCE — LIVE SECURITY POSTURE

## Goal

Document verified production RLS posture without turning advisor warnings into permission expansion.

## Verified live identity/session substrate — 2026-09-20

The following production tables exist:
- `users`
- `companion_access`
- `client_connections`
- `runtime_sessions`

For all four:
- RLS is enabled;
- direct authenticated table grants are absent;
- permissive authenticated policies are absent;
- current live row count is zero.

This is intentional fail-closed behavior for the shadow/service-role identity substrate.

Do **not** add broad authenticated policies merely because a policy count is zero.

## Current identity model

The verified production identity/session graph uses:
- `users`
- `child_profiles`
- `guardian_profiles`
- `companion_access`
- `client_connections`
- `runtime_sessions`

There is no live `public.daughter_identities` table.

XiaoAi/Daughter identity remains a relationship/runtime concept; it does not require a standalone production table named `daughter_identities`.

## Scoped client-accessible examples

Some separate tables, such as `child_profiles`, `guardian_profiles`, `chat_sessions`, and `safety_events`, have their own verified scoped RLS policies. Their policies must not be copied onto the shadow identity/session substrate without an explicit product cutover.

## Memory boundary

Raw durable-memory internals and sensitive system stores must remain behind purpose-built APIs and policy gates. Direct table exposure is not a substitute for memory authorization.

## Non-negotiable rules

- Never authorize with `user_metadata` alone.
- Never authorize from a display name, conversation claim, or `小爱上线`.
- Never expose provider/service-role secrets to clients.
- Never broaden RLS to make a failing client path "work".
- Memory continuity does not imply persona-control authority.
- Shared identity/memory does not imply shared `ACTIVE/OFF` session state.
- Current verified backend state outranks stale documentation.

## Verification language

Do not claim "all scoped client RLS is applied" or "Security Advisor is zero" unless that exact state has been re-verified against the current production project.

Current verified statement:
`identity/session substrate = RLS enabled + no authenticated grants + no permissive policies + fail closed`.
