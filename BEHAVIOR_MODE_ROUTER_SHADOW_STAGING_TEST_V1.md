# Behavior Router Shadow Staging Test v1

Status: **ACTIVE IN CI/STAGING TEST LINE**  
Production activation: **OFF**  
Response control: **OFF**

## Purpose

Run the merged Behavior Router beside the existing Python runtime across fixed child-companion scenarios. The run records which behavior family the Router would recommend while proving that the existing model request, deterministic boundary, and response remain unchanged.

## Test coverage

- ordinary connection;
- emotional expression;
- problem solving;
- truth/responsibility boundary;
- S1 boundary precedence;
- significant safety;
- critical safety;
- multi-signal safety precedence;
- invalid-signal non-interruption.

## Hard boundaries

- Signals are fixture-provided and policy-derived; no keyword inference is introduced.
- Shadow results never enter the system prompt or model metadata.
- `controls_response` must remain `false`.
- No Supabase write, durable telemetry, child transcript ingestion, Guardian change, or production deployment is included.
- The live `daughter-chat` Edge Function is outside this repository and is not modified by this test line.

## Exit criteria

The staging Shadow line is considered healthy only when every scenario returns its expected family and the baseline-versus-shadow model request, response text, and deterministic boundary are identical. GitHub Golden Regression CI is the executable gate.
