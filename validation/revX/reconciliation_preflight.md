# revX reconciliation preflight

## Objetivo
Preparar o arranque da `revX` sem confundir:
- factos já canónicos no repositório
- lacunas documentais ainda abertas
- hipóteses operacionais úteis para planeamento

Este ficheiro **não substitui** a enumeração canónica dos `qid` residuais.
Serve apenas como artefacto de preflight para a próxima sessão.

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
7. O repositório **ainda não contém** um ficheiro canónico que enumere explicitamente os `7 qid` residuais pós-`revW`.

## Evidência canónica relevante
- `handover/HANDOVER_CURRENT.md`
- `validation/revW/global_counts_after_revW.csv`
- `validation/revW/backlog_reconciliation_status.md`
- `validation/revW/period_compare_benchmark_validation.csv`

## Conjunto candidato documentado em revW
O ficheiro `validation/revW/backlog_reconciliation_status.md` indica como conjunto candidato ainda por reconciliar:

- `76`
- `77`
- `81`
- `86`
- `100`
- `114`
- `118`
- `122`
- `137`
- `138`
- `143`

Este conjunto tem `11` perguntas potenciais.
Como o backlog factual após `revW` é `7`, pelo menos `4` destas perguntas já terão sido absorvidas por evidência canónica anterior, mas essa correspondência ainda não está explicitamente enumerada no repositório.

## Hipótese operacional para preparar a revX
**Secção não canónica.**
Usar apenas como hipótese de trabalho até existir um ficheiro residual explícito por `qid`.

Hipótese operacional mais plausível para a próxima revisão:
- família universal residual principal: `time_series`
- `qid` de trabalho dessa família:
  - `86`
  - `100`
  - `114`
  - `122`
  - `137`
  - `138`
- caso especial residual fora da família principal:
  - `76` (`other` / comparação de unidades)

Candidatos de menor prioridade, possivelmente já absorvidos por evidência canónica anterior:
- `77`
- `81`
- `118`
- `143`

## Regra de utilização
1. Não promover esta hipótese a facto canónico sem reconciliação benchmark-wide.
2. Antes de fechar qualquer nova família, criar um ficheiro residual explícito por `qid`.
3. Só depois executar a `revX` sobre a próxima família universal realmente residual.

## Próxima ação obrigatória
Criar:

`validation/revX/backlog_residual_after_revW.csv`

com, no mínimo:
- `qid`
- `question`
- `family`
- `status`
- `evidence_source`
- `is_canonical`

## Recomendação operacional
1. reconciliar primeiro os `7 qid` exatos
2. se a hipótese acima se confirmar, fechar `time_series`
3. validar benchmark por equivalência de resultado
4. criar perguntas novas fora do benchmark
5. comparar SQL manual independente vs SQL do gerador
6. só depois fechar o caso especial `Q76`
