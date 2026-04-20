# Handover index

## Objetivo
Este repositório é o ponto de retoma do projeto universal de Text-to-SQL para SQL Server.

## Política de segurança
- Não copiar `training_data.zip`.
- Não publicar dados de negócio brutos.
- Manter apenas documentação derivada, artefactos textuais seguros, backlog, matrizes e perguntas de teste sem dados sensíveis.

## Ler primeiro numa nova sessão
1. `handover/STATE_RECONSTRUCTED_2026-04-20.md`
2. `handover/KNOWN_DISCREPANCIES.md`
3. `handover/FACTS_VERIFIED_FROM_ZIP.md`
4. `handover/BACKLOG_AND_PRIORITY.md`
5. `handover/RESTART_PLAYBOOK.md`

## Artefactos estruturados preservados
- `source_artifacts/tsql_pass_matrix_q1_q60_v2.csv`
- `source_artifacts/q61_q150_family_map.csv`
- `source_artifacts/holdout_questions_v1.csv`
- `source_artifacts/holdout_questions_v2.csv`
- `source_artifacts/q61_q150_generator_playbook_v1.md`
- `source_artifacts/project_state_log_v1.md`
- `source_artifacts/family_strategy_matrix_v1.md`

## Estado operacional resumido
- Benchmark: 268 perguntas em `examples.sql`.
- Ambiente local descrito como executável para os 268 SQL oráculo.
- Q61-Q150 já mapeado por famílias.
- Prioridade operacional: `rank_within_partition`, `percentage_share`, `cancellation`, `period_compare`.

## Regra de ouro
Em caso de conflito entre resumo narrativo e matriz factual, prevalece a matriz factual até reconciliação explícita.
