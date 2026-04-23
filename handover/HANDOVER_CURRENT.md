# HANDOVER CURRENT

## RETOMA RÁPIDA
- última revisão fechada: revY
- último fecho benchmark-wide: residual benchmark closure
- última família fechada isoladamente: period_compare
- benchmark fechado: 268/268
- backlog aberto: 0/268
- próxima prioridade: WS3 (`lifecycle` segmentado com janelas parametrizáveis) no lote `analyst_free_questions_v2`, após fecho canónico do `WS1`
- próximos passos:
  1. usar `validation/revY/analyst_free_questions_v2_gap_matrix.csv` como matriz operacional de trabalho
  2. tratar `B02`, `B08`, `B10`, `B12`, `B14`, `B18` como capacidade já sincronizada canonicamente em `generators/rank_partition_generator.py`
  3. tratar `B03`, `B11`, `B19` como capacidade já sincronizada canonicamente em `generators/percentage_share_generator.py`
  4. abrir `WS3` para `B05`, `B16`
  5. manter validação por execução paralela na base aceite antes de promover novo estado operacional

## Nota de fork de sessão
Se houver divergência entre conversa e repositório, prevalece o repositório canónico.

Última consolidação: 2026-04-23 (WS1 synced in canonical percentage_share generator; canonical-code reexecution completed)

## Estado factual consolidado
- benchmark total: 268 perguntas
- benchmark fechado com evidência canónica sincronizada: 268/268
- backlog residual atual: 0/268
- `monthly_generalization` fora do benchmark mantém-se aceite com base em `training_data/documentation/f_invoice_sample.csv`
- `analyst_free_questions_v1` mantém-se validado `10/10`
- o lote `analyst_free_questions_v2` mantém 20 perguntas fora do benchmark
- o estado canónico operacional atual para `analyst_free_questions_v2` é cobertura confirmada `13/20` e gap `7/20`
- os casos `B02`, `B08`, `B10`, `B12`, `B14`, `B18` mantêm-se sincronizados em `generators/rank_partition_generator.py`
- os casos `B03`, `B11`, `B19` foram sincronizados em `generators/percentage_share_generator.py`
- a reexecução com o código canónico gravado confirmou equivalência `3/3` entre SQL manual independente e SQL gerado, na base aceite `training_data/documentation/f_invoice_sample.csv`, para `B03`, `B11`, `B19`
- `WS1` fica fechado como capacidade canónica **fora do benchmark**
- `WS4` mantém-se fechado como capacidade canónica **fora do benchmark**

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
- `validation/revY/analyst_free_questions_v2_ws4_manual_sql.sql`
- `validation/revY/analyst_free_questions_v2_ws4_generated_sql.sql`
- `validation/revY/analyst_free_questions_v2_ws4_equivalence_eval.csv`
- `validation/revY/analyst_free_questions_v2_ws4_notes.md`
- `generators/percentage_share_generator.py`
- `generators/rank_partition_generator.py`

## Nota operacional importante
- `B12` não explicita `N` no texto canónico da pergunta.
- Após sincronização final do gerador, a interpretação mantida continua a ser devolver o conjunto ordenado por partição, sem corte `TOP N`, preservando ranking interno.
- Essa interpretação continua coberta pelo código canónico sincronizado, mas esta linha permanece **fora do benchmark**.

## Próxima prioridade
1. abrir `WS3` em `generators/lifecycle_generator.py`
2. cobrir `B05`, `B16` com lifecycle segmentado por dimensão e janelas parametrizáveis
3. reexecutar localmente a validação usando o código canónico já gravado
4. só depois decidir se a prioridade seguinte passa a `WS5` (`cancellation` por dimensão indireta e bucket trimestral)
