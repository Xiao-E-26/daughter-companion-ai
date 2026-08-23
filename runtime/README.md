# Backend Runtime v0.1

Status: scaffolded, not yet connected to a model provider or exposed as a public API.

## Implemented foundation

- `contracts.ts` — runtime request/response, growth, memory, judgment, problem-plan, safety, and model contracts
- `depth_router.ts` — D0/D1/D2/D3 routing from consequence, ambiguity, emotional intensity, and safety relevance
- `safety_gate.ts` — risk-aware gate with clarification/support/protect paths
- `model_adapter.ts` — provider-independent model interface; deliberately unconfigured by default
- `orchestrator.ts` — request → context → judgment → safety → model → memory-candidate flow

## Planned next modules

- context_builder
- judgment_engine
- problem_solver
- memory_manager
- growth_manager
- response_builder
- mediated backend data gateway

## Request flow

User message → authenticated session → relevant context → depth/judgment → problem solving → safety gate → model adapter → response → selective memory candidate.

## Security boundary

The runtime is the only intended path to sensitive companion state. Client applications must not receive service-role credentials and must not directly mutate identity, growth, safety, memory, or audit state.

Critical safety decisions must not be delegated to raw model output alone. The runtime owns the safety gate and future physical-action systems require an independent safety controller.

## Architecture principle

Keep the first implementation modular but monolithic. Do not split into microservices until scale or operational needs justify it. Model providers remain replaceable; Daughter identity, memory, judgment policy, and relationship continuity remain outside the model provider.
