# LMStudio — Provider Local

## Visão Geral

O LMStudio é um servidor local de IA que oferece:
- Interface gráfica para gerenciar modelos
- API OpenAI-compatible
- Execução local (sem dados na nuvem)
- Suporte a modelos GGUF

## Configuração

### Endpoint

```
Base URL: http://localhost:1234/v1/
Formato: OpenAI-compatible
API Key: lm-studio (qualquer valor)
```

### Variáveis de Ambiente

```bash
LMSTUDIO_BASE_URL=http://localhost:1234/v1
LMSTUDIO_API_KEY=lm-studio
```

## Modelos Instalados

| Modelo | Parâmetros | RAM | Uso |
|--------|-----------|-----|-----|
| qwen3.5-9b-deepseek-v4-flash | 9B | ~6GB | Raciocínio, código |
| google/gemma-4-e4b | 4B | ~3GB | Respostas rápidas |

## Integração Python

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
    model="qwen3.5-9b-deepseek-v4-flash"
)
```

## Integração Direta (httpx)

```python
import httpx

async def chat_lmstudio(messages: list, model: str = "qwen3.5-9b-deepseek-v4-flash"):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:1234/v1/chat/completions",
            json={
                "model": model,
                "messages": messages,
                "temperature": 0.7
            }
        )
        return response.json()
```

## Performance

| Modelo | Tokens/s (CPU) | Tokens/s (GPU) |
|--------|---------------|----------------|
| qwen3.5-9b | ~10 | ~30 |
| gemma-4-e4b | ~20 | ~50 |

## Quando Usar

- Desenvolvimento local
- Testes sem custo
- Privacidade de dados
- MVP sem dependência de cloud

## Limitações

- Requer servidor local ligado
- Performance limitada por hardware
- Sem fallback se o servidor cair
- Modelos limitados por RAM

## Referências

- LMStudio: https://lmstudio.ai/
- ADR: ../decisions/007-lmstudio-local.md
