from runtime.speech_io_adapter import (
    SpeechToTextRequest,
    SpeechToTextResult,
    TextToSpeechRequest,
    TextToSpeechResult,
)
from runtime.voice_io_pipeline import VoicePipelineInput, XiaoAiVoiceIOPipeline


class StubSTT:
    provider_name = "stub-stt"

    def __init__(self, text: str = "你好小爱") -> None:
        self.text = text

    def transcribe(self, request: SpeechToTextRequest) -> SpeechToTextResult:
        return SpeechToTextResult(text=self.text, provider=self.provider_name, confidence=1.0)


class StubTTS:
    provider_name = "stub-tts"

    def __init__(self, audio_ref: str = "audio://reply") -> None:
        self.audio_ref = audio_ref
        self.last_text = ""

    def synthesize(self, request: TextToSpeechRequest) -> TextToSpeechResult:
        self.last_text = request.text
        return TextToSpeechResult(audio_ref=self.audio_ref, provider=self.provider_name)


class StubDaughterChat:
    def __init__(self, reply: str = "你好呀") -> None:
        self.reply = reply
        self.last_message = ""
        self.last_session_key = ""

    def send_message(self, *, message: str, session_key: str) -> str:
        self.last_message = message
        self.last_session_key = session_key
        return self.reply


def test_voice_pipeline_uses_same_daughter_chat_runtime() -> None:
    stt = StubSTT("小爱上线")
    tts = StubTTS()
    daughter_chat = StubDaughterChat("小爱上线啦")
    pipeline = XiaoAiVoiceIOPipeline(stt=stt, tts=tts, daughter_chat=daughter_chat)

    result = pipeline.handle(VoicePipelineInput(audio_ref="audio://input", session_key="session-1"))

    assert daughter_chat.last_message == "小爱上线"
    assert daughter_chat.last_session_key == "session-1"
    assert tts.last_text == "小爱上线啦"
    assert result.transcript == "小爱上线"
    assert result.reply_text == "小爱上线啦"
    assert result.audio_ref == "audio://reply"


def test_voice_pipeline_rejects_empty_transcript() -> None:
    pipeline = XiaoAiVoiceIOPipeline(stt=StubSTT("   "), tts=StubTTS(), daughter_chat=StubDaughterChat())

    try:
        pipeline.handle(VoicePipelineInput(audio_ref="audio://input", session_key="session-1"))
    except RuntimeError as exc:
        assert str(exc) == "speech_to_text_empty_transcript"
    else:
        raise AssertionError("expected empty transcript failure")


def test_voice_pipeline_rejects_empty_backend_reply() -> None:
    pipeline = XiaoAiVoiceIOPipeline(stt=StubSTT(), tts=StubTTS(), daughter_chat=StubDaughterChat(""))

    try:
        pipeline.handle(VoicePipelineInput(audio_ref="audio://input", session_key="session-1"))
    except RuntimeError as exc:
        assert str(exc) == "daughter_chat_empty_reply"
    else:
        raise AssertionError("expected empty backend reply failure")


def test_voice_pipeline_rejects_missing_tts_audio() -> None:
    pipeline = XiaoAiVoiceIOPipeline(stt=StubSTT(), tts=StubTTS(""), daughter_chat=StubDaughterChat())

    try:
        pipeline.handle(VoicePipelineInput(audio_ref="audio://input", session_key="session-1"))
    except RuntimeError as exc:
        assert str(exc) == "text_to_speech_missing_audio"
    else:
        raise AssertionError("expected missing TTS audio failure")
