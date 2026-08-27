from runtime.speech_io_adapter import SpeechToTextRequest, SpeechToTextResult, TextToSpeechRequest, TextToSpeechResult
from runtime.voice_shadow_runner import XiaoAiVoiceShadowRunner


class StubSTT:
    provider_name = "stub-stt"

    def transcribe(self, request: SpeechToTextRequest) -> SpeechToTextResult:
        return SpeechToTextResult(text="小爱上线", provider=self.provider_name, confidence=1.0)


class StubTTS:
    provider_name = "stub-tts"

    def synthesize(self, request: TextToSpeechRequest) -> TextToSpeechResult:
        return TextToSpeechResult(audio_ref="audio://shadow", provider=self.provider_name)


def test_shadow_runner_collects_candidate_evidence_only() -> None:
    calls = []

    def candidate_runtime(message: str, session_key: str) -> str:
        calls.append((message, session_key))
        return "候选回复"

    runner = XiaoAiVoiceShadowRunner(stt=StubSTT(), tts=StubTTS(), candidate_runtime=candidate_runtime)
    result = runner.run(audio_ref="audio://input", session_key="session-1")

    assert calls == [("小爱上线", "session-1")]
    assert result.transcript == "小爱上线"
    assert result.candidate_reply == "候选回复"
    assert result.candidate_audio_ref == "audio://shadow"
