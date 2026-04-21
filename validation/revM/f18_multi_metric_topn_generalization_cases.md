# F18 generalization cases — revM

## G01 — Quais são as 7 famílias de produto com maior margem bruta e vendas comerciais líquidas em 2026?

### SQL manual independente
```sql
WITH agg AS (
    SELECT
        pf.TProductFamily AS FamiliaProduto,
        SUM(f.NetCommercialSales) AS VendasComerciaisLiquidas, SUM(f.GrossMargin) AS MargemBruta
    FROM F_Invoice f
    JOIN D_Product p ON f.NIDProduct = p.NIDProduct
    JOIN D_ProductFamily pf ON p.NIDProductFamily = pf.NIDProductFamily
    WHERE f.BillingDocumentIsCancelled = 0 AND f.IsItAnAdditionalCalculatedRecord = 1 AND f.BillingDocumentDate BETWEEN 20260101 AND 20261231
    GROUP BY pf.TProductFamily
)
SELECT *
FROM agg
ORDER BY VendasComerciaisLiquidas DESC, MargemBruta DESC
LIMIT 7;
```

### SQL do gerador universal
```sql
SELECT TOP 7
    pf.TProductFamily AS FamiliaProduto,
    SUM(f.NetCommercialSales) AS VendasComerciaisLiquidas,
    SUM(f.GrossMargin) AS MargemBruta
FROM dbo.F_Invoice f
JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct
JOIN dbo.D_ProductFamily pf ON p.NIDProductFamily = pf.NIDProductFamily
WHERE f.BillingDocumentIsCancelled = 0
  AND f.IsItAnAdditionalCalculatedRecord = 1
  AND f.BillingDocumentDate / 10000 = 2026
GROUP BY pf.TProductFamily
ORDER BY VendasComerciaisLiquidas DESC, MargemBruta DESC;
```

## G02 — Quais são os 12 produtos com maior custo total e margem bruta em 2026?

### SQL manual independente
```sql
WITH agg AS (
    SELECT
        p.TProduct AS Produto,
        SUM(f.CostAmount) AS CustoTotal, SUM(f.GrossMargin) AS MargemBruta
    FROM F_Invoice f
    JOIN D_Product p ON f.NIDProduct = p.NIDProduct
    WHERE f.BillingDocumentIsCancelled = 0 AND f.IsItAnAdditionalCalculatedRecord = 1 AND f.BillingDocumentDate BETWEEN 20260101 AND 20261231
    GROUP BY p.TProduct
)
SELECT *
FROM agg
ORDER BY MargemBruta DESC, CustoTotal DESC
LIMIT 12;
```

### SQL do gerador universal
```sql
SELECT TOP 12
    p.TProduct AS Produto,
    SUM(f.CostAmount) AS CustoTotal,
    SUM(f.GrossMargin) AS MargemBruta
FROM dbo.F_Invoice f
JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct
WHERE f.BillingDocumentIsCancelled = 0
  AND f.IsItAnAdditionalCalculatedRecord = 1
  AND f.BillingDocumentDate / 10000 = 2026
GROUP BY p.TProduct
ORDER BY MargemBruta DESC, CustoTotal DESC;
```

## G03 — Quais são os 4 clientes com maior vendas comerciais líquidas nos últimos 12 meses?

### SQL manual independente
```sql
WITH agg AS (
    SELECT
        c.TCustomer AS Cliente,
        SUM(f.NetCommercialSales) AS VendasComerciaisLiquidas
    FROM F_Invoice f
    JOIN D_Customer c ON f.NIDPayerParty = c.NIDCustomer
    WHERE f.BillingDocumentIsCancelled = 0 AND f.IsItAnAdditionalCalculatedRecord = 1 AND f.BillingDocumentDate >= 20250501
    GROUP BY c.TCustomer
)
SELECT *
FROM agg
ORDER BY VendasComerciaisLiquidas DESC
LIMIT 4;
```

### SQL do gerador universal
```sql
SELECT TOP 4
    c.TCustomer AS Cliente,
    SUM(f.NetCommercialSales) AS VendasComerciaisLiquidas
FROM dbo.F_Invoice f
JOIN dbo.D_Customer c ON f.NIDPayerParty = c.NIDCustomer
WHERE f.BillingDocumentIsCancelled = 0
  AND f.IsItAnAdditionalCalculatedRecord = 1
  AND f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, 1, EOMONTH(GETDATE(), -12)), 112))
GROUP BY c.TCustomer
ORDER BY VendasComerciaisLiquidas DESC;
```

## G04 — Quais são as 8 marcas com maior margem bruta e vendas comerciais líquidas no ano atual?

### SQL manual independente
```sql
WITH agg AS (
    SELECT
        pb.TProductBrand AS MarcaProduto,
        SUM(f.NetCommercialSales) AS VendasComerciaisLiquidas, SUM(f.GrossMargin) AS MargemBruta
    FROM F_Invoice f
    JOIN D_Product p ON f.NIDProduct = p.NIDProduct
    JOIN D_ProductBrand pb ON p.NIDProductBrand = pb.NIDProductBrand
    WHERE f.BillingDocumentIsCancelled = 0 AND f.IsItAnAdditionalCalculatedRecord = 1 AND f.BillingDocumentDate BETWEEN 20260101 AND 20261231
    GROUP BY pb.TProductBrand
)
SELECT *
FROM agg
ORDER BY VendasComerciaisLiquidas DESC, MargemBruta DESC
LIMIT 8;
```

### SQL do gerador universal
```sql
SELECT TOP 8
    pb.TProductBrand AS MarcaProduto,
    SUM(f.NetCommercialSales) AS VendasComerciaisLiquidas,
    SUM(f.GrossMargin) AS MargemBruta
FROM dbo.F_Invoice f
JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct
JOIN dbo.D_ProductBrand pb ON p.NIDProductBrand = pb.NIDProductBrand
WHERE f.BillingDocumentIsCancelled = 0
  AND f.IsItAnAdditionalCalculatedRecord = 1
  AND f.BillingDocumentDate / 10000 = YEAR(GETDATE())
GROUP BY pb.TProductBrand
ORDER BY VendasComerciaisLiquidas DESC, MargemBruta DESC;
```

## G05 — Quais são os 6 tipos de material com maior preço médio líquido por unidade no ano atual?

### SQL manual independente
```sql
WITH agg AS (
    SELECT
        mt.TMaterialType AS TipoMaterial,
        SUM(f.NetAmount) AS ValorLiquidoFaturado,
        SUM(f.BillingQuantity) AS QuantidadeFaturada,
        1.0 * SUM(f.NetAmount) / NULLIF(SUM(f.BillingQuantity), 0) AS PrecoMedioLiquidoUnitario
    FROM F_Invoice f
    JOIN D_Product p ON f.NIDProduct = p.NIDProduct
    JOIN D_MaterialType mt ON p.NIDMaterialType = mt.NIDMaterialType
    WHERE f.BillingDocumentIsCancelled = 0 AND f.BillingDocumentDate BETWEEN 20260101 AND 20261231
    GROUP BY mt.TMaterialType
    HAVING SUM(f.BillingQuantity) <> 0
)
SELECT *
FROM agg
ORDER BY PrecoMedioLiquidoUnitario DESC
LIMIT 6;
```

### SQL do gerador universal
```sql
SELECT TOP 6
    mt.TMaterialType AS TipoMaterial,
    SUM(f.NetAmount) AS ValorLiquidoFaturado,
    SUM(f.BillingQuantity) AS QuantidadeFaturada,
    SUM(f.NetAmount) / NULLIF(SUM(f.BillingQuantity), 0) AS PrecoMedioLiquidoUnitario
FROM dbo.F_Invoice f
JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct
JOIN dbo.D_MaterialType mt ON p.NIDMaterialType = mt.NIDMaterialType
WHERE f.BillingDocumentIsCancelled = 0
  AND f.BillingDocumentDate / 10000 = YEAR(GETDATE())
GROUP BY mt.TMaterialType
HAVING SUM(f.BillingQuantity) <> 0
ORDER BY PrecoMedioLiquidoUnitario DESC;
```

## G06 — Quais são os 9 produtos com maior preço médio líquido por unidade em 2026?

### SQL manual independente
```sql
WITH agg AS (
    SELECT
        p.TProduct AS Produto,
        SUM(f.NetAmount) AS ValorLiquidoFaturado,
        SUM(f.BillingQuantity) AS QuantidadeFaturada,
        1.0 * SUM(f.NetAmount) / NULLIF(SUM(f.BillingQuantity), 0) AS PrecoMedioLiquidoUnitario
    FROM F_Invoice f
    JOIN D_Product p ON f.NIDProduct = p.NIDProduct
    WHERE f.BillingDocumentIsCancelled = 0 AND f.BillingDocumentDate BETWEEN 20260101 AND 20261231
    GROUP BY p.TProduct
    HAVING SUM(f.BillingQuantity) <> 0
)
SELECT *
FROM agg
ORDER BY PrecoMedioLiquidoUnitario DESC
LIMIT 9;
```

### SQL do gerador universal
```sql
SELECT TOP 9
    p.TProduct AS Produto,
    SUM(f.NetAmount) AS ValorLiquidoFaturado,
    SUM(f.BillingQuantity) AS QuantidadeFaturada,
    SUM(f.NetAmount) / NULLIF(SUM(f.BillingQuantity), 0) AS PrecoMedioLiquidoUnitario
FROM dbo.F_Invoice f
JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct
WHERE f.BillingDocumentIsCancelled = 0
  AND f.BillingDocumentDate / 10000 = 2026
GROUP BY p.TProduct
HAVING SUM(f.BillingQuantity) <> 0
ORDER BY PrecoMedioLiquidoUnitario DESC;
```

## G07 — Quais são as 11 famílias de produto com maior preço médio líquido por unidade nos últimos 12 meses?

### SQL manual independente
```sql
WITH agg AS (
    SELECT
        pf.TProductFamily AS FamiliaProduto,
        SUM(f.NetAmount) AS ValorLiquidoFaturado,
        SUM(f.BillingQuantity) AS QuantidadeFaturada,
        1.0 * SUM(f.NetAmount) / NULLIF(SUM(f.BillingQuantity), 0) AS PrecoMedioLiquidoUnitario
    FROM F_Invoice f
    JOIN D_Product p ON f.NIDProduct = p.NIDProduct
    JOIN D_ProductFamily pf ON p.NIDProductFamily = pf.NIDProductFamily
    WHERE f.BillingDocumentIsCancelled = 0 AND f.BillingDocumentDate >= 20250501
    GROUP BY pf.TProductFamily
    HAVING SUM(f.BillingQuantity) <> 0
)
SELECT *
FROM agg
ORDER BY PrecoMedioLiquidoUnitario DESC
LIMIT 11;
```

### SQL do gerador universal
```sql
SELECT TOP 11
    pf.TProductFamily AS FamiliaProduto,
    SUM(f.NetAmount) AS ValorLiquidoFaturado,
    SUM(f.BillingQuantity) AS QuantidadeFaturada,
    SUM(f.NetAmount) / NULLIF(SUM(f.BillingQuantity), 0) AS PrecoMedioLiquidoUnitario
FROM dbo.F_Invoice f
JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct
JOIN dbo.D_ProductFamily pf ON p.NIDProductFamily = pf.NIDProductFamily
WHERE f.BillingDocumentIsCancelled = 0
  AND f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, 1, EOMONTH(GETDATE(), -12)), 112))
GROUP BY pf.TProductFamily
HAVING SUM(f.BillingQuantity) <> 0
ORDER BY PrecoMedioLiquidoUnitario DESC;
```

## G08 — Quais são as 5 marcas com maior vendas comerciais líquidas em 2026?

### SQL manual independente
```sql
WITH agg AS (
    SELECT
        pb.TProductBrand AS MarcaProduto,
        SUM(f.NetCommercialSales) AS VendasComerciaisLiquidas
    FROM F_Invoice f
    JOIN D_Product p ON f.NIDProduct = p.NIDProduct
    JOIN D_ProductBrand pb ON p.NIDProductBrand = pb.NIDProductBrand
    WHERE f.BillingDocumentIsCancelled = 0 AND f.IsItAnAdditionalCalculatedRecord = 1 AND f.BillingDocumentDate BETWEEN 20260101 AND 20261231
    GROUP BY pb.TProductBrand
)
SELECT *
FROM agg
ORDER BY VendasComerciaisLiquidas DESC
LIMIT 5;
```

### SQL do gerador universal
```sql
SELECT TOP 5
    pb.TProductBrand AS MarcaProduto,
    SUM(f.NetCommercialSales) AS VendasComerciaisLiquidas
FROM dbo.F_Invoice f
JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct
JOIN dbo.D_ProductBrand pb ON p.NIDProductBrand = pb.NIDProductBrand
WHERE f.BillingDocumentIsCancelled = 0
  AND f.IsItAnAdditionalCalculatedRecord = 1
  AND f.BillingDocumentDate / 10000 = 2026
GROUP BY pb.TProductBrand
ORDER BY VendasComerciaisLiquidas DESC;
```
