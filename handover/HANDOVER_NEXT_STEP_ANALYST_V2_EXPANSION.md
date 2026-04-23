# HANDOVER NEXT STEP — analyst_free_questions_v2 expansion

## Contexto
Existe um lote de 20 perguntas fora do benchmark (`B01`–`B20`) formulado em linguagem de analista sénior, sem partir do catálogo de famílias técnicas.

## Estado já confirmado
- lote criado em `validation/revY/analyst_free_questions_v2.csv`
- os 4 casos já suportados antes desta sessão mantêm-se válidos
- esta sessão criou artefactos de validação local para `WS4`:
  - `validation/revY/analyst_free_questions_v2_ws4_manual_sql.sql`
  - `validation/revY/analyst_free_questions_v2_ws4_generated_sql.sql`
  - `validation/revY/analyst_free_questions_v2_ws4_equivalence_eval.csv`
  - `validation/revY/analyst_free_questions_v2_ws4_notes.md`
- a validação local desta sessão confirmou equivalência `6/6` para `B02`, `B08`, `B10`, `B12`, `B14`, `B18`
- o ficheiro canónico `generators/rank_partition_generator.py` não ficou ainda sincronizado nesta sessão

## Objetivo da próxima sessão
Sincronizar primeiro `WS4` em `generators/rank_partition_generator.py`, reexecutar a validação usando o código canónico gravado e só depois atualizar o estado operacional do lote `analyst_free_questions_v2`.

## Entrada obrigatória
1. `handover/FORK_RECOVERY_PROTOCOL.md`
2. `handover/HANDOVER_CURRENT.md`
3. `handover/HANDOVER_NEXT_STEP_ANALYST_V2_EXPANSION.md`
4. `validation/revY/analyst_free_questions_v2.csv`
5. `validation/revY/analyst_free_questions_v2_gap_matrix.csv`
6. `validation/revY/analyst_free_questions_v2_expansion_plan.md`
7. `validation/revY/analyst_free_questions_v2_ws4_equivalence_eval.csv`
8. `validation/revY/analyst_free_questions_v2_ws4_notes.md`

## Primeira subtarefa recomendada
Sincronizar `WS4` em `generators/rank_partition_generator.py`, voltar a gerar SQL a partir do código canónico gravado e só então decidir se o gap operacional muda.

## Saída mínima esperada da próxima sessão
- atualização de `generators/rank_partition_generator.py`
- SQL gerado novamente a partir do código canónico já gravado
- reexecução local e comparação por equivalência
- atualização coerente de `HANDOVER_CURRENT.md`, `ARTEFACTS_INDEX.md`, `CHANGELOG.md` e `validation/revY/analyst_free_questions_v2_gap_matrix.csv`

## Regra crítica
Não reabrir benchmark fechado. Esta linha permanece fora do benchmark salvo decisão explícita em contrário.
