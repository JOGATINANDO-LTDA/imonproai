# Histórico de Decisões — ImobPro.ai

## 2026-09-01 — Sessão Inicial

### Decisão: Multi-Provider Agnóstico
- **ADR**: 001
- **Justificativa**: Evitar lock-in, reduzir custo, garantir resiliência
- **Impacto**: Arquitetura de providers, fallback chain, configuração por tenant

### Decisão: RAG Híbrido (LlamaIndex + LangChain)
- **ADR**: 002
- **Justificativa**: Melhor RAG (LlamaIndex) + melhores agents (LangChain)
- **Impacto**: Pipeline de ingestion, retrieval, evaluation

### Decisão: pgvector como Vector Store
- **ADR**: 003
- **Justificativa**: Unificar dados relacionais e vetoriais em um banco
- **Impacto**: Migração do Qdrant, schema do banco, backup

### Decisão: TTS Edge → Coqui → Piper
- **ADR**: 004
- **Justificativa**: Custo zero, qualidade progressiva, PT-BR nativo
- **Impacto**: Pipeline de voz, configuração por tenant

### Decisão: STT faster-whisper
- **ADR**: 005
- **Justificativa**: Velocidade, custo zero, privacidade
- **Impacto**: Transcrição de ligações, pipeline de voz

### Decisão: Opencode ZEN/GO como Providers
- **ADR**: 006
- **Justificativa**: Modelos gratuitos + opção de escalar para pago
- **Impacto**: Integração com AI SDK, custos estimados

### Decisão: LMStudio como Provider Local
- **ADR**: 007
- **Justificativa**: Desenvolvimento sem custo, privacidade
- **Impacto**: Setup de desenvolvimento, testes locais

### Decisão: Git Flow com Conventional Commits
- **ADR**: 008
- **Justificativa**: Histórico limpo, deploy automatizado
- **Impacto**: Fluxo de trabalho, CI/CD

### Decisão: Docker por Ambiente
- **ADR**: 009
- **Justificativa**: Isolamento, reprodutibilidade
- **Impacto**: docker-compose.yml, render.yaml

### Decisão: Framework de Evals
- **ADR**: 010
- **Justificativa**: Medir qualidade, detectar alucinações
- **Impacto**: Pipeline de avaliação, dashboards

### Decisão: Idioma pt-BR
- **Tipo**: Critério Inviolável
- **Justificativa**: Comunicação clara com equipe brasileira
- **Impacto**: Toda comunicação, código, commits, docs

---

## Próximas Decisões Pendentes

1. ~~Multi-Provider~~ ✓
2. ~~RAG Engine~~ ✓
3. ~~Vector Store~~ ✓
4. ~~TTS Stack~~ ✓
5. ~~STT Stack~~ ✓
6. ~~Providers Cloud~~ ✓
7. ~~Provider Local~~ ✓
8. ~~Git Flow~~ ✓
9. ~~Docker~~ ✓
10. ~~Evals~~ ✓
11. **Autenticação**: JWT vs OAuth vs Session
12. **Rate Limiting**: Por tenant vs global
13. **Cache Strategy**: Redis vs in-memory
14. **Monitoring**: Langfuse self-hosted vs cloud
15. **Backup**: Automatizado vs manual
