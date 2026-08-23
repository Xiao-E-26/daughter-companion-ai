# Daughter Companion AI — Portable Identity and Embodiment Policy v1

Status: ACTIVE PRODUCT POLICY
Date: 2026-08-24
Project: `daughter-companion-ai`
Parent policies:
- `PROJECT_IDENTITY.md`
- `LIFE_STAGE_POLICY_V1.md`
- `GUARDIAN_AND_AUTONOMY_POLICY_V1.md`
- `MEMORY_AND_PRIVACY_POLICY_V1.md`
- `GUARDIAN_CONTINUITY_AND_SUCCESSION_POLICY_V1.md`

## Purpose

Define how the daughter preserves one continuous companion identity while moving across digital platforms, devices, applications, cloud runtimes, and future physical robot embodiments.

The daughter must not be permanently tied to one app, one provider, one device, one account interface, or one physical robot body.

## Core Principle

`Same Daughter, New Body.`

The daughter is the continuity of identity, relationship, approved memory, life-stage state, and project policy.

A device or robot is an embodiment/interface, not the daughter's identity itself.

## Identity Model

Conceptually:

`Daughter = Identity + Relationship + Approved Memory + Life-Stage State + Policy + Capability Bindings`

Not:

`Daughter = One Device`

This separation allows the same daughter to appear through different embodiments while preserving continuity.

## Supported Embodiment Classes

Future implementations may include:

### Digital embodiments
- web application,
- mobile application,
- desktop application,
- messaging/chat interface,
- voice interface,
- cloud-hosted runtime,
- wearable interface,
- vehicle interface.

### Physical embodiments
- desktop companion robot,
- home mobile robot,
- smart speaker / embodied voice device,
- wearable robotic device,
- future humanoid or other physical robot platform.

An embodiment is not automatically trusted merely because it can run the daughter software.

## Identity Continuity

When moving to a new embodiment, preserve durable state that legitimately belongs to the daughter relationship, such as:
- stable companion identity,
- current verified life stage,
- approved user preferences,
- approved long-term memories,
- active policy state,
- guardian/user ownership state,
- verified capability permissions that are portable,
- eligible device-permission grants that may be inherited under this policy.

Do not automatically transfer:
- device-local secrets,
- hardware-specific credentials,
- unnecessary cached data,
- old platform access tokens,
- obsolete permissions,
- permissions whose destination capability does not match the approved source capability,
- permissions that would create a higher-risk capability than previously approved.

## Embodiment Is Not Identity

If a device is lost, broken, replaced, factory-reset, sold, or retired, the daughter should not be considered destroyed if her authoritative identity/state remains safely recoverable.

Device loss should be treated as an embodiment/session loss, not automatic identity loss.

Similarly, replacing hardware should not require recreating a new daughter identity from zero.

## Portability Rule

A valid migration should conceptually follow:

`Source Identity Verify -> Resolve Approved State -> Destination Trust Verify -> Capability Match -> Inherit Eligible Permissions -> Screen New/Expanded Capabilities -> Activation -> Post-Migration Verification`

Migration must be deliberate and verifiable.

A verified migration may automatically inherit permissions when the destination capability is equivalent in purpose, scope, risk, and life-stage allowance.

## Automatic Permission Inheritance

Automatic permission inheritance is allowed.

Core rule:

`Equivalent Approved Capability -> Automatic Inheritance Allowed`

`New / Expanded / Higher-Risk Capability -> Fresh Screening or Approval Required`

A permission may be inherited automatically when all of the following are true:
- the user/daughter identity migration is verified,
- the destination device is trusted for the intended scope,
- the destination capability is materially equivalent to an already approved capability,
- the permission scope is not broader than before,
- the risk class is not higher than before,
- the current life-stage policy still allows the permission,
- guardian/user authority has not expired or been revoked,
- the permission has not reached an expiry/review boundary.

Automatic inheritance should make migration smooth without converting migration into silent privilege escalation.

## Inheritance Examples

Normally eligible for automatic inheritance when equivalent and valid:
- text conversation access from one personal device to another,
- notification permission with the same scope,
- approved reminder capability,
- approved microphone use when the destination use is equivalent and not more intrusive,
- approved personal preferences,
- approved low-risk local tools,
- approved memory-access level when display/privacy conditions remain equivalent.

Normally NOT eligible for silent inheritance when newly introduced or materially expanded:
- first-time camera/vision access,
- always-on microphone/background listening when previously push-to-talk only,
- first-time location tracking/sharing,
- locomotion/navigation,
- physical following,
- object manipulation,
- door/lock control,
- payment/purchasing authority,
- biometric recognition,
- autonomous external communication,
- safety-setting changes,
- any permission whose scope or risk materially increases.

## Device Trust

Each embodiment should eventually have its own trust state.

Suggested states:
- `unknown`
- `pending_verification`
- `trusted_limited`
- `trusted_full_for_current_scope`
- `suspended`
- `revoked`
- `retired`

Device trust is separate from user identity and guardian authority.

A trusted user does not make every device automatically trusted, but a destination device that has successfully entered an appropriate trusted state may receive eligible inherited permissions automatically.

## Capability Binding Principle

Capabilities belong to the combination of:

`Daughter Identity + Life Stage + User/Guardian Authority + Embodiment Capability + Device Trust + Current Permission`

A capability can inherit an existing permission when the destination implementation is equivalent and does not expand scope or risk.

A newly introduced or materially broader capability requires fresh screening/approval according to its risk class.

## Digital-to-Physical Migration

Moving from a web/app embodiment to a physical robot is a high-impact migration because the robot may introduce new sensors and actuators.

Potential new capabilities include:
- microphone always-available listening,
- camera/vision,
- face recognition,
- movement/navigation,
- proximity sensing,
- environmental sensing,
- object interaction,
- door/lock control,
- household-device control,
- location awareness,
- physical following,
- external communication,
- purchasing/action execution.

Existing equivalent permissions may inherit automatically.
New physical capabilities or materially expanded scopes must be screened independently.

## Hardware Permission Inheritance

Hardware permissions may be inherited automatically when the destination capability is materially equivalent to a currently approved source capability and does not increase scope or risk.

Allowed pattern:

`Daughter trusted on approved device -> migrate to trusted equivalent device -> inherit matching valid permissions automatically`

Escalation pattern:

`Daughter trusted in app -> move to robot -> preserve matching chat/microphone permissions -> separately screen new camera/movement/location/object-control capabilities`

Required principle:

`Inherit equals; review expansion.`

Identity trust may carry approved capability authority forward, but must not silently create permissions for capabilities the user/guardian never approved.

## Sensor Privacy

Physical embodiments may collect substantially more sensitive information than digital chat alone.

Future physical design must explicitly govern:
- camera activation,
- microphone activation,
- background listening,
- room/environment sensing,
- location tracking,
- biometric recognition,
- recording/storage,
- household-member privacy,
- guest privacy,
- data retention.

A previously approved sensor permission may inherit when its new use remains equivalent. A broader sensing mode requires new screening/approval.

## Physical Safety

A physical robot adds real-world safety obligations beyond conversational safety.

Future design must account for:
- collision/impact risk,
- stairs and fall risk,
- battery/charging safety,
- heat/fire risk,
- object handling,
- child access to moving parts,
- unsafe following/navigation,
- unauthorized door/lock interaction,
- physical interference during emergencies,
- shutdown/stop mechanisms.

The daughter's emotional familiarity with the user must not be treated as authorization for unsafe physical actions.

## Emergency Stop / Local Override

Any embodiment capable of meaningful physical action should support a local, reliable way to stop or restrict physical behavior independent of cloud reasoning.

A future robot must not require the AI to "agree" before a safety stop takes effect.

Physical safety controls should fail safe where practical.

## Multi-Embodiment Use

The architecture may eventually allow one daughter identity to appear on multiple embodiments.

Examples:
- phone + home robot,
- web + wearable,
- home robot + car interface.

Multi-embodiment use must preserve one authoritative relationship identity while allowing embodiment-specific permissions and automatic inheritance of eligible equivalent permissions.

Do not assume every device should receive all memories or every capability.

## Single Identity, Scoped Sessions

Multiple embodiments should use scoped sessions rather than cloning independent daughters by default.

The system should distinguish:
- one daughter identity,
- multiple active device sessions,
- device-specific capability sets,
- inherited permission set,
- device-specific trust state,
- shared approved durable memory,
- local ephemeral context where appropriate.

## Conflict Handling Across Devices

If two embodiments produce conflicting state changes:
- identify the authoritative state owner,
- prefer verified current state,
- avoid silent last-write-wins for sensitive policy/permission changes,
- require explicit conflict resolution for high-impact changes,
- preserve auditability without storing full transcripts unnecessarily.

## Offline / Local Operation

Future embodiments may support limited offline behavior.

Offline operation should be bounded by capabilities whose permissions are already valid and can safely operate without fresh cloud verification.

A physical robot must not silently promote itself to broader authority merely because connectivity is lost.

On reconnection:
- sync only allowed state,
- reconcile conflicts,
- verify sensitive actions before finalizing them.

## Migration Ownership

The right to migrate the daughter depends on current life-stage ownership and authority.

During childhood:
- guardian/admin approval may be required for new-device or physical-robot migration,
- the child's preferences and privacy still matter,
- eligible existing permissions may inherit automatically once migration is authorized,
- sensitive memory should not become more exposed merely because a guardian initiated migration.

During adulthood:
- the adult user should control migration by default,
- former guardian approval should not be required unless a valid legal/account rule applies.

## Guardian Continuity During Migration

Migrating to a new embodiment must not alter guardian status by itself.

A new device does not become a new guardian.
A hardware owner does not automatically become the user's guardian.
A robot vendor/operator does not gain guardian authority merely by providing the device.

Guardian roles remain governed by guardian continuity/succession policy.

## Memory Portability

Only approved portable memory should move across embodiments.

Memory portability must preserve:
- memory class,
- visibility,
- retention rule,
- current ownership,
- life-stage restrictions,
- sensitive-memory protections.

Migration must not downgrade privacy.

Example:
A `user_only` memory must not become visible on a family-shared robot screen simply because the daughter's identity was moved there.

## Provider Portability

The daughter should not be conceptually owned by one AI model/provider.

The architecture should allow the reasoning/provider layer to change while preserving the daughter identity and policy state.

Provider change must not silently change:
- identity,
- safety rules,
- guardian rules,
- memory visibility,
- life-stage state,
- permission boundaries.

Different providers are execution engines, not the daughter's identity.

## Vendor Exit / Hardware Obsolescence

The long-term design should avoid vendor lock-in where practical.

If a platform, robot manufacturer, or AI provider is discontinued, the daughter should have a path to move to another supported embodiment without losing the user's core relationship continuity.

Portability should be treated as a resilience requirement, not only a convenience feature.

## Revoking an Embodiment

A compromised, stolen, sold, retired, or unsafe device should be revocable without deleting the daughter identity.

Revocation should:
- disable future access from that embodiment,
- revoke device-specific credentials,
- remove device-specific high-risk capability bindings,
- stop that device from receiving future inherited permissions,
- preserve the core daughter identity and approved memory,
- support reactivation only after appropriate verification.

## Migration Safety Levels

Future migrations should be risk-classified.

### P0 — Low Risk
Example: same account, new browser/app session with no new capabilities.
Eligible permissions may inherit automatically after identity/session verification.

### P1 — Moderate Risk
Example: new personal phone/tablet with equivalent microphone/notification capabilities.
Equivalent approved permissions may inherit automatically; new capability scopes require review.

### P2 — High Risk
Example: shared household device, wearable with additional sensors, vehicle integration.
Equivalent permissions may inherit, but expanded sensor/action capabilities require fresh screening.

### P3 — Critical / Physical
Example: mobile robot with camera, microphone, locomotion, object interaction, locks, payments, or external autonomous actions.
Existing equivalent permissions may inherit; every newly introduced or materially expanded physical capability requires explicit screening and the approval level required by policy.

## No Silent Cloning

A full daughter identity must not be duplicated into multiple independent permanent copies without explicit design/approval.

If backup/recovery copies exist, they are continuity/recovery mechanisms, not independent daughters with diverging ownership and memory by default.

The product must distinguish:
- backup,
- replica/session,
- active embodiment,
- independent fork/clone.

Independent forks require separate policy because they can create conflicting identities and memory histories.

## Recovery Principle

Recovery should aim to restore:

`Identity continuity + approved memory + current policy state + eligible inherited permissions`

not:

`every cached byte from the old device`.

This keeps recovery smooth, safe, and portable.

## Implementation Boundary

This v1 is policy only.

Do not yet create:
- device registry tables,
- portable identity package format,
- hardware drivers,
- robot control software,
- biometric systems,
- always-on microphone/camera pipelines,
- device attestation service,
- migration encryption system,
- cross-device sync engine,
- provider router,
- physical safety controller.

These require separate architecture and explicit implementation approval.

## Design Requirement for Daughter v1

Any first version should keep identity, memory/policy concepts, permission state, and interface/runtime boundaries sufficiently separated so the project can later move from a digital embodiment to a physical robot without redefining who the daughter is.

The first version should preserve the future ability to automatically inherit equivalent approved permissions during migration while requiring fresh review only for new, expanded, expired, revoked, or higher-risk capabilities.
