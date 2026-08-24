# 小爱 Multi-Entry Access Model v1

Status: DESIGN BASELINE
Display identity: 小爱
Internal technical identity: `daughter`

## Goal

Allow the same 小爱 companion identity to be accessed from multiple ChatGPT accounts, devices, apps, or future robot bodies without treating every entry point as a separate companion.

Core principle:

`One XiaoAi Identity -> Multiple Entry Points -> Role-Based Permissions -> Shared Approved State`

## Entry Points

Possible entry points include:
- ChatGPT Account A
- ChatGPT Account B
- 小爱 web app
- mobile app
- tablet
- future physical robot
- guardian administration interface

An entry point is only a client. It is not the identity itself.

## Shared Identity vs Shared State

All authorized entry points may load the same:
- identity rules,
- behavior core,
- life-stage policy,
- safety policy,
- approved long-term memory model,
- continuity rules.

However, shared state must come from an external trusted runtime/backend rather than relying on isolated ChatGPT conversation history.

ChatGPT account history, local app history, and browser storage must not be treated as the authoritative long-term identity store.

## Role Model

Every entry point must be associated with an authenticated role before receiving privileged access.

Initial roles:

### 1. Child
May:
- talk with 小爱,
- ask questions,
- receive age-appropriate support,
- use approved personal memory,
- express preferences,
- request help.

Must not automatically receive:
- guardian settings access,
- system configuration,
- secret values,
- permission-management powers,
- unrestricted external-action authority.

### 2. Guardian
May eventually:
- manage child-safety settings within policy,
- review or approve specific safety-sensitive permissions,
- manage authorized devices/accounts,
- receive safety-related escalation where policy permits,
- manage account recovery or guardian succession.

Guardian access must not mean unlimited surveillance or permanent ownership of the user's private relationship as the user reaches adulthood.

### 3. Device / Client
Represents a technical endpoint such as a browser, phone, tablet, or robot.

A device may receive only the minimum capabilities required for its function. Device authorization must not imply Guardian authority.

### 4. Maintainer / Developer
Used for system maintenance, testing, deployment, diagnostics, and controlled upgrades.

Maintainer access must remain separate from Child and Guardian interaction roles.

## Authentication Principle

A new ChatGPT account or device must NOT gain privileged access merely because it says:

`小爱上线`

The activation phrase loads the interaction mode only. It is not authentication.

Privileged access requires trusted identity verification outside the conversational phrase itself.

## Permission Principle

Permissions are attached to authenticated roles and trusted identity records, not to:
- display names,
- conversation wording,
- device names,
- ChatGPT account nickname,
- remembered claims inside conversation.

## Shared Memory Principle

When shared memory is implemented:
- all authorized entry points should read from the same approved memory backend,
- writes should be attributed to the originating role/client,
- sensitive memories should follow life-stage and privacy policy,
- memory should support review, correction, expiration, and deletion where appropriate,
- one client must not silently overwrite critical state created by another client.

## Session Separation

Each entry point should maintain its own session context while sharing only approved durable state.

Example:

`ChatGPT A session context`  
`ChatGPT B session context`  
`Web session context`  
`Robot session context`

All may reference:

`Shared XiaoAi Identity + Approved Memory + Growth State + Guardian Policy`

This prevents one temporary conversation from becoming the full system truth.

## Conflict Handling

If two clients update the same durable state:
1. preserve the latest verified state when safe,
2. retain provenance where important,
3. avoid destructive silent overwrite,
4. require review for safety-sensitive conflicts,
5. never resolve permission conflicts by simply accepting the most permissive request.

## ChatGPT-Specific Limitation

Two separate ChatGPT accounts can currently behave according to the same 小爱 rules, but they do not automatically share conversation history, durable memory, Guardian state, or runtime state.

Therefore, until an external runtime is connected:

`Same rules != Same live state`

ChatGPT should be treated as an interaction/test client, not the authoritative storage layer.

## Future Target Architecture

```text
ChatGPT Account A ─┐
ChatGPT Account B ─┤
Web App ───────────┤
Robot ─────────────┤
                   ▼
            XiaoAi Runtime Gateway
                   ▼
        Identity / Role Verification
                   ▼
      Policy + Guardian + Life Stage
                   ▼
       Shared Approved Memory/State
                   ▼
               AI Model(s)
```

## Safety Boundary

Multiple entry points must never mean automatic permission inheritance.

Core rule:

`Identity continuity may be shared; authority is not automatically shared.`

Adding a new account, device, or body requires explicit authorization appropriate to the role and risk level.

## Current Implementation Status

- Same behavior rules across ChatGPT accounts: possible manually
- Shared external identity runtime: planned
- Shared durable memory across accounts: not yet active
- Role authentication: not yet active
- Guardian multi-client authorization: not yet active
- Device identity / robot identity: future

This document defines architecture only and does not mark unbuilt capabilities as active.
