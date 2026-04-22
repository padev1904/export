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
- última revisão fechada: revY
- último fecho benchmark-wide: residual benchmark closure
- última família fechada isoladamente: period_compare
- benchmark fechado com evidência canónica sincronizada: 268/268
- backlog residual atual: 0/268
- próxima prioridade operacional: consolidar/refatorar em camada técnica canónica os padrões residuais fechados em `revY` e manter validação fora do benchmark para travar overfit

## Nota importante
Se houver divergência entre conversa e repositório, prevalece sempre o repositório canónico.

Os artefactos `revX` e `revW` mantêm valor histórico de reconciliação, mas não prevalecem sobre o fecho benchmark-wide já sincronizado em `revY`.

Para a evidência canónica mais recente, ver:
- `handover/HANDOVER_CURRENT.md`
- `validation/revY/benchmark_explicit_gap_before_revY_41.csv`
- `validation/revY/benchmark_residual_closure_validation.csv`
- `validation/revY/global_counts_after_revY.csv`
- `validation/revY/residual_generalization_eval.csv`
- `validation/revY/residual_generalization_cases.csv`

## Próxima ação recomendada
1. confirmar coerência documental do repositório pós-`revY`
2. consolidar/refatorar em camada técnica canónica os padrões residuais fechados em `revY`
3. manter e expandir validação fora do benchmark para os arquétipos agora cobertos
4. atualizar o repositório canónico no fim de cada revisão
