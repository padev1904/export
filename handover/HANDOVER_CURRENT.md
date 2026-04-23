# HANDOVER CURRENT

## RETOMA RÁPIDA
- última revisão fechada: revY
- último fecho benchmark-wide: residual benchmark closure
- última família fechada isoladamente: period_compare
- benchmark fechado: 268/268
- backlog aberto: 0/268
- próxima prioridade: preparar nova linha fora do benchmark após fecho canónico completo de `analyst_free_questions_v2`
- próximos passos:
  1. usar `validation/revY/analyst_free_questions_v2_gap_matrix.csv` como evidência de fecho operacional `20/20`
  2. tratar `B01`–`B20` como capacidade já sincronizada canonicamente nos geradores reais do repositório
  3. não reabrir `analyst_free_questions_v2` sem evidência documental explícita de regressão
  4. preparar novo lote cego fora do benchmark ou regressão dirigida pós-fecho
  5. manter validação por execução paralela na base aceite antes de promover novo estado operacional

## Nota de fork de sessão
Se houver divergência entre conversa e repositório, prevalece o repositório canónico.

Última consolidação: 2026-04-23 (analyst_free_questions_v2 fully closed; canonical-code reexecution completed)

## Estado factual consolidado
- benchmark total: 268 perguntas
- benchmark fechado com evidência canónica sincronizada: 268/268
- backlog residual atual: 0/268
- `monthly_generalization` fora do benchmark mantém-se aceite com base em `training_data/documentation/f_invoice_sample.csv`
- `analyst_free_questions_v1` mantém-se validado `10/10`
- o lote `analyst_free_questions_v2` mantém 20 perguntas fora do benchmark
- o estado canónico operacional atual para `analyst_free_questions_v2` é cobertura confirmada `20/20` e gap `0/20`
- `WS1` mantém-se sincronizado em `generators/percentage_share_generator.py`
- `WS2` ficou sincronizado em `generators/pareto_generator.py`
- `WS3` ficou sincronizado em `generators/lifecycle_generator.py`
- `WS4` mantém-se sincronizado em `generators/rank_partition_generator.py`
- `WS5` ficou sincronizado em `generators/cancellation_generator.py`
- `WS6` ficou sincronizado em `generators/avg_per_document_generator.py` e `generators/period_compare_generator.py`
- a reexecução com o código canónico gravado confirmou equivalência `20/20` entre SQL manual independente e SQL gerado, na base aceite `training_data/documentation/f_invoice_sample.csv`
- `analyst_free_questions_v2` fica fechado como linha canónica **fora do benchmark**

## Evidência canónica relevante
- `handover/HANDOVER_NEXT_STEP_ANALYST_V2_EXPANSION.md`
- `handover/CHANGELOG.md`
- `validation/revY/analyst_free_questions_v2.csv`
- `validation/revY/analyst_free_questions_v2_notes.md`
- `validation/revY/analyst_free_questions_v2_gap_matrix.csv`
- `validation/revY/analyst_free_questions_v2_expansion_plan.md`
- `validation/revY/analyst_free_questions_v2_ws1_manual_sql.sql`
- `validation/revY/analyst_free_questions_v2_ws1_generated_sql.sql`
- `validation/revY/analyst_free_questions_v2_ws1_equivalence_eval.csv`
- `validation/revY/analyst_free_questions_v2_ws1_notes.md`
- `validation/revY/analyst_free_questions_v2_ws2_manual_sql.sql`
- `validation/revY/analyst_free_questions_v2_ws2_generated_sql.sql`
- `validation/revY/analyst_free_questions_v2_ws2_equivalence_eval.csv`
- `validation/revY/analyst_free_questions_v2_ws2_notes.md`
- `validation/revY/analyst_free_questions_v2_ws3_manual_sql.sql`
- `validation/revY/analyst_free_questions_v2_ws3_generated_sql.sql`
- `validation/revY/analyst_free_questions_v2_ws3_equivalence_eval.csv`
- `validation/revY/analyst_free_questions_v2_ws3_notes.md`
- `validation/revY/analyst_free_questions_v2_ws4_manual_sql.sql`
- `validation/revY/analyst_free_questions_v2_ws4_generated_sql.sql`
- `validation/revY/analyst_free_questions_v2_ws4_equivalence_eval.csv`
- `validation/revY/analyst_free_questions_v2_ws4_notes.md`
- `validation/revY/analyst_free_questions_v2_ws5_manual_sql.sql`
- `validation/revY/analyst_free_questions_v2_ws5_generated_sql.sql`
- `validation/revY/analyst_free_questions_v2_ws5_equivalence_eval.csv`
- `validation/revY/analyst_free_questions_v2_ws5_notes.md`
- `validation/revY/analyst_free_questions_v2_ws6_manual_sql.sql`
- `validation/revY/analyst_free_questions_v2_ws6_generated_sql.sql`
- `validation/revY/analyst_free_questions_v2_ws6_equivalence_eval.csv`
- `validation/revY/analyst_free_questions_v2_ws6_notes.md`
- `generators/percentage_share_generator.py`
- `generators/pareto_generator.py`
- `generators/lifecycle_generator.py`
- `generators/rank_partition_generator.py`
- `generators/cancellation_generator.py`
- `generators/avg_per_document_generator.py`
- `generators/period_compare_generator.py`

## Nota operacional importante
- `B12` não explicita `N` no texto canónico da pergunta.
- Após sincronização final do gerador, a interpretação mantida continua a ser devolver o conjunto ordenado por partição, sem corte `TOP N`, preservando ranking interno.
- Essa interpretação continua coberta pelo código canónico sincronizado, mas esta linha permanece **fora do benchmark**.

## Próxima prioridade
1. não reabrir `analyst_free_questions_v2` sem evidência documental explícita de regressão
2. preparar novo lote cego fora do benchmark ou regressão dirigida adicional sobre a camada técnica canónica
3. manter a validação por execução paralela na base aceite
4. só depois promover novo estado operacional adicional
