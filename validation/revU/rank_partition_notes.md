# rank_within_partition notes — revU

## Estado factual
- fonte de verdade usada: repositório canónico `padev1904/export`
- última revisão canónica anterior: revT
- última família fechada antes desta revisão: cancellation
- benchmark fechado antes de revU: 226/268
- backlog aberto antes de revU: 42/268

## Trabalho executado em revU
1. leitura do protocolo de fork e handover canónico
2. validação do gerador `generators/rank_partition_generator.py`
3. execução do benchmark da família sobre base local derivada do `training_data.zip`
4. correção da direção de ordenação para métricas de desconto:
   - `qty_discount`
   - `promo_discount_total`
5. regressão integral das perguntas da família
6. criação de 6 perguntas novas fora do benchmark com SQL manual independente
7. comparação do SQL do gerador com o SQL manual sobre a `f_invoice_sample`

## Resultado da família
- benchmark da família: 27/27 PASS por equivalência de resultado
- benchmark da família: 26/27 PASS em igualdade estrita de grelha
- diferença estrita remanescente:
  - Q108: diferença apenas no alias da métrica (`DiferencaPrecoListaVsLiquido` vs alias do oráculo)
- generalização fora do benchmark: 6/6 PASS por equivalência de resultado

## Observação importante
Foi detetada uma tensão entre:
- contagem global canónica 226/268 antes de revU
- contagens por bloco herdadas em `HANDOVER_CURRENT.md`

Se se assumir que as 27 perguntas desta família ainda não estavam fechadas, a nova contagem global passa para:
- benchmark fechado: 253/268
- backlog aberto: 15/268

As contagens por bloco precisam de reconciliação explícita numa revisão factual posterior se continuarem a aparecer inconsistentes.
