# Memória Persistente — ImobPro.ai

## Propósito

Esta pasta armazena a memória do sistema de decisão do ImobPro.ai. Toda decisão tomada é registrada aqui para:

1. **Anti-alucinação**: O agente consulta aqui antes de decidir
2. **Continuidade**: Sessões futuras retomam contexto
3. **Auditoria**: Histórico completo de decisões

## Estrutura

```
memory/
├── README.md                    # Este arquivo
├── decisions-history.md         # Histórico de decisões
├── lessons-learned.md           # Lições aprendidas
└── session-logs/                # Logs de sessões anteriores
```

## Como Usar

1. **Ao iniciar sessão**: Ler `decisions-history.md`
2. **Ao tomar decisão**: Atualizar `decisions-history.md`
3. **Ao aprender lição**: Atualizar `lessons-learned.md`
4. **Ao finalizar sessão**: Criar log em `session-logs/`

## Regras

- Nunca deletar decisões antigas
- Sempre adicionar timestamp
- Manter formato consistente
- Links para ADRs quando aplicável
