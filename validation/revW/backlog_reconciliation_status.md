# Backlog reconciliation status — revW

## Estado factual confirmado
- benchmark_total: 268
- benchmark_closed: 261
- benchmark_open: 7

Estes valores estão confirmados pelos artefactos:
- `validation/revW/global_counts_after_revW.csv`
- `validation/revW/period_compare_benchmark_validation.csv`

## Lacuna documental original
Antes da sincronização residual da `revX`, não existia um inventário residual pós-revW que enumerasse explicitamente os `qid` ainda abertos.

Os artefactos técnicos comprovavam a contagem global (261/268), mas não incluíam um ficheiro com a lista residual explícita.

## Conjunto candidato inicialmente documentado
A partir do mapa de famílias conhecido do benchmark (Q61–Q150) e da evidência de validação existente, o conjunto candidato mais provável era:

```text
76
77
81
86
100
114
118
122
137
138
143
```

Este conjunto contém 11 perguntas potenciais.

Como o backlog real após `revW` é **7**, pelo menos **4 destas perguntas já terão sido absorvidas por evidência canónica anterior**, mas essa correspondência não estava documentada explicitamente no repositório.

## Estado após sincronização de revX
Foi agora criado:

`validation/revX/backlog_residual_after_revW.csv`

com um working set residual explícito de 7 linhas.

Foram também criados:
- `validation/revX/backlog_residual_candidates_after_revW_11.csv`
- `validation/revX/backlog_residual_after_revW_reconciliation_note.md`

## Regra crítica mantida
O ficheiro residual de 7 linhas foi publicado com:
- `is_canonical = false`

Logo:
- fixa um conjunto de trabalho reconciliado
- não fecha ainda a prova canónica final do residual
- não substitui a necessidade de reconciliação benchmark-wide documentalmente concluída

## Próxima ação obrigatória
Antes de iniciar o fecho da próxima família universal, deve ser validado documentalmente o estado de:
- `77`
- `81`
- `118`
- `143`

Só depois:
1. confirmar ou corrigir o residual de 7 linhas
2. promover `validation/revX/backlog_residual_after_revW.csv` a inventário residual canónico final
3. decidir a próxima família universal residual a fechar

## Objetivo da reconciliação
Garantir que o repositório contém um inventário residual factual, verificável e explicitamente promovido a canónico do benchmark antes de continuar o fecho das famílias universais.
