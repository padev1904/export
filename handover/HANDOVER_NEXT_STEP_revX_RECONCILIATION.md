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
- O repositório ainda **não contém** um ficheiro canónico com a enumeração explícita dos 7 `qid` residuais pós-`revW`.

## Divergência já conhecida
Os ficheiros de topo como `README.md`, `handover/HANDOVER_CURRENT.md` e `handover/CHANGELOG.md` ainda podem refletir o estado anterior (`revV`, `257/268`, `distinct_count`).

Não tratar esses ficheiros como estado mais recente sem os cruzar com:
- `validation/revW/global_counts_after_revW.csv`
- `validation/revW/period_compare_benchmark_validation.csv`
- `validation/revW/backlog_reconciliation_status.md`
- `validation/revX/reconciliation_preflight.md`

## Próxima prioridade operacional
Antes de fechar qualquer nova família universal, reconciliar canonicamente o inventário residual pós-`revW`.

## Tarefa imediata obrigatória
Criar:

`validation/revX/backlog_residual_after_revW.csv`

com, no mínimo, as colunas:
- `qid`
- `question`
- `family`
- `status`
- `evidence_source`
- `is_canonical`

## Método obrigatório
1. Consolidar todos os `benchmark_validation.csv` canónicos existentes no repositório.
2. Marcar todos os `qid` já fechados por equivalência de resultado.
3. Isolar exatamente os `7 qid` ainda abertos.
4. Só depois criar o CSV residual canónico.
5. Só depois decidir a próxima família universal residual a fechar.

## Regra crítica
Não promover hipóteses operacionais a factos canónicos antes da reconciliação benchmark-wide.

## Hipótese operacional útil, mas ainda não canónica
Usar apenas como pista de trabalho até existir o CSV residual explícito por `qid`.

Família universal residual mais plausível:
- `time_series`

QID de trabalho mais prováveis dessa família:
- `86`
- `100`
- `114`
- `122`
- `137`
- `138`

Caso especial residual plausível fora da família principal:
- `76`

Candidatos possivelmente já absorvidos por evidência canónica anterior, mas sem enumeração residual explícita:
- `77`
- `81`
- `118`
- `143`

## Instrução de execução
- Não duplicar trabalho já fechado.
- Não reabrir `period_compare`.
- Não assumir que os 7 residuais são exatamente os candidatos acima.
- Validar tudo contra artefactos reais do repositório.
- Só declarar backlog residual fechado quando existir ficheiro canónico explícito com os 7 `qid`.

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
5. Próxima prioridade operacional: reconciliar canonicamente o inventário residual pós-`revW`
6. Subtarefa concreta seguinte: criar `validation/revX/backlog_residual_after_revW.csv` com os 7 `qid` exatos antes de fechar a próxima família universal residual.

Regra crítica:
- Não promover hipóteses a factos canónicos sem reconciliação benchmark-wide.
- Não reabrir `period_compare`.
- Não assumir que os `qid` candidatos são os residuais finais sem evidência canónica explícita.
"""
