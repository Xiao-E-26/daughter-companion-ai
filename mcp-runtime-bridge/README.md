# XiaoAi MCP Runtime Bridge

Status: compatibility bridge only.

## Canonical runtime path

The current production architecture is:

`ChatGPT (conversational brain) -> xiaoai-mcp-runtime (identity/state/context gateway) -> Supabase`

The bridge in this folder is retained only as a compatibility layer. It MUST NOT become a second conversational brain and MUST NOT route replies through a separate model provider.

## Brain boundary

- ChatGPT generates the conversational reply.
- Supabase owns verified identity, scoped authority, runtime session state, memory, audit and continuity state.
- The runtime gateway returns verified context; it does not generate a second AI reply.
- `daughter-chat` is legacy for the current ChatGPT-brain architecture and must not be used as the canonical reply path.

## Session semantics

- `小爱上线` is the explicit activation command.
- `小爱下班` is the canonical shutdown command.
- `小爱收工` is retained as a backward-compatible shutdown alias.
- Shutdown makes the current session persona `OFF`.
- Ordinary emotional/family language must never auto-activate XiaoAi.

## Identity and authorization

The client must authenticate with its own Supabase Auth Bearer session. Runtime identity is resolved from verified backend bindings; chat claims such as `我是妈妈` do not grant guardian access.

No bridge input may directly grant `user_id`, guardian role, daughter identity, memory visibility or runtime authority.

## Memory and continuity

Authoritative durable memory lives in `memory_private.*` and follows the controlled child-pinned / reviewed promotion model.

Cross-account continuity is selective:

`same XiaoAi identity != full transcript sharing`

Only approved minimal continuity may cross authorized entry points. Sensitive content is not automatically mirrored between accounts or devices.

## Production source of truth

The canonical deployed endpoint is the Supabase Edge Function:

`xiaoai-mcp-runtime`

Repository code and compatibility bridges must align to that contract rather than creating parallel runtime semantics.
