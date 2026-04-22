-- A01
-- Qual o total de descontos de quantidade por zona de transporte do cliente em 2026?
SELECT
    tz.TTranspZone AS ZonaTransporte,
    SUM(f.ZDQ1QtyDiscount) AS DescontoQuantidade
FROM dbo.F_Invoice f
JOIN dbo.D_Customer c ON f.NIDPayerParty = c.NIDCustomer
JOIN dbo.D_TranspZone tz ON c.NIDTranspZone = tz.NIDTranspZone
WHERE f.BillingDocumentDate / 10000 = 2026
  AND f.BillingDocumentIsCancelled = 0
GROUP BY tz.TTranspZone
ORDER BY DescontoQuantidade ASC;

-- A02
-- Qual o peso bruto total por marca de produto em 2026?
SELECT
    pb.TProductBrand AS MarcaProduto,
    SUM(f.ItemGrossWeight) AS PesoBrutoTotal
FROM dbo.F_Invoice f
JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct
JOIN dbo.D_ProductBrand pb ON p.NIDProductBrand = pb.NIDProductBrand
WHERE f.BillingDocumentDate / 10000 = 2026
  AND f.BillingDocumentIsCancelled = 0
GROUP BY pb.TProductBrand
ORDER BY PesoBrutoTotal DESC;

-- A03
-- Qual a diferença entre quantidade faturada e quantidade em unidade base por tipo de material em 2026?
SELECT
    mt.TMaterialType AS TipoMaterial,
    SUM(f.BillingQuantity) - SUM(f.BillingQuantityInBaseUnit) AS DiferencaQuantidadeFaturadaVsBase
FROM dbo.F_Invoice f
JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct
JOIN dbo.D_MaterialType mt ON p.NIDMaterialType = mt.NIDMaterialType
WHERE f.BillingDocumentDate / 10000 = 2026
  AND f.BillingDocumentIsCancelled = 0
GROUP BY mt.TMaterialType
ORDER BY DiferencaQuantidadeFaturadaVsBase DESC;

-- A04
-- Qual o peso líquido total por condição de expedição do cliente em 2026?
SELECT
    sc.TShippingCondition AS CondicaoExpedicao,
    SUM(f.ItemNetWeight) AS PesoLiquidoTotal
FROM dbo.F_Invoice f
JOIN dbo.D_Customer c ON f.NIDPayerParty = c.NIDCustomer
JOIN dbo.D_ShippingCondition sc ON c.NIDShippingCondition = sc.NIDShippingCondition
WHERE f.BillingDocumentDate / 10000 = 2026
  AND f.BillingDocumentIsCancelled = 0
GROUP BY sc.TShippingCondition
ORDER BY PesoLiquidoTotal DESC;

-- A05
-- Quais são os 3 pontos de expedição com maior valor líquido faturado dentro de cada canal de distribuição em 2026?
WITH grouped AS (
    SELECT
        dc.TDistributionChannel AS CanalDistribuicao,
        sp.TShippingPoint AS PontoExpedicao,
        SUM(f.NetAmount) AS ValorLiquidoFaturado
    FROM dbo.F_Invoice f
    JOIN dbo.D_DistributionChannel dc ON f.NIDDistributionChannel = dc.NIDDistributionChannel JOIN dbo.D_ShippingPoint sp ON f.NIDShippingPoint = sp.NIDShippingPoint
    WHERE f.BillingDocumentDate / 10000 = 2026
      AND f.BillingDocumentIsCancelled = 0
    GROUP BY dc.TDistributionChannel, sp.TShippingPoint
), ranked AS (
    SELECT
        g.*,
        ROW_NUMBER() OVER (PARTITION BY CanalDistribuicao ORDER BY ValorLiquidoFaturado DESC, PontoExpedicao) AS rn
    FROM grouped g
)
SELECT
    r.CanalDistribuicao,
    r.PontoExpedicao,
    r.ValorLiquidoFaturado
FROM ranked r
WHERE r.rn <= 3
ORDER BY r.CanalDistribuicao, r.ValorLiquidoFaturado DESC, r.PontoExpedicao;

-- A06
-- Quais são os 2 grupos de preço de cliente com maior desconto de quantidade dentro de cada marca em 2026?
WITH grouped AS (
    SELECT
        pb.TProductBrand AS MarcaProduto,
        cpg.TCustomerPriceGroup AS GrupoPrecoCliente,
        SUM(f.ZDQ1QtyDiscount) AS DescontoQuantidade
    FROM dbo.F_Invoice f
    JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct JOIN dbo.D_ProductBrand pb ON p.NIDProductBrand = pb.NIDProductBrand JOIN dbo.D_CustomerPriceGroup cpg ON f.NIDCustomerPriceGroup = cpg.NIDCustomerPriceGroup
    WHERE f.BillingDocumentDate / 10000 = 2026
      AND f.BillingDocumentIsCancelled = 0
    GROUP BY pb.TProductBrand, cpg.TCustomerPriceGroup
), ranked AS (
    SELECT
        g.*,
        ROW_NUMBER() OVER (PARTITION BY MarcaProduto ORDER BY DescontoQuantidade ASC, GrupoPrecoCliente) AS rn
    FROM grouped g
)
SELECT
    r.MarcaProduto,
    r.GrupoPrecoCliente,
    r.DescontoQuantidade
FROM ranked r
WHERE r.rn <= 2
ORDER BY r.MarcaProduto, r.DescontoQuantidade ASC, r.GrupoPrecoCliente;

-- A07
-- Quais são as 2 famílias de produto com maior preço médio líquido por unidade dentro de cada organização de vendas em 2026?
WITH grouped AS (
    SELECT
        so.TSalesOrganization AS OrganizacaoVendas,
        pf.TProductFamily AS FamiliaProduto,
        SUM(f.NetAmount) / NULLIF(SUM(f.BillingQuantity), 0) AS PrecoMedioLiquidoPorUnidade
    FROM dbo.F_Invoice f
    JOIN dbo.D_SalesOrganization so ON f.NIDSalesOrganization = so.NIDSalesOrganization JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct JOIN dbo.D_ProductFamily pf ON p.NIDProductFamily = pf.NIDProductFamily
    WHERE f.BillingDocumentDate / 10000 = 2026
      AND f.BillingDocumentIsCancelled = 0
    GROUP BY so.TSalesOrganization, pf.TProductFamily
    HAVING SUM(f.BillingQuantity) <> 0
), ranked AS (
    SELECT
        g.*,
        ROW_NUMBER() OVER (PARTITION BY OrganizacaoVendas ORDER BY PrecoMedioLiquidoPorUnidade DESC, FamiliaProduto) AS rn
    FROM grouped g
)
SELECT
    r.OrganizacaoVendas,
    r.FamiliaProduto,
    r.PrecoMedioLiquidoPorUnidade
FROM ranked r
WHERE r.rn <= 2
ORDER BY r.OrganizacaoVendas, r.PrecoMedioLiquidoPorUnidade DESC, r.FamiliaProduto;

-- A08
-- Quais são os 3 clientes com maior crescimento absoluto de quantidade faturada dentro de cada região entre 2025 e 2026?
WITH grouped AS (
    SELECT
        r.TRegion AS Regiao,
        c.TCustomer AS Cliente,
        SUM(CASE WHEN f.BillingDocumentDate / 10000 = 2026 THEN f.BillingQuantity ELSE 0 END)
        - SUM(CASE WHEN f.BillingDocumentDate / 10000 = 2025 THEN f.BillingQuantity ELSE 0 END) AS CrescimentoAbsolutoQuantidade
    FROM dbo.F_Invoice f
    JOIN dbo.D_Region r ON f.NIDRegion = r.NIDRegion JOIN dbo.D_Customer c ON f.NIDPayerParty = c.NIDCustomer
    WHERE CAST(f.BillingDocumentDate / 10000 AS INT) IN (2025, 2026)
      AND f.BillingDocumentIsCancelled = 0
    GROUP BY r.TRegion, c.TCustomer
), ranked AS (
    SELECT
        g.*,
        ROW_NUMBER() OVER (PARTITION BY Regiao ORDER BY CrescimentoAbsolutoQuantidade DESC, Cliente) AS rn
    FROM grouped g
)
SELECT
    r.Regiao,
    r.Cliente,
    r.CrescimentoAbsolutoQuantidade
FROM ranked r
WHERE r.rn <= 3
ORDER BY r.Regiao, r.CrescimentoAbsolutoQuantidade DESC, r.Cliente;

-- A09
-- Qual a diferença entre o preço de lista e o valor líquido faturado por país e por mês em 2026?
WITH monthly_sales AS (
    SELECT
        DATEFROMPARTS(f.BillingDocumentDate / 10000, (f.BillingDocumentDate / 100) % 100, 1) AS Mes,
        co.TCountry AS Pais,
        SUM(f.ZLP1PriceList) - SUM(f.NetAmount) AS DiferencaPrecoListaVsLiquido
    FROM dbo.F_Invoice f
    JOIN dbo.D_Country co ON f.NIDCountry = co.NIDCountry
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate / 10000 = 2026
    GROUP BY DATEFROMPARTS(f.BillingDocumentDate / 10000, (f.BillingDocumentDate / 100) % 100, 1), co.TCountry
)
SELECT
    s.Mes,
    s.Pais,
    s.DiferencaPrecoListaVsLiquido
FROM monthly_sales s
ORDER BY s.Mes ASC, s.Pais;

-- A10
-- Quais são os 2 canais de distribuição com maior taxa de cancelamento de documentos dentro de cada mês em 2026?
WITH docs AS (
    SELECT
        CAST((f.BillingDocumentDate / 100) % 100 AS INT) AS Mes,
        f.BillingDocument,
        f.NIDDistributionChannel,
        MAX(CASE WHEN f.BillingDocumentIsCancelled = 1 THEN 1 ELSE 0 END) AS DocumentoCancelado
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentDate / 10000 = 2026
    GROUP BY CAST((f.BillingDocumentDate / 100) % 100 AS INT), f.BillingDocument, f.NIDDistributionChannel
), grouped AS (
    SELECT
        x.Mes,
        d.TDistributionChannel AS CanalDistribuicao,
        COUNT(*) AS TotalDocumentos,
        SUM(x.DocumentoCancelado) AS DocumentosCancelados,
        100.0 * SUM(x.DocumentoCancelado) / NULLIF(COUNT(*), 0) AS TaxaCancelamento
    FROM docs x
    JOIN dbo.D_DistributionChannel d ON d.NIDDistributionChannel = x.NIDDistributionChannel
    GROUP BY x.Mes, d.TDistributionChannel
), ranked AS (
    SELECT
        g.*,
        ROW_NUMBER() OVER (
            PARTITION BY g.Mes
            ORDER BY g.TaxaCancelamento DESC, g.TotalDocumentos DESC, g.CanalDistribuicao
        ) AS rn
    FROM grouped g
)
SELECT
    Mes,
    CanalDistribuicao,
    TotalDocumentos,
    DocumentosCancelados,
    TaxaCancelamento
FROM ranked
WHERE rn <= 2
ORDER BY Mes, rn;
