# Handover atualizado — 2026-04-20 revC

## O que avançou nesta revisão
- Foi construído um gerador universal temporal executável (`temporal_generator_revC.py`).
- O gerador foi validado por equivalência de resultado contra referência independente na `f_invoice_sample`.
- Foi fechada a primeira tranche executável do backlog de Q151–Q268 no eixo temporal.

## Factos verificados
- A amostra local contém 57 598 linhas em `F_Invoice`.
- A data corrente usada para validação nesta revisão foi fixada em `2026-04-20`.
- O gerador temporal revC cobre 40 perguntas de benchmark:
  - Q151–Q178
  - Q242–Q247
  - Q263–Q268
- Resultado medido nessa tranche: **40/40 PASS** por equivalência de resultado.
- Foram criadas 6 perguntas novas fora do benchmark, todas comparadas contra SQL manual independente.
- Resultado medido fora do benchmark: **6/6 PASS**.

## O que o gerador revC sabe fazer
- evolução mensal nos últimos 6 meses
- comparação mês atual vs mês anterior
- variação percentual mês contra mês
- média móvel de 3 meses
- YTD mensal no ano atual
- quota mensal do desconto promocional total sobre a faturação
- comparação do mês atual com o mesmo mês do ano anterior por dimensão

## Dimensões já suportadas neste gerador
- canal
- região
- país
- marca
- família de produto
- tipo de material

## Regras de negócio aplicadas
- faturação/vendas: `BillingDocumentIsCancelled = 0`
- `GrossMargin`: aplica `IsItAnAdditionalCalculatedRecord = 1`
- percentagens: escala 0–100
- divisões: `NULLIF`
- joins via produto quando necessário para marca/família/tipo de material

## Risco de regressão / estado de regressão
- Não havia no material anexado uma matriz histórica de PASS desta família temporal para usar como baseline externo.
- Para controlar regressão dentro desta revisão, após o último ajuste do classificador foram reexecutadas:
  - as 40 perguntas benchmark cobertas
  - as 6 perguntas novas fora do benchmark
- Estado final reexecutado: **46/46 PASS**

## O que continua por fechar
### No bloco Q151–Q268
- `F17_lifecycle`
- `F16_pareto_80`
- `F02_top_n_global`
- `F12_rank_within_partition`
- `F18_multi_metric_topn`
- `F07_grouped_aggregate_via_product` fora do subespaço temporal já coberto

### Divergências que continuam explícitas
- Q1–Q60 mantém divergência documental:
  - o handover narrativo diz 60/60
  - a matriz factual anexada mostra Q32 e Q34 como `NO_GENERATOR`

## Próximo foco recomendado
1. fechar `F17_lifecycle` de Q206–Q217 com testes novos fora do benchmark
2. fechar `F16_pareto_80` preservando a regra estabilizada antes/depois e não a simplificação do benchmark
3. só depois consolidar top-N e multi-métrica do restante Q179–Q268
