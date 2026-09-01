# ImobPro.ai — Sistema de Decisão Agentico

## Propósito

Esta pasta é a **memória persistente** do sistema de IA que auxilia no desenvolvimento do ImobPro.ai. Todo contexto, decisão e justificativa ficam aqui armazenados para:

1. **Anti-alucinação**: O agente sempre consulta aqui antes de decidir
2. **Reprodutibilidade**: Qualquer desenvolvedor entende o "porquê"
3. **Defesa do projeto**: Cada decisão tem justificativa técnica documentada
4. **Continuidade**: Sessões futuras retomam contexto automaticamente

## Regras Invioláveis

1. **Idioma**: pt-BR em TODA comunicação (código, commits, docs, PRs)
2. **Boas práticas**: Sempre validar decisões contra critérios documentados
3. **Anti-alucinação**: Consultar decisions/ antes de qualquer escolha técnica
4. **Memória**: Atualizar memory/ após cada decisão tomada

## Como Usar

- O agente DEVE ler este README no início de cada sessão
- Antes de qualquer decisão técnica, consultar `decisions/`
- Antes de usar um provider, consultar `providers/`
- Antes de modificar RAG, consultar `rag/`
- Após cada decisão, atualizar `memory/decisions-history.md`

## Estrutura

```
.vibecoding/
├── README.md                    # Este arquivo
├── ARCHITECTURE.md              # Arquitetura do sistema
├── decisions/                   # ADRs (decisões documentadas)
│   ├── 001-multi-provider-ai.md
│   ├── 002-rag-engine-choice.md
│   ├── 003-vector-store-pgvector.md
│   ├── 004-tts-stack.md
│   ├── 005-stt-stack.md
│   ├── 006-opencode-zen-go.md
│   ├── 007-lmstudio-local.md
│   ├── 008-git-flow-strategy.md
│   ├── 009-docker-environments.md
│   └── 010-evals-framework.md
├── providers/                   # Documentação de providers
├── rag/                         # Engine RAG
├── voice/                       # TTS/STT
├── guides/                      # Guias práticos
├── models/                      # Catálogo de modelos
├── evals/                       # Framework de avaliação
├── memory/                      # Memória persistente
└── docs/
    └── aprendizagem/            # LOCAL - não commita
```

## Fluxo de Decisão

1. Consultar memória (`memory/decisions-history.md`)
2. Verificar se há ADR aplicável (`decisions/`)
3. Se não há decisão registrada, criar nova ADR
4. Documentar justificativa e alternativas consideradas
5. Atualizar memória com a decisão tomada
