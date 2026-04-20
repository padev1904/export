# Handover atualizado — revD (2026-04-20)

## Factos verificados nesta revisão

- Foi criado um **emulador T-SQL parcial orientado ao benchmark** sobre SQLite.
- A base local de teste usa `f_invoice_sample.csv` e 45 dimensões JSON.
- O emulador executou com sucesso **268/268 SQL de referência do benchmark**.
- O gerador temporal **revD** foi validado contra o benchmark usando o emulador:
  - cobertura benchmark: **43 perguntas**
  - equivalência semântica: **43/43 PASS**
  - equivalência estrita de grelha: **39/43 PASS**
- Foram criadas **8 perguntas novas fora do benchmark** com SQL manual independente:
  - resultado: **8/8 PASS**

## Correção importante face à revisão anterior

A revisão `revC` tinha resultados otimistas que não estavam suportados por oráculo independente.
Após validação com o emulador, a referência executável correta para o bloco temporal passa a ser a revisão **revD**.

## Estado operacional do gerador temporal revD

### Famílias / padrões cobertos
- `F15_window_trend`
- `F13_period_compare`
- `F11_percentage_share`
- `F10_avg_per_document`

### Dimensões já suportadas
- canal
- região
- país
- marca
- família de produto
- tipo de material

## Backlog real após revD
1. estender o mesmo método de validação a `F17_lifecycle`, `F16_pareto_80`, `F12_rank_within_partition` e `F18_multi_metric_topn`
2. reconciliar explicitamente a divergência antiga de Q1–Q60
3. manter regressão e novas perguntas fora do benchmark com SQL manual independente
