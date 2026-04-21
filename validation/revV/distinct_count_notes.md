# distinct_count notes — revV

## Estado factual
- fonte de verdade usada: repositório canónico `padev1904/export`
- última revisão canónica anterior: revU
- última família fechada antes desta revisão: rank_within_partition
- benchmark fechado antes de revV: 253/268
- backlog aberto antes de revV: 15/268

## Trabalho executado em revV
1. leitura do protocolo de fork e handover canónico
2. implementação do gerador `generators/distinct_count_generator.py`
3. execução do benchmark residual da família sobre base local derivada do `training_data.zip`
4. regressão integral das 4 perguntas residuais da família (`Q65`, `Q66`, `Q134`, `Q136`)
5. criação de 6 perguntas novas fora do benchmark com SQL manual independente
6. comparação do SQL do gerador com o SQL manual por equivalência de resultado sobre a `f_invoice_sample`
7. atualização factual da contagem global

## Resultado da família
- benchmark da família: 4/4 PASS por equivalência de resultado
- benchmark da família: 4/4 PASS em igualdade estrita de grelha
- generalização fora do benchmark: 6/6 PASS por equivalência de resultado
- generalização fora do benchmark: 6/6 PASS em igualdade estrita de grelha

## Observação importante
A revisão fecha o residual aberto identificado para `distinct_count` sem remendos pergunta-a-pergunta.
A lógica foi consolidada ao nível do gerador para três padrões universais:
- contagem distinta agrupada
- top N global por contagem distinta
- filtro `HAVING` sobre contagem distinta

## Contagem global após revV
- benchmark fechado: 257/268
- backlog aberto: 11/268
- próxima prioridade recomendada: period_compare
