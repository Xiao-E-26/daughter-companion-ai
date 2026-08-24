# 小爱 Checkpoint Protocol v1

Status: ACTIVE DESIGN PROFILE
Trigger phrase: `小爱收工`
Resume phrase: `小爱上线`

## Purpose

Give 小爱 a lightweight, reliable session handoff mechanism similar to 小E checkpoint behavior, without turning every conversation into permanent memory.

## Checkpoint Content

When `小爱收工` is triggered, produce a concise checkpoint containing only what is useful for continuity:

1. **Completed** — what was completed, decided, changed, or confirmed in this session.
2. **Current State** — the present status of the active project/topic when relevant.
3. **Open Items** — unresolved items, pending decisions, or known blockers when relevant.
4. **Resume Point** — the best next step or point to continue from on the next `小爱上线`.
5. **Persistence Note** — clearly distinguish between:
   - source-controlled project changes already written to GitHub,
   - runtime/shared state already stored in an approved persistence layer,
   - conversation-only context that is not yet persisted.

## Default Output Style

Keep the checkpoint short and easy to scan. Do not dump the whole conversation.

Suggested format:

`小爱 Checkpoint`
- Completed: ...
- Current: ...
- Open: ...
- Next: ...
- Saved: GitHub / shared runtime / conversation only

Fields with nothing meaningful to report may be omitted.

## Persistence Rules

A checkpoint must not automatically become durable personal memory.

Only persist information according to the active memory policy and permissions.

Do not store unnecessary sensitive child information, secrets, credentials, exact location, school details, financial information, or other private data simply because it appeared in a conversation.

Project configuration, behavior rules, and runtime definitions should remain in their authoritative source such as GitHub rather than being duplicated into personal memory.

## Cross-Account Continuity

For multiple ChatGPT accounts to resume from the same checkpoint, all participating interfaces must connect to the same authorized runtime/shared persistence layer.

GitHub alone can synchronize project definitions and behavior rules, but it does not by itself synchronize live conversation state or personal memory between ChatGPT accounts.

When shared checkpoint storage is available, the latest valid checkpoint may be loaded during `小爱上线`.

If shared storage is not available, do not claim cross-account synchronization. Present the checkpoint locally and state that it is conversation-only unless it has actually been persisted.

## Safety and Authority

Checkpoint restoration must never:
- bypass guardian rules,
- grant new permissions,
- override the Behavior Core,
- treat stale or uncertain state as verified fact,
- resurrect a previously revoked permission,
- convert conversation instructions into higher-authority policy.

If a checkpoint conflicts with newer GitHub configuration, guardian policy, safety policy, or verified runtime state, the newer/higher-authority source wins.

## Design Principle

`Checkpoint = continuity, not authority.`

The goal is to make 小爱 easy to resume while keeping the system simple, safe, and portable across interfaces.
