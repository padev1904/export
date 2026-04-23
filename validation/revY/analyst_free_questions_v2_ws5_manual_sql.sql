-- B07
WITH docs AS (
    SELECT
        CAST(f.BillingDocumentDate / 100 AS INT) AS Mes,
        f.BillingDocument,
        p.NIDProductBrand,
        MAX(CASE WHEN f.BillingDocumentIsCancelled = 1 THEN 1 ELSE 0 END) AS DocumentoCancelado
    FROM dbo.F_Invoice f
    JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct
    WHERE f.BillingDocumentDate / 10000 = YEAR(GETDATE())
    GROUP BY CAST(f.BillingDocumentDate / 100 AS INT), f.BillingDocument, p.NIDProductBrand
)
SELECT
    d.Mes,
    pb.TProductBrand AS MarcaProduto,
    COUNT(*) AS TotalDocumentos,
    SUM(d.DocumentoCancelado) AS DocumentosCancelados,
    100.0 * SUM(d.DocumentoCancelado) / NULLIF(COUNT(*), 0) AS TaxaCancelamento
FROM docs d
JOIN dbo.D_ProductBrand pb ON pb.NIDProductBrand = d.NIDProductBrand
GROUP BY d.Mes, pb.TProductBrand
ORDER BY d.Mes, TaxaCancelamento DESC, TotalDocumentos DESC, MarcaProduto;

-- B20
WITH docs AS (
    SELECT
        CAST((((CAST((f.BillingDocumentDate / 100) AS INT) % 100) - 1) / 3) + 1 AS INT) AS Trimestre,
        f.BillingDocument,
        f.NIDDistributionChannel,
        MAX(CASE WHEN f.BillingDocumentIsCancelled = 1 THEN 1 ELSE 0 END) AS DocumentoCancelado
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentDate / 10000 = YEAR(GETDATE())
    GROUP BY CAST((((CAST((f.BillingDocumentDate / 100) AS INT) % 100) - 1) / 3) + 1 AS INT), f.BillingDocument, f.NIDDistributionChannel
), rates AS (
    SELECT
        d.Trimestre,
        dc.TDistributionChannel AS CanalDistribuicao,
        COUNT(*) AS TotalDocumentos,
        SUM(d.DocumentoCancelado) AS DocumentosCancelados,
        100.0 * SUM(d.DocumentoCancelado) / NULLIF(COUNT(*), 0) AS TaxaCancelamento
    FROM docs d
    JOIN dbo.D_DistributionChannel dc ON dc.NIDDistributionChannel = d.NIDDistributionChannel
    GROUP BY d.Trimestre, dc.TDistributionChannel
), ranked AS (
    SELECT
        r.*,
        ROW_NUMBER() OVER (
            PARTITION BY r.Trimestre
            ORDER BY r.TaxaCancelamento DESC, r.TotalDocumentos DESC, r.CanalDistribuicao
        ) AS rn
    FROM rates r
)
SELECT
    Trimestre,
    CanalDistribuicao,
    TotalDocumentos,
    DocumentosCancelados,
    TaxaCancelamento
FROM ranked
WHERE rn <= 3
ORDER BY Trimestre, rn;
