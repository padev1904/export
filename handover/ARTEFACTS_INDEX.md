# ARTEFACTS INDEX

## Objetivo
Mapear os artefactos técnicos já gerados e indicar onde vivem ou devem viver no repositório canónico.

## Estado de sincronização
### Já sincronizado no repositório
- `generators/temporal_generator.py`
- `validation/revD/tsql_emulator_benchmark_exec.csv`
- `validation/revD/temporal_benchmark_validation.csv`
- `validation/revD/temporal_generalization_eval.csv`
- `validation/revD/temporal_generalization_cases.md`

### Ainda pendente de sincronização técnica
- `generators/lifecycle_generator.py`
- `validation/revE/lifecycle_benchmark_validation.csv`
- `validation/revE/lifecycle_generalization_eval.csv`
- `validation/revE/lifecycle_generalization_cases.md`

Nota:
- nesta sessão foi criado `validation/revE/PENDING_SYNC_NOTE.md` para manter a lacuna explícita e evitar falsa sensação de completude

## Geradores
### Temporal
Ficheiro local existente:
- `temporal_generator_revD.py`

Destino canónico no repositório:
- `generators/temporal_generator.py`

Estado:
- sincronizado

### Lifecycle
Ficheiro local esperado:
- `lifecycle_generator_revE.py`

Destino canónico no repositório:
- `generators/lifecycle_generator.py`

Estado:
- pendente de sincronização nesta sessão

## Validação
### revD
Ficheiros locais existentes:
- `tsql_emulator_benchmark_exec_revD.csv`
- `temporal_generator_revD_benchmark_validation.csv`
- `temporal_generator_revD_generalization_eval.csv`
- `temporal_generator_revD_generalization_cases.md`

Destino canónico:
- `validation/revD/tsql_emulator_benchmark_exec.csv`
- `validation/revD/temporal_benchmark_validation.csv`
- `validation/revD/temporal_generalization_eval.csv`
- `validation/revD/temporal_generalization_cases.md`

Estado:
- sincronizado

### revE
Ficheiros locais esperados:
- `lifecycle_benchmark_validation_revE.csv`
- `lifecycle_generalization_eval_revE.csv`
- `lifecycle_generalization_cases_revE.md`

Destino canónico:
- `validation/revE/lifecycle_benchmark_validation.csv`
- `validation/revE/lifecycle_generalization_eval.csv`
- `validation/revE/lifecycle_generalization_cases.md`

Estado:
- pendente de sincronização nesta sessão

## Documentos históricos que não devem continuar a crescer
- handovers por revisão no topo do repositório
- checklists por revisão
- ZIPs de handover
