from app.agent.voice.tts import TTSEngine
from app.agent.voice.stt import STTEngine


def test_tts_engine_init():
    tts = TTSEngine(provider="edge", voice_id="pt-BR-FranciscaNeural")
    assert tts.provider == "edge"
    assert tts.voice_id == "pt-BR-FranciscaNeural"


def test_stt_engine_init():
    stt = STTEngine(provider="faster-whisper", model="large-v3")
    assert stt.provider == "faster-whisper"
    assert stt.model == "large-v3"
