# revX reconciliation preflight

## Objetivo
Preparar o arranque da `revX` sem confundir:
- factos já canónicos no repositório
- lacunas documentais ainda abertas
- hipóteses operacionais úteis para planeamento

Este ficheiro continua a ser um artefacto de preflight.
Não substitui a promoção canónica final do residual por `qid`.

## Factos verificados
1. A fonte de verdade continua a ser o repositório canónico.
2. A última revisão técnica fechada é `revW`.
3. A última família fechada é `period_compare`.
4. O benchmark fechado com evidência canónica sincronizada está em `261/268`.
5. O backlog residual factual está em `7/268`.
6. A família `period_compare` ficou fechada com:
   - benchmark: `4/4 PASS` por equivalência de resultado
   - benchmark: `4/4 PASS` em igualdade estrita de grelha
   - generalização fora do benchmark: `6/6 PASS`
7. O repositório já contém um ficheiro residual explícito:
   - `validation/revX/backlog_residual_after_revW.csv`
8. Esse ficheiro permanece deliberadamente marcado com:
   - `is_canonical = false`
9. A promoção canónica final do residual ainda exige fecho benchmark-wide documentalmente explícito.

## Evidência canónica relevante
- `handover/HANDOVER_CURRENT.md`
- `validation/revW/global_counts_after_revW.csv`
- `validation/revW/backlog_reconciliation_status.md`
- `validation/revW/period_compare_benchmark_validation.csv`
- `validation/revX/backlog_residual_after_revW.csv`
- `validation/revX/backlog_residual_candidates_after_revW_11.csv`
- `validation/revX/backlog_residual_after_revW_reconciliation_note.md`

## Working set residual sincronizado
O working set residual explícito de 7 linhas publicado em `revX` contém:

- `76`
- `86`
- `100`
- `114`
- `122`
- `137`
- `138`

Todos estes registos foram publicados com:
- `status = OPEN_PROBABLE_RESIDUAL`
- `is_canonical = false`

## Candidatos ainda por fecho documental
Continuam separados como candidatos de menor prioridade, possivelmente já absorvidos por evidência canónica anterior:

- `77`
- `81`
- `118`
- `143`

## Regra de utilização
1. Não promover o working set residual a facto canónico sem reconciliação benchmark-wide fechada.
2. Antes de fechar qualquer nova família, validar documentalmente `Q77`, `Q81`, `Q118` e `Q143`.
3. Só depois confirmar ou corrigir o residual de 7 linhas.
4. Só depois promover esse residual a inventário canónico final.
5. Só depois executar a `revX` sobre a próxima família universal realmente residual.

## Recomendação operacional
1. validar primeiro os 4 candidatos ainda não resolvidos documentalmente
2. se o working set residual se confirmar, fechar `time_series`
3. validar benchmark por equivalência de resultado
4. criar perguntas novas fora do benchmark
5. comparar SQL manual independente vs SQL do gerador
6. só depois fechar o caso especial `Q76`
