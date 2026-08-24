from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path


def _require_deps():
    try:
        import torch
        from speechbrain.inference.speaker import SpeakerRecognition
    except ImportError as exc:
        raise RuntimeError(
            "SpeechBrain backend requires optional dependencies: speechbrain and torch."
        ) from exc
    return torch, SpeakerRecognition


MODEL_SOURCE = os.environ.get(
    "DAUGHTER_VOICE_MODEL_SOURCE",
    "speechbrain/spkrec-ecapa-voxceleb",
)
MODEL_CACHE = os.environ.get(
    "DAUGHTER_VOICE_MODEL_CACHE",
    ".daughter_voice_model_cache",
)
SIGNATURE_DIR = Path(
    os.environ.get("DAUGHTER_VOICE_SIGNATURE_DIR", ".daughter_voice_signatures")
)


def _load_model():
    _, SpeakerRecognition = _require_deps()
    return SpeakerRecognition.from_hparams(
        source=MODEL_SOURCE,
        savedir=MODEL_CACHE,
    )


def _embed_file(model, audio_path: str):
    torch, _ = _require_deps()
    path = Path(audio_path)
    if not path.is_file():
        raise RuntimeError(f"Audio file not found: {audio_path}")

    waveform = model.load_audio(str(path))
    if waveform.numel() == 0:
        raise RuntimeError("Audio file contained no usable samples.")

    batch = waveform.unsqueeze(0)
    embedding = model.encode_batch(batch, normalize=True)
    embedding = embedding.detach().cpu().reshape(-1).to(torch.float32)
    return embedding


def _save_signature(embedding) -> str:
    SIGNATURE_DIR.mkdir(parents=True, exist_ok=True)
    payload = embedding.numpy().tobytes()
    digest = hashlib.sha256(payload).hexdigest()
    ref = f"speechbrain:{digest[:24]}"
    path = SIGNATURE_DIR / f"{digest}.pt"

    torch, _ = _require_deps()
    torch.save(embedding, path)
    return ref


def _load_signature(signature_ref: str):
    if not signature_ref.startswith("speechbrain:"):
        raise RuntimeError("Unsupported signature reference.")

    short = signature_ref.split(":", 1)[1]
    matches = list(SIGNATURE_DIR.glob(f"{short}*.pt"))
    if len(matches) != 1:
        raise RuntimeError("Voice signature reference could not be resolved uniquely.")

    torch, _ = _require_deps()
    return torch.load(matches[0], map_location="cpu", weights_only=True).reshape(-1)


def _cosine_score(reference, current) -> float:
    torch, _ = _require_deps()
    score = torch.nn.functional.cosine_similarity(
        reference.unsqueeze(0),
        current.unsqueeze(0),
        dim=-1,
    )[0].item()
    # Adapter contract expects 0..1. Cosine is -1..1, so normalize.
    normalized = (float(score) + 1.0) / 2.0
    return max(0.0, min(1.0, normalized))


def handle(request: dict[str, object]) -> dict[str, object]:
    operation = str(request.get("operation", "")).strip()
    audio_ref = str(request.get("audio_ref", "")).strip()
    if not audio_ref:
        raise RuntimeError("audio_ref is required.")

    model = _load_model()
    current = _embed_file(model, audio_ref)

    if operation == "create_signature":
        signature_ref = _save_signature(current)
        return {
            "signature_ref": signature_ref,
            "quality_score": 1.0,
            "backend": "speechbrain-ecapa",
            "model_source": MODEL_SOURCE,
            "raw_audio_retained": False,
        }

    if operation == "compare":
        signature_ref = str(request.get("signature_ref", "")).strip()
        if not signature_ref:
            raise RuntimeError("signature_ref is required for compare.")
        reference = _load_signature(signature_ref)
        return {
            "score": _cosine_score(reference, current),
            "backend": "speechbrain-ecapa",
            "model_source": MODEL_SOURCE,
        }

    raise RuntimeError(f"Unsupported operation: {operation}")


def main() -> None:
    try:
        request = json.load(sys.stdin)
        if not isinstance(request, dict):
            raise RuntimeError("Input must be a JSON object.")
        response = handle(request)
        json.dump(response, sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
