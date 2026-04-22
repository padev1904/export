# Universal T-SQL handover repository

Repositório de continuidade do projeto de geração universal de T-SQL para SQL Server.

## Objetivo
Preservar contexto, decisões, estado validado, backlog e artefactos seguros do projeto, sem publicar dados de negócio brutos.

## Prompt de arranque
A prompt de arranque é fixa.
A versão canónica vive em:
- `handover/STARTUP_PROMPT_FIXED.md`

## Entrada recomendada em caso de fork de sessão
Ler sempre por esta ordem:
1. `handover/FORK_RECOVERY_PROTOCOL.md`
2. `handover/HANDOVER_CURRENT.md`
3. `handover/RETOMA_CHECKLIST.md`
4. `handover/ARTEFACTS_INDEX.md`
5. `handover/CHANGELOG.md`

## Estado atual resumido
- benchmark: 268 perguntas
- última revisão fechada: revW
- última família fechada: period_compare
- benchmark fechado com evidência canónica sincronizada: 261/268
- backlog residual consolidado: 7/268
- próxima prioridade operacional: consolidar e promover o inventário residual pós-`revW` a enumeração canónica final, sem reabrir trabalho já fechado

## Nota importante
O repositório já contém um artefacto residual explícito para a `revX`:

- `validation/revX/backlog_residual_after_revW.csv`

Esse ficheiro fixa um conjunto residual de trabalho com 7 linhas, mas permanece marcado com:
- `is_canonical = false`

até existir reconciliação benchmark-wide documentalmente fechada contra toda a evidência canónica anterior.

Para contexto adicional da reconciliação, ver também:
- `validation/revX/backlog_residual_candidates_after_revW_11.csv`
- `validation/revX/backlog_residual_after_revW_reconciliation_note.md`
- `validation/revX/reconciliation_preflight.md`

## Próxima ação recomendada
1. confirmar ou invalidar documentalmente a absorção anterior de `Q77`, `Q81`, `Q118` e `Q143`
2. promover o residual de 7 linhas a enumeração canónica apenas quando essa prova estiver fechada
3. se a hipótese residual se mantiver, fechar a família `time_series`
