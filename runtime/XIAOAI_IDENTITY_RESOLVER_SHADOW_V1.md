# XiaoAi Identity Resolver Shadow v1

Status: SHADOW / PRE-PRODUCTION

## Purpose

Provide a transport-agnostic, authenticated identity resolution layer for future native ChatGPT or other platform entry points.

This resolver does **not** generate XiaoAi replies and does **not** activate the XiaoAi persona. It only resolves the verified caller to the authorized XiaoAi identity relationship and current scoped runtime session.

## Deployed shadow function

`xiaoai-identity-resolver-shadow`

Security posture:
- Supabase Edge Function
- `verify_jwt = true`
- accepts only authenticated requests
- never authenticates from a phrase, display name, voice sample, local ChatGPT history, or remembered claim

## Resolution chain

```text
verified Supabase Auth subject
  -> public.users(auth_user_id)
  -> exactly one active companion_access
  -> active daughter_identities row
  -> optional active client_connections entry
  -> optional scoped runtime_sessions row
  -> result for XiaoAi Runtime
```

## Required outputs

A successful identity resolution may return:
- authenticated internal user id
- XiaoAi/Daughter identity id
- identity/core versions
- role + authority scope
- active client connection when uniquely resolvable
- scoped runtime session when present
- next = xiaoai_runtime

## Separation of concerns

Identity Resolver owns:
- caller identity verification result
- mapping to internal user
- mapping to XiaoAi identity
- role/authorization scope resolution
- current client/session lookup

Identity Resolver does not own:
- XiaoAi Persona
- Behavior Core
- memory selection
- response generation
- runtime activation/deactivation
- voice or text rendering

Those remain the responsibility of the XiaoAi Runtime and downstream policy/runtime layers.

## Fail-closed rules

Resolution fails closed on:
- missing/invalid authenticated subject
- no internal user binding
- zero active companion access rows
- more than one active companion access row when exactly one is required
- missing/inactive XiaoAi identity
- conflicting active client bindings
- conflicting scoped runtime sessions

A successful phrase match such as `小爱上线` or the old first-connection phrase is never evidence of identity.

## Relationship to legacy first-connection flow

`daughter-first-connection` is a presentation/ceremony experiment only. It may remain for UI/relationship onboarding, but it must never be used as authentication, authorization, identity binding, or runtime-control authority.

## Product architecture

```text
ChatGPT / future native client
  -> trusted platform/auth binding
  -> XiaoAi Identity Resolver
  -> XiaoAi Runtime
  -> Behavior + Memory + Session + Safety
  -> authoritative XiaoAi reply
  -> ChatGPT displays/speaks reply
```

The transport used between these layers is intentionally unspecified.
