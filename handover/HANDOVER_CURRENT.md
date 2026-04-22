# HANDOVER CURRENT

## RETOMA RÁPIDA
- última revisão fechada: revW
- última família fechada: period_compare
- benchmark fechado: 261/268
- backlog aberto: 7/268
- próxima prioridade: fechar a lacuna de proveniência documental de `Q77`, `Q81`, `Q118` e `Q143` antes de promover o residual de 7 linhas a inventário canónico final
- próximos passos:
  1. resolver documentalmente o estado de `Q77`, `Q81`, `Q118` e `Q143`
  2. confirmar se o working set residual de 7 linhas resiste à reconciliação benchmark-wide
  3. promover o inventário residual a estado canónico apenas após essa validação
  4. preparar a próxima revisão (`revX`)
  5. fechar a próxima família universal realmente residual sem overfit
  6. criar perguntas novas fora do benchmark
  7. comparar SQL manual independente com SQL do gerador universal por equivalência de resultado
  8. atualizar repositório canónico no fim da revisão

## Nota de fork de sessão
Se houver divergência entre conversa e repositório, prevalece o repositório canónico.

Última consolidação: 2026-04-22 (revX residual working set synced to repo; provenance gap on Q77/Q81/Q118/Q143 explicitly documented)

## Estado factual consolidado
- benchmark total: 268 perguntas
- benchmark fechado com evidência canónica sincronizada: 261/268
- backlog residual atual: 7/268

## Fecho da última revisão técnica
- família fechada: period_compare
- benchmark da família: 4/4 PASS por equivalência de resultado
- benchmark da família: 4/4 PASS em igualdade estrita de grelha
- generalização fora do benchmark: 6/6 PASS

## Evidência canónica relevante
- generators/period_compare_generator.py
- validation/revW/period_compare_benchmark_validation.csv
- validation/revW/period_compare_generalization_eval.csv
- validation/revW/period_compare_notes.md
- validation/revW/global_counts_after_revW.csv
- validation/revW/backlog_reconciliation_status.md
- validation/revX/reconciliation_preflight.md
- validation/revX/backlog_residual_after_revW.csv
- validation/revX/backlog_residual_candidates_after_revW_11.csv
- validation/revX/backlog_residual_after_revW_reconciliation_note.md
- validation/revX/candidate_provenance_gap_Q77_Q81_Q118_Q143.md

## Nota de reconciliação
Os artefactos técnicos de revW estão sincronizados no repositório.

O repositório contém um ficheiro residual explícito por `qid`:
- `validation/revX/backlog_residual_after_revW.csv`

No entanto, esse ficheiro foi deliberadamente publicado com:
- `is_canonical = false`

porque a prova benchmark-wide que distingue definitivamente o residual real de 7 linhas dos 4 candidatos ainda por resolver documentalmente continua em falta.

A tentativa de resolver esses 4 candidatos nesta passagem ficou registada em:
- `validation/revX/candidate_provenance_gap_Q77_Q81_Q118_Q143.md`

## Próxima prioridade
1. resolver documentalmente `Q77`, `Q81`, `Q118` e `Q143`
2. confirmar ou corrigir o working set residual de 7 linhas
3. só depois promover `validation/revX/backlog_residual_after_revW.csv` a inventário residual canónico final
4. preparar `revX` com foco na próxima família universal realmente residual
