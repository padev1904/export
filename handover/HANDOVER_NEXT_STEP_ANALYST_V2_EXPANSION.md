# HANDOVER NEXT STEP — analyst_free_questions_v2 expansion

## Contexto
Existe um lote de 20 perguntas fora do benchmark (`B01`–`B20`) formulado em linguagem de analista sénior, sem partir do catálogo de famílias técnicas.

## Estado já confirmado
- lote criado em `validation/revY/analyst_free_questions_v2.csv`
- `WS1` ficou sincronizado canonicamente em `generators/percentage_share_generator.py`
- `WS2` ficou sincronizado canonicamente em `generators/pareto_generator.py`
- `WS3` ficou sincronizado canonicamente em `generators/lifecycle_generator.py`
- `WS4` ficou sincronizado canonicamente em `generators/rank_partition_generator.py`
- `WS5` ficou sincronizado canonicamente em `generators/cancellation_generator.py`
- `WS6` ficou sincronizado canonicamente em `generators/avg_per_document_generator.py` e `generators/period_compare_generator.py`
- a reexecução com o código canónico gravado confirmou equivalência `20/20` para `B01`–`B20`
- o estado operacional canónico do lote `analyst_free_questions_v2` passa a `20/20` cobertas e `0/20` em gap
- esta linha permanece **fora do benchmark**

## Objetivo da próxima sessão
Não reabrir `analyst_free_questions_v2` sem evidência documental explícita de regressão. A próxima sessão útil deverá preparar um novo lote cego fora do benchmark ou uma regressão dirigida adicional sobre a camada técnica canónica já consolidada.

## Entrada obrigatória
1. `handover/FORK_RECOVERY_PROTOCOL.md`
2. `handover/HANDOVER_CURRENT.md`
3. `handover/HANDOVER_NEXT_STEP_ANALYST_V2_EXPANSION.md`
4. `validation/revY/analyst_free_questions_v2_gap_matrix.csv`
5. `validation/revY/analyst_free_questions_v2_expansion_plan.md`
6. `validation/revY/analyst_free_questions_v2_ws2_equivalence_eval.csv`
7. `validation/revY/analyst_free_questions_v2_ws3_equivalence_eval.csv`
8. `validation/revY/analyst_free_questions_v2_ws5_equivalence_eval.csv`
9. `validation/revY/analyst_free_questions_v2_ws6_equivalence_eval.csv`
10. `handover/CHANGELOG.md`

## Primeira subtarefa recomendada
Criar um novo lote cego fora do benchmark, mantendo a mesma disciplina: SQL manual independente, SQL gerado pelo código canónico real e validação por equivalência na base aceite.

## Saída mínima esperada da próxima sessão
- novo lote fora do benchmark ou nova regressão dirigida documentada
- SQL manual esperado para os novos casos
- SQL gerado novamente a partir do código canónico já gravado
- reexecução local e comparação por equivalência
- atualização coerente de `HANDOVER_CURRENT.md`, `ARTEFACTS_INDEX.md`, `CHANGELOG.md` e do artefacto operacional correspondente

## Regra crítica
Não reabrir benchmark fechado. `analyst_free_questions_v2` fica agora fechado como linha canónica fora do benchmark, salvo regressão documental explícita.
