# ADR-004: Stack de TTS — Prioridade Edge → Coqui → Piper

## Status: Aceito
## Data: 2026-09-01
## Decisor: Equipe ImobPro.ai

## Contexto

O agente comercial precisa falar com leads por telefone. A voz precisa ser:
1. Natural (expressões, entonação)
2. Em PT-BR
3. Baixa latência
4. Custo zero ou mínimo

## Decisão

Hierarquia de TTS:

### Prioridade 1: Edge TTS (Microsoft) — GRATUITO

- **Por que**: Vozes neurais Microsoft gratuitas, boa qualidade PT-BR
- **Vozes PT-BR**: `pt-BR-FranciscoNeural` (masculino), `pt-BR-FranciscaNeural` (feminino)
- **Latência**: ~200ms
- **Custo**: $0
- **Limitação**: Requer internet (Microsoft cloud)
- **Pacote Python**: `edge-tts`

### Prioridade 2: Coqui XTTS v2 — GRATUITO (self-hosted)

- **Por que**: Melhor qualidade, clonagem de voz, 17 idiomas
- **Latência**: ~1-2s (GPU)
- **Custo**: $0 (self-hosted)
- **Requisito**: GPU (4GB+ VRAM)
- **Licença**: MPL-2.0
- **Pacote Python**: `coqui-tts`

### Prioridade 3: Piper TTS — GRATUITO (edge)

- **Por que**: Ultra-rápido, CPU-only, funciona em Raspberry Pi
- **Latência**: ~50ms
- **Custo**: $0
- **Limitação**: Arquivado (Oct 2025), qualidade inferior
- **Pacote**: Binário standalone

### Cloud Pago (BYOK)

- **OpenAI TTS**: $0.015/1K chars — Neural, natural
- **ElevenLabs**: $0.30/1K chars — cloning, expressões
- **Amazon Polly**: $0.004/1K chars — Neural

## Pipeline de Voz

```
Lead liga → Twilio recebe áudio
    → faster-whisper (STT local)
    → LMStudio/ZEN (LLM gera resposta)
    → Edge TTS / Coqui (TTS gera áudio)
    → Twilio envia áudio de volta
```

## Configuração por Tenant

```yaml
voice:
  tts_provider: "edge"        # edge | coqui | piper | openai | elevenlabs
  voice_id: "pt-BR-FranciscaNeural"
  speed: 1.0
  stability: 0.5              # Para Coqui/cloning
  similarity_boost: 0.75      # Para Coqui/cloning
```

## Alternativas Consideradas

| Alternativa | Qualidade | Custo | PT-BR | Latência | Decisão |
|------------|----------|-------|-------|----------|---------|
| ElevenLabs | Excelente | $0.30/1K | Sim | ~300ms | BYOK |
| OpenAI TTS | Muito bom | $0.015/1K | Sim | ~200ms | BYOK |
| Coqui XTTS | Excelente | $0 | Sim | ~1.5s | Prioridade 2 |
| **Edge TTS** | **Bom** | **$0** | **Sim** | **~200ms** | **Prioridade 1** |
| Piper | Razoável | $0 | Sim | ~50ms | Fallback |

## Referências

- Edge TTS: https://github.com/rany2/edge-tts
- Coqui XTTS: https://github.com/idiap/coqui-ai-TTS
- Piper: https://github.com/rhasspy/piper
- OpenAI TTS: https://platform.openai.com/docs/guides/text-to-speech
