# Opencode GO — Provider por Assinatura

## Visão Geral

O Opencode GO é um plano de assinatura que oferece:
- $10/mês
- $60 de limite mensal de uso
- Modelos premium inclusos
- API OpenAI-compatible

## Configuração

### Endpoint

```
Base URL: https://opencode.ai/zen/go/v1/
Formato: OpenAI-compatible
```

### Variáveis de Ambiente

```bash
OPENCODE_GO_API_KEY=sua-chave-aqui
```

## Modelos Inclusos

| Modelo | ID | Tipo | Notas |
|--------|-----|------|-------|
| Grok 4.6 | grok-4.6 | xAI | Premium |
| GPT 5.6 Luna | gpt-5.6-luna | OpenAI | Premium |
| DeepSeek V4 | deepseek-v4 | DeepSeek | Raciocínio |
| Qwen3.x | qwen3.x | Alibaba | Multi-idioma |
| Kimi K3 | kimi-k3 | Moonshot | Long context |

## Integração Python

```python
import httpx

class OpencodeGoProvider:
    def __init__(self, api_key: str):
        self.base_url = "https://opencode.ai/zen/go/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    async def chat(self, messages: list, model: str = "gpt-5.6-luna"):
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
```

## Integração LangChain

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url="https://opencode.ai/zen/go/v1",
    api_key="sua-chave-go",
    model="gpt-5.6-luna"
)
```

## Custos

| Item | Valor |
|------|-------|
| Assinatura | $10/mês |
| Limite mensal | $60 |
| Modelo mais barato | ~$0.14/1M tokens |
| Modelo mais caro | ~$15/1M tokens |

## Cálculo de Uso

```
Exemplo: 1000 requests/dia × 2000 tokens × 30 dias
= 60M tokens/mês
≈ $6-12 (dependendo do modelo)
= dentro do limite de $60
```

## Quando Usar GO

- Produção com tráfego moderado
- Quando ZEN free não é suficiente
- Para modelos premium (Grok, GPT-5.6)
- Para fallback quando otros providers falham

## Referências

- Documentação: https://opencode.ai/docs/pt-br/go/
- ADR: ../decisions/006-opencode-zen-go.md
