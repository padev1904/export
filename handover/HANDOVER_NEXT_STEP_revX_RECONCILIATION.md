# Handover — próximo passo após revW

## Regra de prioridade
A fonte de verdade é o repositório canónico.

Se houver divergência entre conversa anterior, README, handover antigo e artefactos de validação mais recentes, prevalecem os artefactos canónicos mais recentes do repositório.

## Leitura obrigatória no arranque
Ler por esta ordem:

1. `handover/FORK_RECOVERY_PROTOCOL.md`
2. `handover/HANDOVER_CURRENT.md`
3. `handover/RETOMA_CHECKLIST.md`
4. `handover/ARTEFACTS_INDEX.md`
5. `handover/CHANGELOG.md`
6. `validation/revW/backlog_reconciliation_status.md`
7. `validation/revX/reconciliation_preflight.md`
8. `handover/HANDOVER_NEXT_STEP_revX_RECONCILIATION.md`

## Estado factual confirmado
- A última revisão técnica fechada é `revW`.
- A última família fechada é `period_compare`.
- O benchmark fechado com evidência canónica sincronizada está em `261/268`.
- O backlog residual factual está em `7/268`.
- O repositório já contém `validation/revX/backlog_residual_after_revW.csv`, mas esse ficheiro continua explicitamente marcado como não canónico (`is_canonical = false`).

## Divergência já resolvida
Os ficheiros de topo como `README.md`, `handover/HANDOVER_CURRENT.md` e `handover/CHANGELOG.md` já foram sincronizados com o estado pós-`revW` e com o working set residual da `revX`.

## Próxima prioridade operacional
Antes de fechar qualquer nova família universal, consolidar documentalmente o inventário residual pós-`revW` e só depois promovê-lo a canónico.

## Tarefa imediata obrigatória
Validar documentalmente:
- `Q77`
- `Q81`
- `Q118`
- `Q143`

E decidir se:
- já estão absorvidos por evidência canónica anterior
- ou se algum deles deve regressar ao residual explícito de `revX`

## Método obrigatório
1. Consolidar toda a evidência canónica relevante já existente no repositório.
2. Fechar documentalmente o estado de `Q77`, `Q81`, `Q118` e `Q143`.
3. Confirmar ou corrigir `validation/revX/backlog_residual_after_revW.csv`.
4. Só depois promover esse CSV a inventário residual canónico final.
5. Só depois decidir a próxima família universal residual a fechar.

## Regra crítica
Não promover hipóteses operacionais a factos canónicos antes da reconciliação benchmark-wide.

## Working set residual atual
Usar como working set explícito, ainda não canónico:

Família universal residual mais plausível:
- `time_series`

QID de trabalho atuais dessa família:
- `86`
- `100`
- `114`
- `122`
- `137`
- `138`

Caso especial residual fora da família principal:
- `76`

Candidatos ainda por fecho documental:
- `77`
- `81`
- `118`
- `143`

## Instrução de execução
- Não duplicar trabalho já fechado.
- Não reabrir `period_compare`.
- Não assumir que o working set de 7 linhas já é o residual canónico final.
- Validar tudo contra artefactos reais do repositório.
- Só declarar backlog residual fechado quando o CSV residual estiver explicitamente promovido a canónico.

## Prompt de arranque sugerida para a próxima sessão
"""
Consulta o repositório canónico `https://github.com/padev1904/export.git`.

Esta sessão pode ser um fork criado pela edição de uma instrução antiga.
Não assumes que a conversa atual contém o estado mais recente.
A fonte de verdade é o repositório.

Lê e segue, por esta ordem:
1. `handover/FORK_RECOVERY_PROTOCOL.md`
2. `handover/HANDOVER_CURRENT.md`
3. `handover/RETOMA_CHECKLIST.md`
4. `handover/ARTEFACTS_INDEX.md`
5. `handover/CHANGELOG.md`
6. `validation/revW/backlog_reconciliation_status.md`
7. `validation/revX/reconciliation_preflight.md`
8. `handover/HANDOVER_NEXT_STEP_revX_RECONCILIATION.md`

Depois reconstitui o estado real, identifica a próxima prioridade em aberto a partir da documentação canónica do repositório e prossegue sem duplicar trabalho já fechado.

Se houver divergência entre conversa e repositório, prevalece o repositório.

Estado factual já confirmado:
1. Última revisão técnica fechada: `revW`
2. Última família fechada: `period_compare`
3. Benchmark fechado: `261/268`
4. Backlog aberto: `7/268`
5. Próxima prioridade operacional: consolidar e promover o inventário residual pós-`revW` a enumeração canónica final
6. Subtarefa concreta seguinte: validar documentalmente `Q77`, `Q81`, `Q118` e `Q143` antes de promover `validation/revX/backlog_residual_after_revW.csv` a inventário residual canónico final

Regra crítica:
- Não promover hipóteses a factos canónicos sem reconciliação benchmark-wide fechada.
- Não reabrir `period_compare`.
- Não assumir que o working set residual de 7 linhas já é o residual final sem evidência canónica explícita.
"""
