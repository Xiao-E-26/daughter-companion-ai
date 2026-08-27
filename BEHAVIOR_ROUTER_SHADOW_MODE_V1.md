# 小爱 — Behavior Router Shadow Mode v1

Status: candidate  
Activation: off by default

## Purpose

Observe the Behavior Mode Router beside the existing runtime without allowing
the Router to control model instructions, response text, deterministic boundary,
Authority, memory, or tool execution.

## Contract

- Shadow mode is constructor-injected and disabled by default.
- It accepts only explicit policy-derived `RouterInput` signals.
- It does not infer signals from child or Guardian wording.
- Its result is returned as diagnostic `shadow_behavior_route` only.
- It is not included in the system prompt or model metadata.
- Invalid observations are recorded as `ERROR` and do not block the existing path.
- Every observation declares `controls_response=false`.

## Non-goals

- no production enforcement;
- no automatic signal generator;
- no database write or telemetry transport;
- no change to Frozen Core, memory, identity, Guardian, or Authority policy.

## Promotion gate

Before Router output can control behavior, a later isolated phase must add
verified signal generation, mismatch telemetry, multi-sample live-model testing,
explicit owner review, and a separate production approval.
