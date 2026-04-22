-- Executed generated SQL for exact-support cases in analyst_free_questions_v2

-- B04
WITH grouped AS (
    SELECT
        pb.TProductBrand AS MarcaProduto,
        p.TProduct AS Produto,
        SUM(f.NetAmount) / NULLIF(SUM(f.BillingQuantity), 0) AS PrecoMedioLiquidoPorUnidade
    FROM dbo.F_Invoice f
    JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct
    JOIN dbo.D_ProductBrand pb ON p.NIDProductBrand = pb.NIDProductBrand
    WHERE f.BillingDocumentDate >= 20250421
      AND f.BillingDocumentIsCancelled = 0
    GROUP BY pb.TProductBrand, p.TProduct
    HAVING SUM(f.BillingQuantity) <> 0
), ranked AS (
    SELECT
        g.*,
        ROW_NUMBER() OVER (PARTITION BY MarcaProduto ORDER BY PrecoMedioLiquidoPorUnidade DESC, Produto) AS rn
    FROM grouped g
)
SELECT MarcaProduto, Produto, PrecoMedioLiquidoPorUnidade
FROM ranked
WHERE rn <= 5
ORDER BY MarcaProduto, PrecoMedioLiquidoPorUnidade DESC, Produto;

-- B06
WITH grouped AS (
    SELECT
        dc.TDistributionChannel AS CanalDistribuicao,
        co.TCountry AS Pais,
        SUM(CASE WHEN f.BillingDocumentDate / 10000 = 2026 THEN f.NetAmount ELSE 0 END)
        - SUM(CASE WHEN f.BillingDocumentDate / 10000 = 2025 THEN f.NetAmount ELSE 0 END) AS CrescimentoAbsoluto
    FROM dbo.F_Invoice f
    JOIN dbo.D_DistributionChannel dc ON f.NIDDistributionChannel = dc.NIDDistributionChannel
    JOIN dbo.D_Country co ON f.NIDCountry = co.NIDCountry
    WHERE CAST(f.BillingDocumentDate / 10000 AS INT) IN (2025, 2026)
      AND f.BillingDocumentIsCancelled = 0
    GROUP BY dc.TDistributionChannel, co.TCountry
), ranked AS (
    SELECT g.*, ROW_NUMBER() OVER (PARTITION BY CanalDistribuicao ORDER BY CrescimentoAbsoluto DESC, Pais) AS rn
    FROM grouped g
)
SELECT CanalDistribuicao, Pais, CrescimentoAbsoluto
FROM ranked
WHERE rn <= 3
ORDER BY CanalDistribuicao, CrescimentoAbsoluto DESC, Pais;

-- B13
SELECT
    so.TSalesOrganization AS OrganizacaoVendas,
    pf.TProductFamily AS FamiliaProduto,
    SUM(f.BillingQuantity) - SUM(f.BillingQuantityInBaseUnit) AS DiferencaQuantidadeFaturadaVsBase
FROM dbo.F_Invoice f
JOIN dbo.D_SalesOrganization so ON f.NIDSalesOrganization = so.NIDSalesOrganization
JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct
JOIN dbo.D_ProductFamily pf ON p.NIDProductFamily = pf.NIDProductFamily
WHERE f.BillingDocumentDate / 10000 = 2026
  AND f.BillingDocumentIsCancelled = 0
GROUP BY so.TSalesOrganization, pf.TProductFamily
ORDER BY DiferencaQuantidadeFaturadaVsBase DESC;

-- B17
WITH monthly_sales AS (
    SELECT
        DATEFROMPARTS(f.BillingDocumentDate / 10000, (f.BillingDocumentDate / 100) % 100, 1) AS Mes,
        so.TSalesOrganization AS OrganizacaoVendas,
        SUM(f.NetAmount) AS ValorLiquidoFaturado
    FROM dbo.F_Invoice f
    JOIN dbo.D_SalesOrganization so ON f.NIDSalesOrganization = so.NIDSalesOrganization
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate / 10000 = YEAR(GETDATE())
      AND f.BillingDocumentDate <= CONVERT(int, CONVERT(char(8), CAST(GETDATE() AS date), 112))
    GROUP BY DATEFROMPARTS(f.BillingDocumentDate / 10000, (f.BillingDocumentDate / 100) % 100, 1), so.TSalesOrganization
)
SELECT
    s.Mes,
    s.OrganizacaoVendas,
    s.ValorLiquidoFaturado,
    SUM(s.ValorLiquidoFaturado) OVER (PARTITION BY s.OrganizacaoVendas ORDER BY s.Mes ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS ValorLiquidoFaturadoYTD
FROM monthly_sales s
ORDER BY s.Mes ASC, s.OrganizacaoVendas;
