# ARTEFACTS INDEX

## Objetivo
Mapear os artefactos técnicos e documentais relevantes e indicar o respetivo estado no repositório canónico.

## Estado de sincronização
### Já sincronizado no repositório
#### Documentação canónica
- `README.md`
- `handover/HANDOVER_CURRENT.md`
- `handover/CHANGELOG.md`
- `handover/SAFE_SOURCE_MANIFEST.md`
- `handover/RETOMA_CHECKLIST.md`
- `handover/ARTEFACTS_INDEX.md`
- `repo_structure/REPO_STRUCTURE_CANONICAL.md`

#### Camada técnica
- `generators/temporal_generator.py`
- `generators/lifecycle_generator.py`
- `generators/pareto_generator.py`
- `generators/rank_partition_generator.py`
- `generators/f18_multi_metric_topn_generator.py`
- `validation/revD/tsql_emulator_benchmark_exec.csv`
- `validation/revD/temporal_benchmark_validation.csv`
- `validation/revD/temporal_generalization_eval.csv`
- `validation/revD/temporal_generalization_cases.md`
- `validation/revE/lifecycle_benchmark_validation.csv`
- `validation/revE/lifecycle_generalization_eval.csv`
- `validation/revE/lifecycle_generalization_cases.md`
- `validation/revK/f16_pareto_benchmark_validation.csv`
- `validation/revK/f16_pareto_family_regression.csv`
- `validation/revK/f16_pareto_generalization_eval.csv`
- `validation/revK/f16_pareto_generalization_cases.md`
- `validation/revK/f16_pareto_notes.md`
- `validation/revL/f12_rank_partition_benchmark_validation.csv`
- `validation/revL/f12_rank_partition_family_regression.csv`
- `validation/revL/f12_rank_partition_generalization_eval.csv`
- `validation/revL/f12_rank_partition_generalization_cases.md`
- `validation/revL/f12_rank_partition_notes.md`
- `validation/revM/f18_multi_metric_topn_benchmark_validation.csv`
- `validation/revM/f18_multi_metric_topn_generalization_cases.md`
- `validation/revM/f18_multi_metric_topn_notes.md`

## Mapeamento de origem local para destino canónico
### Temporal (revD)
Destino canónico:
- `generators/temporal_generator.py`
- `validation/revD/tsql_emulator_benchmark_exec.csv`
- `validation/revD/temporal_benchmark_validation.csv`
- `validation/revD/temporal_generalization_eval.csv`
- `validation/revD/temporal_generalization_cases.md`

Estado:
- sincronizado

### Lifecycle (revE)
Destino canónico:
- `generators/lifecycle_generator.py`
- `validation/revE/lifecycle_benchmark_validation.csv`
- `validation/revE/lifecycle_generalization_eval.csv`
- `validation/revE/lifecycle_generalization_cases.md`

Estado:
- sincronizado

### Pareto 80 (revK)
Destino canónico:
- `generators/pareto_generator.py`
- `validation/revK/f16_pareto_benchmark_validation.csv`
- `validation/revK/f16_pareto_family_regression.csv`
- `validation/revK/f16_pareto_generalization_eval.csv`
- `validation/revK/f16_pareto_generalization_cases.md`
- `validation/revK/f16_pareto_notes.md`

Estado:
- sincronizado

### Rank within partition (revL)
Destino canónico:
- `generators/rank_partition_generator.py`
- `validation/revL/f12_rank_partition_benchmark_validation.csv`
- `validation/revL/f12_rank_partition_family_regression.csv`
- `validation/revL/f12_rank_partition_generalization_eval.csv`
- `validation/revL/f12_rank_partition_generalization_cases.md`
- `validation/revL/f12_rank_partition_notes.md`

Estado:
- sincronizado

### F18 multi_metric_topn (revM)
Destino canónico:
- `generators/f18_multi_metric_topn_generator.py`
- `validation/revM/f18_multi_metric_topn_benchmark_validation.csv`
- `validation/revM/f18_multi_metric_topn_generalization_cases.md`
- `validation/revM/f18_multi_metric_topn_notes.md`

Estado:
- sincronizado

## O que não deve continuar a crescer no repositório
- handovers por revisão fora da árvore `handover/`
- checklists por revisão fora da árvore `handover/`
- ZIPs de handover
- cópias redundantes do mesmo estado em múltiplos caminhos
- qualquer ficheiro bruto derivado diretamente do ZIP original
- artefactos intermédios supersedidos quando já existir a versão canónica sincronizada
