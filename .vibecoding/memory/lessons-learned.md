# Lições Aprendidas — ImobPro.ai

## 2026-09-01

### Lição 1: Documentar Decisões Antes de Codar

**Problema**: Começar a codar sem justificativa leva a refatoração desnecessária.

**Solução**: Criar ADRs antes de implementar.

**Resultado**: Código com propósito claro, fácil de defender em entrevistas.

### Lição 2: Anti-Alucinação é Essencial

**Problema**: Agentes de IA podem "inventar" informações.

**Solução**: Sempre consultar documentação antes de decidir.

**Resultado**: Decisões baseadas em fatos, não em suposições.

### Lição 3: Multi-Provider é Investimento

**Problema**: Provider único = lock-in + risco de custo.

**Solução**: Registry pattern com fallback chain.

**Resultado**: Flexibilidade para trocar providers sem reescrever código.

### Lição 4: pgvector Unifica Ops

**Probledo**: Dois bancos (PostgreSQL + Qdrant) = complexidade.

**Solução**: pgvector para tudo.

**Resultado**: Um backup, uma restore, uma conexão.

### Lição 5: Voz em PT-BR Exige Cuidado

**Problema**: Modelos genéricos podem ter sotaque errado.

**Solução**: Edge TTS com vozes neurais PT-BR.

**Resultado**: Voz natural, sem sotaque estrangeiro.

---

## Padrões Aprendidos

1. **Sempre documentar o "porquê"**
2. **Anti-alucinação: consultar fontes antes de decidir**
3. **Multi-provider para resiliência**
4. **Unificar infra quando possível**
5. **Testar cada provider individualmente**
