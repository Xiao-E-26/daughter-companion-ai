# Daughter Companion AI — Guardian Continuity and Succession Policy v1

Status: ACTIVE PRODUCT POLICY
Date: 2026-08-24
Project: `daughter-companion-ai`
Parent policies:
- `PROJECT_IDENTITY.md`
- `LIFE_STAGE_POLICY_V1.md`
- `GUARDIAN_AND_AUTONOMY_POLICY_V1.md`
- `MEMORY_AND_PRIVACY_POLICY_V1.md`

## Purpose

Define how the daughter maintains safe companionship continuity when a guardian is temporarily unavailable, permanently unavailable, incapacitated, legally replaced, deceased, or otherwise no longer able to act as the child's primary guardian.

This policy protects two goals at the same time:

1. the child's relationship with the daughter should not break merely because one guardian disappears,
2. guardian authority must never transfer to a new person without proper verification and scope control.

## Core Principle

`Guardian can change; companion continuity must not break.`

A guardian is an authorized safety/administrative role, not the permanent owner of the daughter's identity.

The daughter belongs to the continuity of the user's companion relationship, not to one guardian account forever.

## Guardian Roles

Future implementation should support role separation rather than one permanent guardian record.

Suggested roles:

- `primary_guardian` — current main guardian responsible for safety/administrative approval during childhood
- `backup_guardian` — pre-authorized replacement who may assume selected duties if the primary guardian becomes unavailable
- `trusted_adult` — lower-authority support contact who may be used for limited safety/support functions but does not automatically inherit guardian control
- `former_guardian` — historical guardian whose active authority has ended
- `adult_user_owner` — the user after valid ownership transition into adulthood

Role names are product concepts; legal definitions may differ by jurisdiction.

## No Single-Guardian Lock-In

The architecture must not require one permanent guardian account to remain available forever in order for the daughter to continue functioning.

If the primary guardian becomes unavailable, the system should preserve low-risk companionship while restricting only the actions that genuinely require guardian authority.

Do not freeze the entire companion relationship because one approver is missing.

## Guardian Availability States

Future product state should distinguish at minimum:

- `available`
- `temporarily_unavailable`
- `unreachable`
- `incapacitated`
- `authority_disputed`
- `authority_ended`
- `deceased`
- `replacement_pending`
- `replacement_verified`

Do not infer permanent unavailability from a short period of inactivity alone.

## Temporary Guardian Absence

When the primary guardian is temporarily unavailable:

The daughter should continue low-risk capabilities that were already valid for the user's current life stage, such as:
- normal conversation,
- age-appropriate learning support,
- emotional support within policy,
- problem-solving,
- previously approved low-risk routines,
- local non-sensitive personalization.

Actions that require fresh guardian approval should remain pending or unavailable until an authorized approver is restored or a valid substitute is verified.

Temporary absence must not trigger automatic transfer of guardian authority.

## Permanent Guardian Unavailability

If the primary guardian is permanently unavailable, including death or verified long-term incapacity:

1. preserve the daughter identity and normal low-risk companion continuity,
2. preserve existing valid user memories subject to privacy policy,
3. suspend only permissions that depend on the unavailable guardian's active authority,
4. enter a guardian succession state,
5. verify the next authorized guardian or legal/account transition path,
6. re-issue only the permissions appropriate to the new authority and current life stage,
7. do not automatically expose historical private conversations or sensitive memories to the successor guardian.

Guardian replacement is not memory ownership transfer.

## Backup Guardian

A backup guardian may be pre-authorized before a succession event.

Backup status should be scoped and revocable.

A pre-authorized backup may reduce recovery friction, but activation should still require evidence that:
- the backup identity is valid,
- the backup relationship/authority is still valid,
- the triggering condition is legitimate,
- current life-stage rules permit the transition.

Pre-authorization must not mean silent permanent co-ownership of the child's private data.

## Trusted Adult Boundary

A trusted adult is not automatically a guardian.

A trusted adult may eventually be allowed to:
- receive a safety escalation when configured,
- provide temporary support,
- assist with account recovery steps,
- help initiate guardian transition verification.

A trusted adult must not automatically gain:
- account ownership,
- full memory access,
- transcript access,
- guardian approval powers,
- location access,
- financial control,
- permission-management authority.

Those require separate verified authorization.

## Succession Verification

Guardian succession must not rely on a conversation claim alone.

Forbidden pattern:

`User says "this person is my new guardian" -> transfer control`

Required pattern:

`Succession request -> identity evidence -> authority/relationship verification -> life-stage check -> scope decision -> activation -> verification`

The exact verification mechanism is intentionally not defined in v1 and must be designed according to jurisdiction, account model, and product risk.

## Child / Teen Voice in Succession

The user's own voice should have increasing weight as they mature.

During childhood:
- legal/safety guardian verification may dominate formal authority transfer.

During adolescence:
- the teen's expressed preference should be considered where legally and safely allowed,
- a disputed guardian transition should not silently override the teen's privacy or safety concerns.

During young adulthood/adulthood:
- guardian succession should normally give way to user ownership transition rather than appointing a new controlling guardian.

## Conflict / Dispute State

If two adults claim guardian authority or the child's safety/privacy could be affected by a disputed transition:

- enter `authority_disputed`,
- keep low-risk companion functions available where safe,
- freeze new high-risk permissions,
- do not expand data visibility,
- do not transfer account ownership,
- preserve existing privacy boundaries,
- require stronger verification before changing authority.

Do not resolve a guardian dispute by choosing the first requester or the most recently authenticated adult.

## Emergency Continuity

Guardian unavailability does not remove the daughter's obligation to support the user during a safety concern.

If a configured guardian is unavailable during a significant safety event:
- follow the current safety-escalation policy,
- use only valid pre-configured backup/trusted contacts or approved emergency mechanisms,
- disclose only minimum necessary information,
- do not fabricate contact success,
- do not grant a new guardian role merely because someone was contacted during an emergency.

Emergency contact is not guardian succession.

## Permission Continuity

When guardian authority changes, existing permissions must be reviewed by class.

Possible outcomes:
- continue unchanged,
- suspend pending review,
- require new approval,
- expire automatically,
- transfer only with explicit user/guardian consent,
- prohibit transfer.

High-risk permissions such as location sharing, spending, new integrations, account-security changes, and external autonomous actions should not silently transfer to a successor guardian.

## Memory Continuity During Succession

The child's memories belong to the companion relationship, not to the outgoing guardian.

A guardian transition must not automatically:
- delete the daughter's relationship history,
- transfer all private memories to the new guardian,
- expose old transcripts,
- change user-private memory into guardian-visible memory.

Memory visibility remains controlled by life-stage and memory/privacy policy.

If a guardian dies or loses authority, the user should not lose all meaningful relationship continuity with the daughter merely because the guardian account is removed.

## Account Recovery Boundary

Account recovery and guardian succession are related but distinct.

Recovering technical account access must not automatically assign legal/guardian authority.

Likewise, becoming a verified guardian must not automatically reveal all historical private data if the role does not require it.

Future architecture should keep:
- authentication recovery,
- guardian authority,
- user ownership,
- memory visibility,
- high-risk approvals
as separate concepts.

## Transition Toward Adult Ownership

If guardian unavailability occurs near or after adulthood eligibility, the preferred path may be direct user ownership verification instead of appointing a new guardian.

Do not force an eligible adult or young-adult user through a new guardian dependency merely because the previous guardian disappeared.

At valid adulthood transition:
- verify user ownership,
- review/remove childhood guardian permissions,
- make the user primary controller,
- preserve appropriate companion continuity and memory,
- require the adult user's explicit consent for any continuing former-guardian or trusted-adult access.

## No Automatic Successor Ownership

A successor guardian receives only the authority necessary for the current life stage and product policy.

They do not inherit:
- ownership of the daughter's identity,
- unrestricted access to private conversations,
- permanent access into adulthood,
- all historical memory,
- all permissions granted to the former guardian.

## Revocation and Reversal

Guardian succession decisions should be reviewable and reversible when evidence changes, except where law or immediate safety requirements dictate otherwise.

If a transition is found to be incorrect:
- revoke invalid authority,
- restore the correct authority state,
- review any permissions or data exposure that occurred,
- preserve the user's companion continuity,
- document only the minimum necessary audit evidence.

## Implementation Boundary

This v1 is policy only.

Do not yet create:
- guardian succession tables,
- backup guardian enrollment,
- legal-document verification flows,
- death/incapacity verification services,
- automated guardian inactivity detection,
- authority dispute workflows,
- emergency notification infrastructure,
- inheritance-style account ownership transfer.

These require separate architecture and explicit implementation approval.

## Design Requirement for v1 Product Scope

Any future `DAUGHTER_V1_PRODUCT_SCOPE.md` must ensure that:
- ordinary low-risk companionship can continue if the guardian is temporarily unavailable,
- guardian-dependent high-risk actions fail safely,
- the system has no single permanent guardian lock-in,
- future succession can be added without replacing the daughter's identity or losing the user's relationship continuity.
