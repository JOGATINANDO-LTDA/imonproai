import hashlib
import hmac
import logging
from typing import Any

import httpx

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class WhatsAppService:
    """Serviço de integração WhatsApp via Evolution API."""

    def __init__(self):
        self.base_url = settings.EVOLUTION_API_URL
        self.api_key = settings.EVOLUTION_API_KEY
        self.headers = {"apikey": self.api_key, "Content-Type": "application/json"}

    async def send_text(self, instance: str, to: str, message: str) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/message/sendText/{instance}",
                json={"number": to, "text": message},
                headers=self.headers,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()

    async def send_image(self, instance: str, to: str, image_url: str, caption: str = "") -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/message/sendImage/{instance}",
                json={"number": to, "image": image_url, "caption": caption},
                headers=self.headers,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()

    async def send_audio(self, instance: str, to: str, audio_url: str) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/message/sendAudio/{instance}",
                json={"number": to, "audio": audio_url},
                headers=self.headers,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()

    async def send_document(
        self, instance: str, to: str, document_url: str, filename: str = ""
    ) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/message/sendDocument/{instance}",
                json={"number": to, "document": document_url, "fileName": filename},
                headers=self.headers,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()

    async def get_instance_info(self, instance: str) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/instance/connectionState/{instance}",
                headers=self.headers,
                timeout=15,
            )
            response.raise_for_status()
            return response.json()

    def verify_webhook_signature(self, body: bytes, signature: str) -> bool:
        if not settings.EVOLUTION_API_KEY:
            return True
        expected = hmac.new(settings.EVOLUTION_API_KEY.encode(), body, hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, signature)
