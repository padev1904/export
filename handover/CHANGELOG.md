# CHANGELOG

## 2026-04-22 — monthly generalization candidate set for post-revY temporal archetypes
- criação de `validation/revY/monthly_generalization_candidate_cases.csv`
- criação de `validation/revY/monthly_generalization_candidate_notes.md`
- atualização de `handover/ARTEFACTS_INDEX.md`
- preparação explícita de casos fora do benchmark para os arquétipos mensais recém-consolidados
- estes casos ficam marcados como `pending_execution` e não são promovidos a PASS/FAIL canónico sem comparação por equivalência de resultado
- foco dos candidatos:
  - mensal por `grupo de contas de cliente`
  - mensal por `organização de vendas`
  - mensal por `tipo de processamento de devolução`
  - métrica `list_minus_net`
  - janelas de `ano atual`, `ano corrente`, ano explícito e últimos 6 meses

## 2026-04-22 — post-revY monthly dimension closure within time series consolidation
- atualização de `generators/temporal_generator.py`
- atualização de `validation/revY/post_closure_timeseries_cancellation_consolidation_validation.csv`
- atualização de `validation/revY/post_closure_timeseries_cancellation_consolidation_notes.md`
- atualização de `handover/HANDOVER_CURRENT.md`
- extensão da consolidação temporal mensal para cobrir os casos que tinham ficado inicialmente fora do âmbito do `temporal_generator`
- cobertura dirigida adicional nesta passagem sobre:
  - `Q100`
  - `Q114`
  - `Q122`
  - `Q137`
- consolidação de suporte mensal explícito por ano para:
  - `grupo de contas de cliente`
  - `organização de vendas`
  - `tipo de processamento de devolução`
  - métrica `list_minus_net`
- sem evidência documental de regressão do estado canónico `268/268`

## 2026-04-22 — post-revY time series and cancellation consolidation pass
- atualização de `generators/sqlserver_patterns.py`
- atualização de `generators/temporal_generator.py`
- atualização de `generators/cancellation_generator.py`
- criação de `validation/revY/post_closure_timeseries_cancellation_consolidation_validation.csv`
- criação de `validation/revY/post_closure_timeseries_cancellation_consolidation_notes.md`
- atualização de `handover/ARTEFACTS_INDEX.md`
- atualização de `handover/HANDOVER_CURRENT.md`
- consolidação técnica dirigida sobre padrões temporais mensais e cancelamento mensal por dimensão já fechados benchmark-wide em `revY`
- validação dirigida nesta passagem sobre:
  - `Q61`, `Q62`, `Q86`, `Q104`, `Q125`, `Q138`, `Q144`
- clarificação explícita de que alguns casos mensais por dimensão permanecem fora do âmbito do `temporal_generator` atual e exigem consolidação posterior
- sem evidência documental de regressão do estado canónico `268/268`

## 2026-04-22 — post-revY temporal consolidation pass
- atualização de `generators/sqlserver_patterns.py`
- atualização de `generators/topn_global_generator.py`
- atualização de `generators/rank_partition_generator.py`
- criação de `validation/revY/post_closure_temporal_consolidation_validation.csv`
- criação de `validation/revY/post_closure_temporal_consolidation_notes.md`
- atualização de `handover/ARTEFACTS_INDEX.md`
- consolidação técnica dirigida sobre variantes `current_year` e `last_12_months` já fechadas benchmark-wide em `revY`
- validação dirigida nesta passagem sobre:
  - `Q180`, `Q181`, `Q183`, `Q184`, `Q186`, `Q187`, `Q224`, `Q225`, `Q226`
  - `Q191`, `Q192`, `Q193`, `Q194`, `Q195`, `Q196`
- sem evidência documental de regressão do estado canónico `268/268`

## 2026-04-22 — post-revY technical consolidation pass
- criação de `generators/sqlserver_patterns.py`
- criação de `generators/avg_per_document_generator.py` em versão funcional mínima
- atualização de `generators/lifecycle_generator.py` para sintaxe temporal coerente com T-SQL
- criação de `validation/revY/post_closure_refactor_semantic_validation.csv`
- criação de `validation/revY/post_closure_refactor_notes.md`
- atualização de `handover/ARTEFACTS_INDEX.md`
- consolidação técnica dirigida sobre padrões temporais e `avg_per_document` já fechados benchmark-wide em `revY`
- validação dirigida nesta passagem sobre:
  - `Q118`, `Q143`, `Q218`, `Q219`, `Q220`
  - `Q206`, `Q208`, `Q211`, `Q212`, `Q213`, `Q214`, `Q215`, `Q216`, `Q217`
- mantida a distinção entre esta consolidação técnica e uma eventual validação benchmark-wide futura
- sem evidência documental de regressão do estado canónico `268/268`

## 2026-04-22 — post-revY repo coherence sync
- atualização de `README.md`
- atualização de `handover/RETOMA_CHECKLIST.md`
- atualização de `handover/ARTEFACTS_INDEX.md`
- criação de `validation/revY/residual_pattern_consolidation_scope.md`
- sincronização dos documentos canónicos ainda presos no estado pré-`revY`
- clarificação explícita de que `revX` e `revW` permanecem como histórico de reconciliação e não prevalecem sobre o fecho benchmark-wide já sincronizado em `revY`
- explicitação do próximo bloco técnico útil pós-`revY`: consolidar/refatorar em camada técnica canónica os padrões residuais agora fechados, sem reabrir benchmark já encerrado

## 2026-04-22 — revY benchmark residual closure
- criação de `validation/revY/benchmark_explicit_gap_before_revY_41.csv`
- criação de `validation/revY/benchmark_residual_closure_validation.csv`
- criação de `validation/revY/global_counts_after_revY.csv`
- criação de `validation/revY/residual_generalization_eval.csv`
- criação de `validation/revY/residual_generalization_cases.csv`
- atualização de `handover/ARTEFACTS_INDEX.md`
- atualização de `handover/HANDOVER_CURRENT.md`
- fechamento benchmark-wide do residual explícito anterior a `revY`
- validação do gap de `41 qid` por equivalência de resultado face aos SQL-oráculo do benchmark
- atualização factual da contagem global para `268/268` fechadas e `0/268` abertas
- validação adicional fora do benchmark para os padrões residuais fechados: `10/10 PASS`

## 2026-04-22 — revX provenance-gap note
- criação de `validation/revX/candidate_provenance_gap_Q77_Q81_Q118_Q143.md`
- atualização de `handover/ARTEFACTS_INDEX.md`
- atualização de `handover/HANDOVER_CURRENT.md`
- registo explícito de que a passagem atual não identificou prova documental canónica suficiente, no conjunto canónico atualmente indexado, para fechar a proveniência de `Q77`, `Q81`, `Q118` e `Q143`
- clarificação de que o bloqueio remanescente é de proveniência documental e não de fecho técnico de famílias já concluídas

## 2026-04-22 — revX residual working set sync
- criação de `validation/revX/backlog_residual_after_revW.csv`
- criação de `validation/revX/backlog_residual_candidates_after_revW_11.csv`
- criação de `validation/revX/backlog_residual_after_revW_reconciliation_note.md`
- atualização de `README.md`
- atualização de `handover/HANDOVER_CURRENT.md`
- atualização de `handover/RETOMA_CHECKLIST.md`
- atualização de `handover/ARTEFACTS_INDEX.md`
- atualização de `validation/revW/backlog_reconciliation_status.md`
- atualização de `validation/revX/reconciliation_preflight.md`
- atualização de `handover/HANDOVER_NEXT_STEP_revX_RECONCILIATION.md`
- sincronização explícita do working set residual no repositório
- manutenção da distinção entre:
  - contagem factual já canónica (`261/268`, backlog `7/268`)
  - enumeração residual de trabalho ainda não promovida a canónica
- próxima ação obrigatória: fechar documentalmente o estado de `Q77`, `Q81`, `Q118` e `Q143` antes de promover o residual de 7 linhas a inventário canónico final

## 2026-04-22 — revX preflight repo sync
- sincronização de `README.md` com o estado canónico pós-`revW`
- criação de `validation/revX/reconciliation_preflight.md`
- atualização de `handover/HANDOVER_CURRENT.md` para referenciar o artefacto de preflight da `revX`
- atualização de `handover/ARTEFACTS_INDEX.md` com o artefacto `revX`
- separação explícita entre:
  - factos verificados
  - hipóteses operacionais de trabalho
  - lacunas documentais ainda abertas
- mantida a regra factual de que os `7 qid` residuais exatos continuam por enumerar canonicamente

## 2026-04-22 — revW period_compare closure
- fechamento canónico da família period_compare
- benchmark da família: 4/4 PASS por equivalência de resultado
- benchmark da família: 4/4 PASS em igualdade estrita de grelha
- generalização fora do benchmark: 6/6 PASS
- criação de generators/period_compare_generator.py
- criação de validation/revW/period_compare_benchmark_validation.csv
- criação de validation/revW/period_compare_generalization_eval.csv
- criação de validation/revW/period_compare_notes.md
- criação de validation/revW/global_counts_after_revW.csv
- atualização factual da contagem global para 261/268 fechadas e 7/268 abertas

## 2026-04-22 — handover sync after revW repo audit
- atualização de handover/HANDOVER_CURRENT.md para refletir estado revW
- atualização de handover/ARTEFACTS_INDEX.md com artefactos revW
- criação de validation/revW/backlog_reconciliation_status.md
- documentação da necessidade de reconciliação benchmark-wide para identificar os 7 `qid` ainda abertos

## 2026-04-22 — revV distinct_count closure
- fechamento canónico da família distinct_count
- benchmark da família: 4/4 PASS por equivalência de resultado
- benchmark da família: 4/4 PASS em igualdade estrita de grelha
- generalização fora do benchmark: 6/6 PASS
- criação de generators/distinct_count_generator.py
- criação de validation/revV/distinct_count_benchmark_validation.csv
- criação de validation/revV/distinct_count_generalization_eval.csv
- criação de validation/revV/distinct_count_generalization_cases.md
- criação de validation/revV/distinct_count_notes.md
- criação de validation/revV/global_counts_after_revV.csv
- atualização factual da contagem global para 257/268 fechadas e 11/268 abertas
- próxima prioridade factual: period_compare

## 2026-04-21 — revU rank_within_partition closure
- fechamento canónico da família rank_within_partition
- benchmark da família: 27/27 PASS por equivalência de resultado
- benchmark da família: 26/27 PASS em igualdade estrita de grelha
- diferença estrita remanescente: Q108 com alias divergente mas resultado equivalente
- generalização fora do benchmark: 6/6 PASS
- atualização de generators/rank_partition_generator.py
- criação de validation/revU/rank_partition_benchmark_validation.csv
- criação de validation/revU/rank_partition_generalization_eval.csv
- criação de validation/revU/rank_partition_generalization_cases.md
- criação de validation/revU/rank_partition_notes.md
- criação de validation/revU/global_counts_after_revU.csv
- atualização factual da contagem global para 253/268 fechadas e 15/268 abertas, assumindo não sobreposição das 27 perguntas da família

## 2026-04-21 — revT cancellation closure
- fechamento canónico da família cancellation
- benchmark da família: 8/8 PASS
- generalização fora do benchmark: 6/6 PASS
- criação de generators/cancellation_generator.py
- criação de validation/revT/cancellation_benchmark_validation.csv
- criação de validation/revT/cancellation_generalization_eval.csv
- criação de validation/revT/cancellation_generalization_cases.md
- criação de validation/revT/cancellation_notes.md
- criação de validation/revT/global_counts_after_revT.csv
- atualização factual da contagem global para 226/268 fechadas e 42/268 abertas

## 2026-04-21 — revS top_n closure
- fechamento canónico da família top_n
- benchmark da família: 6/6 PASS
- generalização fora do benchmark: 6/6 PASS
- criação de generators/topn_generator.py
- criação de validation/revS/topn_benchmark_validation.csv
- criação de validation/revS/topn_generalization_eval.csv
- criação de validation/revS/topn_notes.md
- criação de validation/revS/global_counts_after_revS.csv
- atualização factual da contagem global para 218/268 fechadas e 50/268 abertas

## 2026-04-21 — revR top_n_global closure
- fechamento canónico da família top_n_global
- benchmark da família: 12/12 PASS
- generalização fora do benchmark: 6/6 PASS
- criação de generators/topn_global_generator.py
- criação de validation/revR/topn_global_benchmark_validation.csv
- criação de validation/revR/topn_global_generalization_eval.csv
- criação de validation/revR/topn_global_generalization_cases.md
- criação de validation/revR/topn_global_notes.md
- criação de validation/revR/global_counts_after_revR.csv
- atualização factual da contagem global para 212/268 fechadas e 56/268 abertas

## 2026-04-21 — revQ percentage_share closure
- fechamento canónico da família percentage_share
- benchmark da família: 20/20 PASS
- generalização fora do benchmark: 6/6 PASS
- criação de generators/percentage_share_generator.py
- criação de validation/revQ/percentage_share_benchmark_validation.csv
- criação de validation/revQ/percentage_share_generalization_eval.csv
- criação de validation/revQ/percentage_share_generalization_cases.md
- criação de validation/revQ/percentage_share_notes.md
- criação de validation/revQ/global_counts_after_revQ.csv
- atualização factual da contagem global para 204/268 fechadas e 64/268 abertas

## 2026-04-21 — revP grouped_aggregate closure
- fechamento canónico da família grouped_aggregate
- benchmark da família: 40/40 PASS
- generalização fora do benchmark: 6/6 PASS
- criação de generators/grouped_aggregate_generator.py
- criação de validation/revP/grouped_aggregate_benchmark_validation.csv
- criação de validation/revP/grouped_aggregate_generalization_eval.csv
- criação de validation/revP/grouped_aggregate_generalization_cases.md
- criação de validation/revP/grouped_aggregate_notes.md
- criação de validation/revP/global_counts_after_revP.csv
- atualização factual da contagem global para 187/268 fechadas e 81/268 abertas

## 2026-04-21 — revO benchmark residual inventory
- criação do inventário residual factual do benchmark após revN
- consolidação factual: benchmark fechado com evidência canónica = 147/268
- backlog residual atual = 121/268

## 2026-04-21 — revN Q32/Q34 reconciliation
- fechamento canónico do arquétipo top_n_with_cross_filter
- benchmark da família: 2/2 PASS
- generalização fora do benchmark: 6/6 PASS
