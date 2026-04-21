# revT — cancellation closure

## Resultado factual
- família fechada: cancellation
- benchmark da família: 8/8 PASS
- generalização fora do benchmark: 6/6 PASS

## QIDs do benchmark cobertos
- 61, 62, 63, 93, 104, 116, 125, 127

## Estratégia universal
1. deduplicar ao nível de `BillingDocument`
2. marcar `DocumentoCancelado = MAX(CASE WHEN BillingDocumentIsCancelled = 1 THEN 1 ELSE 0 END)`
3. agregar por mês e/ou dimensão
4. calcular `TaxaCancelamento = 100.0 * SUM(DocumentoCancelado) / NULLIF(COUNT(*), 0)`
5. para top N dentro do mês, aplicar `ROW_NUMBER() OVER (PARTITION BY Mes ORDER BY TaxaCancelamento DESC, TotalDocumentos DESC, Label)`

## Regra crítica
- não aplicar o filtro global `BillingDocumentIsCancelled = 0` nesta família
- as taxas são calculadas sobre documentos deduplicados e não sobre linhas de fatura

## Contagem global após a revisão
- benchmark fechado: 226/268
- backlog aberto: 42/268
