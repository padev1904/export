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
- próxima prioridade operacional: reconciliar inventário residual factual pós-revW e preparar a revX

## Nota importante
O estado canónico já está sincronizado para `revW`, mas a enumeração explícita dos `7 qid` residuais ainda não existe como ficheiro canónico dedicado.

Para a preparação da próxima revisão, ver:
- `validation/revW/backlog_reconciliation_status.md`
- `validation/revX/reconciliation_preflight.md`
