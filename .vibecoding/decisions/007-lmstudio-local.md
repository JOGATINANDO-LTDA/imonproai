# ADR-007: LMStudio como Provider Local Padrão

## Status: Aceito
## Data: 2026-09-01
## Decisor: Equipe ImobPro.ai

## Contexto

O ImobPro.ai precisa de um provider local para:
- Desenvolvimento sem custo
- Privacidade de dados
- Funcionamento offline
- MVP sem dependência de cloud

## Decisão

Usar **LMStudio** como provider local padrão, com modelos:
- `qwen3.5-9b-deepseek-v4-flash` — Principal (razão/código)
- `google/gemma-4-e4b` — Alternativo (leve, rápido)

## Justificativa

### Por que LMStudio?

1. **Interface gráfica**: Fácil de gerenciar modelos
2. **OpenAI-compatible**: Mesmo formato de API
3. **Local**: Dados nunca saem do computador
4. **Gratuito**: Sem limite de requests
5. **Suporte a GGUF**: Formato otimizado para CPU/GPU

### Configuração

```python
# LMStudio - OpenAI compatible
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
    model="qwen3.5-9b-deepseek-v4-flash"
)
```

### Modelos Instalados

| Modelo | Parâmetros | Uso | RAM |
|--------|-----------|-----|-----|
| qwen3.5-9b-deepseek-v4-flash | 9B | Raciocínio, código | ~6GB |
| google/gemma-4-e4b | 4B | Respostas rápidas | ~3GB |

## Alternativas Consideradas

| Alternativa | Prós | Contras | Decisão |
|------------|------|---------|---------|
| Ollama | CLI, scripts | Sem GUI, menos features | Rejeitado |
| LM Studio | GUI, completo | Desktop only | Aceito |
| vLLM | Performance | Complexo, GPU obrigatória | Rejeitado |

## Referências

- LMStudio: https://lmstudio.ai/
- Modelos GGUF: https://huggingface.co/models?library=gguf
