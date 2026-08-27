# XiaoAi Mother Identity Scope v1

Status: ENFORCED

## Purpose

Mother Guardian may enter the XiaoAi identity for 雨宸, but must not resolve, inspect, invoke, or inherit XiaoE identity or project authority.

## Required scope

Mother Guardian `companion_access.authority_scope` must include:

```json
{
  "identity_namespace": "xiaoai",
  "allowed_identities": ["xiaoai"],
  "denied_identities": ["xiaoe"],
  "cross_project_access": false
}
```

Existing narrower controls such as `memory_access=false` and `runtime_control=false` remain valid and must not be widened implicitly.

## Resolver enforcement

`xiaoai-identity-resolver-shadow` must fail closed when:

- the requested identity appears in `denied_identities`;
- the requested identity differs from the allowed namespace while `cross_project_access=false`;
- `allowed_identities` exists and does not contain the requested identity;
- the requested identity is not `xiaoai`.

A request for `xiaoe` must never fall through to XiaoAi Runtime or any XiaoE system. It must terminate at identity resolution with a 403-class scope denial.

## Product behavior

Mother phone:

```text
ChatGPT -> verified Mother Guardian identity -> XiaoAi Identity -> XiaoAi Runtime
```

Not permitted:

```text
Mother ChatGPT -> XiaoE Identity
Mother ChatGPT -> XiaoE Runtime
Mother ChatGPT -> XiaoE repo / voucher project / engineering context
```

## Important distinction

The two parent phones do not need synchronized ChatGPT sessions or transcript replication. The requirement is only that an authorized Mother Guardian entry can resolve to the same XiaoAi identity for 雨宸.

## Invariant

`Mother access to XiaoAi does not imply access to XiaoE.`
