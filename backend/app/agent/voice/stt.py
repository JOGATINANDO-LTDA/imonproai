import logging

logger = logging.getLogger(__name__)


class STTEngine:
    """Engine de Speech-to-Text."""

    def __init__(self, provider: str = "faster-whisper", model: str = "large-v3"):
        self.provider = provider
        self.model = model

    async def transcribe(self, audio_bytes: bytes) -> str:
        if self.provider == "faster-whisper":
            return await self._faster_whisper(audio_bytes)
        raise ValueError(f"Provider STT não suportado: {self.provider}")

    async def _faster_whisper(self, audio_bytes: bytes) -> str:
        try:
            from faster_whisper import WhisperModel

            model = WhisperModel(self.model, device="cpu", compute_type="int8")
            segments, _ = model.transcribe(audio_bytes, language="pt")
            return " ".join([s.text for s in segments])
        except ImportError:
            logger.warning("faster-whisper não instalado")
            return ""
