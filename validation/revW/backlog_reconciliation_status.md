# Backlog reconciliation status — revW

## Estado factual confirmado
- benchmark_total: 268
- benchmark_closed: 261
- benchmark_open: 7

Estes valores estão confirmados pelos artefactos:
- `validation/revW/global_counts_after_revW.csv`
- `validation/revW/period_compare_benchmark_validation.csv`

## Lacuna documental identificada
Antes desta atualização do repositório, não existia um inventário residual pós-revW que enumerasse explicitamente os `qid` ainda abertos.

Os artefactos técnicos comprovam a contagem global (261/268), mas não incluíam um ficheiro com a lista canónica das 7 perguntas remanescentes.

## Candidatos ainda por reconciliar
A partir do mapa de famílias conhecido do benchmark (Q61–Q150) e da evidência de validação existente, o conjunto candidato mais provável inclui:

```
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

Como o backlog real após `revW` é **7**, pelo menos **4 destas perguntas já terão sido absorvidas por evidência canónica anterior**, mas essa correspondência ainda não estava documentada explicitamente no repositório.

## Próxima ação obrigatória
Antes de iniciar `revX`, deve ser executada uma reconciliação benchmark-wide:

1. consolidar todos os `benchmark_validation.csv` existentes
2. marcar todos os `qid` já fechados por equivalência de resultado
3. isolar exatamente os **7 `qid` ainda abertos**
4. criar um ficheiro canónico:

```
validation/revX/backlog_residual_after_revW.csv
```

## Objetivo da reconciliação
Garantir que o repositório contém um inventário residual factual e verificável do benchmark antes de continuar o fecho das famílias universais.
