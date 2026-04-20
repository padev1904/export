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
- `validation/revD/tsql_emulator_benchmark_exec.csv`
- `validation/revD/temporal_benchmark_validation.csv`
- `validation/revD/temporal_generalization_eval.csv`
- `validation/revD/temporal_generalization_cases.md`
- `validation/revE/lifecycle_benchmark_validation.csv`
- `validation/revE/lifecycle_generalization_eval.csv`
- `validation/revE/lifecycle_generalization_cases.md`
- `validation/revJ/pareto_benchmark_subset.csv`
- `validation/revJ/pareto_benchmark_notes.md`

## Mapeamento de origem local para destino canónico
### Temporal (revD)
Origem local existente:
- `revd_artifacts_2026-04-20/temporal_generator_revD.py`
- `revd_artifacts_2026-04-20/tsql_emulator_benchmark_exec_revD.csv`
- `revd_artifacts_2026-04-20/temporal_generator_revD_benchmark_validation.csv`
- `revd_artifacts_2026-04-20/temporal_generator_revD_generalization_eval.csv`
- `revd_artifacts_2026-04-20/temporal_generator_revD_generalization_cases.md`

Destino canónico no repositório:
- `generators/temporal_generator.py`
- `validation/revD/tsql_emulator_benchmark_exec.csv`
- `validation/revD/temporal_benchmark_validation.csv`
- `validation/revD/temporal_generalization_eval.csv`
- `validation/revD/temporal_generalization_cases.md`

Estado:
- sincronizado

### Lifecycle (revE)
Origem local existente:
- `lifecycle_generator_revE.py`
- `lifecycle_benchmark_validation_revE.csv`
- `lifecycle_generalization_eval_revE.csv`
- `lifecycle_generalization_cases_revE.md`

Destino canónico no repositório:
- `generators/lifecycle_generator.py`
- `validation/revE/lifecycle_benchmark_validation.csv`
- `validation/revE/lifecycle_generalization_eval.csv`
- `validation/revE/lifecycle_generalization_cases.md`

Estado:
- sincronizado

### Pareto 80 (revJ)
Origem local existente nesta sessão:
- `pareto_revJ_2026-04-20/F16_pareto_80_SPEC_revJ.md`
- `pareto_revJ_2026-04-20/pareto_generator_revJ.py`
- `pareto_revJ_2026-04-20/pareto_benchmark_subset_revJ.csv`
- `pareto_revJ_2026-04-20/pareto_benchmark_oracle_notes_revJ.md`
- `pareto_revJ_2026-04-20/handover_delta_revJ_F16_start.md`

Destino canónico no repositório:
- `generators/pareto_generator.py`
- `validation/revJ/pareto_benchmark_subset.csv`
- `validation/revJ/pareto_benchmark_notes.md`

Estado:
- sincronizado parcialmente
- falta ainda adicionar validação executável da família e casos de generalização fora do benchmark

## O que não deve continuar a crescer no repositório
- handovers por revisão fora da árvore `handover/`
- checklists por revisão
- ZIPs de handover
- cópias redundantes do mesmo estado em múltiplos caminhos
- qualquer ficheiro bruto derivado diretamente do ZIP original
