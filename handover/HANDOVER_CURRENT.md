# HANDOVER CURRENT

## RETOMA RÁPIDA
- última revisão fechada: revY
- último fecho benchmark-wide: residual benchmark closure
- última família fechada isoladamente: period_compare
- benchmark fechado: 268/268
- backlog aberto: 0/268
- próxima prioridade: ampliar progressivamente a camada técnica para cobrir o lote `analyst_free_questions_v2` fora do benchmark, em blocos de capacidade reutilizável
- próximos passos:
  1. usar `validation/revY/analyst_free_questions_v2_gap_matrix.csv` como matriz operacional do gap atual
  2. seguir `validation/revY/analyst_free_questions_v2_expansion_plan.md` por workstreams, com `WS4` já fechado e `WS1` como próximo alvo recomendado
  3. preservar a regra de que esta linha é fora do benchmark e não altera `268/268`
  4. manter o bloco mensal atual congelado por estabilização, salvo evidência nova independente desta linha

## Nota de fork de sessão
Se houver divergência entre conversa e repositório, prevalece o repositório canónico.

Última consolidação: 2026-04-23 (analyst-free question set v2 WS4 closure synced)

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

### Sexta passagem pós-fecho
- criação de `validation/revY/analyst_free_questions_v1.csv`
- criação de `validation/revY/analyst_free_questions_eval_v1.csv`
- criação de `validation/revY/analyst_free_questions_notes_v1.md`
- criação de `validation/revY/analyst_free_questions_manual_sql_v1.sql`
- criação de `validation/revY/analyst_free_questions_generated_sql_v1.sql`
- novo lote de 10 perguntas formuladas a partir da documentação de `F_Invoice` e dimensões, em estilo de analista de negócio e sem partir do catálogo de famílias como critério de formulação
- execução local do SQL manual e do SQL gerado pelo código real dos geradores, com equivalência 10/10 na base aceite `f_invoice_sample.csv`

### Sétima passagem pós-fecho
- criação de `validation/revY/analyst_free_questions_v2.csv`
- criação de `validation/revY/analyst_free_questions_v2_notes.md`
- lote de 20 perguntas adicionais, mais exigentes do que os lotes anteriores, formuladas em estilo de analista sénior e sem dependência do catálogo de famílias
- cobertura por execução confirmada apenas em `4/20`
- gap real identificado em `16/20`
- criação de `validation/revY/analyst_free_questions_v2_gap_matrix.csv`
- criação de `validation/revY/analyst_free_questions_v2_expansion_plan.md`
- criação de `handover/HANDOVER_NEXT_STEP_ANALYST_V2_EXPANSION.md`
- decisão explícita: a próxima sessão deve ampliar capacidades por workstream reutilizável, começando por `WS4`

### Oitava passagem pós-fecho
- atualização de `generators/rank_partition_generator.py`
- criação de `validation/revY/analyst_free_questions_v2_ws4_manual_sql.sql`
- criação de `validation/revY/analyst_free_questions_v2_ws4_generated_sql.sql`
- criação de `validation/revY/analyst_free_questions_v2_ws4_equivalence_eval.csv`
- criação de `validation/revY/analyst_free_questions_v2_ws4_notes.md`
- atualização de `validation/revY/analyst_free_questions_v2_gap_matrix.csv`
- fecho de `WS4 — rank derived / multi-partition` na linha fora do benchmark `analyst_free_questions_v2`
- cobertura incremental confirmada por execução local em `6/6` para `B02`, `B08`, `B10`, `B12`, `B14`, `B18`
- cobertura acumulada do lote `analyst_free_questions_v2` passa para `10/20`
- gap remanescente do lote `analyst_free_questions_v2` passa para `10/20`
- nota operacional explícita: `B12` não explicita `N` no texto canónico e foi tratado nesta passagem como lista ordenada por partição sem corte `TOP N`, sem promover esse detalhe a facto documental externo ao repositório

## Evidência canónica relevante
- generators/period_compare_generator.py
- generators/sqlserver_patterns.py
- generators/avg_per_document_generator.py
- generators/topn_global_generator.py
- generators/rank_partition_generator.py
- generators/temporal_generator.py
- generators/cancellation_generator.py
- generators/lifecycle_generator.py
- generators/pareto_generator.py
- generators/percentage_share_generator.py
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
- validation/revY/analyst_free_questions_v1.csv
- validation/revY/analyst_free_questions_eval_v1.csv
- validation/revY/analyst_free_questions_notes_v1.md
- validation/revY/analyst_free_questions_manual_sql_v1.sql
- validation/revY/analyst_free_questions_generated_sql_v1.sql
- validation/revY/analyst_free_questions_v2.csv
- validation/revY/analyst_free_questions_v2_notes.md
- validation/revY/analyst_free_questions_v2_gap_matrix.csv
- validation/revY/analyst_free_questions_v2_expansion_plan.md
- validation/revY/analyst_free_questions_v2_ws4_manual_sql.sql
- validation/revY/analyst_free_questions_v2_ws4_generated_sql.sql
- validation/revY/analyst_free_questions_v2_ws4_equivalence_eval.csv
- validation/revY/analyst_free_questions_v2_ws4_notes.md
- handover/STABILIZATION_DECISION_MONTHLY_DIMENSION_REFACTOR.md
- handover/HANDOVER_NEXT_STEP_ANALYST_V2_EXPANSION.md

## Nota de reconciliação
O fecho `revY` substitui a necessidade de continuar a reconciliação residual aberta em `revX`.

O benchmark residual explícito anterior a `revY` foi enumerado em:
- `validation/revY/benchmark_explicit_gap_before_revY_41.csv`

Esse gap foi fechado benchmark-wide com validação por equivalência de resultado em:
- `validation/revY/benchmark_residual_closure_validation.csv`

## Próxima prioridade
1. ampliar capacidades para reduzir o gap `10/20` do lote `analyst_free_questions_v2`
2. `WS4` está fechado; o próximo alvo recomendado é `WS1` (`nested share / partition share`)
3. preservar a distinção entre benchmark fechado e expansão fora do benchmark
4. evitar reabertura de trabalho benchmark-wide já fechado sem nova evidência de regressão
