# ARTEFACTS INDEX

## Objetivo
Mapear os artefactos técnicos já gerados e indicar onde devem viver no repositório canónico.

## Geradores
### Temporal
Ficheiro local existente:
- `temporal_generator_revD.py`

Destino recomendado no repositório:
- `generators/temporal_generator.py`

### Lifecycle
Ficheiro local existente:
- `lifecycle_generator_revE.py`

Destino recomendado no repositório:
- `generators/lifecycle_generator.py`

## Validação
### revD
Ficheiros locais existentes:
- `tsql_emulator_benchmark_exec_revD.csv`
- `temporal_generator_revD_benchmark_validation.csv`
- `temporal_generator_revD_generalization_eval.csv`
- `temporal_generator_revD_generalization_cases.md`

Destino recomendado:
- `validation/revD/tsql_emulator_benchmark_exec.csv`
- `validation/revD/temporal_benchmark_validation.csv`
- `validation/revD/temporal_generalization_eval.csv`
- `validation/revD/temporal_generalization_cases.md`

### revE
Ficheiros locais existentes:
- `lifecycle_benchmark_validation_revE.csv`
- `lifecycle_generalization_eval_revE.csv`
- `lifecycle_generalization_cases_revE.md`

Destino recomendado:
- `validation/revE/lifecycle_benchmark_validation.csv`
- `validation/revE/lifecycle_generalization_eval.csv`
- `validation/revE/lifecycle_generalization_cases.md`

## Documentos históricos que não devem continuar a crescer
- handovers por revisão no topo do repositório
- checklists por revisão
- ZIPs de handover
