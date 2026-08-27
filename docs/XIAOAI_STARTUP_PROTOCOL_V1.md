# XiaoAi Startup Protocol V1

## Purpose

Make the phrase `小爱上线` a deterministic startup command instead of a conversational persona switch.

This protocol exists so XiaoAi startup does not depend on short-term chat memory.

## Trigger

Exact user intent: `小爱上线`

Default meaning:

> Start the GitHub-backed XiaoAi runtime context for `Xiao-E-26/daughter-companion-ai`, then enter XiaoAi persona only after startup checks complete.

The user does not need to say `GitHub 小爱` every time.

## Mandatory startup sequence

1. Resolve repository: `Xiao-E-26/daughter-companion-ai`.
2. Confirm the current default/production branch state, with `main` as the current canonical branch unless the repository says otherwise.
3. Read the active Runtime / Behavior / Memory / Session / Context definitions required for the current interaction.
4. If connected production services such as Supabase are required for the requested interaction, verify or read them before claiming the full runtime is active.
5. Only after the checks above, activate the XiaoAi persona and respond in XiaoAi style.

## Failure rule

If GitHub or required runtime sources cannot be read, do **not** pretend XiaoAi has fully started.

Instead, clearly report that startup is partial or failed and identify the unavailable source.

A greeting-only persona switch does not count as successful startup.

## Architecture constraints

- Do not create a second Voice Persona.
- Do not modify the frozen Behavior Core through this protocol.
- Do not create a parallel XiaoAi runtime.
- Text and voice are two I/O paths into the same XiaoAi Persona / Behavior / Runtime / Memory / Session / Context.
- Keep the existing production path intact.

## Operational interpretation

`小爱上线` is a startup protocol trigger, not merely a style instruction.

Expected conceptual path:

`小爱上线` → GitHub/runtime verification → required context load → XiaoAi persona active → reply to user

## Success criterion

Startup is successful only when the response is grounded in the actual current XiaoAi project/runtime sources required for that turn.
