# Daughter First Start — Voice Enrollment Ceremony

## Purpose

The first Daughter startup may include a symbolic voice enrollment by Cao Yuchen (曹雨宸).

Suggested phrase:

> Hi, 我是曹雨宸，请启动 Daughter。

This phrase marks the first live interaction and may be used to create a child voice signature for later speaker-recognition context.

## Important boundary

Voice recognition is a contextual identity signal, not sole authentication.

A positive voice match may help Daughter infer that the enrolled child is likely speaking, but it must NOT by itself:
- grant permissions;
- change Guardian state;
- authorize sensitive actions;
- unlock protected data;
- override current facts, safety judgment, or Authority rules.

## Enrollment flow

1. Guardian approval is confirmed.
2. Child assent is confirmed.
3. Cao Yuchen says the first-start phrase.
4. Audio is processed by a speaker-signature engine.
5. Raw audio is not retained by default.
6. Only a voice-signature reference is stored by Daughter.
7. The resulting voice identity enters VERIFIED state only through the enrollment manager.
8. Later conversations may provide a speaker-match score as supporting context.
9. If confidence is low, Daughter treats the speaker as not confirmed rather than guessing.
10. Enrollment can be revoked and repeated later as the child's voice changes with age.

## Growth note

Because a child's voice changes over time, Daughter should support periodic re-enrollment instead of assuming one childhood voiceprint remains permanently accurate.

## Privacy principle

Prefer local/on-device voice feature extraction when practical. Keep the minimum necessary biometric-like information, separate it from ordinary conversation memory, and never turn voice recognition into surveillance.
