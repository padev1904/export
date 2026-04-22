# analyst free questions v2 — execution gap notes

## Objetivo
Avaliar o lote `B01`–`B20` apenas do ponto de vista de execução de SQL gerado pelo estado atual dos geradores universais, e medir no fim o gap real de capacidade.

## Regra desta passagem
- sem escrever SQL manual esperado para o lote `v2`
- sem expandir geradores nesta sessão
- apenas medir o que o código atual suporta com exatidão suficiente para execução material

## Base de evidência usada
- `training_data/documentation/f_invoice_sample.csv`
- dimensões `.json` necessárias da mesma `training_data.zip`
- motor SQLite local com tradução mecânica do subconjunto T-SQL necessário para os casos executados

## Resultado agregado
- suporte exato com execução material: 4/20
- gap total identificado: 16/20

## Casos com suporte exato e execução bem-sucedida
- `B04`
- `B06`
- `B13`
- `B17`

## Tipos principais de gap observados
1. falta de partições compostas adicionais (`canal + mês`, `organização + mês`, `trimestre`)
2. falta de métricas compostas específicas em ranking (`peso líquido médio por unidade`, crescimento em janelas móveis)
3. falta de suporte lifecycle por dimensão além de `organização de vendas`
4. suporte parcial/semântico insuficiente em casos onde o código atual simplifica a pergunta e perde uma dimensão pedida
5. ausência de alguns buckets temporais exigidos pelo lote (`trimestre`, janelas móveis comparativas mais ricas)

## Leitura operacional
O lote `v2` funciona como stress test cego à modelação existente.
O resultado `4/20` mostra que o motor atual já responde a uma parte relevante do espaço analítico avançado, mas ainda está longe de cobrir de forma robusta perguntas livres de analista sénior com múltiplas condições simultâneas.
