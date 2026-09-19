# 小爱 Multi-Entry Access Model v1

Status: ACTIVE ARCHITECTURE BASELINE / PARTIAL IMPLEMENTATION
Display identity: 小爱
Internal technical identity: `daughter`

## Goal

Allow the same XiaoAi relationship to be accessed from multiple authorized entry points without treating each device/account as a separate companion.

Core principle:

`One XiaoAi Relationship -> Multiple Entry Points -> Role-Based Permissions -> Shared Approved State`

## Entry-point boundary

An entry point is a client, not the identity itself.

Potential entry points include ChatGPT, web, mobile, tablet, and future physical bodies.

No entry point gains authority merely by saying `小爱上线`.

## Shared identity vs shared state

Authorized clients may eventually share:
- identity rules;
- behavior core;
- life-stage and safety policy;
- approved durable memory;
- continuity rules.

ChatGPT-local history, browser storage, or a device-local prompt must not become authoritative shared XiaoAi state.

## Role model

Roles remain conceptually separated:
- Child
- Guardian
- Device / Client
- Maintainer / Developer

Authority is attached to verified role/binding, not display name, wording, device name, or remembered claim.

## Current verified backend primitives — 2026-09-20

Production schema contains:
- `users`
- `child_profiles`
- `guardian_profiles`
- `companion_access`
- `client_connections`
- `runtime_sessions`

The child-device Auth enrollment cutover can create verified user/access/client bindings.

However, current production counts for auth users, user bindings, companion access, client connections, and runtime sessions are all zero.

## Session/persona distinction

`runtime_sessions` is currently a verified session substrate.

It is **not** yet a production persona-state store:
- no live `persona_state` column is present;
- no production persona persistence RPC is deployed;
- only `start_child_runtime_session_shadow_v1` is verified for session start.

Therefore do not label "Session/persona state model" as fully ACTIVE.

## Memory posture

Memory V2 protected production path is deployed and `child_pinned_only` is enabled.

Current Memory V2 subjects/accounts/links/memories counts are all zero, so the path is production-capable but not yet in real-user use.

## ChatGPT boundary

Separate ChatGPT accounts do not share authoritative XiaoAi state through local chat history.

A ChatGPT entry participates in XiaoAi continuity only after a trusted platform identity handoff and verified backend authorization path are connected.

That end-to-end ChatGPT path is not active yet.

## Current implementation status

- Shared XiaoAi architecture: ACTIVE
- Identity/access schema: DEPLOYED
- Child-device enrollment auth path: CUT OVER
- Real bound identities: NONE
- Real client connections: NONE
- Runtime-session substrate: DEPLOYED / SHADOW
- Production persona persistence: NOT YET
- Guardian multi-client live path: NOT YET
- Memory V2 protected production path: DEPLOYED / ENABLED
- Memory V2 real-user usage: NONE
- Every ChatGPT/front-end entry connected E2E: NOT YET
- Live conversational serving: NOT ACTIVE
- Physical robot body: FUTURE

## Safety boundary

Identity continuity may be shared; authority is never inherited automatically.

Adding an account, device, client, or body requires authorization appropriate to the role and risk level.
