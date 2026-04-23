# HANDOVER NEXT STEP — analyst_free_questions_v2 expansion

## Contexto
Existe um lote de 20 perguntas fora do benchmark (`B01`–`B20`) formulado em linguagem de analista sénior, sem partir do catálogo de famílias técnicas.

## Estado já confirmado
- lote criado em `validation/revY/analyst_free_questions_v2.csv`
- os 4 casos já suportados anteriormente mantêm-se válidos
- `WS4` ficou agora sincronizado canonicamente em `generators/rank_partition_generator.py`
- a reexecução com o código canónico gravado confirmou equivalência `6/6` para `B02`, `B08`, `B10`, `B12`, `B14`, `B18`
- o estado operacional canónico do lote `analyst_free_questions_v2` passa a `10/20` cobertas e `10/20` em gap

## Objetivo da próxima sessão
Abrir `WS1` (`nested share / partition share`) em `generators/percentage_share_generator.py`, reexecutar a validação usando o código canónico gravado e só depois atualizar novamente o estado operacional do lote `analyst_free_questions_v2`.

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
Implementar `WS1` para cobrir `B03`, `B11` e `B19`, começando por quota por entidade dentro de partição explícita, com suporte a `current_year`, `last_12_months`, bucket mensal e métricas com `requires_additional`.

## Saída mínima esperada da próxima sessão
- atualização de `generators/percentage_share_generator.py`
- SQL manual esperado para `B03`, `B11`, `B19`
- SQL gerado novamente a partir do código canónico já gravado
- reexecução local e comparação por equivalência
- atualização coerente de `HANDOVER_CURRENT.md`, `ARTEFACTS_INDEX.md`, `CHANGELOG.md` e `validation/revY/analyst_free_questions_v2_gap_matrix.csv`

## Regra crítica
Não reabrir benchmark fechado. Esta linha permanece fora do benchmark salvo decisão explícita em contrário.
