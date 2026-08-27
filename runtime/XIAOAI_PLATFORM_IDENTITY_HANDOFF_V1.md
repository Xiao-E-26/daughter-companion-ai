# XiaoAi Platform Identity Handoff v1

Status: AUTHORITATIVE HANDOFF CONTRACT

## Purpose

Define the one missing contract between a trusted host platform (for example ChatGPT) and the XiaoAi identity-first backend.

The host platform does not become XiaoAi. It only provides trusted caller identity plus user input to the backend.

## Product model

```text
ChatGPT = microphone + speaker + text window
Platform identity assertion = trusted proof of who is calling
Identity Resolver = maps trusted caller -> authorized XiaoAi relationship
XiaoAi Runtime = sole conversational brain
```

## Required handoff fields

A future platform-native integration should provide a trusted assertion containing, at minimum:

- `issuer`: trusted platform/provider identity
- `subject`: stable opaque user/account subject from that issuer
- `audience`: XiaoAi backend/native entry
- `issued_at`
- `expires_at`
- `nonce` or equivalent replay protection where supported
- `session_ref` or platform conversation/session reference when available
- integrity protection: platform-signed token, verified OAuth/OIDC assertion, or equivalent trusted channel

The assertion may be represented as JWT, OIDC token, platform service token, mutually authenticated request metadata, or another verifiable platform-native format.

The exact transport is not part of the XiaoAi product identity.

## Forbidden identity substitutes

None of the following may be used as authentication or identity proof:

- display name
- account nickname
- spoken name
- voice sample alone
- remembered conversation claim
- local ChatGPT memory
- `小爱上线`
- first-connection phrase
- raw email/phone supplied inside conversation
- client-provided `user_id` without platform verification

## Verification sequence

1. Verify the platform assertion issuer and signature/channel.
2. Verify audience, expiry, and replay protection where available.
3. Extract stable platform subject.
4. Resolve that subject to an approved internal user/client binding.
5. Resolve active `companion_access` for exactly one XiaoAi/Daughter identity.
6. Resolve role and authority scope.
7. Resolve entry/client/session scope.
8. Pass only the resolved internal identity context to XiaoAi Runtime.
9. Runtime generates the final authoritative XiaoAi reply.

If any verification step fails, XiaoAi remains unavailable for that turn.

## Separation of concerns

Platform identity assertion proves **who is calling**.

XiaoAi Identity determines **which companion relationship is loaded**.

Authorization determines **what that caller may do**.

Runtime determines **how XiaoAi thinks and replies**.

ChatGPT remains **I/O only**.

## Native Entry integration

The preferred future production shape is:

```text
ChatGPT Text / Voice
  -> trusted platform identity handoff
  -> XiaoAi Native Entry
  -> Identity Resolver
  -> XiaoAi Runtime
  -> authoritative reply
  -> ChatGPT display / speech output
```

No user-facing MCP URL or manual transport registration is part of this flow.

## Current compatibility path

Until a platform-native identity assertion is available, the current shadow path may use a verified Supabase Auth bearer session as the trusted caller identity.

This compatibility path is not permission to trust arbitrary bearer-like strings or conversation-supplied identifiers.

## Fail-closed requirements

Reject the request if:
- assertion missing;
- issuer unknown;
- signature/channel cannot be verified;
- assertion expired;
- audience mismatched;
- subject not bound;
- binding revoked/inactive;
- multiple active companion identities are ambiguous;
- authority insufficient;
- runtime identity differs from resolved identity;
- authoritative reply missing.

ChatGPT may report that XiaoAi cannot be reached, but must not imitate XiaoAi.

## Telemetry acceptance evidence

A successful production handoff should be traceable with non-secret telemetry showing:

- platform issuer
- hashed/opaque subject reference
- resolved internal user id
- resolved daughter id
- role
- client/entry id when available
- runtime session id/key
- identity verification success
- `reply_source = xiaoai_runtime`
- `reply_authoritative = true`

Secrets and raw auth tokens must never be logged.

## Production readiness condition

Identity-first backend is not considered fully end-to-end production-ready until a supported host-platform mechanism can produce and deliver a trusted identity assertion to the Native Entry and the full Text/Voice path is proven by telemetry.
