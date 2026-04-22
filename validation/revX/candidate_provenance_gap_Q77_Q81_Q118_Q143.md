# Candidate provenance gap — Q77, Q81, Q118, Q143

## Objetivo
Registar explicitamente o resultado da tentativa de resolução documental dos 4 candidatos separados do working set residual de 7 linhas.

## Factos verificados
- o estado factual canónico do repositório mantém-se em `261/268` fechadas e `7/268` abertas
- o residual explícito de trabalho publicado em `validation/revX/backlog_residual_after_revW.csv` continua marcado com `is_canonical = false`
- a documentação canónica de topo (`README.md`, `handover/HANDOVER_CURRENT.md`, `handover/CHANGELOG.md`, `validation/revW/backlog_reconciliation_status.md`, `validation/revX/reconciliation_preflight.md`) mantém a necessidade de fechar documentalmente o estado de:
  - `Q77`
  - `Q81`
  - `Q118`
  - `Q143`

## Resultado desta passagem
Nesta passagem não foi identificada, no conjunto canónico atualmente indexado e explicitamente referenciado no repositório, prova documental suficiente para promover qualquer um destes 4 `qid` a:
- já absorvido por evidência canónica anterior
- ou ainda residual final de forma definitivamente comprovada

## Evidência adicional obtida no histórico de commits
A inspeção do histórico de commits associado aos geradores canónicos atualmente expostos no repositório mostra commits para:
- `temporal`
- `lifecycle`
- `pareto`
- `rank_partition`
- `F18 multi metric topn`
- `top_n_with_cross_filter`
- `grouped_aggregate`
- `percentage_share`
- `top_n_global`
- `top_n`
- `cancellation`
- `distinct_count`
- `period_compare`

Foi também observado um commit de remoção de um gerador obsoleto `revC`, mas esse commit removia apenas `temporal_generator_revC.py` e não constitui evidência de fecho anterior para `avg_per_document` nem para a família `other`.

No histórico inspecionado nesta passagem, não apareceu commit explícito de gerador dedicado para:
- `avg_per_document`
- `other`

## Interpretação correta
Isto é um bloqueio de proveniência documental canónica.
Não é evidência de erro nas contagens globais.
Também não é evidência suficiente para reabrir famílias já fechadas.

## Consequência operacional
- o working set residual de 7 linhas mantém-se publicado
- continua com `is_canonical = false`
- a promoção do residual a inventário canónico final permanece bloqueada até existir prova documental explícita para `Q77`, `Q81`, `Q118` e `Q143`

## Próxima ação obrigatória
Resolver a proveniência canónica destes 4 `qid` antes de promover `validation/revX/backlog_residual_after_revW.csv` a residual final canónico.
