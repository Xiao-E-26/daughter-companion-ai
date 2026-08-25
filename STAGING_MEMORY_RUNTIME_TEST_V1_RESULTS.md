# Daughter Staging Memory Runtime Test v1 Results

Status: DATABASE-LEVEL SYNTHETIC RUNTIME PASS / AUTH E2E NOT YET TESTED
Date: 2026-08-25
Project: `daughter-companion-ai`
Supabase environment: existing dedicated Daughter project designated as staging

## Applied migrations

- `20260825002557` — `daughter_memory_runtime_foundation_v1`
- `20260825003041` — `daughter_memory_internal_runtime_v1`

The second migration added:
- `memory_private.memory_candidates`
- `create_memory_candidate_internal(...)`
- `pin_child_memory_internal(...)`
- `retrieve_memories_internal(...)`
- `delete_memory_internal(...)`

The functions live in the private schema, use `SECURITY DEFINER` with an empty search path, and are not executable by `public`, `anon`, or `authenticated`. Current execution is restricted to the trusted server/service-role path.

## Test method

A real Postgres transaction was executed against Daughter staging using synthetic identities only.

Synthetic roles represented:
- child
- father guardian
- mother guardian
- runtime
- unrelated account

All test rows were wrapped in `BEGIN ... ROLLBACK`.
After rollback, a separate verification query confirmed zero residual synthetic subjects, accounts, candidates, memories, and tombstones.

No real child memory was written.

## Result

**15 / 15 assertions PASS**

### Assertions

1. Linked Dad with candidate permission may submit a memory candidate.
2. Unrelated account is denied candidate submission.
3. Verified child-direct long-term-memory pin succeeds.
4. Repeated pin with the same idempotency key returns the same memory ID.
5. Guardian cannot impersonate a verified child-direct pin operation.
6. `reminder_or_task` intent cannot use the durable Child-Pinned path.
7. Child-Pinned memory is available for `reasoning_context` by default.
8. Child-Pinned memory is available for `explicit_user_query` by default.
9. Child-Pinned memory is not proactively surfaced by default.
10. Dad cannot retrieve the child's default self-only pin.
11. Unknown retrieval purpose fails closed.
12. Authorized child deletion succeeds.
13. Deleted memory is excluded from normal retrieval.
14. Deletion creates a monotonic tombstone.
15. Deleted entity state is explicitly recorded with `status=deleted` and `deleted_at`.

## Retention / Retrieval / Disclosure behavior verified

The first database-level runtime test demonstrates that the implemented path can distinguish:

- Retention: child-pinned durable state
- Retrieval / internal reasoning: allowed
- Retrieval / proactive surface: denied by default
- Retrieval / explicit query: allowed
- Disclosure: default pin is limited to the actor account unless separately broadened

This is a real database runtime result, not merely a policy simulation.

## Security posture after migration

Supabase Security Advisor reports only `RLS enabled no policy` informational notices for `memory_private` tables.

This is intentional at this stage:
- internal tables have RLS enabled
- direct `anon` and `authenticated` table access is revoked
- no client-facing table policies exist yet
- internal functions are not executable by `anon` or `authenticated`

These notices do not constitute approval for production exposure.

## Important limits

The following are **not yet tested**:
- real Supabase Auth sessions / JWT end-to-end
- client-facing API schema
- actual Dad/Mum/Child account binding
- correction runtime RPC
- retrieval/disclosure policy mutation RPCs
- revoked-account E2E through real Auth
- cross-account sync E2E
- stale-client replay E2E
- production migration/fresh rebuild

Durable real child memory remains **OFF**.

## Next safe gate

Continue staging with:
1. correction RPC
2. retrieval-policy mutation RPC
3. disclosure-policy mutation RPC
4. synthetic cross-account and revocation tests
5. then real Auth-session E2E before any real child memory activation

Canonical status:

`Memory runtime has begun passing real staging database tests, but real-child durable memory remains disabled until authorization and Auth E2E gates pass.`
