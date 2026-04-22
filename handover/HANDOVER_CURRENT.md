# HANDOVER CURRENT

## RETOMA RÁPIDA
- última revisão fechada: revW
- última família fechada: period_compare
- benchmark fechado: 261/268
- backlog aberto: 7/268
- próxima prioridade: reconciliar inventário residual factual pós-revW
- próximos passos:
  1. identificar exatamente as 7 perguntas ainda abertas no benchmark
  2. reconciliar o inventário residual real por `qid`
  3. mapear cada pergunta à família correta
  4. preparar a próxima revisão (`revX`)
  5. fechar a próxima família universal sem overfit
  6. criar perguntas novas fora do benchmark
  7. comparar SQL manual independente com SQL do gerador universal por equivalência de resultado
  8. atualizar repositório canónico no fim da revisão

## Nota de fork de sessão
Se houver divergência entre conversa e repositório, prevalece o repositório canónico.

Última consolidação: 2026-04-22 (revW period_compare closed; handover sync after repo audit; revX preflight note added)

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

## Nota de reconciliação
Os artefactos técnicos de revW estão sincronizados no repositório.
A enumeração exata dos 7 `qid` ainda abertos continua a exigir reconciliação benchmark-wide porque o repositório não tinha, até esta atualização, um inventário residual pós-revW explicitamente enumerado por pergunta.

Foi acrescentado o artefacto `validation/revX/reconciliation_preflight.md` para separar claramente:
- factos verificados
- hipóteses operacionais de trabalho
- próxima ação obrigatória

Esse artefacto é de preflight e **não substitui** a enumeração canónica ainda em falta.

## Próxima prioridade
1. reconciliar inventário residual factual pós-revW
2. identificar exatamente os 7 `qid` ainda abertos
3. criar `validation/revX/backlog_residual_after_revW.csv`
4. preparar `revX` com foco na próxima família universal realmente residual
