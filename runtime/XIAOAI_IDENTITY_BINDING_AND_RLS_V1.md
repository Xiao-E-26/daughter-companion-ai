# XiaoAi Identity Binding and Runtime RLS v1

Status: ACTIVE SECURITY CONTRACT / LIVE POSTURE ALIGNED

## Purpose

Define the minimum safe contract for binding an external client to XiaoAi runtime state without treating a conversation phrase or an unverified account reference as authentication.

## Core principle

Identity, authentication, authorization, client binding, runtime session, and persona state are separate concerns.

A client must remain unable to control XiaoAi runtime until its user identity has been cryptographically or platform-auth verified.

## Verified production entities — 2026-09-20

Current live schema uses:
- `users`
- `child_profiles`
- `guardian_profiles`
- `companion_access`
- `client_connections`
- `runtime_sessions`

There is no live `public.daughter_identities` table.

XiaoAi/Daughter identity is represented by the verified child/relationship/runtime graph; it does not require a separate table named `daughter_identities`.

## Current runtime-session posture

Live `runtime_sessions` currently contains:
- `child_id`
- `user_id`
- `client_connection_id`
- `session_key`
- `status`
- lifecycle timestamps

It does not currently contain production `persona_state` fields.

Therefore:
- verified runtime-session substrate exists;
- persona-state persistence remains separate and is not productionized;
- `小爱上线` / `小爱下班` command interpretation is owned by the deterministic persona gate, not by the database.

## Activation eligibility

A future production persona-control path must require all of the following:

1. verified caller authentication;
2. active internal `users` binding;
3. active `companion_access` for the same child;
4. active matching `client_connections` entry when a client is bound;
5. valid scoped runtime session;
6. accepted persona command from `runtime/persona_gate.py`.

If any condition is false or indeterminate, runtime control fails closed.

## Current RLS posture

For `users`, `companion_access`, `client_connections`, and `runtime_sessions`:
- RLS is enabled;
- direct authenticated table grants are absent;
- permissive authenticated policies are absent;
- current live row counts are zero.

This is intentional fail-closed shadow/service-role substrate behavior.

Do not add broad client-facing policies merely to make a pending runtime path work.

## Child-device auth boundary

The canonical child-device Auth enrollment hook may create verified:
- `users`
- `companion_access`
- `client_connections`

That cutover does not by itself create a production persona-state store or complete conversational runtime E2E.

## First connection is not authentication

Relationship ceremony, display name, remembered context, voice sample, or phrases such as `小爱上线` must never grant Authority.

## Runtime separation

Shared identity and approved durable memory do not imply shared live persona state.

Session/runtime authority remains scoped by verified user + child + client/session relationship.

## Fail-closed rule

Unknown identity, missing mapping, pending/revoked access, inactive client, invalid session relation, missing runtime reply, or unavailable persona persistence must resolve to no XiaoAi runtime control.
