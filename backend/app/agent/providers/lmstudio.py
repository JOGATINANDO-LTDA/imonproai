import logging

import httpx

from app.agent.providers.base import BaseProvider, ModelInfo

logger = logging.getLogger(__name__)


class LMStudioProvider(BaseProvider):
    """Provider local via LMStudio com gerenciamento de modelos."""

    def __init__(self, base_url: str = "http://localhost:1234"):
        self.base_url = base_url.rstrip("/")
        self._api_base = f"{self.base_url}/api/v1"

    @property
    def name(self) -> str:
        return "lmstudio"

    @property
    def is_available(self) -> bool:
        try:
            response = httpx.get(f"{self._api_base}/models", timeout=3.0)
            return response.status_code == 200
        except Exception:
            return False

    @property
    def supports_model_management(self) -> bool:
        return True

    async def list_models(self) -> list[ModelInfo]:
        """Lista todos os modelos disponíveis no LMStudio via API nativa."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self._api_base}/models", timeout=5.0)
                response.raise_for_status()
                data = response.json()

            models = []
            for m in data.get("models", []):
                key = m.get("key", "")
                loaded_instances = m.get("loaded_instances", [])
                is_loaded = len(loaded_instances) > 0
                instance_id = loaded_instances[0].get("id") if loaded_instances else None

                models.append(ModelInfo(
                    name=key,
                    loaded=is_loaded,
                    size_bytes=m.get("size_bytes"),
                    provider=self.name,
                    instance_id=instance_id,
                ))
            return models
        except Exception as e:
            logger.error(f"Erro ao listar modelos LMStudio: {e}")
            return []

    async def load_model(self, model: str, ttl: int = 300, **kwargs) -> dict:
        """Carrega um modelo no LMStudio. TTL é gerenciado pelo ModelManager."""
        try:
            async with httpx.AsyncClient() as client:
                payload = {"model": model}
                response = await client.post(
                    f"{self._api_base}/models/load",
                    json=payload,
                    timeout=60.0,
                )
                response.raise_for_status()
                result = response.json()
                logger.info(f"Modelo {model} carregado no LMStudio: {result}")
                return {
                    "status": "loaded",
                    "model": model,
                    "instance_id": result.get("instance_id"),
                    "load_time_seconds": result.get("load_time_seconds"),
                }
        except httpx.HTTPStatusError as e:
            error_body = e.response.text
            logger.error(f"Erro HTTP ao carregar modelo {model}: {error_body}")
            return {"status": "error", "error": error_body}
        except Exception as e:
            logger.error(f"Erro ao carregar modelo {model}: {e}")
            return {"status": "error", "error": str(e)}

    async def unload_model(self, instance_id: str) -> dict:
        """Descarrega um modelo do LMStudio."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self._api_base}/models/unload",
                    json={"instance_id": instance_id},
                    timeout=30.0,
                )
                response.raise_for_status()
                result = response.json()
                logger.info(f"Modelo descarregado do LMStudio: {result}")
                return {"status": "unloaded", "instance_id": result.get("instance_id")}
        except Exception as e:
            logger.error(f"Erro ao descarregar modelo {instance_id}: {e}")
            return {"status": "error", "error": str(e)}

    async def is_model_loaded(self, model: str) -> bool:
        """Verifica se um modelo está carregado no LMStudio."""
        try:
            models = await self.list_models()
            for m in models:
                if m.name == model and m.loaded:
                    return True
            return False
        except Exception:
            return False

    async def chat(self, messages: list[dict], model: str | None = None) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/v1/chat/completions",
                json={
                    "model": model or "qwen3.5-9b-deepseek-v4-flash",
                    "messages": messages,
                    "temperature": 0.7,
                },
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()

    async def embed(self, text: str) -> list[float]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/v1/embeddings",
                json={
                    "model": "nomic-embed-text-v1.5",
                    "input": text,
                },
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()["data"][0]["embedding"]
