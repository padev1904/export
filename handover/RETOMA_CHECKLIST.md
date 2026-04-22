# RETOMA CHECKLIST

## Entrada obrigatória quando a sessão pode ser um fork
1. ler `handover/FORK_RECOVERY_PROTOCOL.md`
2. ler `handover/HANDOVER_CURRENT.md`
3. ler `handover/RETOMA_CHECKLIST.md`
4. ler `handover/ARTEFACTS_INDEX.md`
5. ler `handover/CHANGELOG.md`
6. usar o bloco `RETOMA RÁPIDA` de `HANDOVER_CURRENT.md` como ponto de arranque

## Antes de continuar o projeto
1. confirmar a última revisão fechada
2. confirmar a última família fechada
3. confirmar benchmark fechado e backlog aberto
4. confirmar a próxima prioridade operacional
5. confirmar a evidência canónica da última revisão
6. confirmar se existe working set residual explícito em `validation/revX/backlog_residual_after_revW.csv`
7. confirmar se esse ficheiro já foi promovido a canónico ou se continua com `is_canonical = false`

## Regra de saída obrigatória
No final de cada resposta de progresso, incluir sempre:
`Próximos passos para a prompt de arranque`

## Próximo alvo acordado
1. não reabrir `period_compare`
2. validar documentalmente `Q77`, `Q81`, `Q118` e `Q143`
3. confirmar ou corrigir o residual de 7 linhas publicado em `validation/revX/backlog_residual_after_revW.csv`
4. só depois promover esse inventário residual a estado canónico final
5. se a hipótese residual se confirmar, fechar `time_series`
6. criar perguntas novas fora do benchmark
7. comparar SQL manual independente com SQL do gerador universal por equivalência de resultado
8. atualizar repositório canónico
