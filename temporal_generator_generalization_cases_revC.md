# Casos de generalização — revC

Cada caso abaixo usa uma pergunta nova fora do benchmark e um SQL manual independente para comparação com o gerador universal.

## G01 — Qual é a evolução mensal da faturação por família de produto nos últimos 6 meses?

```sql
SELECT
    f.MonthStart AS Mes,
    pf.TProductFamily AS FamiliaProduto,
    SUM(f.NetAmount) AS ValorLiquidoFaturado
FROM F_Invoice f
JOIN D_Product p
  ON p.NIDProduct = f.NIDProduct
JOIN D_ProductFamily pf
  ON pf.NIDProductFamily = p.NIDProductFamily
WHERE f.BillingDocumentIsCancelled = 0
  AND f.BillingDocumentDate BETWEEN 20251101 AND 20260420
GROUP BY f.MonthStart, pf.TProductFamily
ORDER BY Mes ASC, FamiliaProduto ASC;
```

## G02 — Como evoluiu mensalmente a margem bruta por canal de distribuição no último semestre móvel?

```sql
WITH monthly_margin AS (
    SELECT
        f.MonthStart AS Mes,
        dc.TDistributionChannel AS Canal,
        SUM(f.GrossMargin) AS MargemBruta
    FROM F_Invoice f
    JOIN D_DistributionChannel dc
      ON dc.NIDDistributionChannel = f.NIDDistributionChannel
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.IsItAnAdditionalCalculatedRecord = 1
      AND f.BillingDocumentDate >= 20251101
      AND f.BillingDocumentDate <= 20260420
    GROUP BY f.MonthStart, dc.TDistributionChannel
)
SELECT *
FROM monthly_margin
ORDER BY Mes, Canal;
```

## G03 — Qual a rolling average de 3 meses da faturação por marca?

```sql
WITH sales_by_brand AS (
    SELECT
        f.MonthStart AS Mes,
        pb.TProductBrand AS Marca,
        SUM(f.NetAmount) AS ValorLiquidoFaturado
    FROM F_Invoice f
    JOIN D_Product p
      ON p.NIDProduct = f.NIDProduct
    JOIN D_ProductBrand pb
      ON pb.NIDProductBrand = p.NIDProductBrand
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= 20250901
      AND f.BillingDocumentDate <= 20260420
    GROUP BY f.MonthStart, pb.TProductBrand
)
SELECT
    Mes,
    Marca,
    ValorLiquidoFaturado,
    AVG(ValorLiquidoFaturado) OVER (
        PARTITION BY Marca
        ORDER BY Mes
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS MediaMovel3Meses
FROM sales_by_brand
ORDER BY Mes, Marca;
```

## G04 — Qual é o acumulado mensal YTD da faturação por canal no ano atual?

```sql
WITH monthly_sales AS (
    SELECT
        f.MonthStart AS Mes,
        dc.TDistributionChannel AS Canal,
        SUM(f.NetAmount) AS ValorLiquidoFaturado
    FROM F_Invoice f
    JOIN D_DistributionChannel dc
      ON dc.NIDDistributionChannel = f.NIDDistributionChannel
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingYear = 2026
      AND f.BillingDocumentDate <= 20260420
    GROUP BY f.MonthStart, dc.TDistributionChannel
)
SELECT
    Mes,
    Canal,
    ValorLiquidoFaturado,
    SUM(ValorLiquidoFaturado) OVER (
        PARTITION BY Canal
        ORDER BY Mes
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS ValorLiquidoFaturadoYTD
FROM monthly_sales
ORDER BY Mes, Canal;
```

## G05 — Qual é o crescimento da faturação por marca no mês atual face ao mesmo mês do ano anterior?

```sql
SELECT
    pb.TProductBrand AS Marca,
    SUM(CASE
        WHEN f.BillingDocumentDate >= 20260401
         AND f.BillingDocumentDate < 20260501
        THEN f.NetAmount ELSE 0 END) AS ValorMesAtual,
    SUM(CASE
        WHEN f.BillingDocumentDate >= 20250401
         AND f.BillingDocumentDate < 20250501
        THEN f.NetAmount ELSE 0 END) AS ValorMesmoMesAnoAnterior,
    SUM(CASE
        WHEN f.BillingDocumentDate >= 20250401
         AND f.BillingDocumentDate < 20250501
        THEN f.NetAmount ELSE 0 END) AS BaseComparacao,
    CASE
        WHEN SUM(CASE
            WHEN f.BillingDocumentDate >= 20250401
             AND f.BillingDocumentDate < 20250501
            THEN f.NetAmount ELSE 0 END) = 0 THEN NULL
        ELSE ((SUM(CASE
            WHEN f.BillingDocumentDate >= 20260401
             AND f.BillingDocumentDate < 20260501
            THEN f.NetAmount ELSE 0 END)
        -
        SUM(CASE
            WHEN f.BillingDocumentDate >= 20250401
             AND f.BillingDocumentDate < 20250501
            THEN f.NetAmount ELSE 0 END)) * 100.0)
        / NULLIF(SUM(CASE
            WHEN f.BillingDocumentDate >= 20250401
             AND f.BillingDocumentDate < 20250501
            THEN f.NetAmount ELSE 0 END), 0)
    END AS VariacaoPercentual
FROM F_Invoice f
JOIN D_Product p
  ON p.NIDProduct = f.NIDProduct
JOIN D_ProductBrand pb
  ON pb.NIDProductBrand = p.NIDProductBrand
WHERE f.BillingDocumentIsCancelled = 0
GROUP BY pb.TProductBrand
HAVING ValorMesAtual <> 0 OR ValorMesmoMesAnoAnterior <> 0
ORDER BY VariacaoPercentual DESC, Marca ASC;
```

## G06 — Qual é o peso do desconto promocional total sobre a faturação por canal de distribuição por mês nos últimos 6 meses?

```sql
SELECT
    f.MonthStart AS Mes,
    dc.TDistributionChannel AS Canal,
    SUM(f.NetAmount) AS ValorLiquidoFaturado,
    SUM(f.ZDPRPromotional + f.ZCPRPromotionalCampaign + f.REA1PromotionalDiscount) AS DescontoPromocionalTotal,
    SUM(f.ZDPRPromotional + f.ZCPRPromotionalCampaign + f.REA1PromotionalDiscount) * 100.0 /
      NULLIF(SUM(f.NetAmount), 0) AS PercentagemDescontoPromocional
FROM F_Invoice f
JOIN D_DistributionChannel dc
  ON dc.NIDDistributionChannel = f.NIDDistributionChannel
WHERE f.BillingDocumentIsCancelled = 0
  AND f.BillingDocumentDate >= 20251101
  AND f.BillingDocumentDate <= 20260420
GROUP BY f.MonthStart, dc.TDistributionChannel
ORDER BY Mes, Canal;
```
