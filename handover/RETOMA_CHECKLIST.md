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
6. se existirem artefactos históricos de reconciliação em `revX` ou `revW`, tratá-los como históricos quando divergirem de `revY`
7. não reabrir trabalho benchmark-wide já fechado sem evidência documental explícita de regressão
8. sincronizar primeiro a documentação canónica se houver divergência interna entre `README.md`, `HANDOVER_CURRENT.md` e os artefactos `validation/revY/*`

## Regra de saída obrigatória
No final de cada resposta de progresso, incluir sempre:
`Próximos passos para a prompt de arranque`

## Próximo alvo acordado
1. não reabrir `period_compare`
2. não reabrir o residual benchmark-wide fechado em `revY` sem evidência documental explícita de regressão
3. confirmar coerência documental do repositório pós-`revY`
4. consolidar/refatorar em camada técnica canónica os padrões residuais fechados em `revY`
5. manter perguntas novas fora do benchmark para os arquétipos residuais agora cobertos
6. comparar SQL manual independente com SQL do gerador universal por equivalência de resultado nos novos padrões
7. atualizar repositório canónico
