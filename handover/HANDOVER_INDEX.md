# Handover index

## Objetivo
Este repositório é o ponto de retoma do projeto universal de Text-to-SQL para SQL Server.

## Política de segurança
- Não copiar `training_data.zip`.
- Não publicar dados de negócio brutos.
- Manter apenas documentação derivada, artefactos textuais seguros, backlog, matrizes e perguntas de teste sem dados sensíveis.

## Ler primeiro numa nova sessão
1. `README.md`
2. `handover/STATE_RECONSTRUCTED_2026-04-20.md`
3. `handover/SAFE_SOURCE_MANIFEST.md`
4. `handover/VERIFIED_RULES_FROM_SOURCE_2026-04-20.md`
5. `handover_atualizado_2026-04-20_revD.md`
6. `checklist_retoma_sessao_2026-04-20_revD.md`

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
- A divergência Q1–Q60 continua explícita: matriz factual aponta 58 PASS e 2 NO_GENERATOR até reconciliação.
- O bloco Q61–Q150 está mapeado por famílias.
- A referência executável atual para o bloco temporal é a revisão `revD`.
- Próximas famílias prioritárias: `F17_lifecycle`, `F16_pareto_80`, `F12_rank_within_partition`, `F18_multi_metric_topn`.

## Regra de ouro
Em caso de conflito entre resumo narrativo e matriz factual, prevalece a matriz factual até reconciliação explícita.
