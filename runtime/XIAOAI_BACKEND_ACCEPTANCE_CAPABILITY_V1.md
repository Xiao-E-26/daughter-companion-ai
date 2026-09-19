# XiaoAi Backend Acceptance Capability v1

Status: REFERENCE / DESIGN — NOT DEPLOYED

## Purpose

Define the intended backend acceptance model without claiming a capability exists in production when it has not been deployed.

## Intended two-layer model

### Layer A — routine backend regression

Target checks may include:
- active companion-access count;
- active client count;
- runtime-session uniqueness;
- persona-state readiness when such persistence exists;
- auth binding counts;
- overall identity-first readiness.

Earlier design text referenced:

`xiaoai_internal.backend_acceptance_snapshot()`

A live production database inspection on 2026-09-20 found no deployed backend-acceptance, acceptance-snapshot, identity-first acceptance, or native-entry acceptance function matching this design.

Therefore that function name is a target/reference, not a current capability.

### Layer B — real authenticated identity E2E

Target flow:

```text
real user session
  -> trusted identity handoff
  -> Identity Resolver
  -> XiaoAi Runtime
  -> authoritative reply
```

This remains the decisive proof for live identity/session readiness.

## Current verified posture

- identity/session schema exists;
- current live identity/session row counts are zero;
- persona-state persistence is not productionized;
- supported host-platform identity handoff is not connected end-to-end;
- live conversational serving is not active.

## Acceptance rule

A design document, test that checks document wording, or database schema presence must not be presented as proof of deployed backend acceptance.

Production acceptance requires live implementation evidence and read-back/telemetry from the actual runtime path.

## Deprecated workflow

Do not recreate temporary acceptance pages, repeated OTP flows, retired shadow transports, or service-role impersonation merely to make this design appear active.
