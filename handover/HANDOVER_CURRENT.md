# HANDOVER CURRENT

## RETOMA RÁPIDA
- última revisão fechada: revY
- último fecho benchmark-wide: residual benchmark closure
- última família fechada isoladamente: period_compare
- benchmark fechado: 268/268
- backlog aberto: 0/268
- próxima prioridade: manter a distinção entre benchmark fechado e validação fora do benchmark já aceite com base em `f_invoice_sample.csv`, sem nova refatoração estrutural do bloco mensal salvo evidência nova
- próximos passos:
  1. usar `validation/revY/monthly_generalization_eval.csv` como evidência aceite para `MG01`–`MG08`
  2. preservar a regra de que esta aceitação é fora do benchmark e não altera `268/268`
  3. tratar o bloco mensal atual como congelado por estabilização, salvo regressão ou novo conjunto material de casos
  4. manter o repositório canónico sincronizado sempre que houver nova revisão

## Nota de fork de sessão
Se houver divergência entre conversa e repositório, prevalece o repositório canónico.

Última consolidação: 2026-04-22 (monthly generalization accepted on sufficient sample basis; monthly block frozen for stabilization)

## Estado factual consolidado
- benchmark total: 268 perguntas
- benchmark fechado com evidência canónica sincronizada: 268/268
- backlog residual atual: 0/268

## Fecho da última revisão técnica
- revisão fechada: revY
- natureza do fecho: benchmark-wide residual closure sobre o gap explícito de `41 qid`
- benchmark residual validado: 41/41 PASS por equivalência de resultado
- generalização adicional fora do benchmark para os padrões residuais: 10/10 PASS

## Última família fechada isoladamente
- família fechada: period_compare
- benchmark da família: 4/4 PASS por equivalência de resultado
- benchmark da família: 4/4 PASS em igualdade estrita de grelha
- generalização fora do benchmark: 6/6 PASS

## Consolidação técnica pós-`revY` já sincronizada
### Primeira passagem pós-fecho
- criação de `generators/sqlserver_patterns.py`
- criação de `generators/avg_per_document_generator.py` em versão funcional mínima
- atualização de `generators/lifecycle_generator.py` para sintaxe temporal coerente com T-SQL
- validação dirigida em `validation/revY/post_closure_refactor_semantic_validation.csv`

### Segunda passagem pós-fecho
- atualização de `generators/sqlserver_patterns.py`
- atualização de `generators/topn_global_generator.py`
- atualização de `generators/rank_partition_generator.py`
- validação dirigida em `validation/revY/post_closure_temporal_consolidation_validation.csv`
- notas em `validation/revY/post_closure_temporal_consolidation_notes.md`

### Terceira passagem pós-fecho
- atualização de `generators/sqlserver_patterns.py`
- atualização de `generators/temporal_generator.py`
- atualização de `generators/cancellation_generator.py`
- validação dirigida em `validation/revY/post_closure_timeseries_cancellation_consolidation_validation.csv`
- notas em `validation/revY/post_closure_timeseries_cancellation_consolidation_notes.md`
- extensão posterior da mesma passagem para cobrir também:
  - `Q100`
  - `Q114`
  - `Q122`
  - `Q137`

### Quarta passagem pós-fecho
- criação de `validation/revY/monthly_generalization_candidate_cases.csv`
- criação de `validation/revY/monthly_generalization_candidate_notes.md`
- atualização de `generators/temporal_generator.py` para aceitar formulações mensais com `ano atual` / `ano corrente` / `este ano`
- criação de `validation/revY/monthly_generalization_candidate_parser_validation.csv`
- candidatos `MG01`–`MG08` ficam com `parser_ok=1` e `sql_shape_ok=1`
- criação de `validation/revY/monthly_generalization_manual_oracle_sql.sql`

### Quinta passagem pós-fecho
- criação de `validation/revY/monthly_generalization_local_sample_equivalence_eval.csv`
- criação de `validation/revY/monthly_generalization_local_sample_equivalence_notes.md`
- `MG01`–`MG08` equivalentes em amostra local sobre `training_data/documentation/f_invoice_sample.csv`
- criação de `validation/revY/monthly_generalization_acceptance_notes.md`
- criação de `validation/revY/monthly_generalization_eval.csv`
- por decisão operacional desta sessão, `f_invoice_sample.csv` é aceite como suficientemente amplo para esta linha de validação fora do benchmark
- `MG01`–`MG08` ficam aceites como PASS fora do benchmark com base nessa amostra
- criação de `handover/STABILIZATION_DECISION_MONTHLY_DIMENSION_REFACTOR.md`
- decisão explícita de não avançar agora com nova refatoração estrutural do bloco mensal

## Evidência canónica relevante
- generators/period_compare_generator.py
- generators/sqlserver_patterns.py
- generators/avg_per_document_generator.py
- generators/topn_global_generator.py
- generators/rank_partition_generator.py
- generators/temporal_generator.py
- generators/cancellation_generator.py
- generators/lifecycle_generator.py
- validation/revY/benchmark_explicit_gap_before_revY_41.csv
- validation/revY/benchmark_residual_closure_validation.csv
- validation/revY/global_counts_after_revY.csv
- validation/revY/residual_generalization_eval.csv
- validation/revY/residual_generalization_cases.csv
- validation/revY/post_closure_refactor_semantic_validation.csv
- validation/revY/post_closure_refactor_notes.md
- validation/revY/post_closure_temporal_consolidation_validation.csv
- validation/revY/post_closure_temporal_consolidation_notes.md
- validation/revY/post_closure_timeseries_cancellation_consolidation_validation.csv
- validation/revY/post_closure_timeseries_cancellation_consolidation_notes.md
- validation/revY/monthly_generalization_candidate_cases.csv
- validation/revY/monthly_generalization_candidate_notes.md
- validation/revY/monthly_generalization_candidate_parser_validation.csv
- validation/revY/monthly_generalization_manual_oracle_sql.sql
- validation/revY/monthly_generalization_local_sample_equivalence_eval.csv
- validation/revY/monthly_generalization_local_sample_equivalence_notes.md
- validation/revY/monthly_generalization_acceptance_notes.md
- validation/revY/monthly_generalization_eval.csv
- handover/STABILIZATION_DECISION_MONTHLY_DIMENSION_REFACTOR.md

## Nota de reconciliação
O fecho `revY` substitui a necessidade de continuar a reconciliação residual aberta em `revX`.

O benchmark residual explícito anterior a `revY` foi enumerado em:
- `validation/revY/benchmark_explicit_gap_before_revY_41.csv`

Esse gap foi fechado benchmark-wide com validação por equivalência de resultado em:
- `validation/revY/benchmark_residual_closure_validation.csv`

## Próxima prioridade
1. manter a distinção entre benchmark fechado e generalização fora do benchmark aceite nesta amostra
2. não refatorar o bloco mensal sem evidência nova de valor
3. evitar reabertura de trabalho benchmark-wide já fechado sem nova evidência de regressão
4. continuar a atualizar o repositório canónico no fim de cada revisão
