# distinct_count — generalization cases revV

## G01

Qual o número de documentos de faturação distintos por canal de distribuição em 2026?

```sql
WITH distinct_docs AS (
    SELECT DISTINCT
        f.BillingDocument,
        f.NIDDistributionChannel AS EntityKey
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentDate / 10000 = 2026
      AND f.BillingDocumentIsCancelled = 0
)
SELECT
    dc.TDistributionChannel AS CanalDistribuicao,
    COUNT(*) AS NumeroDocumentos
FROM distinct_docs d
JOIN dbo.D_DistributionChannel dc ON d.EntityKey = dc.NIDDistributionChannel
GROUP BY dc.TDistributionChannel
ORDER BY NumeroDocumentos DESC;
```

## G02

Quais são os 5 produtos com maior número de documentos de faturação distintos em 2026?

```sql
WITH distinct_docs AS (
    SELECT DISTINCT
        f.BillingDocument,
        f.NIDProduct AS EntityKey
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentDate / 10000 = 2026
      AND f.BillingDocumentIsCancelled = 0
)
SELECT TOP 5
    p.TProduct AS Produto,
    COUNT(*) AS NumeroDocumentos
FROM distinct_docs d
JOIN dbo.D_Product p ON d.EntityKey = p.NIDProduct
GROUP BY p.TProduct
ORDER BY NumeroDocumentos DESC;
```

## G03

Quais são os clientes com mais de 20 documentos de faturação em 2026?

```sql
WITH distinct_docs AS (
    SELECT DISTINCT
        f.BillingDocument,
        f.NIDPayerParty AS EntityKey
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentDate / 10000 = 2026
      AND f.BillingDocumentIsCancelled = 0
)
SELECT
    c.TCustomer AS Cliente,
    COUNT(*) AS NumeroDocumentosFaturacao
FROM distinct_docs d
JOIN dbo.D_Customer c ON d.EntityKey = c.NIDCustomer
GROUP BY c.TCustomer
HAVING COUNT(*) > 20
ORDER BY NumeroDocumentosFaturacao DESC;
```

## G04

Quais são os produtos presentes em mais de 70 documentos de faturação em 2026?

```sql
WITH distinct_docs AS (
    SELECT DISTINCT
        f.BillingDocument,
        f.NIDProduct AS EntityKey
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentDate / 10000 = 2026
      AND f.BillingDocumentIsCancelled = 0
)
SELECT
    p.TProduct AS Produto,
    COUNT(*) AS NumeroDocumentosFaturacao
FROM distinct_docs d
JOIN dbo.D_Product p ON d.EntityKey = p.NIDProduct
GROUP BY p.TProduct
HAVING COUNT(*) > 70
ORDER BY NumeroDocumentosFaturacao DESC;
```

## G05

Qual o número de documentos de faturação distintos por país em 2026?

```sql
WITH distinct_docs AS (
    SELECT DISTINCT
        f.BillingDocument,
        f.NIDCountry AS EntityKey
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentDate / 10000 = 2026
      AND f.BillingDocumentIsCancelled = 0
)
SELECT
    co.TCountry AS Pais,
    COUNT(*) AS NumeroDocumentos
FROM distinct_docs d
JOIN dbo.D_Country co ON d.EntityKey = co.NIDCountry
GROUP BY co.TCountry
ORDER BY NumeroDocumentos DESC;
```

## G06

Quais são os 3 países com maior número de documentos de faturação distintos no ano atual?

```sql
WITH distinct_docs AS (
    SELECT DISTINCT
        f.BillingDocument,
        f.NIDCountry AS EntityKey
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentDate / 10000 = 2026
      AND f.BillingDocumentIsCancelled = 0
)
SELECT TOP 3
    co.TCountry AS Pais,
    COUNT(*) AS NumeroDocumentos
FROM distinct_docs d
JOIN dbo.D_Country co ON d.EntityKey = co.NIDCountry
GROUP BY co.TCountry
ORDER BY NumeroDocumentos DESC;
```
