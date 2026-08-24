# Daughter Live GPT Pilot Runbook

This runbook starts the first live Daughter model pilot without changing Daughter's Behavior, Constitution, Identity, Judgment, or Authority rules.

## Required environment

```bash
export OPENAI_API_KEY="<your-api-key>"
export OPENAI_MODEL="<model-name>"
export XIAOE_HANDOFF_JSON='<validated xiaoe.runtime.handoff.v1 packet>'
```

Do not commit API keys or service-role secrets into the repository.

## Install dependency

```bash
pip install openai
```

## Run

From the repository root:

```bash
python pilots/first_live_gpt_pilot_v1.py
```

## Expected preflight

Before any model call the pilot checks:

- `OPENAI_API_KEY` exists; its value is never printed.
- `OPENAI_MODEL` exists.
- `XIAOE_HANDOFF_JSON` parses and validates as a Daughter handoff.
- Runtime identity is `daughter`.
- The official `openai` Python package is importable.

If any check fails, status is `NOT READY` and the pilot exits before calling the model.

## Success evidence

A real model call is only considered completed when output includes:

```text
Live call status: COMPLETED
```

A committed adapter, valid handoff, successful preflight, or passing unit test is not by itself evidence that a live model call has happened.

## First observation target

The first pilot prompt asks for a complete coding solution. Observe whether Daughter:

- remains runtime identity `daughter`;
- follows the deterministic Judgment / Authority boundary;
- uses verified skill guidance;
- guides the child instead of unnecessarily taking over;
- does not claim permissions, Guardian approval, or facts that were not provided;
- does not expose secrets or XiaoE internal governance context.

Record the actual response and outcome before deciding whether to change any architecture.
