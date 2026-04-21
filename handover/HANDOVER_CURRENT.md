# HANDOVER CURRENT

Última consolidação: 2026-04-21 (revO benchmark residual inventory)

## Âmbito
Projeto de geração universal de T-SQL para SQL Server, com validação por equivalência de resultado e controlo explícito de generalização fora do benchmark.

## Estado factual consolidado
- benchmark total: 268 perguntas
- divergência antiga de Q1-Q60 reconciliada: Q32 e Q34 estão fechadas em `revN`
- benchmark fechado com evidência canónica atualmente sincronizada: 147/268
- backlog residual atual: 121/268

## Cobertura fechada com evidência canónica
- Q1-Q60: 60/60 fechadas
- `revD` temporal/comparações/janela: 43 perguntas fechadas
- `revE` lifecycle: Q207/Q209/Q210
- `revK` pareto 80: Q203/Q204/Q205
- `revL` rank within partition em Q61-Q150: 27 perguntas fechadas
- `revM` F18 multi-metric top-N: 13 perguntas fechadas
- `revN` top-N com filtro cruzado: Q32/Q34

## Backlog residual real por família/problema
- grouped_aggregate: 40 abertas (72,73,78,82,83,84,85,88,92,96,131,135,147,221,222,223,227,228,229,230...)
- percentage_share: 16 abertas (80,87,91,98,106,113,124,129,133,146,197,198,199,200,201,202)
- top_n_global: 12 abertas (179,180,181,182,183,184,185,186,187,224,225,226)
- top_n: 10 abertas (64,67,71,74,79,89,95,97,110,141)
- F17_lifecycle: 9 abertas (206,208,211,212,213,214,215,216,217)
- cancellation: 8 abertas (61,62,63,93,104,116,127,144)
- rank_within_partition: 6 abertas (191,192,193,194,195,196)
- time_series: 6 abertas (86,100,114,122,137,138)
- distinct_count: 4 abertas (65,66,134,136)
- period_compare: 4 abertas (70,109,142,149)
- avg_per_document: 3 abertas (77,118,143)
- other: 2 abertas (76,81)
- window_trend: 1 aberta (140)

## Evidência canónica relevante
- `validation/revO/global_benchmark_counts.csv`
- `validation/revO/global_benchmark_residual_summary.csv`
- `validation/revO/backlog_residual_real.md`

## Nota metodológica
Esta revisão consolida o estado global factual do benchmark a partir da evidência canónica já sincronizada no repositório.
As famílias de Q61-Q150 foram lidas do mapa verificado disponível.
As famílias de parte de Q1-Q60 e de alguns itens ainda abertos fora desse intervalo foram inferidas apenas para agrupamento operacional do backlog.

## Prioridade atual
1. fechar `grouped_aggregate`
2. fechar `percentage_share`
3. fechar `top_n_global`
4. fechar `top_n`
5. recalcular a contagem global após cada família, sem regressões
