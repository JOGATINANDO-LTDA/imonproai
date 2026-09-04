import asyncio
import logging
import time
from dataclasses import dataclass, field

from app.agent.providers.base import BaseProvider, ModelInfo
from app.agent.providers.groq import GroqProvider
from app.agent.providers.kilo import KiloProvider
from app.agent.providers.lmstudio import LMStudioProvider
from app.agent.providers.opencode_go import OpenCodeGoProvider
from app.agent.providers.opencode_zen import OpencodeZenProvider
from app.agent.providers.openrouter import OpenRouterProvider
from app.agent.providers.registry import ProviderRegistry
from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


@dataclass
class ModelEntry:
    """Estado de um modelo gerenciado."""
    name: str
    provider_name: str
    loaded: bool = False
    instance_id: str | None = None
    last_used: float = 0.0
    ttl_seconds: int = 300
    load_time_seconds: float = 0.0


class ModelManager:
    """Gerencia ciclo de vida de modelos: listagem, load, unload, TTL."""

    _instance: "ModelManager | None" = None

    def __new__(cls) -> "ModelManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self._initialized = True
        self._registry = ProviderRegistry()
        self._models: dict[str, ModelEntry] = {}
        self._ttl_task: asyncio.Task | None = None
        self._setup_providers()

    def _setup_providers(self) -> None:
        """Registra providers disponíveis."""
        # 1. LMStudio (local, sem auth)
        lmstudio = LMStudioProvider(base_url=settings.LMSTUDIO_URL)
        self._registry.register(lmstudio)

        # 2. OpenRouter (26+ free, 50 req/dia)
        if settings.OPENROUTER_API_KEY:
            openrouter = OpenRouterProvider(api_key=settings.OPENROUTER_API_KEY)
            self._registry.register(openrouter)

        # 3. Kilo Gateway (8+ free, 200 req/hr)
        if settings.KILO_API_KEY:
            kilo = KiloProvider(api_key=settings.KILO_API_KEY)
            self._registry.register(kilo)

        # 4. Opencode Zen (7 free, pay-per-token)
        if settings.OPencode_ZEN_API_KEY:
            zen = OpencodeZenProvider(api_key=settings.OPencode_ZEN_API_KEY)
            self._registry.register(zen)

        # 5. Opencode Go ($10/mês, 25+ modelos)
        if settings.OPENCODE_GO_API_KEY:
            go = OpenCodeGoProvider(api_key=settings.OPENCODE_GO_API_KEY)
            self._registry.register(go)

        # 6. Groq (4 models, 2000 req/dia)
        if settings.GROQ_API_KEY:
            groq = GroqProvider(api_key=settings.GROQ_API_KEY)
            self._registry.register(groq)

    @property
    def registry(self) -> ProviderRegistry:
        return self._registry

    async def list_all_models(self) -> list[dict]:
        """Lista todos os modelos de todos os providers."""
        result = []
        for name in self._registry.available_providers:
            provider = self._registry.get(name)
            if provider is None:
                continue
            try:
                models = await provider.list_models()
                for m in models:
                    entry = self._models.get(f"{m.provider}:{m.name}")
                    result.append({
                        "name": m.name,
                        "provider": m.provider,
                        "loaded": entry.loaded if entry else m.loaded,
                        "instance_id": entry.instance_id if entry else m.instance_id,
                        "size_bytes": m.size_bytes,
                        "supports_load_unload": provider.supports_model_management,
                        "last_used": entry.last_used if entry else 0,
                        "ttl_remaining": self._ttl_remaining(entry) if entry and entry.loaded else None,
                    })
            except Exception as e:
                logger.warning(f"Erro ao listar modelos do provider {name}: {e}")
        return result

    async def load_model(self, model: str, provider_name: str | None = None, ttl: int | None = None) -> dict:
        """Carrega um modelo em um provider específico."""
        ttl = ttl or settings.MODEL_TTL_SECONDS

        if provider_name:
            provider = self._registry.get(provider_name)
            if provider is None:
                return {"status": "error", "error": f"Provider {provider_name} não encontrado"}
            if not provider.supports_model_management:
                return {"status": "error", "error": f"Provider {provider_name} não suporta load/unload"}
            return await self._do_load(provider, model, ttl)

        # Sem provider especificado: tentar todos que suportam load/unload
        for name in self._registry.available_providers:
            provider = self._registry.get(name)
            if provider and provider.supports_model_management:
                result = await self._do_load(provider, model, ttl)
                if result.get("status") == "loaded":
                    return result
        return {"status": "error", "error": f"Nenhum provider pôde carregar o modelo {model}"}

    async def _do_load(self, provider: BaseProvider, model: str, ttl: int) -> dict:
        """Executa o load em um provider e atualiza o estado."""
        key = f"{provider.name}:{model}"

        # 1. Verificar se já está no ModelManager
        existing = self._models.get(key)
        if existing and existing.loaded:
            existing.last_used = time.time()
            logger.info(f"Modelo {model} já está registrado como carregado, resetando TTL")
            return {"status": "already_loaded", "model": model, "instance_id": existing.instance_id}

        # 2. Verificar se já está carregado no provider (estado real)
        if provider.supports_model_management:
            try:
                is_loaded = await provider.is_model_loaded(model)
                if is_loaded:
                    # Registrar no ModelManager SEM chamar load_model novamente
                    models = await provider.list_models()
                    for m in models:
                        if m.name == model and m.loaded:
                            self._models[key] = ModelEntry(
                                name=model,
                                provider_name=provider.name,
                                loaded=True,
                                instance_id=m.instance_id,
                                last_used=time.time(),
                                ttl_seconds=ttl,
                            )
                            self._start_ttl_task()
                            logger.info(f"Modelo {model} já estava carregado no {provider.name}, registrado sem recarregar")
                            return {"status": "already_loaded", "model": model, "instance_id": m.instance_id}
            except Exception as e:
                logger.debug(f"Erro ao verificar modelo {model} no {provider.name}: {e}")

        # 3. Carregar o modelo
        result = await provider.load_model(model, ttl=ttl)

        if result.get("status") == "loaded":
            self._models[key] = ModelEntry(
                name=model,
                provider_name=provider.name,
                loaded=True,
                instance_id=result.get("instance_id"),
                last_used=time.time(),
                ttl_seconds=ttl,
                load_time_seconds=result.get("load_time_seconds", 0),
            )
            self._start_ttl_task()
        return result

    async def unload_model(self, model: str, provider_name: str | None = None) -> dict:
        """Descarrega um modelo."""
        key = f"{provider_name or 'lmstudio'}:{model}"
        entry = self._models.get(key)

        if not entry:
            return {"status": "error", "error": f"Modelo {model} não está registrado como carregado"}

        provider = self._registry.get(entry.provider_name)
        if provider is None:
            return {"status": "error", "error": f"Provider {entry.provider_name} não encontrado"}

        if not entry.instance_id:
            return {"status": "error", "error": "Modelo não tem instance_id registrado"}

        result = await provider.unload_model(entry.instance_id)
        if result.get("status") == "unloaded":
            del self._models[key]
        return result

    async def ensure_loaded(self, model: str, fallback_model: str | None = None) -> dict:
        """Garante que um modelo está carregado. Carrega se necessário. Usado pelo engine."""
        # 1. Verificar se já está no ModelManager
        for key, entry in self._models.items():
            if entry.name == model and entry.loaded:
                entry.last_used = time.time()
                return {"provider": entry.provider_name, "model": model, "status": "already_loaded"}

        # 2. Verificar se já está carregado no provider (estado real)
        for name in self._registry.available_providers:
            provider = self._registry.get(name)
            if provider and provider.supports_model_management:
                try:
                    is_loaded = await provider.is_model_loaded(model)
                    if is_loaded:
                        # Registrar no ModelManager sem recarregar
                        models = await provider.list_models()
                        for m in models:
                            if m.name == model and m.loaded:
                                key = f"{provider.name}:{model}"
                                self._models[key] = ModelEntry(
                                    name=model,
                                    provider_name=provider.name,
                                    loaded=True,
                                    instance_id=m.instance_id,
                                    last_used=time.time(),
                                    ttl_seconds=settings.MODEL_TTL_SECONDS,
                                )
                                self._start_ttl_task()
                                return {"provider": provider.name, "model": model, "status": "already_loaded"}
                except Exception:
                    pass

        # 3. Tentar carregar o modelo solicitado
        result = await self.load_model(model)
        if result.get("status") in ("loaded", "already_loaded"):
            return {"provider": result.get("provider", "unknown"), "model": model, "status": result["status"]}

        # 4. Fallback
        if fallback_model:
            result = await self.load_model(fallback_model)
            if result.get("status") in ("loaded", "already_loaded"):
                return {"provider": result.get("provider", "unknown"), "model": fallback_model, "status": f"loaded_fallback"}

        # 5. Fallback para primeiro provider disponível
        for name in self._registry.available_providers:
            provider = self._registry.get(name)
            if provider and provider.supports_model_management:
                models = await provider.list_models()
                if models:
                    first_model = models[0].name
                    result = await self.load_model(first_model, provider_name=name)
                    if result.get("status") in ("loaded", "already_loaded"):
                        return {"provider": name, "model": first_model, "status": "loaded_fallback"}

        return {"provider": None, "model": model, "status": "error", "error": "Não foi possível carregar nenhum modelo"}

    def touch(self, model: str) -> None:
        """Atualiza o timestamp de último uso (reseta TTL)."""
        for entry in self._models.values():
            if entry.name == model and entry.loaded:
                entry.last_used = time.time()

    def get_provider_for_model(self, model: str) -> BaseProvider | None:
        """Retorna o provider que possui o modelo carregado."""
        for entry in self._models.values():
            if entry.name == model and entry.loaded:
                return self._registry.get(entry.provider_name)
        return None

    def get_model_status(self, model: str) -> dict | None:
        """Retorna status de um modelo específico."""
        for key, entry in self._models.items():
            if entry.name == model:
                return {
                    "name": entry.name,
                    "provider": entry.provider_name,
                    "loaded": entry.loaded,
                    "instance_id": entry.instance_id,
                    "last_used": entry.last_used,
                    "ttl_remaining": self._ttl_remaining(entry),
                }
        return None

    def _ttl_remaining(self, entry: ModelEntry | None) -> int | None:
        """Calcula o TTL restante em segundos."""
        if not entry or not entry.loaded:
            return None
        elapsed = time.time() - entry.last_used
        remaining = int(entry.ttl_seconds - elapsed)
        return max(0, remaining)

    def _start_ttl_task(self) -> None:
        """Inicia a task de verificação de TTL se não estiver rodando."""
        if self._ttl_task is None or self._ttl_task.done():
            self._ttl_task = asyncio.create_task(self._ttl_checker())

    async def _ttl_checker(self) -> None:
        """Verifica periodicamente modelos expirados e descarrega."""
        while True:
            try:
                await asyncio.sleep(30)  # Verifica a cada 30s
                now = time.time()
                expired = []

                for key, entry in self._models.items():
                    if entry.loaded:
                        elapsed = now - entry.last_used
                        if elapsed >= entry.ttl_seconds:
                            expired.append((key, entry))

                for key, entry in expired:
                    logger.info(f"TTL expirado para {entry.name} ({entry.provider_name}), descarregando...")
                    await self.unload_model(entry.name, entry.provider_name)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Erro no TTL checker: {e}")
                await asyncio.sleep(10)
