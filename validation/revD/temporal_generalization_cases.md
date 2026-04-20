# Casos de generalização — revD

## G01 — Como evoluiu mensalmente a faturação por marca nos últimos 6 meses?
- Família: `F15_window_trend`
- Operação: `monthly_trend`
- Estado: **PASS**

### SQL manual independente
```sql
WITH x AS ( SELECT f.MonthStart AS Mes, b.TProductBrand AS MarcaProduto, SUM(f.NetAmount) AS ValorLiquidoFaturado FROM F_Invoice f JOIN D_Product p ON f.NIDProduct = p.NIDProduct JOIN D_ProductBrand b ON p.NIDProductBrand = b.NIDProductBrand WHERE f.BillingDocumentIsCancelled = 0 AND f.BillingDocumentDate BETWEEN 20251101 AND 20260420 GROUP BY f.MonthStart, b.TProductBrand ) SELECT Mes, MarcaProduto, ValorLiquidoFaturado FROM x ORDER BY Mes, MarcaProduto;
```

### SQL do gerador universal
```sql
WITH base AS (
    SELECT
        f.MonthStart AS Mes,
        d.TProductBrand AS MarcaProduto, f.NetAmount AS metric
    FROM F_Invoice f
    JOIN D_Product p ON f.NIDProduct = p.NIDProduct JOIN D_ProductBrand d ON p.NIDProductBrand = d.NIDProductBrand
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= 20251101
      AND f.BillingDocumentDate <= 20260420
)
SELECT
    Mes,
    MarcaProduto, SUM(metric) AS ValorLiquidoFaturado
FROM base
GROUP BY Mes, MarcaProduto
ORDER BY Mes ASC, MarcaProduto;
```

## G02 — Como evoluiu mensalmente a margem bruta por família de produto nos últimos 6 meses?
- Família: `F15_window_trend`
- Operação: `monthly_trend`
- Estado: **PASS**

### SQL manual independente
```sql
SELECT f.MonthStart AS Mes, pf.TProductFamily AS FamiliaProduto, SUM(f.GrossMargin) AS MargemBruta FROM F_Invoice f JOIN D_Product p ON f.NIDProduct = p.NIDProduct JOIN D_ProductFamily pf ON p.NIDProductFamily = pf.NIDProductFamily WHERE f.BillingDocumentIsCancelled = 0 AND f.IsItAnAdditionalCalculatedRecord = 1 AND f.BillingDocumentDate BETWEEN 20251101 AND 20260420 GROUP BY f.MonthStart, pf.TProductFamily ORDER BY Mes, FamiliaProduto;
```

### SQL do gerador universal
```sql
WITH base AS (
    SELECT
        f.MonthStart AS Mes,
        d.TProductFamily AS FamiliaProduto, f.GrossMargin AS metric
    FROM F_Invoice f
    JOIN D_Product p ON f.NIDProduct = p.NIDProduct JOIN D_ProductFamily d ON p.NIDProductFamily = d.NIDProductFamily
    WHERE f.BillingDocumentIsCancelled = 0 AND f.IsItAnAdditionalCalculatedRecord = 1
      AND f.BillingDocumentDate >= 20251101
      AND f.BillingDocumentDate <= 20260420
)
SELECT
    Mes,
    FamiliaProduto, SUM(metric) AS MargemBruta
FROM base
GROUP BY Mes, FamiliaProduto
ORDER BY Mes ASC, FamiliaProduto;
```

## G03 — Qual é a média móvel de 3 meses da faturação por canal?
- Família: `F15_window_trend`
- Operação: `rolling_avg_3m`
- Estado: **PASS**

### SQL manual independente
```sql
WITH monthly AS ( SELECT f.MonthStart AS Mes, dc.TDistributionChannel AS CanalDistribuicao, SUM(f.NetAmount) AS ValorLiquidoFaturado FROM F_Invoice f JOIN D_DistributionChannel dc ON f.NIDDistributionChannel = dc.NIDDistributionChannel WHERE f.BillingDocumentIsCancelled = 0 AND f.BillingDocumentDate BETWEEN 20250901 AND 20260420 GROUP BY f.MonthStart, dc.TDistributionChannel ) SELECT Mes, CanalDistribuicao, ValorLiquidoFaturado, AVG(ValorLiquidoFaturado) OVER (PARTITION BY CanalDistribuicao ORDER BY Mes ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS MediaMovel3Meses FROM monthly ORDER BY Mes, CanalDistribuicao;
```

### SQL do gerador universal
```sql
WITH monthly_sales AS (
    SELECT
        f.MonthStart AS Mes,
        d.TDistributionChannel AS CanalDistribuicao, SUM(f.NetAmount) AS ValorLiquidoFaturado
    FROM F_Invoice f
    JOIN D_DistributionChannel d ON f.NIDDistributionChannel = d.NIDDistributionChannel
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= 20250901
      AND f.BillingDocumentDate <= 20260420
    GROUP BY f.MonthStart, CanalDistribuicao
)
SELECT
    Mes,
    CanalDistribuicao,
    ValorLiquidoFaturado,
    AVG(ValorLiquidoFaturado) OVER (PARTITION BY CanalDistribuicao ORDER BY Mes ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS MediaMovel3Meses
FROM monthly_sales
ORDER BY Mes ASC, CanalDistribuicao;
```

## G04 — Qual é a variação percentual mensal da quantidade faturada por região nos últimos 6 meses?
- Família: `F15_window_trend`
- Operação: `mom_pct_change`
- Estado: **PASS**

### SQL manual independente
```sql
WITH monthly AS ( SELECT f.MonthStart AS Mes, r.TRegion AS Regiao, SUM(f.BillingQuantity) AS QuantidadeFaturada FROM F_Invoice f JOIN D_Region r ON f.NIDRegion = r.NIDRegion WHERE f.BillingDocumentIsCancelled = 0 AND f.BillingDocumentDate BETWEEN 20251101 AND 20260420 GROUP BY f.MonthStart, r.TRegion ) SELECT Mes, Regiao, QuantidadeFaturada, LAG(QuantidadeFaturada) OVER (PARTITION BY Regiao ORDER BY Mes) AS ValorMesAnterior, CASE WHEN LAG(QuantidadeFaturada) OVER (PARTITION BY Regiao ORDER BY Mes) IS NULL THEN NULL WHEN LAG(QuantidadeFaturada) OVER (PARTITION BY Regiao ORDER BY Mes) = 0 THEN NULL ELSE ((QuantidadeFaturada - LAG(QuantidadeFaturada) OVER (PARTITION BY Regiao ORDER BY Mes)) * 100.0) / NULLIF(LAG(QuantidadeFaturada) OVER (PARTITION BY Regiao ORDER BY Mes), 0) END AS VariacaoPercentual FROM monthly ORDER BY Mes, Regiao;
```

### SQL do gerador universal
```sql
WITH monthly_sales AS (
    SELECT
        f.MonthStart AS Mes,
        d.TRegion AS Regiao, SUM(f.BillingQuantity) AS QuantidadeFaturada
    FROM F_Invoice f
    JOIN D_Region d ON f.NIDRegion = d.NIDRegion
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= 20251101
      AND f.BillingDocumentDate <= 20260420
    GROUP BY f.MonthStart, Regiao
)
SELECT
    Mes,
    Regiao,
    QuantidadeFaturada,
    LAG(QuantidadeFaturada) OVER (PARTITION BY Regiao ORDER BY Mes) AS ValorMesAnterior,
    CASE
        WHEN LAG(QuantidadeFaturada) OVER (PARTITION BY Regiao ORDER BY Mes) IS NULL THEN NULL
        WHEN LAG(QuantidadeFaturada) OVER (PARTITION BY Regiao ORDER BY Mes) = 0 THEN NULL
        ELSE ((QuantidadeFaturada - LAG(QuantidadeFaturada) OVER (PARTITION BY Regiao ORDER BY Mes)) * 100.0) / NULLIF(LAG(QuantidadeFaturada) OVER (PARTITION BY Regiao ORDER BY Mes), 0)
    END AS VariacaoPercentual
FROM monthly_sales
ORDER BY Mes ASC, Regiao;
```

## G05 — Qual é o peso do desconto promocional total sobre a faturação por mês e por canal nos últimos 6 meses?
- Família: `F11_percentage_share`
- Operação: `monthly_ratio_to_billing`
- Estado: **PASS**

### SQL manual independente
```sql
WITH monthly AS ( SELECT f.MonthStart AS Mes, dc.TDistributionChannel AS CanalDistribuicao, SUM(f.NetAmount) AS ValorLiquidoFaturado, SUM(f.ZDPRPromotional + f.ZCPRPromotionalCampaign + f.REA1PromotionalDiscount) AS DescontoPromocionalTotal FROM F_Invoice f JOIN D_DistributionChannel dc ON f.NIDDistributionChannel = dc.NIDDistributionChannel WHERE f.BillingDocumentIsCancelled = 0 AND f.BillingDocumentDate BETWEEN 20251101 AND 20260420 GROUP BY f.MonthStart, dc.TDistributionChannel ) SELECT Mes, CanalDistribuicao, ValorLiquidoFaturado, DescontoPromocionalTotal, (DescontoPromocionalTotal * 100.0) / NULLIF(ValorLiquidoFaturado, 0) AS PercentagemDescontoPromocional FROM monthly ORDER BY Mes, CanalDistribuicao;
```

### SQL do gerador universal
```sql
WITH monthly_totals AS (
    SELECT
        f.MonthStart AS Mes,
        d.TDistributionChannel AS CanalDistribuicao, SUM(f.NetAmount) AS ValorLiquidoFaturado,
        SUM((f.ZDPRPromotional + f.ZCPRPromotionalCampaign + f.REA1PromotionalDiscount)) AS DescontoPromocionalTotal
    FROM F_Invoice f
    JOIN D_DistributionChannel d ON f.NIDDistributionChannel = d.NIDDistributionChannel
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= 20251101
      AND f.BillingDocumentDate <= 20260420
    GROUP BY f.MonthStart, CanalDistribuicao
)
SELECT
    Mes,
    CanalDistribuicao, ValorLiquidoFaturado,
    DescontoPromocionalTotal,
    (DescontoPromocionalTotal * 100.0) / NULLIF(ValorLiquidoFaturado, 0) AS PercentagemDescontoPromocional
FROM monthly_totals
ORDER BY Mes ASC, CanalDistribuicao;
```

## G06 — Qual é o crescimento da faturação por país no mês atual face ao mesmo mês do ano anterior?
- Família: `F13_period_compare`
- Operação: `yoy_same_month_by_dimension`
- Estado: **PASS**

### SQL manual independente
```sql
SELECT c.TCountry AS Pais, SUM(CASE WHEN f.BillingDocumentDate BETWEEN 20260401 AND 20260430 THEN f.NetAmount ELSE 0 END) AS ValorMesAtual, SUM(CASE WHEN f.BillingDocumentDate BETWEEN 20250401 AND 20250430 THEN f.NetAmount ELSE 0 END) AS ValorMesmoMesAnoAnterior, CASE WHEN SUM(CASE WHEN f.BillingDocumentDate BETWEEN 20250401 AND 20250430 THEN f.NetAmount ELSE 0 END) = 0 THEN NULL ELSE ((SUM(CASE WHEN f.BillingDocumentDate BETWEEN 20260401 AND 20260430 THEN f.NetAmount ELSE 0 END) - SUM(CASE WHEN f.BillingDocumentDate BETWEEN 20250401 AND 20250430 THEN f.NetAmount ELSE 0 END)) * 100.0) / NULLIF(SUM(CASE WHEN f.BillingDocumentDate BETWEEN 20250401 AND 20250430 THEN f.NetAmount ELSE 0 END), 0) END AS VariacaoPercentual FROM F_Invoice f JOIN D_Country c ON f.NIDCountry = c.NIDCountry WHERE f.BillingDocumentIsCancelled = 0 GROUP BY c.TCountry HAVING ValorMesAtual <> 0 OR ValorMesmoMesAnoAnterior <> 0 ORDER BY VariacaoPercentual DESC, Pais ASC;
```

### SQL do gerador universal
```sql
SELECT
    d.TCountry AS Pais,
    SUM(CASE WHEN f.BillingDocumentDate >= 20260401 AND f.BillingDocumentDate < 20260501 THEN f.NetAmount ELSE 0 END) AS ValorMesAtual,
    SUM(CASE WHEN f.BillingDocumentDate >= 20250401 AND f.BillingDocumentDate < 20250501 THEN f.NetAmount ELSE 0 END) AS ValorMesmoMesAnoAnterior,
    CASE
        WHEN SUM(CASE WHEN f.BillingDocumentDate >= 20250401 AND f.BillingDocumentDate < 20250501 THEN f.NetAmount ELSE 0 END) = 0 THEN NULL
        ELSE ((SUM(CASE WHEN f.BillingDocumentDate >= 20260401 AND f.BillingDocumentDate < 20260501 THEN f.NetAmount ELSE 0 END) - SUM(CASE WHEN f.BillingDocumentDate >= 20250401 AND f.BillingDocumentDate < 20250501 THEN f.NetAmount ELSE 0 END)) * 100.0) / NULLIF(SUM(CASE WHEN f.BillingDocumentDate >= 20250401 AND f.BillingDocumentDate < 20250501 THEN f.NetAmount ELSE 0 END), 0)
    END AS VariacaoPercentual
FROM F_Invoice f
JOIN D_Country d ON f.NIDCountry = d.NIDCountry
WHERE f.BillingDocumentIsCancelled = 0
GROUP BY Pais
HAVING ValorMesAtual <> 0 OR ValorMesmoMesAnoAnterior <> 0
ORDER BY VariacaoPercentual DESC, Pais ASC;
```

## G07 — Qual foi a quantidade faturada do mês atual versus o mês anterior?
- Família: `F13_period_compare`
- Operação: `current_vs_previous_month`
- Estado: **PASS**

### SQL manual independente
```sql
WITH periods AS ( SELECT CASE WHEN f.BillingDocumentDate BETWEEN 20260401 AND 20260430 THEN 'MesAtual' WHEN f.BillingDocumentDate BETWEEN 20260301 AND 20260331 THEN 'MesAnterior' ELSE NULL END AS Periodo, f.BillingQuantity AS metric FROM F_Invoice f WHERE f.BillingDocumentIsCancelled = 0 AND f.BillingDocumentDate BETWEEN 20260301 AND 20260430 ) SELECT Periodo, SUM(metric) AS QuantidadeFaturada FROM periods WHERE Periodo IS NOT NULL GROUP BY Periodo ORDER BY Periodo;
```

### SQL do gerador universal
```sql
WITH base AS (
    SELECT
        CASE
            WHEN f.BillingDocumentDate >= 20260401 AND f.BillingDocumentDate < 20260501 THEN 'MesAtual'
            WHEN f.BillingDocumentDate >= 20260301 AND f.BillingDocumentDate < 20260401 THEN 'MesAnterior'
            ELSE NULL
        END AS Periodo,
        f.BillingQuantity AS metric
    FROM F_Invoice f
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= 20260301
      AND f.BillingDocumentDate < 20260501
)
SELECT
    Periodo,
    SUM(metric) AS QuantidadeFaturada
FROM base
WHERE Periodo IS NOT NULL
GROUP BY Periodo
ORDER BY Periodo ASC;
```

## G08 — Qual é o acumulado YTD da margem bruta por canal no ano corrente?
- Família: `F15_window_trend`
- Operação: `ytd`
- Estado: **PASS**

### SQL manual independente
```sql
WITH monthly AS ( SELECT f.MonthStart AS Mes, dc.TDistributionChannel AS CanalDistribuicao, SUM(f.GrossMargin) AS MargemBruta FROM F_Invoice f JOIN D_DistributionChannel dc ON f.NIDDistributionChannel = dc.NIDDistributionChannel WHERE f.BillingDocumentIsCancelled = 0 AND f.IsItAnAdditionalCalculatedRecord = 1 AND f.BillingDocumentDate BETWEEN 20260101 AND 20260420 GROUP BY f.MonthStart, dc.TDistributionChannel ) SELECT Mes, CanalDistribuicao, MargemBruta, SUM(MargemBruta) OVER (PARTITION BY CanalDistribuicao ORDER BY Mes ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS MargemBrutaYTD FROM monthly ORDER BY Mes, CanalDistribuicao;
```

### SQL do gerador universal
```sql
WITH monthly_sales AS (
    SELECT
        f.MonthStart AS Mes,
        d.TDistributionChannel AS CanalDistribuicao, SUM(f.GrossMargin) AS MargemBruta
    FROM F_Invoice f
    JOIN D_DistributionChannel d ON f.NIDDistributionChannel = d.NIDDistributionChannel
    WHERE f.BillingDocumentIsCancelled = 0 AND f.IsItAnAdditionalCalculatedRecord = 1
      AND f.BillingYear = 2026
      AND f.BillingDocumentDate <= 20260420
    GROUP BY f.MonthStart, CanalDistribuicao
)
SELECT
    Mes,
    CanalDistribuicao,
    MargemBruta,
    SUM(MargemBruta) OVER (PARTITION BY CanalDistribuicao ORDER BY Mes ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS MargemBrutaYTD
FROM monthly_sales
ORDER BY Mes ASC, CanalDistribuicao;
```
