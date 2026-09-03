import logging

from fastapi import APIRouter
from pydantic import BaseModel

from app.agent.model_manager import ModelManager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/models", tags=["Models"])

model_manager = ModelManager()


class LoadModelRequest(BaseModel):
    model: str
    provider: str | None = None
    ttl: int | None = None


class UnloadModelRequest(BaseModel):
    model: str
    provider: str | None = None


@router.get("")
async def list_models():
    """Lista todos os modelos disponíveis em todos os providers."""
    models = await model_manager.list_all_models()
    providers = model_manager.registry.available_providers

    # Encontrar modelo ativo (primeiro carregado)
    active = None
    for m in models:
        if m.get("loaded"):
            active = m
            break

    return {
        "models": models,
        "providers": providers,
        "active_model": active,
    }


@router.post("/load")
async def load_model(req: LoadModelRequest):
    """Carrega um modelo na memória."""
    result = await model_manager.load_model(
        model=req.model,
        provider_name=req.provider,
        ttl=req.ttl,
    )
    return result


@router.post("/unload")
async def unload_model(req: UnloadModelRequest):
    """Descarrega um modelo da memória."""
    result = await model_manager.unload_model(
        model=req.model,
        provider_name=req.provider,
    )
    return result


@router.get("/status")
async def model_status():
    """Status de todos os modelos gerenciados."""
    models = await model_manager.list_all_models()
    loaded = [m for m in models if m.get("loaded")]
    return {
        "total": len(models),
        "loaded": len(loaded),
        "models": models,
    }
