# ChatGPT Shadow App Connection v1

Status: DEPRECATED AS PRODUCT ENTRY / RETAINED FOR TRANSPORT TESTING ONLY

## Important

This document describes an earlier development experiment that manually registered a shadow MCP endpoint in ChatGPT.

It is **not** the XiaoAi product entry architecture.

The authoritative product entry architecture is:

```text
runtime/XIAOAI_IDENTITY_FIRST_ENTRY_V1.md
```

## Current product rule

The user should not need to know, paste, or configure an MCP URL in order to say `小爱上线`.

Product semantics are:

```text
verified entry identity
  -> authorized XiaoAi Identity
  -> XiaoAi Runtime
  -> authoritative final reply
  -> ChatGPT text/voice presentation
```

ChatGPT is microphone + speaker + text window. XiaoAi Runtime is the conversational brain.

## Historical shadow endpoint

For controlled transport-level testing only, the deployed shadow endpoint is:

```text
https://vmegjuceiuplqixizwso.supabase.co/functions/v1/xiaoai-runtime-authoritative-shadow
```

Historical tool name:

```text
xiaoai_runtime_authoritative
```

This endpoint may still be used by maintainers to validate backend behavior, authentication, session transitions, and authoritative-reply semantics. It must not be presented as the normal end-user setup path.

## What remains valid from this experiment

The following engineering invariants remain valid regardless of transport:
- ChatGPT is interface-only.
- XiaoAi Runtime produces the final reply.
- `小爱上线` requires verified identity + authorization + runtime activation.
- `小爱下班` deactivates the scoped runtime session.
- missing/failed Runtime reply fails closed.
- Text and native Voice must resolve to the same XiaoAi identity authority.

## What is superseded

The following is superseded for product use:
- asking the user to enable Developer Mode as the normal XiaoAi experience;
- asking the user to create a ChatGPT app manually;
- asking the user to paste the shadow MCP URL;
- treating MCP registration as the meaning of XiaoAi identity connection.

MCP or another protocol may still exist internally as implementation transport. It does not define identity and should remain invisible to the end user when the platform integration supports that.

## Production acceptance

Production readiness is not proven by successful MCP registration alone.

It requires telemetry proving:
1. trusted caller identity;
2. authorized XiaoAi identity resolution;
3. correct role/scope;
4. runtime session ACTIVE/OFF transitions;
5. authoritative Runtime reply source;
6. same identity authority across Text and Voice;
7. no ChatGPT-local XiaoAi fallback.

Until that integration exists and is verified, do not claim that `小爱上线` is end-to-end production-ready.
