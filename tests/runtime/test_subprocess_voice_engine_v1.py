from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

from runtime.subprocess_voice_engine import LocalVoiceBackendConfig, SubprocessVoiceEngine
from runtime.voice_input_adapter import VoiceSample


def _write_backend(path: Path) -> None:
    path.write_text(
        """
import json, sys
payload = json.loads(sys.stdin.read())
if payload['operation'] == 'create_signature':
    print(json.dumps({'signature_ref': 'voice:test-child', 'quality_score': 0.92}))
elif payload['operation'] == 'compare':
    print(json.dumps({'score': 0.91}))
else:
    raise SystemExit(3)
""".strip(),
        encoding="utf-8",
    )


def test_local_backend_contract_create_and_compare() -> None:
    with tempfile.TemporaryDirectory() as directory:
        backend = Path(directory) / "voice_backend.py"
        _write_backend(backend)
        engine = SubprocessVoiceEngine(
            LocalVoiceBackendConfig(command=[sys.executable, str(backend)])
        )
        sample = VoiceSample(audio_ref="local://sample.wav", transcript="Hi, 我是曹雨宸，请启动 Daughter。")

        signature = engine.create_signature(sample)
        assert signature.signature_ref == "voice:test-child"
        assert signature.quality_score == 0.92

        match = engine.compare(sample, signature_ref=signature.signature_ref)
        assert match.score == 0.91


def test_local_backend_rejects_invalid_score() -> None:
    with tempfile.TemporaryDirectory() as directory:
        backend = Path(directory) / "voice_backend.py"
        backend.write_text(
            "import json, sys; json.loads(sys.stdin.read()); print(json.dumps({'score': 2.0}))",
            encoding="utf-8",
        )
        engine = SubprocessVoiceEngine(
            LocalVoiceBackendConfig(command=[sys.executable, str(backend)])
        )
        sample = VoiceSample(audio_ref="local://sample.wav", transcript="hello")
        try:
            engine.compare(sample, signature_ref="voice:test")
        except RuntimeError as exc:
            assert "between 0 and 1" in str(exc)
        else:
            raise AssertionError("invalid backend score should be rejected")
