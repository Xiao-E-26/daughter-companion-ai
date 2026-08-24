from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from runtime.voice_input_adapter import (
    SpeakerMatchResult,
    VoiceInputAdapter,
    VoiceSample,
    VoiceSignatureResult,
)


@dataclass(frozen=True)
class LocalVoiceBackendConfig:
    command: Sequence[str]
    timeout_seconds: float = 30.0


class SubprocessVoiceEngine(VoiceInputAdapter):
    """Adapter for a real local/on-device speaker-recognition backend.

    The backend is an executable chosen by deployment. Daughter sends JSON on
    stdin and expects JSON on stdout. This keeps biometric model selection out of
    Daughter's protected core and avoids vendor lock-in.

    Protocol:
      create_signature input:
        {"operation":"create_signature","audio_ref":"...","transcript":"..."}
      expected output:
        {"signature_ref":"...","quality_score":0.0..1.0}

      compare input:
        {"operation":"compare","audio_ref":"...","transcript":"...",
         "signature_ref":"..."}
      expected output:
        {"score":0.0..1.0}

    This adapter does not grant permissions or Authority. The referenced local
    backend must separately implement secure audio handling and model inference.
    """

    provider_name = "local-subprocess"

    def __init__(self, config: LocalVoiceBackendConfig) -> None:
        if not config.command:
            raise ValueError("Local voice backend command is required.")
        self.config = config

    def create_signature(self, sample: VoiceSample) -> VoiceSignatureResult:
        payload = {
            "operation": "create_signature",
            "audio_ref": sample.audio_ref,
            "transcript": sample.transcript,
        }
        response = self._invoke(payload)
        signature_ref = str(response.get("signature_ref", "")).strip()
        quality = float(response.get("quality_score", -1.0))
        if not signature_ref:
            raise RuntimeError("Voice backend returned no signature_ref.")
        self._validate_score(quality, "quality_score")
        return VoiceSignatureResult(signature_ref=signature_ref, quality_score=quality)

    def compare(self, sample: VoiceSample, *, signature_ref: str) -> SpeakerMatchResult:
        payload = {
            "operation": "compare",
            "audio_ref": sample.audio_ref,
            "transcript": sample.transcript,
            "signature_ref": signature_ref,
        }
        response = self._invoke(payload)
        score = float(response.get("score", -1.0))
        self._validate_score(score, "score")
        return SpeakerMatchResult(score=score)

    def _invoke(self, payload: dict[str, object]) -> dict[str, object]:
        completed = subprocess.run(
            list(self.config.command),
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            timeout=self.config.timeout_seconds,
            check=False,
        )
        if completed.returncode != 0:
            stderr = completed.stderr.strip()
            raise RuntimeError(
                f"Local voice backend failed with exit={completed.returncode}: {stderr}"
            )
        try:
            parsed = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            raise RuntimeError("Local voice backend returned invalid JSON.") from exc
        if not isinstance(parsed, dict):
            raise RuntimeError("Local voice backend response must be a JSON object.")
        return parsed

    @staticmethod
    def _validate_score(value: float, field: str) -> None:
        if not 0.0 <= value <= 1.0:
            raise RuntimeError(f"Voice backend {field} must be between 0 and 1.")
