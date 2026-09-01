# ADR-006: Integração Opencode ZEN e GO como Providers

## Status: Aceito
## Data: 2026-09-01
## Decisor: Equipe ImobPro.ai

## Contexto

O ImobPro.ai precisa de providers cloud que sejam:
1. Compatíveis com AI SDK (Vercel)
2. Com modelos gratuitos para MVP
3. Com opção de escalar para pago sem mudar código

## Decisão

Integrar Opencode ZEN (pay-as-you-go) e GO ($10/mês) como providers primários cloud.

## Especificações Técnicas

### ZEN (Pay-as-you-go)

- Endpoint: `https://opencode.ai/zen/v1/`
- Formato: OpenAI-compatible
- Pacote AI SDK: `@ai-sdk/openai` (GPT/Grok), `@ai-sdk/anthropic` (Claude), `@ai-sdk/google` (Gemini)

### Modelos Gratuitos ZEN

| Modelo | ID | Notas |
|--------|-----|-------|
| MiMo-V2.5 Free | mimo-v2.5-free | Período limitado |
| Big Pickle | big-pickle | Stealth model |
| Nemotron 3 Ultra Free | nemotron-3-ultra-free | NVIDIA |
| Nemotron 3.5 Lightning Free | nemotron-3.5-lightning-free | NVIDIA |
| Ling 3.0 Flash Fin Free | ling-3.0-flash-fin-free | Período limitado |
| Muse Spark 1.2 Contributor Free | muse-spark-1.2-contributor-free | Meta |

### GO ($10/mês)

- Endpoint: `https://opencode.ai/zen/go/v1/`
- Limite mensal: $60 de uso
- Modelos incluídos: Grok 4.6, GPT 5.6 Luna, DeepSeek V4, Qwen3.x, Kimi K3

### Integração com AI SDK (Python)

```python
import httpx

class OpencodeZEN:
    def __init__(self, api_key: str):
        self.base_url = "https://opencode.ai/zen/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    async def chat(self, messages, model="deepseek-v4-flash"):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json={"model": model, "messages": messages}
            )
            return response.json()
```

## Custos Estimados (MVP)

| Provider | Custo mensal | Uso estimado |
|----------|-------------|--------------|
| LMStudio (local) | $0 | 80% das requests |
| ZEN Free models | $0 | 15% das requests |
| ZEN pay-as-you-go | ~$5-20 | 5% das requests |
| **Total** | **~$5-20** | |

## Consequências

- API key management por provider
- Fallback chain precisa testar cada provider
- Monitoramento de uso por provider
- BYOK necessário para clientes com preferência

## Referências

- Opencode ZEN: https://opencode.ai/docs/pt-br/zen/
- Opencode GO: https://opencode.ai/docs/pt-br/go/
- AI SDK: https://ai-sdk.dev/
