-- B03
WITH aggregated AS (
    SELECT
        CAST(f.BillingDocumentDate / 100 AS INT) AS Mes,
        dc.TDistributionChannel AS CanalDistribuicao,
        so.TSalesOrganization AS OrganizacaoVendas,
        SUM(f.NetAmount) AS ValorLiquidoFaturado
    FROM dbo.F_Invoice f
    JOIN dbo.D_DistributionChannel dc ON f.NIDDistributionChannel = dc.NIDDistributionChannel
    JOIN dbo.D_SalesOrganization so ON f.NIDSalesOrganization = so.NIDSalesOrganization
    WHERE f.BillingDocumentDate / 10000 = YEAR(GETDATE())
      AND f.BillingDocumentIsCancelled = 0
    GROUP BY CAST(f.BillingDocumentDate / 100 AS INT), dc.TDistributionChannel, so.TSalesOrganization
)
SELECT
    Mes,
    CanalDistribuicao,
    OrganizacaoVendas,
    ValorLiquidoFaturado,
    100.0 * ValorLiquidoFaturado / NULLIF(SUM(ValorLiquidoFaturado) OVER (PARTITION BY Mes, CanalDistribuicao), 0) AS Percentagem
FROM aggregated
ORDER BY Mes, CanalDistribuicao, Percentagem DESC, OrganizacaoVendas;

-- B11
WITH aggregated AS (
    SELECT
        CAST(f.BillingDocumentDate / 100 AS INT) AS Mes,
        pf.TProductFamily AS FamiliaProduto,
        pb.TProductBrand AS MarcaProduto,
        SUM(f.GrossMargin) AS MargemBruta
    FROM dbo.F_Invoice f
    JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct
    JOIN dbo.D_ProductFamily pf ON p.NIDProductFamily = pf.NIDProductFamily
    JOIN dbo.D_ProductBrand pb ON p.NIDProductBrand = pb.NIDProductBrand
    WHERE f.BillingDocumentDate / 10000 = YEAR(GETDATE())
      AND f.BillingDocumentIsCancelled = 0
      AND f.IsItAnAdditionalCalculatedRecord = 1
    GROUP BY CAST(f.BillingDocumentDate / 100 AS INT), pf.TProductFamily, pb.TProductBrand
)
SELECT
    Mes,
    FamiliaProduto,
    MarcaProduto,
    MargemBruta,
    100.0 * MargemBruta / NULLIF(SUM(MargemBruta) OVER (PARTITION BY Mes, FamiliaProduto), 0) AS Percentagem
FROM aggregated
ORDER BY Mes, FamiliaProduto, Percentagem DESC, MarcaProduto;

-- B19
WITH aggregated AS (
    SELECT
        so.TSalesOrganization AS OrganizacaoVendas,
        co.TCountry AS Pais,
        SUM(f.NetAmount) AS ValorLiquidoFaturado
    FROM dbo.F_Invoice f
    JOIN dbo.D_SalesOrganization so ON f.NIDSalesOrganization = so.NIDSalesOrganization
    JOIN dbo.D_Country co ON f.NIDCountry = co.NIDCountry
    WHERE f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, 1, EOMONTH(CAST(GETDATE() AS date), -12)), 112))
      AND f.BillingDocumentIsCancelled = 0
    GROUP BY so.TSalesOrganization, co.TCountry
)
SELECT
    OrganizacaoVendas,
    Pais,
    ValorLiquidoFaturado,
    100.0 * ValorLiquidoFaturado / NULLIF(SUM(ValorLiquidoFaturado) OVER (PARTITION BY OrganizacaoVendas), 0) AS Percentagem
FROM aggregated
ORDER BY OrganizacaoVendas, Percentagem DESC, Pais;
