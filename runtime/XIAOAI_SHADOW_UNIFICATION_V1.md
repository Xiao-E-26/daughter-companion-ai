# XiaoAi Shadow Unification v1

Status: DESIGN / SHADOW ONLY

## Non-negotiable constraints

- Frozen Behavior Logic MUST NOT change.
- Existing `daughter-chat` reply path remains authoritative during Shadow.
- Shadow path MUST NOT write `runtime_sessions`, `client_connections`, memory, Guardian state, continuity, or audit records.
- Shadow path MUST NOT call a model provider for user-facing output.
- Shadow failure MUST NEVER fail or delay the current production reply path.

## Problem

The live `daughter-chat` function currently performs its own identity/access/session resolution and provider call. The existing `xiaoai-mcp-runtime` is already a useful authoritative context/state gateway, but calling it directly from `daughter-chat` is not a valid Shadow design because it writes runtime session state and last-seen metadata.

## Target architecture

`daughter-chat current path`

-> existing production reply (unchanged)

AND, independently:

-> `ReadOnlyRuntimeContextResolver`
-> normalized runtime snapshot
-> Shadow comparator / telemetry candidate

## ReadOnlyRuntimeContextResolver contract

Input:
- authenticated Supabase user identity;
- session_key;
- current message metadata only as needed for correlation (never for authority inference).

Reads only:
- `users`;
- `companion_access`;
- `daughter_identities` via authorized relationship;
- `client_connections`;
- `runtime_sessions`;
- role-visible continuity state;
- scoped preferred conversational name.

Must not mutate any state.

Output fields:
- resolved: boolean;
- daughter_id;
- internal_user_id;
- role;
- authority_scope;
- client_connection_id;
- persona_state;
- child_name;
- session_key;
- continuity_visible: boolean;
- resolver_version;
- error_code (safe enum only).

## Shadow comparator

The first comparator should compare only deterministic runtime facts already resolved by live `daughter-chat` against the read-only resolver:

- daughter_id equality;
- user scope equality;
- client connection equality;
- persona_state equality;
- child_name equality;
- role / authority_scope equality.

It must not compare free-form LLM responses yet.

## Telemetry contract

Initial telemetry should contain only:
- timestamp;
- correlation id;
- resolver version;
- match booleans by deterministic field;
- safe error code;
- latency bucket.

Do not store child message text, full transcripts, raw tokens, secrets, or private memory payloads.

## Promotion criteria

Shadow runtime may influence production only after:
1. deterministic identity/session comparisons are stable;
2. no authority widening is observed;
3. no cross-account visibility regression is observed;
4. telemetry is privacy-safe;
5. Behavior Logic Freeze and Golden Regression remain green;
6. a separate explicit cutover approval is given.

## Explicitly excluded

`xiaoai-brain-core-test` is experimental and keyword-driven. It is NOT the canonical production brain and must not be wired into live response control under this Shadow phase.
