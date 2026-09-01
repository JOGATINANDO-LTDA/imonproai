# ADR-001: Arquitetura Multi-Provider Agnóstica

## Status: Aceito
## Data: 2026-09-01
## Decisor: Equipe ImobPro.ai

## Contexto

O ImobPro.ai precisa de IA para:
- Conversação com leads (chat)
- Processamento de documentos (RAG)
- Geração de áudio (TTS)
- Transcrição de áudio (STT)

O mercado de IA muda rapidamente. Ficar preso a um provider é risco estratégico.

## Decisão

Implementar um **Provider Registry** agnóstico que suporta:
- **Local**: LMStudio (qwen3.5-9b-deepseek-v4-flash, gemma-4-e4b)
- **Gratuito cloud**: Opencode ZEN (modelos free), Groq, Together AI
- **Pago cloud**: Opencode ZEN (pay-as-you-go), Opencode GO ($10/mês), OpenAI (BYOK)
- **Fallback chain**: local → gratuito → pago

## Justificativa

### Por que agnóstico?

1. **Custo**: Local = $0. Gratuito = $0. Só paga se necessário.
2. **Resiliência**: Se um provider cai, fallback automático.
3. **Escalabilidade**: Cada tenant pode usar provider diferente.
4. **Privacidade**: Dados sensíveis ficam no local.

### Por que não usar apenas OpenAI?

- Custo: $2.50-15/1M tokens vs $0 (local/gratuito)
- Lock-in: Mudar de provider requer reescrever código
- Privacidade: Dados vão para EUA (LGPD)

### Por que não usar apenas LMStudio?

- Limitação de hardware local
- Sem fallback se o servidor cair
- Qualidade inferior para tarefas complexas

## Alternativas Consideradas

| Alternativa | Prós | Contras | Decisão |
|------------|------|---------|---------|
| OpenAI only | Simples | Caro, lock-in | Rejeitado |
| LMStudio only | Gratuito, privado | Limitado, sem fallback | Rejeitado |
| OpenRouter | Multi-provider | Sem suporte local | Rejeitado |
| **Multi-provider** | **Flexível, resiliente** | **Mais complexo** | **Aceito** |

## Consequências

- Implementação mais complexa (Registry pattern)
- Necessidade de testes por provider
- Monitoramento de custo por provider
- Fallback chain precisa de testes de integração

## Referências

- AI SDK: https://ai-sdk.dev/
- OpenCode ZEN: https://opencode.ai/docs/pt-br/zen/
- OpenCode GO: https://opencode.ai/docs/pt-br/go/
- LMStudio: https://lmstudio.ai/
