# Guia de Git Flow — ImobPro.ai

## Branches

### Principais

- `main` — Produção, sempre estável
- `develop` — Integração, últimos features

### De Suporte

- `feature/*` — Features novas
- `fix/*` — Correções de bugs
- `hotfix/*` — Correções urgentes em produção
- `release/*` — Preparação de release
- `staging/*` — Deploy para homologação

## Fluxos

### Feature

```
develop → feature/xyz → develop
```

```bash
git checkout develop
git checkout -b feature/multi-provider
# ... trabalhar ...
git add .
git commit -m "feat(provider): implement Opencode ZEN provider"
git push origin feature/multi-provider
# Abrir PR para develop
```

### Release

```
develop → release/v1.0.0 → main + develop
```

```bash
git checkout develop
git checkout -b release/v1.0.0
# ... bug fixes apenas ...
git push origin release/v1.0.0
# PR para main E develop
git checkout main
git merge release/v1.0.0
git tag v1.0.0
```

### Hotfix

```
main → hotfix/fix-xyz → main + develop
```

```bash
git checkout main
git checkout -b hotfix/fix-critical
# ... correção mínima ...
git push origin hotfix/fix-critical
# PR para main E develop
```

## Conventional Commits

### Formato

```
<type>(<scope>): <description>
```

### Tipos

| Tipo | Descrição | Exemplo |
|------|-----------|---------|
| `feat` | Feature nova | `feat(rag): add hybrid search` |
| `fix` | Correção | `fix(voice): correct PT-BR encoding` |
| `docs` | Documentação | `docs: update README` |
| `refactor` | Refatoração | `refactor: extract provider registry` |
| `test` | Testes | `test: add provider unit tests` |
| `chore` | Manutenção | `chore: update dependencies` |

### Scopes

| Scope | Módulo |
|-------|--------|
| `rag` | Engine RAG |
| `voice` | TTS/STT |
| `agent` | Agente de IA |
| `provider` | Provider registry |
| `api` | Backend API |
| `ui` | Frontend |
| `infra` | Docker/Deploy |
| `db` | Database |

## Branch Protection

### main

- 2 approving reviews
- Status checks (CI)
- Sem force push
- Sem delete

### develop

- 1 approving review
- Status checks
- Force push permitido

## Referências

- [ADR-008: Git Flow](../decisions/008-git-flow-strategy.md)
- Git Flow: https://nvie.com/posts/a-successful-git-branching-model/
