# Groq — Provider Gratuito de Alta Velocidade

## Visão Geral

Groq oferece inferência de IA com latência ultra-baixa via hardware customizado (LPU). Planos gratuitos disponíveis.

## Configuração

### Endpoint

```
Base URL: https://api.groq.com/openai/v1/
Formato: OpenAI-compatible
```

### Variáveis de Ambiente

```bash
GROQ_API_KEY=gsk_sua-chave-aqui
```

## Modelos Disponíveis (Gratuito)

| Modelo | ID | Limite |
|--------|-----|--------|
| Llama 3.3 70B | llama-3.3-70b-versatile | 14,400 req/dia |
| Llama 3.1 8B | llama-3.1-8b-instant | 14,400 req/dia |
| Gemma 2 9B | gemma2-9b-it | 14,400 req/dia |
| Mixtral 8x7B | mixtral-8x7b-32768 | 14,400 req/dia |

## Integração Python

```python
from langchain_groq import ChatGroq

llm = ChatGroq(
    groq_api_key="gsk_sua-chave",
    model_name="llama-3.3-70b-versatile"
)
```

## Performance

| Modelo | Latência | Tokens/s |
|--------|----------|----------|
| Llama 3.3 70B | ~200ms | ~100 |
| Llama 3.1 8B | ~100ms | ~200 |

## Custos

| Tier | Preço | Limite |
|------|-------|--------|
| Gratuito | $0 | 14,400 req/dia |
| Pro | $0.59/1M tokens | Ilimitado |

## Quando Usar

- Fallback quando LMStudio não está disponível
- Respostas rápidas em produção
- Modelos open-source de alta qualidade

## Referências

- Groq: https://console.groq.com/
- Docs: https://console.groq.com/docs
