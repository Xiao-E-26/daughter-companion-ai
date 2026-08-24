from runtime.local_voice_engine import LocalVoiceEngine
from runtime.voice_input_adapter import VoiceSample


def test_local_voice_engine_same_sample_matches() -> None:
    engine = LocalVoiceEngine()
    sample = VoiceSample(audio_ref="local://sample-a", transcript="Hi, 我是曹雨宸，请启动 Daughter。")
    signature = engine.create_signature(sample)
    match = engine.compare(sample, signature_ref=signature.signature_ref)

    assert signature.quality_score == 0.9
    assert match.score == 1.0


def test_local_voice_engine_different_sample_does_not_match() -> None:
    engine = LocalVoiceEngine()
    enrolled = VoiceSample(audio_ref="local://sample-a", transcript="Hi, 我是曹雨宸，请启动 Daughter。")
    other = VoiceSample(audio_ref="local://sample-b", transcript="Hello")

    signature = engine.create_signature(enrolled)
    match = engine.compare(other, signature_ref=signature.signature_ref)

    assert match.score == 0.0
