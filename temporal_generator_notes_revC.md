# Temporal generator revC

## Escopo fechado nesta revisão
Gerador universal temporal para um subconjunto operacional de:
- `F15_window_trend`
- `F13_period_compare`
- `F11_percentage_share` (subcaso temporal mensal)

## Padrões suportados
1. Evolução mensal nos últimos 6 meses
2. Mês atual versus mês anterior
3. Variação percentual mês contra mês
4. Média móvel de 3 meses
5. Acumulado mensal YTD no ano atual
6. Peso do desconto promocional total sobre a faturação por mês
7. Crescimento do mês atual face ao mesmo mês do ano anterior por dimensão

## Dimensões suportadas no revC
- sem dimensão
- canal de distribuição
- região da linha
- país da linha
- marca de produto
- família de produto
- tipo de material

## Métricas suportadas
- `NetAmount`
- `BillingQuantity`
- `GrossMargin` com `IsItAnAdditionalCalculatedRecord = 1`
- desconto promocional total:
  `ZDPRPromotional + ZCPRPromotionalCampaign + REA1PromotionalDiscount`

## Janela temporal fixada nesta validação
Para a amostra local e esta revisão:
- data corrente usada na validação: `2026-04-20`
- últimos 6 meses: desde `2025-11-01`
- últimos 8 meses (média móvel 3m): desde `2025-09-01`
- mês atual: `2026-04`
- mês anterior: `2026-03`
- mesmo mês do ano anterior: `2025-04`

## Resultado medido
- Benchmark coberto nesta revisão: **40/40 PASS**
- Testes novos fora do benchmark: **6/6 PASS**

## Nota de regressão
Não existe no material anexado uma matriz histórica anterior de PASS para esta família temporal específica.
Para reduzir risco de regressão, após o último ajuste do classificador foi reexecutado o conjunto completo coberto nesta revisão:
- 40 perguntas benchmark
- 6 perguntas novas fora do benchmark
- total final reexecutado: **46/46 PASS**
