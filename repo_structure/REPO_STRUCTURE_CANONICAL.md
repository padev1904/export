# REPO STRUCTURE CANONICAL

## Estrutura mínima recomendada
```text
README.md
handover/
  HANDOVER_CURRENT.md
  CHANGELOG.md
  SAFE_SOURCE_MANIFEST.md
  RETOMA_CHECKLIST.md
  ARTEFACTS_INDEX.md
repo_structure/
  REPO_STRUCTURE_CANONICAL.md
generators/
  temporal_generator.py
  lifecycle_generator.py
validation/
  revD/
    tsql_emulator_benchmark_exec.csv
    temporal_benchmark_validation.csv
    temporal_generalization_eval.csv
    temporal_generalization_cases.md
  revE/
    lifecycle_benchmark_validation.csv
    lifecycle_generalization_eval.csv
    lifecycle_generalization_cases.md
```

## Princípios
- documentos canónicos sem versão no nome
- resultados de validação agrupados por revisão
- um gerador canónico por família
- nada de ZIPs de handover no repositório
- nada de dados brutos
