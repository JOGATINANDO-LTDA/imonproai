# ADR-010: Framework de Evals para IA

## Status: Aceito
## Data: 2026-09-01
## Decisor: Equipe ImobPro.ai

## Contexto

O ImobPro.ai precisa medir a qualidade das respostas de IA:
- O agente está respondendo com base em documentos?
- As respostas são relevantes para a pergunta?
- O RAG está recuperando os chunks certos?
- O custo está dentro do orçamento?

## Decisão

Usar **Ragas** + **DeepEval** para evals, com **Langfuse** para tracing.

### Evals Implementadas

| Eval | Métrica | Target | Framework |
|------|---------|--------|-----------|
| Faithfulness | % de tokens grounded | > 0.8 | Ragas |
| Relevancy | Resposta pergunta respondida | > 0.7 | Ragas |
| Context Recall | Retrieval encontrou certo | > 0.75 | Ragas |
| Context Precision | Chunks relevantes no topo | > 0.7 | Ragas |
| Answer Relevancy | Resposta é relevante | > 0.7 | DeepEval |
| Hallucination | Resposta não inventa | < 0.1 | DeepEval |

## Justificativa

### Por que Ragas?

- **Específico para RAG**: Métricas dedicadas
- **Ground truth**: Compara com respostas esperadas
- **Integração**: Langfuse, LangSmith
- **Open-source**: Gratuito

### Por que DeepEval?

- **Hallucination detection**: Mede alucinações
- **Bias detection**: Detecta viés
- **Toxicity**: Verifica conteúdo tóxico
- **Multi-provider**: Funciona com qualquer LLM

### Por que Langfuse?

- **Tracing**: Cada passo registrado
- **Custo**: Custo por request
- **Dashboard**: Visualização em tempo real
- **Self-hosted**: Dados locais

## Pipeline de Evals

```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy

# Roda evals após cada resposta
result = evaluate(
    dataset=test_dataset,
    metrics=[faithfulness, answer_relevancy],
)

# Salva no Langfuse
langfuse.score(
    name="faithfulness",
    value=result["faithfulness"],
    comment="Eval automática"
)
```

## Dashboard

- **Faithfulness**: % de respostas grounded
- **Custo**: $/request por provider
- **Latência**: Tempo de resposta
- **Eror rate**: % de falhas

## Referências

- Ragas: https://docs.ragas.io/
- DeepEval: https://docs.confident-ai.com/
- Langfuse: https://langfuse.com/
