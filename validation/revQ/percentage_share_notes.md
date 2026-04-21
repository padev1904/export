# Percentage share notes — revQ

## Fecho factual local
- família trabalhada: percentage_share
- benchmark executado nesta revisão: 20/20 PASS
- generalização fora do benchmark: 6/6 PASS

## Padrões estabilizados
1. percentagens e quotas em escala 0–100
2. uso obrigatório de `NULLIF` no denominador
3. rácios agregados por `SUM()/SUM()` em vez de médias linha a linha
4. aplicação do filtro `BillingDocumentIsCancelled = 0` por defeito
5. aplicação do filtro `IsItAnAdditionalCalculatedRecord = 1` quando a medida é `GrossMargin` ou `NetCommercialSales`
6. quotas por partição com `SUM(...) OVER (PARTITION BY ...)`
7. quando a pergunta é rácio por entidade, o rácio é calculado depois da agregação da entidade

## Cobertura benchmark desta revisão
- Q60, Q80, Q87, Q91, Q98, Q106, Q113, Q124, Q129, Q133, Q140, Q146, Q197, Q198, Q199, Q200, Q201, Q202, Q245, Q246

## Generalização verificada fora do benchmark
- quota da faturação do mês atual por canal
- quota dos últimos 12 meses por região
- preço médio líquido por unidade por marca com exclusão de quantidade total zero
- percentagem de margem bruta por marca com registos adicionais calculados
- quota de faturação de cada país dentro de cada organização de vendas
- percentagem do desconto promocional total sobre a faturação por mês nos últimos 6 meses

## Contagem global após revQ
- benchmark total: 268
- benchmark fechado: 204
- backlog aberto: 64

## Próxima prioridade recomendada
1. top_n_global
2. top_n
3. cancellation
4. rank_within_partition
