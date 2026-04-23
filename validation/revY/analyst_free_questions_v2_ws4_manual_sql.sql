-- B02
WITH base AS (
    SELECT
        pf.TProductFamily AS FamiliaProduto,
        pb.TProductBrand AS MarcaProduto,
        SUM(CASE
                WHEN f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEFROMPARTS(YEAR(GETDATE()), MONTH(GETDATE()), 1), 112))
                 AND f.BillingDocumentDate < CONVERT(int, CONVERT(char(8), DATEADD(month, 1, DATEFROMPARTS(YEAR(GETDATE()), MONTH(GETDATE()), 1)), 112))
                THEN f.GrossMargin ELSE 0 END) AS MargemBrutaMesAtual,
        SUM(CASE
                WHEN f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(year, -1, DATEFROMPARTS(YEAR(GETDATE()), MONTH(GETDATE()), 1)), 112))
                 AND f.BillingDocumentDate < CONVERT(int, CONVERT(char(8), DATEADD(month, 1, DATEADD(year, -1, DATEFROMPARTS(YEAR(GETDATE()), MONTH(GETDATE()), 1))), 112))
                THEN f.GrossMargin ELSE 0 END) AS MargemBrutaMesmoMesAnoAnterior
    FROM dbo.F_Invoice f
    JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct
    JOIN dbo.D_ProductBrand pb ON p.NIDProductBrand = pb.NIDProductBrand
    JOIN dbo.D_ProductFamily pf ON p.NIDProductFamily = pf.NIDProductFamily
    WHERE f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(year, -1, DATEFROMPARTS(YEAR(GETDATE()), MONTH(GETDATE()), 1)), 112))
      AND f.BillingDocumentDate < CONVERT(int, CONVERT(char(8), DATEADD(month, 1, DATEFROMPARTS(YEAR(GETDATE()), MONTH(GETDATE()), 1)), 112))
      AND f.BillingDocumentIsCancelled = 0
      AND f.IsItAnAdditionalCalculatedRecord = 1
    GROUP BY pf.TProductFamily, pb.TProductBrand
), scored AS (
    SELECT
        FamiliaProduto,
        MarcaProduto,
        MargemBrutaMesAtual,
        MargemBrutaMesmoMesAnoAnterior,
        100.0 * (MargemBrutaMesAtual - MargemBrutaMesmoMesAnoAnterior) / NULLIF(MargemBrutaMesmoMesAnoAnterior, 0) AS CrescimentoPercentualMargemBruta
    FROM base
    WHERE MargemBrutaMesAtual <> 0 OR MargemBrutaMesmoMesAnoAnterior <> 0
), ranked AS (
    SELECT
        s.*,
        ROW_NUMBER() OVER (
            PARTITION BY s.FamiliaProduto
            ORDER BY s.CrescimentoPercentualMargemBruta DESC, s.MarcaProduto
        ) AS rn
    FROM scored s
)
SELECT
    FamiliaProduto,
    MarcaProduto,
    MargemBrutaMesAtual,
    MargemBrutaMesmoMesAnoAnterior,
    CrescimentoPercentualMargemBruta
FROM ranked
WHERE rn <= 3
ORDER BY FamiliaProduto, CrescimentoPercentualMargemBruta DESC, MarcaProduto;

-- B08
WITH aggregated AS (
    SELECT
        CAST((f.BillingDocumentDate / 100) % 100 AS INT) AS Mes,
        so.TSalesOrganization AS OrganizacaoVendas,
        plt.TPriceListType AS TipoListaPrecos,
        SUM(f.ZLP1PriceList) - SUM(f.NetAmount) AS DiferencaPrecoListaVsLiquido
    FROM dbo.F_Invoice f
    JOIN dbo.D_SalesOrganization so ON f.NIDSalesOrganization = so.NIDSalesOrganization
    JOIN dbo.D_PriceListType plt ON f.NIDPriceListType = plt.NIDPriceListType
    WHERE f.BillingDocumentDate / 10000 = 2026
      AND f.BillingDocumentIsCancelled = 0
    GROUP BY CAST((f.BillingDocumentDate / 100) % 100 AS INT), so.TSalesOrganization, plt.TPriceListType
), ranked AS (
    SELECT
        a.*,
        ROW_NUMBER() OVER (
            PARTITION BY a.Mes, a.OrganizacaoVendas
            ORDER BY a.DiferencaPrecoListaVsLiquido DESC, a.TipoListaPrecos
        ) AS rn
    FROM aggregated a
)
SELECT Mes, OrganizacaoVendas, TipoListaPrecos, DiferencaPrecoListaVsLiquido
FROM ranked
WHERE rn <= 2
ORDER BY Mes, OrganizacaoVendas, DiferencaPrecoListaVsLiquido DESC, TipoListaPrecos;

-- B10
WITH aggregated AS (
    SELECT
        co.TCountry AS Pais,
        c.TCustomer AS Cliente,
        SUM(CASE
                WHEN f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -90, CAST(GETDATE() AS date)), 112))
                THEN f.BillingQuantity ELSE 0 END) AS QuantidadeUltimos90Dias,
        SUM(CASE
                WHEN f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -180, CAST(GETDATE() AS date)), 112))
                 AND f.BillingDocumentDate < CONVERT(int, CONVERT(char(8), DATEADD(day, -90, CAST(GETDATE() AS date)), 112))
                THEN f.BillingQuantity ELSE 0 END) AS Quantidade90DiasAnteriores
    FROM dbo.F_Invoice f
    JOIN dbo.D_Country co ON f.NIDCountry = co.NIDCountry
    JOIN dbo.D_Customer c ON f.NIDPayerParty = c.NIDCustomer
    WHERE f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -180, CAST(GETDATE() AS date)), 112))
      AND f.BillingDocumentIsCancelled = 0
    GROUP BY co.TCountry, c.TCustomer
), scored AS (
    SELECT
        Pais,
        Cliente,
        QuantidadeUltimos90Dias,
        Quantidade90DiasAnteriores,
        QuantidadeUltimos90Dias - Quantidade90DiasAnteriores AS CrescimentoAbsolutoQuantidade
    FROM aggregated
), ranked AS (
    SELECT
        s.*,
        ROW_NUMBER() OVER (
            PARTITION BY s.Pais
            ORDER BY s.CrescimentoAbsolutoQuantidade DESC, s.Cliente
        ) AS rn
    FROM scored s
)
SELECT Pais, Cliente, QuantidadeUltimos90Dias, Quantidade90DiasAnteriores, CrescimentoAbsolutoQuantidade
FROM ranked
WHERE rn <= 3
ORDER BY Pais, CrescimentoAbsolutoQuantidade DESC, Cliente;

-- B12
WITH docs AS (
    SELECT
        dc.TDistributionChannel AS CanalDistribuicao,
        f.BillingDocument,
        ABS(SUM(f.NetAmount)) AS ValorLiquidoAbsolutoTotal,
        MIN(f.NetAmount) AS ValorMinimoLinha,
        MAX(f.NetAmount) AS ValorMaximoLinha
    FROM dbo.F_Invoice f
    JOIN dbo.D_DistributionChannel dc ON f.NIDDistributionChannel = dc.NIDDistributionChannel
    WHERE f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, 1, EOMONTH(CAST(GETDATE() AS date), -12)), 112))
      AND f.BillingDocumentIsCancelled = 0
    GROUP BY dc.TDistributionChannel, f.BillingDocument
    HAVING MIN(f.NetAmount) < 0 AND MAX(f.NetAmount) > 0
), ranked AS (
    SELECT
        d.*,
        ROW_NUMBER() OVER (
            PARTITION BY d.CanalDistribuicao
            ORDER BY d.ValorLiquidoAbsolutoTotal DESC, d.BillingDocument
        ) AS rn
    FROM docs d
)
SELECT CanalDistribuicao, BillingDocument, ValorLiquidoAbsolutoTotal, ValorMinimoLinha, ValorMaximoLinha
FROM ranked
ORDER BY CanalDistribuicao, ValorLiquidoAbsolutoTotal DESC, BillingDocument;

-- B14
WITH aggregated AS (
    SELECT
        CAST((f.BillingDocumentDate / 100) % 100 AS INT) AS Mes,
        pb.TProductBrand AS MarcaProduto,
        cg.TCustomerGroup AS GrupoCliente,
        SUM(f.ZDPRPromotional + f.ZCPRPromotionalCampaign + f.REA1PromotionalDiscount) AS DescontoPromocionalTotal
    FROM dbo.F_Invoice f
    JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct
    JOIN dbo.D_ProductBrand pb ON p.NIDProductBrand = pb.NIDProductBrand
    JOIN dbo.D_CustomerGroup cg ON f.NIDCustomerGroup = cg.NIDCustomerGroup
    WHERE f.BillingDocumentDate / 10000 = 2026
      AND f.BillingDocumentIsCancelled = 0
    GROUP BY CAST((f.BillingDocumentDate / 100) % 100 AS INT), pb.TProductBrand, cg.TCustomerGroup
), ranked AS (
    SELECT
        a.*,
        ROW_NUMBER() OVER (
            PARTITION BY a.Mes, a.MarcaProduto
            ORDER BY a.DescontoPromocionalTotal DESC, a.GrupoCliente
        ) AS rn
    FROM aggregated a
)
SELECT Mes, MarcaProduto, GrupoCliente, DescontoPromocionalTotal
FROM ranked
WHERE rn <= 3
ORDER BY Mes, MarcaProduto, DescontoPromocionalTotal DESC, GrupoCliente;

-- B18
WITH aggregated AS (
    SELECT
        so.TSalesOrganization AS OrganizacaoVendas,
        pf.TProductFamily AS FamiliaProduto,
        SUM(f.ItemNetWeight) / NULLIF(SUM(f.BillingQuantity), 0) AS PesoLiquidoMedioPorUnidade
    FROM dbo.F_Invoice f
    JOIN dbo.D_SalesOrganization so ON f.NIDSalesOrganization = so.NIDSalesOrganization
    JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct
    JOIN dbo.D_ProductFamily pf ON p.NIDProductFamily = pf.NIDProductFamily
    WHERE f.BillingDocumentDate / 10000 = 2026
      AND f.BillingDocumentIsCancelled = 0
    GROUP BY so.TSalesOrganization, pf.TProductFamily
    HAVING SUM(f.BillingQuantity) <> 0
), ranked AS (
    SELECT
        a.*,
        ROW_NUMBER() OVER (
            PARTITION BY a.OrganizacaoVendas
            ORDER BY a.PesoLiquidoMedioPorUnidade DESC, a.FamiliaProduto
        ) AS rn
    FROM aggregated a
)
SELECT OrganizacaoVendas, FamiliaProduto, PesoLiquidoMedioPorUnidade
FROM ranked
WHERE rn <= 2
ORDER BY OrganizacaoVendas, PesoLiquidoMedioPorUnidade DESC, FamiliaProduto;
