# ADR-008: Git Flow com Conventional Commits

## Status: Aceito
## Data: 2026-09-01
## Decisor: Equipe ImobPro.ai

## Contexto

O projeto precisa de:
- Controle de versão organizado
- Histórico limpo e legível
- Deploy automatizado
- Code review obrigatório

## Decisão

Usar **Git Flow** com **Conventional Commits**:

### Branches

- `main` — Produção, sempre estável
- `develop` — Integração, últimos features
- `feature/*` — Features novas
- `fix/*` — Correções de bugs
- `hotfix/*` — Correções urgentes
- `release/*` — Preparação de release
- `staging/*` — Deploy para homologação

### Commits

```
<type>(<scope>): <description>

feat(provider): implement Opencode ZEN provider with fallback
feat(rag): add pgvector hybrid search with BM25
fix(voice): correct Coqui XTTS memory leak on GPU
docs(providers): add Opencode GO pricing table
```

## Justificativa

### Por que Git Flow?

- **main** sempre deployável
- **develop** para integração contínua
- **feature** para trabalho paralelo
- **hotfix** para correções urgentes

### Por que Conventional Commits?

- **Legibilidade**: Histórico fácil de entender
- **Automação**: Changelogs automáticos
- **Semantic Versioning**: Tags automáticas
- **Filtro**: `git log --grep="feat"` para features

## Branch Protection

### main

- 2 approving reviews
- Status checks (CI)
- Sem force push
- Sem delete

### develop

- 1 approving review
- Status checks
- Force push permitido (rebase)

## Referências

- Git Flow: https://nvie.com/posts/a-successful-git-branching-model/
- Conventional Commits: https://www.conventionalcommits.org/
