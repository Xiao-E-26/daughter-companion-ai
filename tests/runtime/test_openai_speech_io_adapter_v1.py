from pathlib import Path

from runtime.openai_speech_io_adapter import OpenAISpeechIOAdapter
from runtime.speech_io_adapter import SpeechToTextRequest, TextToSpeechRequest


class FakeTranscriptionResponse:
    text = "你好小爱"


class FakeTranscriptions:
    def create(self, **kwargs):
        self.kwargs = kwargs
        return FakeTranscriptionResponse()


class FakeSpeechResponse:
    def __init__(self, content: bytes = b"mp3-bytes") -> None:
        self.content = content


class FakeSpeech:
    def create(self, **kwargs):
        self.kwargs = kwargs
        return FakeSpeechResponse()


class FakeAudio:
    def __init__(self) -> None:
        self.transcriptions = FakeTranscriptions()
        self.speech = FakeSpeech()


class FakeClient:
    def __init__(self) -> None:
        self.audio = FakeAudio()


def build_adapter(tmp_path: Path, client: FakeClient | None = None) -> OpenAISpeechIOAdapter:
    return OpenAISpeechIOAdapter(
        client=client or FakeClient(),
        stt_model="stt-test",
        tts_model="tts-test",
        tts_voice="voice-test",
        output_dir=str(tmp_path),
    )


def test_openai_speech_adapter_transcribes_local_file(tmp_path: Path) -> None:
    audio = tmp_path / "input.wav"
    audio.write_bytes(b"wav")
    client = FakeClient()
    adapter = build_adapter(tmp_path, client)

    result = adapter.transcribe(SpeechToTextRequest(audio_ref=str(audio), language_hint="zh"))

    assert result.text == "你好小爱"
    assert result.provider == "openai"
    assert client.audio.transcriptions.kwargs["model"] == "stt-test"
    assert client.audio.transcriptions.kwargs["language"] == "zh"


def test_openai_speech_adapter_synthesizes_audio(tmp_path: Path) -> None:
    client = FakeClient()
    adapter = build_adapter(tmp_path, client)

    result = adapter.synthesize(TextToSpeechRequest(text="你好呀"))

    output = Path(result.audio_ref)
    assert output.read_bytes() == b"mp3-bytes"
    assert result.provider == "openai"
    assert client.audio.speech.kwargs["model"] == "tts-test"
    assert client.audio.speech.kwargs["voice"] == "voice-test"
    assert client.audio.speech.kwargs["input"] == "你好呀"


def test_openai_speech_adapter_rejects_missing_local_audio(tmp_path: Path) -> None:
    adapter = build_adapter(tmp_path)

    try:
        adapter.transcribe(SpeechToTextRequest(audio_ref=str(tmp_path / "missing.wav")))
    except RuntimeError as exc:
        assert str(exc) == "speech_to_text_audio_ref_not_local_file"
    else:
        raise AssertionError("expected missing local audio failure")


def test_openai_speech_adapter_rejects_empty_tts_input(tmp_path: Path) -> None:
    adapter = build_adapter(tmp_path)

    try:
        adapter.synthesize(TextToSpeechRequest(text="   "))
    except RuntimeError as exc:
        assert str(exc) == "text_to_speech_empty_input"
    else:
        raise AssertionError("expected empty TTS input failure")
