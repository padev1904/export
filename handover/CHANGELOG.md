# CHANGELOG

## 2026-04-21 — revN Q32/Q34 reconciliation
- fechamento canónico do arquétipo `top_n_with_cross_filter`
- promoção de `generators/topn_cross_filter_generator.py` para a versão canónica `revN`
- validação executável direta de `Q32/Q34`
- benchmark da família: `2/2 PASS` por equivalência de resultado
- generalização fora do benchmark com SQL manual independente: `6/6 PASS`
- criação de `validation/revN/q32_q34_benchmark_validation.csv`
- criação de `validation/revN/q32_q34_regression_slice.csv`
- criação de `validation/revN/q32_q34_generalization_eval.csv`
- criação de `validation/revN/q32_q34_generalization_cases.md`
- criação de `validation/revN/q32_q34_notes.md`
- reconciliação explícita da divergência factual antiga de `Q1-Q60`
- atualização de `HANDOVER_CURRENT.md`, `CHANGELOG.md`, `ARTEFACTS_INDEX.md`, `RETOMA_CHECKLIST.md` e `README.md`
- próxima prioridade operacional passa a ser o cálculo do backlog residual real pós-`Q32/Q34` e a consolidação da contagem global do benchmark

## 2026-04-21 — revM F18 multi-metric-topN closure
- fechamento canónico da família `F18_multi_metric_topn`
- promoção de `generators/f18_multi_metric_topn_generator.py` para a versão canónica `revM`
- validação executável do subset benchmark `Q58/Q59/Q75/Q90/Q188/Q189/Q190/Q248/Q249/Q250/Q251/Q252/Q253`
- benchmark da família: `13/13 PASS` por equivalência semântica
- regressão integral da família em `revM`: `13/13 PASS`
- generalização fora do benchmark com SQL manual independente: `8/8 PASS`
- criação de `validation/revM/f18_multi_metric_topn_benchmark_validation.csv`
- criação de `validation/revM/f18_multi_metric_topn_generalization_cases.md`
- criação de `validation/revM/f18_multi_metric_topn_notes.md`
- atualização de `HANDOVER_CURRENT.md`, `CHANGELOG.md`, `ARTEFACTS_INDEX.md`, `RETOMA_CHECKLIST.md` e `README.md`
- próxima prioridade operacional passa a ser a reconciliação explícita de `Q32/Q34`

## 2026-04-20 — revL rank-within-partition closure
- fechamento canónico da família `F12_rank_within_partition`
- promoção de `generators/rank_partition_generator.py` para a versão canónica `revL`
- validação executável do subset benchmark `Q61-Q150` classificado como `rank_within_partition`
- benchmark da família: `27/27 PASS` por equivalência semântica
- equivalência estrita de grelha: `26/27`
- generalização fora do benchmark com SQL manual independente: `8/8 PASS`
- regressão integral da família em `revL`: `27/27 PASS`
- criação de `validation/revL/f12_rank_partition_benchmark_validation.csv`
- criação de `validation/revL/f12_rank_partition_family_regression.csv`
- criação de `validation/revL/f12_rank_partition_generalization_eval.csv`
- criação de `validation/revL/f12_rank_partition_generalization_cases.md`
- criação de `validation/revL/f12_rank_partition_notes.md`
- atualização de `HANDOVER_CURRENT.md`, `CHANGELOG.md`, `ARTEFACTS_INDEX.md`, `RETOMA_CHECKLIST.md` e `README.md`

## 2026-04-20 — revK pareto closure
- fechamento canónico da família `F16_pareto_80`
- promoção de `generators/pareto_generator.py` para a versão canónica `revK`
- validação executável do subset benchmark `Q203/Q204/Q205`
- compatibilidade com benchmark legado: `3/3 PASS`
- medição explícita do impacto da fronteira antes/depois e do guardrail de contributos positivos
- criação de `validation/revK/f16_pareto_benchmark_validation.csv`
- criação de `validation/revK/f16_pareto_family_regression.csv`
- criação de `validation/revK/f16_pareto_generalization_eval.csv`
- criação de `validation/revK/f16_pareto_generalization_cases.md`
- criação de `validation/revK/f16_pareto_notes.md`
- generalização fora do benchmark com SQL manual independente: `8/8 PASS`
- regressão integral da família em `revK`: `14/14 PASS`
- atualização de `HANDOVER_CURRENT.md`, `CHANGELOG.md`, `ARTEFACTS_INDEX.md`, `RETOMA_CHECKLIST.md` e `README.md`
- `validation/revJ/` deixa de ser a referência canónica de Pareto e é removido para evitar redundância

## 2026-04-20 — revI lifecycle sync completion
- sincronização técnica de `revE`
- criação de `generators/lifecycle_generator.py`
- criação de `validation/revE/lifecycle_benchmark_validation.csv`
- criação de `validation/revE/lifecycle_generalization_eval.csv`
- criação de `validation/revE/lifecycle_generalization_cases.md`

## 2026-04-20 — revG technical sync
- sincronização da camada técnica canónica disponível nesta sessão
- criação de `generators/temporal_generator.py`
- criação de `validation/revD/tsql_emulator_benchmark_exec.csv`
- criação de `validation/revD/temporal_benchmark_validation.csv`
- criação de `validation/revD/temporal_generalization_eval.csv`
- criação de `validation/revD/temporal_generalization_cases.md`

## 2026-04-20 — revA
- bootstrap do repositório
- política explícita de não publicação do ZIP bruto
- reconstrução inicial do estado do projeto
- inventário estrutural seguro das fontes
- registo da divergência factual Q1-Q60
