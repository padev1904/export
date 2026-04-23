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
    x.Mes,
    pb.TProductBrand AS MarcaProduto,
    COUNT(*) AS TotalDocumentos,
    SUM(x.DocumentoCancelado) AS DocumentosCancelados,
    100.0 * SUM(x.DocumentoCancelado) / NULLIF(COUNT(*), 0) AS TaxaCancelamento
FROM docs x
JOIN dbo.D_ProductBrand pb ON pb.NIDProductBrand = x.NIDProductBrand
GROUP BY x.Mes, pb.TProductBrand
ORDER BY x.Mes, TaxaCancelamento DESC, TotalDocumentos DESC, MarcaProduto;

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
), grouped AS (
    SELECT
        x.Trimestre,
        d.TDistributionChannel AS CanalDistribuicao,
        COUNT(*) AS TotalDocumentos,
        SUM(x.DocumentoCancelado) AS DocumentosCancelados,
        100.0 * SUM(x.DocumentoCancelado) / NULLIF(COUNT(*), 0) AS TaxaCancelamento
    FROM docs x
    JOIN dbo.D_DistributionChannel d ON d.NIDDistributionChannel = x.NIDDistributionChannel
    GROUP BY x.Trimestre, d.TDistributionChannel
), ranked AS (
    SELECT
        g.*,
        ROW_NUMBER() OVER (
            PARTITION BY g.Trimestre
            ORDER BY g.TaxaCancelamento DESC, g.TotalDocumentos DESC, g.CanalDistribuicao
        ) AS rn
    FROM grouped g
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
