# ARTEFACTS INDEX

## Documentação canónica
- `README.md`
- `handover/HANDOVER_CURRENT.md`
- `handover/CHANGELOG.md`
- `handover/SAFE_SOURCE_MANIFEST.md`
- `handover/RETOMA_CHECKLIST.md`
- `handover/ARTEFACTS_INDEX.md`
- `repo_structure/REPO_STRUCTURE_CANONICAL.md`

## Camada técnica canónica
- `generators/temporal_generator.py`
- `generators/lifecycle_generator.py`
- `generators/pareto_generator.py`
- `generators/rank_partition_generator.py`
- `generators/f18_multi_metric_topn_generator.py`
- `generators/topn_cross_filter_generator.py`
- `validation/revD/`
- `validation/revE/`
- `validation/revK/`
- `validation/revL/`
- `validation/revM/`
- `validation/revN/`
- `validation/revO/global_benchmark_counts.csv`
- `validation/revO/global_benchmark_residual_summary.csv`
- `validation/revO/backlog_residual_real.md`

## Nota
`revO` não cria novo gerador; consolida o estado global real do benchmark e o backlog residual canónico.
A matriz global completa desta revisão existe como artefacto local descarregável, enquanto o repositório mantém a síntese canónica mínima para evitar crescimento redundante.
