# 小爱 — Behavior Mode Router v1 Merge Readiness

Status: **READY FOR NON-ACTIVATING MERGE**  
Date: 2026-08-27  
Pull request: #6  
Head: `1570d656e62f4a5723e02090bd3086368b291034`  
Base: `main@dd7db2f436ac537611ce6937040e0f062dde43a2`

## Repository state reviewed

- PR is open and Draft.
- Mergeability: clean.
- Branch is 13 commits ahead and 0 commits behind `main`.
- Changed files: 11.
- Additions: 874.
- Deletions: 0.
- Frozen Behavior Core was not modified.
- Memory, identity, permission, database, and production integration were not modified.
- Latest Golden Regression CI: SUCCESS.

## Evidence

- Context-shift semantic dry-run: 19/19 PASS.
- Executable Router and existing regression set: PASS.
- Multi-conflict Router matrix: 11/11 PASS.
- Wording candidate baseline: 6/6 scenarios PASS.
- Full targeted local regression after additions: 31/31 test functions PASS.
- Latest GitHub Golden Regression CI at PR head: SUCCESS.

## Architectural finding

The Router remains a small classification layer above existing policy-derived
signals. It does not infer safety, authority, memory truth, or Guardian status
from raw text. It selects one primary family:

`SAFETY > BOUNDARY > GUIDE > COMPANION`

Existing interaction modes and Frozen Core remain the policy owners.

## Important non-activation boundary

This PR adds the Router contract, executable module, tests, CI coverage, and
reviewed wording fixtures. It does **not** wire `BehaviorModeRouter` into the
production orchestrator or any live model path.

Therefore merging this PR means:

- the candidate Router becomes part of the main codebase;
- regression protection becomes part of main CI;
- live XiaoAi behavior does not automatically change.

It must not be described as a production Router rollout.

## Known limitations

1. Wording regression uses reviewed candidate fixtures, not repeated live-model sampling.
2. Cross-device handoff tests confirm that context must not expand authority; they do not prove live account delivery or database RLS.
3. The Router trusts upstream policy-derived booleans and safety level; upstream signal generation needs its own integration review.
4. No production telemetry, shadow routing, or rollback automation exists for Router activation.

## Merge conditions

The PR is ready to leave Draft and merge only as a non-activating infrastructure
change if the owner accepts the boundary above.

Do not combine this merge with orchestrator activation, policy migration,
database changes, or production deployment.

## Rollback

If the merge causes repository or CI regression, revert the PR merge commit as
one unit. Because this PR does not activate runtime routing or modify persisted
data, rollback requires no database migration or memory repair.

## Separate next phase after merge

Create a new isolated activation branch for:

1. orchestrator adapter contract;
2. shadow-mode routing with no response control;
3. live-model multi-sample wording evaluation;
4. mismatch telemetry between legacy interaction mode and Router family;
5. explicit owner review before any production enforcement.
