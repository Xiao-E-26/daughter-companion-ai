# XiaoAi ChatGPT App Entry Contract v1

Status: DESIGN LOCK — ENTRY LAYER ONLY

## Purpose

Provide a native ChatGPT App entry for XiaoAi so an authorized Guardian can use ordinary ChatGPT text or voice as the interface while all identity, behavior, memory, safety, continuity, and reply authority remain inside the existing XiaoAi backend.

## Canonical flow

```text
ChatGPT text / voice
-> XiaoAi ChatGPT App tool
-> verified app authorization context
-> XiaoAi Native Entry
-> XiaoAi Identity Resolver
-> XiaoAi Runtime
-> authoritative XiaoAi reply
-> ChatGPT displays / speaks reply
```

## Non-negotiable invariants

1. ChatGPT is interface only: microphone, speaker, text window, and tool caller.
2. The ChatGPT App MUST NOT define a second XiaoAi persona.
3. The ChatGPT App MUST NOT own XiaoAi memory.
4. The ChatGPT App MUST NOT infer identity from names, phrases, voice, or conversation text.
5. `小爱上线` is an activation command, not an authentication factor.
6. The app MUST fail closed when the authorization context cannot be mapped to an existing XiaoAi access record.
7. No Runtime reply = no XiaoAi reply.
8. Mother Guardian scope is XiaoAi-only. XiaoE access is denied before runtime entry.
9. Text and Voice use the same tool and same backend path.
10. No browser/device page is part of the primary ChatGPT path.

## Identity rule

The app must obtain identity only from an authenticated/authorized app session and map it to the existing XiaoAi identity graph.

Existing backend identity chain remains authoritative:

```text
authenticated app subject
-> public.users
-> companion_access
-> client_connections
-> daughter_identities
```

The adapter must not create a new Guardian, companion access, client connection, or daughter identity merely because authorization is missing or failed.

## Mother Guardian restriction

Mother Guardian may resolve only:

```text
identity_namespace = xiaoai
allowed_identities = [xiaoai]
denied_identities = [xiaoe]
cross_project_access = false
```

A XiaoE request from Mother Guardian must terminate before XiaoAi Runtime or XiaoE systems are invoked.

## Tool surface

Primary tool:

`xiaoai_message`

Input:
- `message`: required user text after speech-to-text when Voice is used.
- `session_key`: optional; default `xiaoai-current`.

Behavior:
- Forward the authenticated authorization context and message to the existing XiaoAi Native Entry.
- Do not rewrite Persona or behavior instructions.
- Return only an authoritative backend reply when `reply_authoritative=true` and `reply_source=xiaoai_runtime`.
- Otherwise return a structured failure and never imitate XiaoAi locally.

## Activation / deactivation

The same tool handles:
- `小爱上线`
- normal conversation
- `小爱下班`

No separate Voice tool and no separate activation Persona.

## Acceptance evidence

A successful Mother Guardian ChatGPT test requires:

1. ChatGPT App is connected/authorized.
2. Expected XiaoAi tool is available.
3. Sending `小爱上线` invokes the tool.
4. Backend Identity Resolver resolves the existing Mother Guardian access.
5. The resolved identity is the existing XiaoAi daughter identity.
6. Runtime session transitions to ACTIVE.
7. Reply has `reply_authoritative=true` and `reply_source=xiaoai_runtime`.
8. No new Guardian/access/daughter identity is created.
9. A XiaoE request is denied by identity scope.

## Explicitly out of scope

- Device webpage as primary entry.
- Voiceprint identity authentication.
- Automatic account guessing.
- Full transcript synchronization between parent accounts.
- XiaoE engineering/project access from Mother Guardian.
- A second MCP Persona or second Memory store.

## Product invariant

`One XiaoAi Identity + one Runtime + many authorized interfaces.`
