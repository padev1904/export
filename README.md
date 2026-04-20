# Universal T-SQL handover repository

Repositório de preservação de contexto para o projeto de geração universal de T-SQL sobre SQL Server.

## Política de conteúdo
Este repositório não deve receber o ficheiro `training_data.zip` nem dados de negócio brutos. Apenas deve conter:
- documentação derivada
- inventário estrutural
- regras estabilizadas
- backlog e estado de validação
- artefactos textuais seguros

## Estado verificado nesta sessão
- Existe um `training_data.zip` com `ddl/`, `documentation/` e `example_queries/`.
- O ZIP contém 8 ficheiros Markdown de documentação, 45 ficheiros JSON de dimensões, `f_invoice_sample.csv` e `examples.sql`.
- `examples.sql` contém 268 blocos `-- Question:`.
- O bloco Q61-Q150 já tem mapeamento de famílias e playbook SQL Server.
- Existem dois conjuntos hold-out anexos nesta sessão: `holdout_questions_v1` e `holdout_questions_v2`, ambos com 12 perguntas.

## Nota importante
Foi detetada uma divergência factual entre artefactos anexos:
- o handover resume Q1-Q60 como 60/60 fechadas
- a matriz `tsql_pass_matrix_q1_q60_v2.csv` anexada mostra 58 PASS e 2 NO_GENERATOR (Q32 e Q34)

Até reconciliação, esta divergência deve ser mantida visível e não escondida.
