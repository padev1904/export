# Nota de reconciliação — backlog residual após revW

Este artefacto foi criado a partir da evidência canónica atualmente disponível no repositório em:
- handover/HANDOVER_CURRENT.md
- handover/CHANGELOG.md
- validation/revW/backlog_reconciliation_status.md
- validation/revX/reconciliation_preflight.md
- handover/HANDOVER_NEXT_STEP_revX_RECONCILIATION.md

## Importante
- O repositório confirma canonicamente as contagens globais após `revW`: **261 fechadas / 7 abertas**.
- O repositório também confirma canonicamente que ainda não existia um ficheiro residual explícito por `qid` após `revW`.
- O CSV de 7 linhas criado nesta revisão é, por isso, um **working set reconciliado de melhor esforço**, e não uma enumeração residual já fechada canonicamente.
- As linhas permanecem marcadas com `is_canonical = false` até existir reconciliação benchmark-wide concluída contra toda a evidência de fecho anterior.

## Objetivo operacional
- fixar um ponto de trabalho explícito para `revX`
- evitar reabertura de famílias já fechadas (`period_compare` incluída)
- separar factos verificados de hipótese operacional residual
