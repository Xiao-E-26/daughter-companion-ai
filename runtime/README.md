# Runtime Skeleton v0.1

Planned components:

- orchestrator
- depth_router
- context_builder
- judgment_engine
- problem_solver
- memory_manager
- growth_manager
- safety_gate
- response_builder
- model_adapter

## Request flow
User message → session → depth routing → relevant context → judgment/problem solving → safety gate → model → response → memory candidate.

## Principle
Keep the first implementation modular but monolithic. Do not split into microservices until scale or operational needs justify it.
