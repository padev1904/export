-- B02
WITH grouped AS (
    SELECT
        pf.TProductFamily AS FamiliaProduto,
        pb.TProductBrand AS MarcaProduto,
        SUM(CASE WHEN f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEFROMPARTS(YEAR(CAST(GETDATE() AS date)), MONTH(CAST(GETDATE() AS date)), 1), 112)) AND f.BillingDocumentDate < CONVERT(int, CONVERT(char(8), DATEADD(month, 1, DATEFROMPARTS(YEAR(CAST(GETDATE() AS date)), MONTH(CAST(GETDATE() AS date)), 1)), 112)) THEN f.GrossMargin ELSE 0 END) AS MargemBrutaMesAtual,
        SUM(CASE WHEN f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(year, -1, DATEFROMPARTS(YEAR(CAST(GETDATE() AS date)), MONTH(CAST(GETDATE() AS date)), 1)), 112)) AND f.BillingDocumentDate < CONVERT(int, CONVERT(char(8), DATEADD(month, 1, DATEADD(year, -1, DATEFROMPARTS(YEAR(CAST(GETDATE() AS date)), MONTH(CAST(GETDATE() AS date)), 1))), 112)) THEN f.GrossMargin ELSE 0 END) AS MargemBrutaMesmoMesAnoAnterior
    FROM dbo.F_Invoice f
    JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct JOIN dbo.D_ProductFamily pf ON p.NIDProductFamily = pf.NIDProductFamily JOIN dbo.D_ProductBrand pb ON p.NIDProductBrand = pb.NIDProductBrand
    WHERE f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(year, -1, DATEFROMPARTS(YEAR(CAST(GETDATE() AS date)), MONTH(CAST(GETDATE() AS date)), 1)), 112)) AND
      f.BillingDocumentDate < CONVERT(int, CONVERT(char(8), DATEADD(month, 1, DATEFROMPARTS(YEAR(CAST(GETDATE() AS date)), MONTH(CAST(GETDATE() AS date)), 1)), 112)) AND
      f.BillingDocumentIsCancelled = 0 AND
      f.IsItAnAdditionalCalculatedRecord = 1
    GROUP BY pf.TProductFamily, pb.TProductBrand
), filtered AS (
    SELECT *
    FROM grouped
    WHERE MargemBrutaMesAtual <> 0 OR MargemBrutaMesmoMesAnoAnterior <> 0
), ranked AS (
    SELECT
        g.*,
        100.0 * (g.MargemBrutaMesAtual - g.MargemBrutaMesmoMesAnoAnterior) / NULLIF(g.MargemBrutaMesmoMesAnoAnterior, 0) AS CrescimentoPercentualMargemBruta,
        ROW_NUMBER() OVER (
            PARTITION BY FamiliaProduto
            ORDER BY 100.0 * (g.MargemBrutaMesAtual - g.MargemBrutaMesmoMesAnoAnterior) / NULLIF(g.MargemBrutaMesmoMesAnoAnterior, 0) DESC, MarcaProduto
        ) AS rn
    FROM filtered g
)
SELECT
    r.FamiliaProduto,
    r.MarcaProduto,
    r.MargemBrutaMesAtual,
    r.MargemBrutaMesmoMesAnoAnterior,
    r.CrescimentoPercentualMargemBruta
FROM ranked r
WHERE r.rn <= 3
ORDER BY r.FamiliaProduto, r.CrescimentoPercentualMargemBruta DESC, r.MarcaProduto;

-- B08
WITH grouped AS (
    SELECT
        CAST((f.BillingDocumentDate / 100) % 100 AS INT) AS Mes,
        so.TSalesOrganization AS OrganizacaoVendas,
        plt.TPriceListType AS TipoListaPrecos,
        SUM(f.ZLP1PriceList) - SUM(f.NetAmount) AS DiferencaPrecoListaVsLiquido
    FROM dbo.F_Invoice f
    JOIN dbo.D_SalesOrganization so ON f.NIDSalesOrganization = so.NIDSalesOrganization JOIN dbo.D_PriceListType plt ON f.NIDPriceListType = plt.NIDPriceListType
    WHERE f.BillingDocumentDate / 10000 = 2026 AND
      f.BillingDocumentIsCancelled = 0
    GROUP BY CAST((f.BillingDocumentDate / 100) % 100 AS INT), so.TSalesOrganization, plt.TPriceListType
), ranked AS (
    SELECT
        g.*,
        ROW_NUMBER() OVER (PARTITION BY Mes, OrganizacaoVendas ORDER BY DiferencaPrecoListaVsLiquido DESC, TipoListaPrecos) AS rn
    FROM grouped g
)
SELECT
    r.Mes, r.OrganizacaoVendas,
    r.TipoListaPrecos,
    r.DiferencaPrecoListaVsLiquido
FROM ranked r
WHERE r.rn <= 2
ORDER BY r.Mes, r.OrganizacaoVendas, r.DiferencaPrecoListaVsLiquido DESC, r.TipoListaPrecos;

-- B10
WITH grouped AS (
    SELECT
        co.TCountry AS Pais,
        c.TCustomer AS Cliente,
        SUM(CASE WHEN f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -90, CAST(GETDATE() AS date)), 112)) THEN f.BillingQuantity ELSE 0 END) AS QuantidadeUltimos90Dias,
        SUM(CASE WHEN f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -180, CAST(GETDATE() AS date)), 112)) AND f.BillingDocumentDate < CONVERT(int, CONVERT(char(8), DATEADD(day, -90, CAST(GETDATE() AS date)), 112)) THEN f.BillingQuantity ELSE 0 END) AS Quantidade90DiasAnteriores,
        SUM(CASE WHEN f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -90, CAST(GETDATE() AS date)), 112)) THEN f.BillingQuantity ELSE 0 END)
        - SUM(CASE WHEN f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -180, CAST(GETDATE() AS date)), 112)) AND f.BillingDocumentDate < CONVERT(int, CONVERT(char(8), DATEADD(day, -90, CAST(GETDATE() AS date)), 112)) THEN f.BillingQuantity ELSE 0 END) AS CrescimentoAbsolutoQuantidade
    FROM dbo.F_Invoice f
    JOIN dbo.D_Country co ON f.NIDCountry = co.NIDCountry JOIN dbo.D_Customer c ON f.NIDPayerParty = c.NIDCustomer
    WHERE f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -180, CAST(GETDATE() AS date)), 112)) AND
      f.BillingDocumentIsCancelled = 0
    GROUP BY co.TCountry, c.TCustomer
), ranked AS (
    SELECT
        g.*,
        ROW_NUMBER() OVER (PARTITION BY Pais ORDER BY CrescimentoAbsolutoQuantidade DESC, Cliente) AS rn
    FROM grouped g
)
SELECT
    r.Pais,
    r.Cliente,
    r.QuantidadeUltimos90Dias,
    r.Quantidade90DiasAnteriores,
    r.CrescimentoAbsolutoQuantidade
FROM ranked r
WHERE r.rn <= 3
ORDER BY r.Pais, r.CrescimentoAbsolutoQuantidade DESC, r.Cliente;

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
    WHERE f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, 1, EOMONTH(CAST(GETDATE() AS date), -12)), 112)) AND
      f.BillingDocumentIsCancelled = 0
    GROUP BY dc.TDistributionChannel, f.BillingDocument
    HAVING MIN(f.NetAmount) < 0 AND MAX(f.NetAmount) > 0
), ranked AS (
    SELECT
        d.*,
        ROW_NUMBER() OVER (PARTITION BY CanalDistribuicao ORDER BY d.ValorLiquidoAbsolutoTotal DESC, d.BillingDocument) AS rn
    FROM docs d
)
SELECT
    r.CanalDistribuicao,
    r.BillingDocument,
    r.ValorLiquidoAbsolutoTotal,
    r.ValorMinimoLinha,
    r.ValorMaximoLinha
FROM ranked r

ORDER BY r.CanalDistribuicao, r.ValorLiquidoAbsolutoTotal DESC, r.BillingDocument;

-- B14
WITH grouped AS (
    SELECT
        CAST((f.BillingDocumentDate / 100) % 100 AS INT) AS Mes,
        pb.TProductBrand AS MarcaProduto,
        cg.TCustomerGroup AS GrupoCliente,
        SUM(f.ZDPRPromotional + f.ZCPRPromotionalCampaign + f.REA1PromotionalDiscount) AS DescontoPromocionalTotal
    FROM dbo.F_Invoice f
    JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct JOIN dbo.D_ProductBrand pb ON p.NIDProductBrand = pb.NIDProductBrand JOIN dbo.D_CustomerGroup cg ON f.NIDCustomerGroup = cg.NIDCustomerGroup
    WHERE f.BillingDocumentDate / 10000 = 2026 AND
      f.BillingDocumentIsCancelled = 0
    GROUP BY CAST((f.BillingDocumentDate / 100) % 100 AS INT), pb.TProductBrand, cg.TCustomerGroup
), ranked AS (
    SELECT
        g.*,
        ROW_NUMBER() OVER (PARTITION BY Mes, MarcaProduto ORDER BY DescontoPromocionalTotal DESC, GrupoCliente) AS rn
    FROM grouped g
)
SELECT
    r.Mes, r.MarcaProduto,
    r.GrupoCliente,
    r.DescontoPromocionalTotal
FROM ranked r
WHERE r.rn <= 3
ORDER BY r.Mes, r.MarcaProduto, r.DescontoPromocionalTotal DESC, r.GrupoCliente;

-- B18
WITH grouped AS (
    SELECT
        so.TSalesOrganization AS OrganizacaoVendas,
        pf.TProductFamily AS FamiliaProduto,
        SUM(f.ItemNetWeight) / NULLIF(SUM(f.BillingQuantity), 0) AS PesoLiquidoMedioPorUnidade
    FROM dbo.F_Invoice f
    JOIN dbo.D_SalesOrganization so ON f.NIDSalesOrganization = so.NIDSalesOrganization JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct JOIN dbo.D_ProductFamily pf ON p.NIDProductFamily = pf.NIDProductFamily
    WHERE f.BillingDocumentDate / 10000 = 2026 AND
      f.BillingDocumentIsCancelled = 0
    GROUP BY so.TSalesOrganization, pf.TProductFamily
    HAVING SUM(f.BillingQuantity) <> 0
), ranked AS (
    SELECT
        g.*,
        ROW_NUMBER() OVER (PARTITION BY OrganizacaoVendas ORDER BY PesoLiquidoMedioPorUnidade DESC, FamiliaProduto) AS rn
    FROM grouped g
)
SELECT
    r.OrganizacaoVendas,
    r.FamiliaProduto,
    r.PesoLiquidoMedioPorUnidade
FROM ranked r
WHERE r.rn <= 2
ORDER BY r.OrganizacaoVendas, r.PesoLiquidoMedioPorUnidade DESC, r.FamiliaProduto;
