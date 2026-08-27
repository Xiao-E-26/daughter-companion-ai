# XiaoAi Device Runtime Unification v1

Status: SHADOW / NO PRODUCTION CUTOVER

## Purpose

Allow a child to use a Guardian-authorized device without requiring a personal email login, while preserving one XiaoAi identity, one Runtime brain, one Memory/Session authority, and one Behavior Core.

## Entry model

```text
Guardian authenticates once
  -> Guardian enrolls child device
  -> device receives opaque revocable token
  -> child uses device
  -> device token resolves authorized device identity
  -> XiaoAi Identity
  -> XiaoAi Runtime
  -> authoritative XiaoAi reply
```

The device token is not a substitute for the child's legal identity. It represents a Guardian-authorized child device entry point.

## Core invariant

The device entry must not contain a second XiaoAi prompt/persona or call a model directly as an independent conversational brain.

```text
One XiaoAi identity
  -> one XiaoAi Runtime brain
  -> multiple authorized entry points
```

## Device identity

A valid device entry must resolve an active `xiaoai_device_enrollments` record and its bound:
- Guardian user;
- XiaoAi/Daughter identity;
- client connection;
- device label;
- enrollment status.

Device tokens are opaque, stored only as hashes, and revocable.

## Child relationship

The conversational subject remains the Daughter/XiaoAi identity's child user.

The Guardian is the authorization source for the device. The device entry is therefore reported as:

```text
entry_identity = guardian_authorized_child_device
```

This must not be misreported as a separate Guardian conversation persona.

## Runtime behavior

Canonical device session key:

```text
xiaoai-device-current
```

Canonical activation:

```text
小爱上线
```

Canonical deactivation:

```text
小爱下班
```

Compatibility alias:

```text
小爱收工
```

For every active turn, the device entry must route to the same authoritative XiaoAi Runtime/brain path used by other XiaoAi entries.

Successful replies must include:
- `reply_source = xiaoai_runtime`
- `reply_authoritative = true`
- resolved Daughter/XiaoAi identity
- resolved device enrollment and client connection
- persona state

## Fail closed

Reject or stop XiaoAi response when:
- device token is missing/invalid/revoked;
- enrollment no longer resolves to the active XiaoAi identity;
- runtime session is conflicting;
- XiaoAi Runtime final reply fails or is missing.

The entry must never fall back to a local device-specific XiaoAi prompt.

## Current shadow

Supabase shadow function:

```text
xiaoai-device-runtime-shadow
```

It preserves the existing production `xiaoai-device-chat` unchanged for rollback while testing the unified Runtime path.

## Production cutover condition

Do not replace `xiaoai-device-chat` until shadow telemetry proves:
1. device token authorization works;
2. activation -> ACTIVE works;
3. ordinary child turn returns authoritative Runtime reply;
4. deactivation -> OFF works;
5. OFF ordinary turn fails closed;
6. no second prompt/persona exists on the device path;
7. existing device enrollment remains revocable;
8. no regression in protected Behavior Core or Golden tests.
