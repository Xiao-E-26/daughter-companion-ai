# Daughter Voice Engine Status

## Current state

Daughter now has:
- a provider-neutral voice input contract;
- child voice enrollment and revocation rules;
- speaker identity as supporting runtime context;
- a local voice engine scaffold for deterministic pipeline testing.

## Important limitation

`runtime/local_voice_engine.py` is NOT a real biometric speaker-recognition engine.

Its current feature extraction and similarity functions are deterministic placeholders so the enrollment -> signature -> compare -> Daughter context pipeline can be tested without claiming production voice recognition.

Do not use its match score as evidence that a real person has been identified.

## Production requirement

Before real speaker recognition is enabled, replace the placeholder feature extractor with a vetted local/on-device speaker-embedding backend and validate it on:
- multiple recordings from the enrolled child;
- different rooms/noise levels;
- age-related voice change;
- false-positive speakers;
- replayed recordings;
- low-quality input;
- revocation/re-enrollment.

Voice identity remains supporting context only and must never become the sole credential for permissions or sensitive actions.
