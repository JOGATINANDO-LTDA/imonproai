# Providers de IA — ImobPro.ai

## Visão Geral

O ImobPro.ai suporta múltiplos providers de IA via **Provider Registry**. Cada provider é uma implementação padronizada que pode ser trocada sem alterar o código do agente.

## Providers Disponíveis

### Local (Gratuito)

| Provider | Modelo | Uso | Latência |
|----------|--------|-----|----------|
| LMStudio | qwen3.5-9b-deepseek-v4-flash | Raciocínio, código | ~2s |
| LMStudio | google/gemma-4-e4b | Respostas rápidas | ~1s |

### Cloud Gratuito

| Provider | Modelo | Limite | Uso |
|----------|--------|--------|-----|
| Opencode ZEN | MiMo-V2.5 Free | Período limitado | Raciocínio |
| Opencode ZEN | Nemotron 3 Ultra Free | Ilimitado | Geral |
| Opencode ZEN | Nemotron 3.5 Lightning Free | Ilimitado | Rápido |
| Groq | llama-3.3-70b | 14,400 req/dia | Raciocínio |
| Together AI | Llama 3.3 70B | Créditos grátis | Geral |

### Cloud Pago

| Provider | Modelo | Custo | Uso |
|----------|--------|-------|-----|
| Opencode ZEN | DeepSeek V4 | Pay-as-you-go | Raciocínio |
| Opencode GO | Grok 4.6 | $10/mês | Premium |
| OpenAI | GPT-4o | BYOK | Premium |

## Arquitetura do Registry

```python
# backend/app/agent/providers/base.py
from abc import ABC, abstractmethod

class BaseProvider(ABC):
    @abstractmethod
    async def chat(self, messages: list, model: str) -> dict:
        pass

    @abstractmethod
    async def embed(self, text: str) -> list[float]:
        pass

# backend/app/agent/providers/registry.py
class ProviderRegistry:
    def __init__(self):
        self.providers = {}

    def register(self, name: str, provider: BaseProvider):
        self.providers[name] = provider

    async def chat(self, messages, model=None, provider=None):
        if provider:
            return await self.providers[provider].chat(messages, model)
        # Fallback chain
        for name, p in self.providers.items():
            try:
                return await p.chat(messages, model)
            except Exception:
                continue
        raise Exception("Todos os providers falharam")
```

## Fallback Chain

```
1. LMStudio (local) → Se disponível
2. Opencode ZEN Free → Se modelo free
3. Groq → Se disponível
4. Opencode ZEN Pago → Se disponível
5. OpenAI BYOK → Último recurso
```

## Seleção por Tenant

Cada imobiliária pode configurar seu provider:

```yaml
# Configuração do tenant
ai_provider:
  primary: "opencode-zen"
  fallback: "lmstudio"
  model: "deepseek-v4-flash"
  api_key: "sk-..."  # BYOK
```

## Referências

- [ADR-001: Multi-Provider](../decisions/001-multi-provider-ai.md)
- [ADR-006: Opencode ZEN/GO](../decisions/006-opencode-zen-go.md)
- [ADR-007: LMStudio](../decisions/007-lmstudio-local.md)
