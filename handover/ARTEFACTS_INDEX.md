# ARTEFACTS INDEX

## Documentação canónica
- README.md
- handover/HANDOVER_CURRENT.md
- handover/FORK_RECOVERY_PROTOCOL.md
- handover/CHANGELOG.md
- handover/SAFE_SOURCE_MANIFEST.md
- handover/RETOMA_CHECKLIST.md
- handover/ARTEFACTS_INDEX.md
- repo_structure/REPO_STRUCTURE_CANONICAL.md
- handover/STARTUP_PROMPT_FIXED.md

## Camada técnica canónica
- generators/temporal_generator.py
- generators/lifecycle_generator.py
- generators/pareto_generator.py
- generators/rank_partition_generator.py
- generators/f18_multi_metric_topn_generator.py
- generators/topn_cross_filter_generator.py
- generators/grouped_aggregate_generator.py
- generators/percentage_share_generator.py
- generators/topn_global_generator.py
- generators/topn_generator.py
- generators/cancellation_generator.py
- generators/distinct_count_generator.py
- generators/period_compare_generator.py
- generators/sqlserver_patterns.py
- generators/avg_per_document_generator.py

## Validação por revisão
- validation/revD/
- validation/revE/
- validation/revK/
- validation/revL/
- validation/revM/
- validation/revN/
- validation/revO/

### revP
- validation/revP/grouped_aggregate_benchmark_validation.csv
- validation/revP/grouped_aggregate_generalization_eval.csv
- validation/revP/grouped_aggregate_generalization_cases.md
- validation/revP/grouped_aggregate_notes.md
- validation/revP/global_counts_after_revP.csv

### revQ
- validation/revQ/percentage_share_benchmark_validation.csv
- validation/revQ/percentage_share_generalization_eval.csv
- validation/revQ/percentage_share_notes.md
- validation/revQ/global_counts_after_revQ.csv

### revR
- validation/revR/topn_global_benchmark_validation.csv
- validation/revR/topn_global_generalization_eval.csv
- validation/revR/topn_global_generalization_cases.md
- validation/revR/topn_global_notes.md
- validation/revR/global_counts_after_revR.csv

### revS
- validation/revS/topn_benchmark_validation.csv
- validation/revS/topn_generalization_eval.csv
- validation/revS/topn_notes.md
- validation/revS/global_counts_after_revS.csv

### revT
- validation/revT/cancellation_benchmark_validation.csv
- validation/revT/cancellation_generalization_eval.csv
- validation/revT/cancellation_generalization_cases.md
- validation/revT/cancellation_notes.md
- validation/revT/global_counts_after_revT.csv

### revU
- validation/revU/rank_partition_benchmark_validation.csv
- validation/revU/rank_partition_generalization_eval.csv
- validation/revU/rank_partition_generalization_cases.md
- validation/revU/rank_partition_notes.md
- validation/revU/global_counts_after_revU.csv

### revV
- validation/revV/distinct_count_benchmark_validation.csv
- validation/revV/distinct_count_generalization_eval.csv
- validation/revV/distinct_count_generalization_cases.md
- validation/revV/distinct_count_notes.md
- validation/revV/global_counts_after_revV.csv

### revW
- validation/revW/period_compare_benchmark_validation.csv
- validation/revW/period_compare_generalization_eval.csv
- validation/revW/period_compare_notes.md
- validation/revW/global_counts_after_revW.csv
- validation/revW/backlog_reconciliation_status.md

### revX preflight and residual reconciliation
- validation/revX/reconciliation_preflight.md
- validation/revX/backlog_residual_after_revW.csv
- validation/revX/backlog_residual_candidates_after_revW_11.csv
- validation/revX/backlog_residual_after_revW_reconciliation_note.md
- validation/revX/candidate_provenance_gap_Q77_Q81_Q118_Q143.md
- validation/revX/candidate_evidence_matrix_Q77_Q81_Q118_Q143.csv

### revY benchmark residual closure
- validation/revY/benchmark_explicit_gap_before_revY_41.csv
- validation/revY/benchmark_residual_closure_validation.csv
- validation/revY/global_counts_after_revY.csv
- validation/revY/residual_generalization_eval.csv
- validation/revY/residual_generalization_cases.csv
- validation/revY/residual_pattern_consolidation_scope.md
- validation/revY/post_closure_refactor_semantic_validation.csv
- validation/revY/post_closure_refactor_notes.md
- validation/revY/post_closure_temporal_consolidation_validation.csv
- validation/revY/post_closure_temporal_consolidation_notes.md
- validation/revY/post_closure_timeseries_cancellation_consolidation_validation.csv
- validation/revY/post_closure_timeseries_cancellation_consolidation_notes.md
- validation/revY/monthly_generalization_candidate_cases.csv
- validation/revY/monthly_generalization_candidate_notes.md

## Ponto de entrada em caso de fork
1. handover/FORK_RECOVERY_PROTOCOL.md
2. handover/HANDOVER_CURRENT.md
3. handover/RETOMA_CHECKLIST.md
4. handover/ARTEFACTS_INDEX.md
5. handover/CHANGELOG.md
