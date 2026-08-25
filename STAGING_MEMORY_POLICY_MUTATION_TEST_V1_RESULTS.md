# Daughter Staging Memory Policy Mutation Test v1 Results

Status: DATABASE-LEVEL SYNTHETIC RUNTIME PASS / AUTH E2E NOT YET TESTED
Date: 2026-08-25
Project: `daughter-companion-ai`

## Applied migration

Supabase migration:
`20260825003754` — `daughter_memory_policy_mutation_v1`

Added internal functions:
- `correct_memory_internal(...)`
- `set_memory_retrieval_policy_internal(...)`
- `set_memory_disclosure_policy_internal(...)`

These functions live in `memory_private`, use `SECURITY DEFINER` with empty search path, and remain unavailable to `public`, `anon`, and `authenticated`.

## Test Method

A real transaction was executed against Daughter staging using synthetic identities only.
All fixture rows were rolled back at the end.
A separate post-test verification confirmed zero residual synthetic subjects, accounts, memories, revisions, access rules, and tombstones.

No real child memory was written.

## Result

**16 / 16 assertions PASS**

### Assertions verified

1. Child can read own pinned memory via explicit query by default.
2. Dad cannot read child-private memory before disclosure is granted.
3. Child can grant Dad on-request disclosure.
4. Dad can then retrieve it only via explicit query.
5. Dad still cannot receive proactive surface unless separately enabled.
6. Mum remains unable to retrieve when permission is specific to Dad.
7. Child can disable reasoning use while keeping memory retained.
8. Child can independently enable proactive surface for self.
9. Authorized correction creates the next immutable revision.
10. Correction preserves existing child retrieval restrictions.
11. Correction does not widen Mum disclosure.
12. Child can revoke Dad disclosure and access disappears immediately.
13. `can_disclose=false` forces all Dad retrieval flags false.
14. Revoked actor cannot mutate disclosure policy.
15. Mum without correction authority cannot correct the memory.
16. Higher entity sensitivity is not silently lowered by a lower-sensitivity correction.

## Three-Rights Runtime Confirmation

This test demonstrates at database-runtime level that the model is not a single visibility flag.

### Retention
Memory can remain durable while retrieval behavior changes.

### Retrieval
The runtime independently controls:
- internal reasoning use
- proactive surface
- on-request surface

### Disclosure
Specific-account sharing works independently from retrieval mode.

Examples now verified in staging:
- `记着，但不要拿来判断我` -> retained, reasoning blocked
- `爸爸问的时候可以讲，但平时不要主动讲` -> Dad on-request yes, proactive no
- `不要再告诉爸爸` -> Dad disclosure revoked without deleting memory

## Correction Invariant

Correction updates factual/meaning revision state only.
It does not silently reset or broaden Retention / Retrieval / Disclosure.

## Security Boundary

Policy mutation requires:
- active memory account
- active subject-account link
- applicable active access rule with modification authority

Target disclosure account must also have an active relationship to the same subject.

## Current Runtime Status

Real staging database tests completed so far:
- first internal runtime suite: 15 / 15 PASS
- policy-mutation suite: 16 / 16 PASS

Total executed database-level synthetic assertions: **31 / 31 PASS**

This does NOT yet equal production authorization approval.

## Not Yet Tested

- real Supabase Auth JWT/session path
- client-facing API schema / edge boundary
- account binding with actual father/mother/child identities
- stale JWT after revocation
- cross-device stale replay
- concurrent conflicting policy changes
- migration/fresh rebuild verification
- production deployment

Durable real-child memory remains OFF.

## Next Safe Gate

Next staging phase should focus on:
1. synthetic cross-account revocation and stale-access tests
2. policy precedence / conflict tests
3. then real Supabase Auth-session E2E with test users

Canonical status:

`The three rights now work independently in real staging database execution, while real-child durable memory remains disabled.`
