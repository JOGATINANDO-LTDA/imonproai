# Together AI — Provider Gratuito de Modelos Open-Source

## Visão Geral

Together AI oferece inferência de modelos open-source com tier gratuito.

## Configuração

### Endpoint

```
Base URL: https://api.together.xyz/v1/
Formato: OpenAI-compatible
```

### Variáveis de Ambiente

```bash
TOGETHER_API_KEY=sua-chave-aqui
```

## Modelos Disponíveis (Gratuito)

| Modelo | ID | Notas |
|--------|-----|-------|
| Llama 3.3 70B | meta-llama/Llama-3.3-70B-Instruct-Turbo | Raciocínio |
| Mixtral 8x22B | mistralai/Mixtral-8x22B-Instruct-v0.1 | Multi-idioma |
| DeepSeek V3 | deepseek-ai/DeepSeek-V3 | Código |

## Integração Python

```python
from langchain_together import ChatTogether

llm = ChatTogether(
    together_api_key="sua-chave",
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo"
)
```

## Custos

| Tier | Créditos | Modelos |
|------|---------|---------|
| Gratuito | $1.00 | Todos |
| Pago | Pay-as-you-go | Todos |

## Quando Usar

- Fallback secundário
- Modelos específicos não disponíveis em outros providers
- Testes de modelos open-source

## Referências

- Together AI: https://api.together.xyz/
- Docs: https://docs.together.ai/
