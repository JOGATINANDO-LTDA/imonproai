import logging
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)


class TTSEngine:
    """Engine de Text-to-Speech."""

    def __init__(self, provider: str = "edge", voice_id: str = "pt-BR-FranciscaNeural"):
        self.provider = provider
        self.voice_id = voice_id

    async def synthesize(self, text: str) -> bytes:
        if self.provider == "edge":
            return await self._edge_tts(text)
        raise ValueError(f"Provider TTS não suportado: {self.provider}")

    async def _edge_tts(self, text: str) -> bytes:
        try:
            import edge_tts

            communicate = edge_tts.Communicate(text, self.voice_id)
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                await communicate.save(f.name)
                audio_bytes = Path(f.name).read_bytes()
                Path(f.name).unlink()
                return audio_bytes
        except ImportError:
            logger.warning("edge-tts não instalado")
            return b""
