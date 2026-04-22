# analyst free questions v2 — notes

## Objetivo
Criar um novo conjunto de 20 perguntas fora do benchmark, com complexidade superior ao lote anterior, formuladas como perguntas que um analista de negócio exigente e experiente poderia fazer.

## Regra metodológica desta passagem
- formulação cega à existência de famílias técnicas
- perguntas desenhadas a partir da documentação de `F_Invoice`, métricas, dimensões e relações facto-dimensão
- sem preocupação prévia com o encaixe nos geradores já existentes
- complexidade orientada para cenários analíticos reais: partições, quotas, janelas móveis, comparações entre períodos, lifecycle, cancelamentos, rácios agregados e métricas compostas

## Estado deste lote
Este ficheiro contém apenas o lote de perguntas.
Nesta passagem ainda não foi registada validação por execução/comparação de resultados para `B01`–`B20`.

## Critério de complexidade
O lote foi construído para ser, em média, mais exigente do que `analyst_free_questions_v1`, incluindo mais combinações simultâneas de:
- dimensão indireta
- bucket temporal
- partição interna
- métrica derivada
- regra documental implícita
