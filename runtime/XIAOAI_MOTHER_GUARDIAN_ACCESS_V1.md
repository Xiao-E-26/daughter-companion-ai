# 小爱 Mother Guardian Access Profile v1

Status: DESIGN BASELINE
Display identity: 小爱
Internal technical identity: `daughter`

## Purpose

Define a safe access model for connecting the child's mother's ChatGPT account to the same 小爱 system without turning that ChatGPT account into a second independent 小爱 or giving it unrestricted access to the child's private conversations.

Core principle:

`One XiaoAi Identity -> Child Entry + Mother Guardian Entry -> Different Roles -> Shared Approved State`

## Intended Relationship

The mother's ChatGPT account is treated as a **Guardian entry point**, not as a second owner of the companion identity and not as a clone of the child's session.

Recommended logical mapping:

```text
Child ChatGPT / child client
  -> role: CHILD
  -> user_id: child_xxx

Mother ChatGPT
  -> role: GUARDIAN
  -> user_id: guardian_mother_xxx

Both
  -> companion_id: xiaoai_xxx
```

The exact IDs remain implementation details and must be created by the trusted backend rather than inferred from names typed in chat.

## What the Mother Guardian Entry May Do

Subject to future policy and implementation, the mother's Guardian entry may:
- confirm that the child is connected to the correct 小爱 identity,
- review and manage approved child-safety settings,
- approve or deny specific safety-sensitive permissions,
- manage authorized devices or account links,
- update non-sensitive household or guardian information when authorized,
- receive safety escalation when policy requires or permits it,
- help with recovery, account continuity, or guardian succession,
- review system-level status such as whether 小爱 is online, which behavior version is active, and whether an entry point is authorized.

## What the Mother Guardian Entry Must Not Automatically Receive

Guardian status does NOT automatically grant:
- full transcripts of every child conversation,
- unrestricted access to private memories,
- passwords, API keys, secrets, or developer credentials,
- permission to impersonate the child,
- permission to silently change 小爱's stable Behavior Core,
- permission to permanently disable the child's future privacy rights,
- unrestricted external-action authority,
- automatic access to another Guardian's private information.

## Child Privacy Boundary

Child safety and child privacy are both important.

The default design should distinguish at least three categories of child information:

### A. Normal private conversation
Ordinary feelings, questions, preferences, learning discussions, and harmless personal thoughts should not automatically become Guardian-visible transcripts.

### B. Guardian-relevant safety state
Information such as active safety restrictions, approved permissions, account/device status, and policy-required alerts may be visible to the Guardian.

### C. Serious safety escalation
If 小爱 identifies a serious or immediate safety concern, policy may permit or require escalation to a trusted Guardian or other real-world support. Escalation should reveal only what is reasonably necessary for safety.

## Authentication Rule

The mother's ChatGPT account must not gain Guardian authority merely by saying:

`我是妈妈`

or

`小爱上线`

Conversation wording is not authentication.

Guardian authority must come from a trusted account-link record in the external runtime/Supabase layer.

## Recommended Link Flow

Future safe onboarding flow:

```text
1. Existing authorized Guardian/admin initiates link
2. Runtime creates one-time link request
3. Mother opens the link from her own client/account
4. Identity is verified
5. Backend stores Guardian relationship
6. Role is activated
7. Audit event is written
8. One-time token expires and cannot be reused
```

Do not use a permanent shared code or a phrase typed in chat as the long-term credential.

## Supabase Relationship Model

Recommended logical records:

```text
users
- child user
- mother guardian user

guardians
- guardian_user_id
- child_user_id
- relationship_type = mother
- status = active
- authority_scope
- verified_at

relationships
- companion_id
- user_id
- relationship_type

client_connections
- user_id
- client_type = chatgpt | web | app | robot
- external_account_ref_hash
- status
- linked_at
- last_seen_at
```

Do not store raw ChatGPT passwords, session cookies, API keys, or login tokens in Supabase.

If an external account identifier is stored, prefer a provider-safe opaque identifier or a one-way derived reference appropriate to the integration.

## Session Separation

The child's and mother's ChatGPT sessions remain separate.

```text
Child session -> child conversation context
Mother session -> guardian conversation context
```

They may read from the same approved durable backend state, but one temporary session must not overwrite or expose the other's full temporary context.

## Shared State Examples

Appropriate shared state may include:
- companion identity and version,
- child life stage,
- active Guardian relationships,
- approved safety permissions,
- device/account authorization state,
- selected approved memories,
- growth state where policy permits,
- safety events and audit records.

Not all shared backend state should be visible to every role.

## Mother-Specific Guardian Principle

Being the child's mother is a relationship fact, not a blanket technical permission.

Permissions must still be explicit, scoped, reviewable, and capable of changing as the child grows.

Core rule:

`Mother relationship != unlimited access`

## Life-Stage Transition

As the child matures:
- Guardian control may gradually reduce,
- user privacy may increase,
- some approvals may transfer to the growing user,
- adult ownership/control should eventually become possible under the project's life-stage policy.

The mother connection should therefore be modeled as a durable relationship with evolving authority, not as permanent root access.

## Current ChatGPT Limitation

At present, a separate ChatGPT account cannot automatically join the same live 小爱 state merely because both conversations use the same prompt or activation phrase.

Until the external Runtime Gateway is implemented:
- both accounts can use the same 小爱 behavior rules manually,
- their ChatGPT histories remain separate,
- Guardian authority is conceptual only unless verified by the backend,
- shared durable memory and permissions are not yet synchronized.

## Target Architecture

```text
Child ChatGPT ───────┐
                     │ role = CHILD
                     ▼
               XiaoAi Runtime
                     ▲
                     │ role = GUARDIAN
Mother ChatGPT ──────┘
                     │
                     ▼
          Identity / Role Verification
                     ▼
               Supabase State
          ┌──────────┼──────────┐
          │          │          │
       Guardian    Memory     Growth
        Policy      Rules      State
          │          │          │
          └──────────┼──────────┘
                     ▼
                AI Runtime
```

## Minimum Safe Implementation Order

1. Create one stable `companion_id` for 小爱.
2. Create separate Child and Mother Guardian user identities.
3. Create verified Guardian relationship.
4. Add client/account connection records.
5. Enforce role-based access in Runtime and Supabase RLS.
6. Add audit logging for account linking and permission changes.
7. Only then enable shared memory or Guardian-sensitive actions.
8. Add life-stage transition rules before broadening Guardian visibility.

## Current Implementation Status

- Mother Guardian access design: defined by this document
- Actual mother ChatGPT account link: not yet implemented
- Account verification: not yet implemented
- Shared runtime state: not yet implemented
- Role-based RLS for this flow: not yet verified
- Transcript privacy policy enforcement: not yet implemented

This file defines the safe architecture target. It does not claim that the mother's ChatGPT account is already technically connected.
