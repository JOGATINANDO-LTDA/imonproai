# Stack de Voz — TTS/STT

## Visão Geral

O ImobPro.ai suporta comunicação por voz via:
- **STT (Speech-to-Text)**: Transcreve áudio de ligações
- **TTS (Text-to-Speech)**: Gera áudio para respostas

## Pipeline de Voz

```
Lead liga → Twilio recebe áudio
    → faster-whisper (STT local)
    → LMStudio/ZEN (LLM gera resposta)
    → Edge TTS / Coqui (TTS gera áudio)
    → Twilio envia áudio de volta
```

## STT (Speech-to-Text)

### faster-whisper (Principal)

```python
from faster_whisper import WhisperModel

model = WhisperModel("large-v3", device="cuda", compute_type="float16")

def transcribe(audio_bytes):
    segments, info = model.transcribe(audio_bytes, language="pt")
    return " ".join([s.text for s in segments])
```

| Modelo | Tamanho | RAM | Velocidade | Qualidade |
|--------|---------|-----|-----------|-----------|
| tiny | 39MB | 1GB | ~32x | Baixa |
| base | 74MB | 1GB | ~16x | Razoável |
| medium | 769MB | 5GB | ~6x | Boa |
| **large-v3** | **1.5GB** | **10GB** | **~3x** | **Excelente** |

### whisper.cpp (Alternativa)

- Mais leve que faster-whisper
- Suporta CPU e GPU
- Bom para Raspberry Pi

## TTS (Text-to-Speech)

### Prioridade 1: Edge TTS (Microsoft)

```python
import edge_tts

async def text_to_speech(text: str):
    communicate = edge_tts.Communicate(text, "pt-BR-FranciscaNeural")
    await communicate.save("output.mp3")
```

| Voz | Gênero | Notas |
|-----|--------|-------|
| pt-BR-FranciscoNeural | Masculino | Natural |
| pt-BR-FranciscaNeural | Feminino | Natural |

### Prioridade 2: Coqui XTTS v2

```python
from TTS.api import TTS

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
tts.tts_to_file(text="Olá!", speaker_wav="reference.wav", language="pt")
```

- Melhor qualidade
- Clonagem de voz
- Requer GPU

### Prioridade 3: Piper TTS

- Ultra-rápido (~50ms)
- CPU-only
- Qualidade inferior

## Configuração por Tenant

```yaml
voice:
  stt_provider: "faster-whisper"
  stt_model: "large-v3"

  tts_provider: "edge"        # edge | coqui | piper | openai
  voice_id: "pt-BR-FranciscaNeural"
  speed: 1.0
```

## Referências

- [ADR-004: TTS Stack](../decisions/004-tts-stack.md)
- [ADR-005: STT Stack](../decisions/005-stt-stack.md)
- faster-whisper: https://github.com/SYSTRAN/faster-whisper
- Edge TTS: https://github.com/rany2/edge-tts
- Coqui TTS: https://github.com/idiap/coqui-ai-TTS
