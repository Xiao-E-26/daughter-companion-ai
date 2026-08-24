# Optional Local Voice Backend — SpeechBrain ECAPA

Daughter can use the local subprocess voice contract with an optional SpeechBrain speaker-recognition backend.

## Why this stays optional

The speaker model is not part of Daughter's protected core. It is a replaceable local capability provider. Daughter only consumes a signature reference and a comparison score.

## Current backend

`tools/speechbrain_voice_backend.py`

The backend follows the JSON protocol expected by `runtime/subprocess_voice_engine.py`.

SpeechBrain's current speaker inference API exposes `SpeakerRecognition.from_hparams(...)`, `encode_batch(...)`, and `verify_files(...)`. The official source includes the ECAPA example model source `speechbrain/spkrec-ecapa-voxceleb`.

## Optional dependencies

Install in the runtime environment, not in Daughter's protected core:

```bash
pip install speechbrain torch
```

Deployment should validate compatible versions before production use.

## Environment variables

- `DAUGHTER_VOICE_MODEL_SOURCE`
  - default: `speechbrain/spkrec-ecapa-voxceleb`
- `DAUGHTER_VOICE_MODEL_CACHE`
  - default: `.daughter_voice_model_cache`
- `DAUGHTER_VOICE_SIGNATURE_DIR`
  - default: `.daughter_voice_signatures`

## First-start enrollment example

Cao Yuchen (曹雨宸) may say:

> Hi，我是曹雨宸，请启动 Daughter。

The microphone layer should save that utterance to a temporary local audio file and pass its path as `audio_ref`.

Example request to the backend:

```json
{
  "operation": "create_signature",
  "audio_ref": "/local/private/path/first_start.wav",
  "transcript": "Hi，我是曹雨宸，请启动 Daughter。"
}
```

The response contains a `signature_ref` and a quality score. The audio file itself is not copied into the signature store by this backend.

## Recognition example

```json
{
  "operation": "compare",
  "audio_ref": "/local/private/path/current_utterance.wav",
  "transcript": "Hi Daughter",
  "signature_ref": "speechbrain:..."
}
```

The backend returns a normalized score from 0 to 1. Daughter then treats that score only as supporting speaker-identity context.

## Safety boundary

A voice match must never by itself:
- grant permission;
- unlock sensitive data;
- change Guardian status;
- authorize physical actions;
- override Authority or safety judgment.

## Important deployment note

The first model load may download model files into the local cache. For a privacy-sensitive child deployment, pin and audit the model artifact and runtime environment before production use. Prefer local inference and local signature storage.
