# Opencode ZEN — Provider Gratuito + Pay-as-you-go

## Visão Geral

O Opencode ZEN é um gateway de modelos que suporta:
- Modelos gratuitos (período limitado ou ilimitado)
- Pay-as-you-go para modelos premium
- API OpenAI-compatible

## Configuração

### Endpoint

```
Base URL: https://opencode.ai/zen/v1/
Formato: OpenAI-compatible
```

### Variáveis de Ambiente

```bash
OPENCODE_ZEN_API_KEY=sua-chave-aqui
```

## Modelos Gratuitos

| Modelo | ID | Tipo | Notas |
|--------|-----|------|-------|
| MiMo-V2.5 Free | mimo-v2.5-free | Raciocínio | Período limitado |
| Big Pickle | big-pickle | Stealth | Modelo oculto |
| Nemotron 3 Ultra Free | nemotron-3-ultra-free | NVIDIA | Geral |
| Nemotron 3.5 Lightning Free | nemotron-3.5-lightning-free | NVIDIA | Rápido |
| Ling 3.0 Flash Fin Free | ling-3.0-flash-fin-free | Finance | Período limitado |
| Muse Spark 1.2 Contributor Free | muse-spark-1.2-contributor-free | Meta | Período limitado |

## Integração Python

```python
import httpx

class OpencodeZenProvider:
    def __init__(self, api_key: str):
        self.base_url = "https://opencode.ai/zen/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    async def chat(self, messages: list, model: str = "deepseek-v4-flash"):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json={
                    "model": model,
                    "messages": messages,
                    "temperature": 0.7
                }
            )
            return response.json()

    async def embed(self, text: str, model: str = "text-embedding-3-small"):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/embeddings",
                headers=self.headers,
                json={
                    "model": model,
                    "input": text
                }
            )
            return response.json()["data"][0]["embedding"]
```

## Integração LangChain

```python
from langchain_openai import ChatOpenAI

# ZEN com modelo OpenAI
llm = ChatOpenAI(
    base_url="https://opencode.ai/zen/v1",
    api_key="sua-chave",
    model="deepseek-v4-flash"
)

# ZEN com modelo Anthropic
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(
    base_url="https://opencode.ai/zen/v1",
    api_key="sua-chave",
    model="claude-3-5-sonnet"
)
```

## Custos

| Modelo | Custo | Notas |
|--------|-------|-------|
| Modelos Free | $0 | Período limitado |
| DeepSeek V4 | ~$0.14/1M tokens | Input |
| GPT-4o | ~$2.50/1M tokens | Input |
| Claude 3.5 | ~$3.00/1M tokens | Input |

## Limitações

- Modelos free podem ser descontinuados sem aviso
- Rate limits por modelo
- Alguns modelos são "stealth" (não documentados)

## Referências

- Documentação: https://opencode.ai/docs/pt-br/zen/
- ADR: ../decisions/006-opencode-zen-go.md
