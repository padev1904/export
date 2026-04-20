# Estado reconstituído — 2026-04-20

## Factos verificados
- O ZIP do projeto contém `ddl/`, `documentation/` e `example_queries/`.
- O ZIP contém 45 ficheiros JSON de dimensões e um `f_invoice_sample.csv`.
- `examples.sql` contém 268 perguntas SQL de benchmark.
- O ficheiro `q61_q150_family_map.csv` contém 90 perguntas, cobrindo Q61-Q150.
- Distribuição dominante de famílias em Q61-Q150:
  - rank_within_partition: 27
  - grouped_aggregate: 13
  - top_n: 12
  - percentage_share: 10
  - cancellation: 8
  - time_series: 6
  - distinct_count: 4
  - period_compare: 4
  - avg_per_document: 3
  - other: 2
  - window_trend: 1
- A matriz `tsql_pass_matrix_q1_q60_v2.csv` disponível nesta sessão mostra:
  - 58 PASS
  - 2 NO_GENERATOR
  - falhas remanescentes: Q32 e Q34
- `holdout_questions_v1.csv` tem 12 perguntas.
- `holdout_questions_v2.csv` tem 12 perguntas.

## Regras estabilizadas confirmadas na documentação do ZIP
- `dbo.F_Invoice` é a âncora central.
- Faturação/vendas: aplicar por defeito `BillingDocumentIsCancelled = 0`, salvo perguntas sobre cancelamento.
- Valor líquido faturado: `SUM(f.NetAmount)`.
- Preço de lista: `SUM(f.ZLP1PriceList)`.
- Desconto promocional total: `SUM(f.ZDPRPromotional + f.ZCPRPromotionalCampaign + f.REA1PromotionalDiscount)`.
- Preço médio líquido por unidade: `SUM(f.NetAmount) / NULLIF(SUM(f.BillingQuantity), 0)`.
- Peso líquido médio por unidade: `SUM(f.ItemNetWeight) / NULLIF(SUM(f.BillingQuantity), 0)`.
- `GrossMargin` e `NetCommercialSales`: default operacional com `IsItAnAdditionalCalculatedRecord = 1` quando relevante.
- Quotas e taxas percentuais devem sair em escala 0-100.
- Taxas de cancelamento devem ser consolidadas primeiro ao nível de `BillingDocument`.
- Marca/família/tipo de material: via `D_Product`.
- Grupo de contas/condição expedição/zona transporte/geografia cliente: via `D_Customer`.

## Divergências a manter explícitas
- O handover textual resume Q1-Q60 como fechado em 60/60.
- A matriz factual anexada mostra 58/60 com Q32 e Q34 ainda sem gerador.
- Até prova adicional, a verdade operacional deve seguir a matriz factual e não o resumo narrativo.

## Backlog real recomendado
1. Reconciliar Q1-Q60, fechando ou confirmando Q32 e Q34.
2. Fechar famílias prioritárias de Q61-Q150 nesta ordem:
   - rank_within_partition
   - percentage_share
   - cancellation
   - period_compare
3. Só depois consolidar os casos especiais e avançar para Q151-Q268.
4. Manter hold-out fora do benchmark como barreira anti-memorização.
