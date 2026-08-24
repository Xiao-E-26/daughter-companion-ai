# XiaoAi Identity Binding and Runtime RLS v1

## Purpose

Define the minimum safe contract for binding an external client (for example ChatGPT) to XiaoAi runtime state without treating a conversation phrase or an unverified account reference as authentication.

## Core principle

Identity, authorization, client binding, and persona runtime state are separate concerns.

A client may be known to the system but must remain unable to control XiaoAi runtime until its user identity has been cryptographically or platform-auth verified.

## Entities

- `users`: internal people identities. `auth_user_id` is nullable until Supabase Auth binding is complete.
- `daughter_identities`: the persistent XiaoAi/Daughter identity associated with the child subject.
- `companion_access`: authorization relationship between a user and Daughter.
- `client_connections`: one external client/account/device entry point.
- `runtime_sessions`: session-scoped runtime state, including `persona_state` (`OFF` or `ACTIVE`).

## Primary ChatGPT bootstrap state

The primary guardian ChatGPT entry may be pre-registered only as a pending client.

Required pending state:

- guardian internal user exists
- `auth_user_id = NULL`
- `companion_access.status = 'pending'`
- `authority_scope.runtime_control = false`
- `client_connections.status = 'pending'`
- `external_account_ref_hash = NULL` unless obtained from a verifiable provider-side binding flow
- no runtime session is created merely because the pending client exists

## Activation eligibility

A client may control `runtime_sessions.persona_state` only when all of these are true:

1. Request is authenticated by Supabase Auth.
2. `users.auth_user_id = auth.uid()` for the acting internal user.
3. The matching `companion_access` row for that `daughter_id` is `active`.
4. If a `client_connection_id` is attached, the connection belongs to the same user and Daughter and is `active`.
5. The persona command is accepted by `runtime/persona_gate.py`.

If any condition is false or indeterminate, runtime control fails closed.

## RLS contract

`runtime_sessions` SELECT/INSERT/UPDATE policies must require an authenticated user mapping plus active companion access.

Insert/update must additionally verify any supplied `client_connection_id` belongs to the same authorized user/Daughter pair and is active.

`companion_access` and `client_connections` may be read only by the authenticated internal user mapped through `users.auth_user_id`.

No client-facing policy should authorize based only on:

- a display name
- a ChatGPT conversation
- `小爱上线`
- a raw external account string
- `user_metadata`
- child-like language or remembered context

## Runtime separation

Shared identity and memory do not imply shared live persona state.

Runtime state is scoped by at least:

- Daughter
- internal user
- session key
- client connection when available

This allows Dad ChatGPT and Mom ChatGPT to share XiaoAi identity/memory while remaining independently `OFF` or `ACTIVE`.

## Required transition to verified state

Pending guardian/client rows must not be promoted to `active` until a real authentication/binding flow produces a trustworthy identity mapping. Promotion should set:

- `users.auth_user_id`
- `companion_access.status = 'active'`
- appropriate authority scope
- `companion_access.verified_at`
- `client_connections.status = 'active'`
- `client_connections.linked_at`
- verifiable external reference hash when available

## First connection is not authentication

The first-connection phrase and relationship ceremony remain presentation/relationship logic only. They must never grant Authority or activate runtime access by themselves.

## Fail-closed rule

Unknown identity, missing mapping, pending access, revoked client, inactive client, invalid session relation, or unexpected persona state must resolve to no XiaoAi runtime control.
