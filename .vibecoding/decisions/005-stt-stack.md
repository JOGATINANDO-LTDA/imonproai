# ADR-005: STT com faster-whisper (local)

## Status: Aceito
## Data: 2026-09-01
## Decisor: Equipe ImobPro.ai

## Contexto

O agente comercial precisa transcrever áudio de ligações telefônicas. Requisitos:
- Suporte a PT-BR
- Baixa latência
- Custo zero
- Funcionamento offline (privacidade)

## Decisão

Usar **faster-whisper** como STT principal, com whisper.cpp como alternativa.

## Justificativa

### Por que faster-whisper?

1. **Velocidade**: 4x mais rápido que whisper original
2. **Custo**: $0 (local)
3. **Privacidade**: Áudio não sai do servidor
4. **PT-BR**: Modelo large-v3 suporta português
5. **CTranslate2**: Otimizado para CPU e GPU

### Modelos Disponíveis

| Modelo | Tamanho | RAM | Velocidade | Qualidade |
|--------|---------|-----|-----------|-----------|
| tiny | 39MB | 1GB | ~32x | Baixa |
| base | 74MB | 1GB | ~16x | Razoável |
| medium | 769MB | 5GB | ~6x | Boa |
| **large-v3** | **1.5GB** | **10GB** | **~3x** | **Excelente** |

### Pipeline STT

```python
from faster_whisper import WhisperModel

model = WhisperModel("large-v3", device="cuda", compute_type="float16")

def transcribe(audio_bytes):
    segments, info = model.transcribe(audio_bytes, language="pt")
    return " ".join([s.text for s in segments])
```

## Alternativas Consideradas

| Alternativa | Velocidade | Custo | PT-BR | Privacidade | Decisão |
|------------|-----------|-------|-------|------------|---------|
| OpenAI Whisper API | ~1x | $0.006/min | Sim | Não | Rejeitado |
| whisper.cpp | ~3x | $0 | Sim | Sim | Alternativa |
| **faster-whisper** | **~4x** | **$0** | **Sim** | **Sim** | **Aceito** |
| AssemblyAI | ~2x | $0.005/min | Sim | Não | Rejeitado |
| Deepgram | ~2x | $0.0059/min | Sim | Não | Rejeitado |

## Referências

- faster-whisper: https://github.com/SYSTRAN/faster-whisper
- whisper.cpp: https://github.com/ggerganov/whisper.cpp
- CTranslate2: https://github.com/OpenNMT/CTranslate2
