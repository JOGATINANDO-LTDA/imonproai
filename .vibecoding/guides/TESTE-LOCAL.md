# Guia de Teste Local — ImobPro.ai

> **Objetivo:** Validar que o agente comercial de IA funciona sem nenhuma dependência paga ou externa.
> Tudo roda na sua máquina via Docker + LMStudio.

---

## Pré-requisitos

| Item | Como verificar | Status esperado |
|------|---------------|-----------------|
| Docker Desktop rodando | Ícone do Docker na bandeja do sistema | Verde (Running) |
| LMStudio rodando | Abrir LMStudio → modelo carregado | Modelo `qwen3.5-9b-deepseek-v4-flash` com status "Loaded" |
| Portas disponíveis | Verificar se 3010, 8888, 5432, 6379 estão livres | Nenhum processo usando essas portas |

---

## 1. Subindo o Sistema

### 1.1 — Limpar ambiente anterior (se existir)

```bash
cd D:\Workspace\ia-system\imobpro-ai
docker compose down -v
```

### 1.2 — Subir todos os containers

```bash
docker compose up -d
```

### 1.3 — Aguardar inicialização (~30 segundos)

```bash
# Verificar se o backend está pronto
docker logs imobpro-ai-backend-1 --tail 5
```

**Saída esperada:**
```
INFO:     Application startup complete.
INFO:app.main:Tabelas criadas com sucesso!
```

### 1.4 — Carregar dados demo (seed)

```bash
curl -X POST http://localhost:8888/api/seed
```

**Resposta esperada:**
```json
{
  "message": "Dados demo criados com sucesso",
  "data": {
    "tenant": "Imobiliária Modelo",
    "user": "admin@imobpro.ai",
    "contacts": 8,
    "properties": 6,
    "agents": 2,
    "conversations": 3
  }
}
```

---

## 2. Login e Acesso

### 2.1 — Abrir o sistema

Abra no navegador: **http://localhost:3010**

**Resultado esperado:** Landing page com o logo "ImobPro.ai", descrição do produto, e botão "Entrar".

### 2.2 — Fazer login

- Clique em **"Entrar"**
- Na tela de login, clique em **"Entrar como Demo"**
- Aguarde redirecionamento

**Resultado esperado:** Dashboard com métricas e sidebar de navegação à esquerda.

### 2.3 — Verificar autenticação

Na sidebar, na parte inferior, deve aparecer:
- Nome: **Carlos Mendes**
- Role: **admin**
- Botão **"Sair"**

---

## 3. Dashboard — Métricas

### 3.1 — Verificar cards de métricas

No topo da página, verifique os 8 cards:

| Card | Valor esperado |
|------|---------------|
| Total de Leads | 8 |
| Conversas Ativas | 3 |
| Imóveis Cadastrados | 6 |
| Leads Ganhos | 2 |
| Leads Perdidos | 1 |
| Mensagens Hoje | ≥ 4 |

> **Nota:** Os gráficos de "Conversas por Canal" e "Pipeline de Vendas" mostram dados de exemplo (mock). Apenas os cards numéricos são dados reais do banco.

---

## 4. Contatos

### 4.1 — Acessar a página

Clique em **"Contatos"** na sidebar.

**Resultado esperado:** Tabela com 8 contatos listados.

### 4.2 — Verificar dados

| Nome | Status | Score |
|------|--------|-------|
| Maria Silva | Ganho | 95 |
| João Santos | Qualificado | 72 |
| Ana Oliveira | Proposta | 85 |
| Pedro Costa | Novo | 45 |
| Luciana Ferreira | Ganho | 88 |
| Roberto Almeida | Perdido | 30 |
| Fernanda Lima | Qualificado | 67 |
| Marcos Souza | Proposta | 78 |

### 4.3 — Testar filtro

No dropdown "Filtrar por status", selecione **"Qualificados"**.

**Resultado esperado:** Apenas João Santos e Fernanda Lima aparecem.

Volte para **"Todos os status"**.

---

## 5. Imóveis

### 5.1 — Acessar a página

Clique em **"Imóveis"** na sidebar.

**Resultado esperado:** Grid de cards com 6 imóveis.

### 5.2 — Verificar imóveis

| Imóvel | Preço | Quartos | Tipo |
|--------|-------|---------|------|
| Apartamento Jardins 3 quartos | R$ 850.000 | 3 | Apartamento |
| Cobertura Vila Mariana | R$ 1.500.000 | 4 | Apartamento |
| Casa Alphaville 4 quartos | R$ 2.200.000 | 4 | Casa |
| Studio Paulista | R$ 420.000 | 1 | Apartamento |
| Sala Comercial Faria Lima | R$ 980.000 | 0 | Comercial |
| Apartamento Moema 2 quartos | R$ 650.000 | 2 | Apartamento |

### 5.3 — Verificar detalhes

Em cada card, confirme que aparece:
- Endereço completo
- Metragem (m²)
- Status (Disponível ou Reservado)
- Lista de features (Varanda, Piscina, etc.)

---

## 6. Agentes

### 6.1 — Acessar a página

Clique em **"Agentes"** na sidebar.

**Resultado esperado:** Cards com 2 agentes.

### 6.2 — Verificar agentes

| Agente | Modelo | Voz | Telefone |
|--------|--------|-----|----------|
| Assistente Virtual | qwen3.5-9b-deepseek-v4-flash | nova | (11) 99999-0001 |
| Consultor Especializado | qwen3.5-9b-deepseek-v4-flash | vera | (11) 99999-0002 |

---

## 7. Modelos de IA

### 7.1 — Acessar a página

Clique em **"Modelos"** na sidebar.

**Resultado esperado:** Tabela com ~15 modelos listados e auto-refresh a cada 10 segundos.

### 7.2 — Verificar modelo ativo

Na parte superior, deve aparecer:
- Indicador verde com nome: **qwen3.5-9b-deepseek-v4-flash**
- Provider: **lmstudio**
- Status: **Carregado**

### 7.3 — Verificar modelos na tabela

Confirme que os modelos aparecem com:
- Nome do modelo
- Badge do provider (lmstudio)
- Status (Carregado/Descarregado)
- Tamanho em MB
- Botão de ação (Carregar/Descarregar)

### 7.4 — Testar unload (opcional)

Clique no botão **"Descarregar"** ao lado de um modelo descarregado.

**Resultado esperado:** Status muda para "Descarregado". O modelo pode ser recarregado depois.

---

## 8. Teste de Voz (Simulação Local)

Este é o teste mais importante — prova que o agente IA conversa em português.

### 8.1 — Acessar a página

Clique em **"Teste de Voz"** na sidebar.

**Resultado esperado:** Interface de chat com:
- Badge verde **"Modo Local"** no header
- Campo de texto na parte inferior
- Botão de microfone (🎤)
- 4 botões de sugestão rápida

### 8.2 — Primeira mensagem

No campo de texto, digite:

```
Olá, tenho interesse num apartamento de 3 quartos na região dos Jardins
```

Clique no botão **Enviar** (ou pressione Enter).

**Resultado esperado:**
1. Indicador de "digitando" aparece (bolinhas animadas)
2. Resposta em texto do agente aparece (ex: "Olá! Temos um apartamento incrível nos Jardins...")
3. **Áudio é reproduzido automaticamente** com voz feminina em português
4. Player de áudio aparece abaixo da mensagem

### 8.3 — Segunda mensagem (continuidade)

Na mesma conversa, digite:

```
Qual o valor exato?
```

**Resultado esperado:** Agente responde com o valor (R$ 850.000) usando o contexto da conversa anterior. Áudio é reproduzido.

### 8.4 — Terceira mensagem (agendamento)

```
Quero agendar uma visita para sábado de manhã
```

**Resultado esperado:** Agente confirma o agendamento e pergunta horário preferido.

### 8.5 — Teste de microfone

1. Clique no ícone **🎤** (microfone)
2. Fale em voz alta: **"Olá"**
3. Aguarde o navegador transcrever

**Resultado esperado:** Texto "Olá" aparece no campo de entrada. Clique Enviar para o agente responder.

> **Nota:** O microfone funciona apenas no Chrome/Edge. No Firefox pode não funcionar.

### 8.6 — Sugestões rápidas

Clique em um dos botões de sugestão (ex: "Quero apartamento").

**Resultado esperado:** Mensagem é enviada automaticamente e agente responde com áudio.

### 8.7 — Nova conversa

Clique em **"Nova conversa"**.

**Resultado esperado:** Conversa reseta. Mensagens anteriores somem. Contexto é perdido (nova sessão).

### 8.8 — Testar com domínio específico

Envie estas mensagens em sequência:

```
1. "Olá, sou da Alta Impacto e quero vender meu apartamento"
2. "É na Vila Mariana, 2 quartos, 80m²"
3. "Qual o valor de mercado?"
4. "Posso agendar uma visita para avaliar?"
```

**Resultado esperado:** Agente mantém contexto, faz perguntas sobre o imóvel, e oferece agendamento. Cada resposta gera áudio.

---

## 9. Configurações

### 9.1 — Acessar a página

Clique em **"Configurações"** na sidebar.

**Resultado esperado:** 4 seções visíveis:
- Configurações da Imobiliária
- Modelo por Agente
- Integrações
- Equipe

### 9.2 — Testar troca de modelo

Na seção **"Modelo por Agente"**:
1. Encontre o agente "Assistente Virtual"
2. No dropdown, selecione outro modelo (ex: `deepseek/deepseek-r1-0528-qwen3-8b`)
3. Verifique que a mudança foi salva

**Resultado esperado:** Dropdown mantém a seleção após troca.

### 9.3 — Verificar integrações

Na seção **"Integrações"**, verifique os status:

| Integração | Status esperado |
|-----------|----------------|
| WhatsApp (Evolution API) | Não configurado |
| Telefone (Twilio) | Não configurado |
| E-mail (SMTP) | Não configurado |
| LMStudio (Local) | Conectado |

> **Nota:** Apenas LMStudio está funcionando. As outras integrações requerem configuração de credenciais.

---

## 10. Teste Completo do Fluxo de Voz

Execute este roteiro completo para validar o fluxo do agente:

### Cenário: Lead procura apartamento

| Passo | Sua mensagem | Resposta esperada do agente |
|-------|-------------|---------------------------|
| 1 | "Olá, vi um apartamento no site" | Cumprimento + pergunta sobre preferências |
| 2 | "Até R$ 900.000, perto do metrô" | Sugere apartamento nos Jardins (R$ 850.000) |
| 3 | "Tem varanda?" | Confirma que tem varanda + lista features |
| 4 | "Posso visitar?" | Oferece agendar visita + pergunta data/horário |
| 5 | "Sábado às 10h" | Confirma agendamento |

### Cenário: Lead quer vender imóvel

| Passo | Sua mensagem | Resposta esperada do agente |
|-------|-------------|---------------------------|
| 1 | "Quero vender meu apartamento" | Pergunta localização e características |
| 2 | "Vila Mariana, 3 quartos, 120m²" | Estima valor + oferece avaliação |
| 3 | "Qual o valor?" | Responde com faixa de preço estimada |
| 4 | "Como funciona a avaliação?" | Explica processo + oferece visita técnica |

---

## Troubleshooting

### Backend não inicia

```bash
# Ver logs
docker logs imobpro-ai-backend-1 --tail 20

# Reiniciar
docker restart imobpro-ai-backend-1
```

### Seed retorna "Internal Server Error"

O banco de dados não foi inicializado. O backend cria tabelas automaticamente no startup. Aguarde 10 segundos após o `docker compose up` e tente novamente.

### Modelo não aparece na lista de modelos

Verifique se o LMStudio está rodando e com o modelo carregado:
```bash
curl http://localhost:1234/v1/models
```

### Voice simulate retorna erro

Verifique se o LMStudio está acessível:
```bash
curl -X POST http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen3.5-9b-deepseek-v4-flash","messages":[{"role":"user","content":"teste"}]}'
```

### Áudio não reproduce

- Verifique se o navegador não bloqueou autoplay
- Clique no player de áudio manualmente
- Teste em Chrome ou Edge (suporte mais confiável a áudio)

### Porta 3010 já em uso

```bash
# Verificar o que está usando a porta
netstat -ano | findstr :3010

# Matar o processo ou mudar a porta no docker-compose.yml
```

---

## Resumo do que foi validado

| Capacidade | Status |
|-----------|--------|
| Login e autenticação | ✅ Funcional |
| Dashboard com métricas reais | ✅ Funcional |
| Listagem de contatos | ✅ Funcional |
| Listagem de imóveis | ✅ Funcional |
| Listagem de agentes | ✅ Funcional |
| Gerenciamento de modelos (load/unload) | ✅ Funcional |
| Simulação de voz com IA | ✅ Funcional |
| Text-to-Speech em português | ✅ Funcional |
| Speech-to-Text (microfone) | ✅ Funcional |
| Contexto de conversa | ✅ Funcional |
| Troca de modelo por agente | ✅ Funcional |

**Conclusão:** O produto funciona localmente sem nenhuma dependência paga. O agente conversa em português, entende contexto, e gera áudio natural.
