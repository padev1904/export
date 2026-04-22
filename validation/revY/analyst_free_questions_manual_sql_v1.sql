-- A01
-- Qual o total de descontos de quantidade por zona de transporte do cliente em 2026?
SELECT
    tz.TTranspZone AS ZonaTransporte,
    SUM(f.ZDQ1QtyDiscount) AS DescontoQuantidade
FROM dbo.F_Invoice f
JOIN dbo.D_Customer c
    ON c.NIDCustomer = f.NIDPayerParty
JOIN dbo.D_TranspZone tz
    ON tz.NIDTranspZone = c.NIDTranspZone
WHERE f.BillingDocumentIsCancelled = 0
  AND f.BillingDocumentDate >= 20260101
  AND f.BillingDocumentDate <= 20261231
GROUP BY tz.TTranspZone
ORDER BY DescontoQuantidade ASC, ZonaTransporte ASC;

-- A02
-- Qual o peso bruto total por marca de produto em 2026?
SELECT
    pb.TProductBrand AS MarcaProduto,
    SUM(f.ItemGrossWeight) AS PesoBrutoTotal
FROM dbo.F_Invoice f
JOIN dbo.D_Product p
    ON p.NIDProduct = f.NIDProduct
JOIN dbo.D_ProductBrand pb
    ON pb.NIDProductBrand = p.NIDProductBrand
WHERE f.BillingDocumentIsCancelled = 0
  AND f.BillingDocumentDate >= 20260101
  AND f.BillingDocumentDate <= 20261231
GROUP BY pb.TProductBrand
ORDER BY PesoBrutoTotal DESC, MarcaProduto ASC;

-- A03
-- Qual a diferença entre quantidade faturada e quantidade em unidade base por tipo de material em 2026?
SELECT
    mt.TMaterialType AS TipoMaterial,
    SUM(f.BillingQuantity) - SUM(f.BillingQuantityInBaseUnit) AS DiferencaQuantidadeFaturadaVsBase
FROM dbo.F_Invoice f
JOIN dbo.D_Product p
    ON p.NIDProduct = f.NIDProduct
JOIN dbo.D_MaterialType mt
    ON mt.NIDMaterialType = p.NIDMaterialType
WHERE f.BillingDocumentIsCancelled = 0
  AND f.BillingDocumentDate >= 20260101
  AND f.BillingDocumentDate <= 20261231
GROUP BY mt.TMaterialType
ORDER BY DiferencaQuantidadeFaturadaVsBase DESC, TipoMaterial ASC;

-- A04
-- Qual o peso líquido total por condição de expedição do cliente em 2026?
SELECT
    sc.TShippingCondition AS CondicaoExpedicao,
    SUM(f.ItemNetWeight) AS PesoLiquidoTotal
FROM dbo.F_Invoice f
JOIN dbo.D_Customer c
    ON c.NIDCustomer = f.NIDPayerParty
JOIN dbo.D_ShippingCondition sc
    ON sc.NIDShippingCondition = c.NIDShippingCondition
WHERE f.BillingDocumentIsCancelled = 0
  AND f.BillingDocumentDate >= 20260101
  AND f.BillingDocumentDate <= 20261231
GROUP BY sc.TShippingCondition
ORDER BY PesoLiquidoTotal DESC, CondicaoExpedicao ASC;

-- A05
-- Quais são os 3 pontos de expedição com maior valor líquido faturado dentro de cada canal de distribuição em 2026?
WITH grouped AS (
    SELECT
        dc.TDistributionChannel AS CanalDistribuicao,
        sp.TShippingPoint AS PontoExpedicao,
        SUM(f.NetAmount) AS ValorLiquidoFaturado
    FROM dbo.F_Invoice f
    JOIN dbo.D_DistributionChannel dc ON dc.NIDDistributionChannel = f.NIDDistributionChannel
    JOIN dbo.D_ShippingPoint sp ON sp.NIDShippingPoint = f.NIDShippingPoint
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= 20260101 AND f.BillingDocumentDate <= 20261231
    GROUP BY dc.TDistributionChannel, sp.TShippingPoint
), ranked AS (
    SELECT g.*, ROW_NUMBER() OVER (PARTITION BY g.CanalDistribuicao ORDER BY g.ValorLiquidoFaturado DESC, g.PontoExpedicao ASC) AS rn
    FROM grouped g
)
SELECT CanalDistribuicao, PontoExpedicao, ValorLiquidoFaturado
FROM ranked
WHERE rn <= 3
ORDER BY CanalDistribuicao ASC, ValorLiquidoFaturado DESC, PontoExpedicao ASC;

-- A06
-- Quais são os 2 grupos de preço de cliente com maior desconto de quantidade dentro de cada marca em 2026?
WITH grouped AS (
    SELECT
        pb.TProductBrand AS MarcaProduto,
        cpg.TCustomerPriceGroup AS GrupoPrecoCliente,
        SUM(f.ZDQ1QtyDiscount) AS DescontoQuantidade
    FROM dbo.F_Invoice f
    JOIN dbo.D_Product p ON p.NIDProduct = f.NIDProduct
    JOIN dbo.D_ProductBrand pb ON pb.NIDProductBrand = p.NIDProductBrand
    JOIN dbo.D_CustomerPriceGroup cpg ON cpg.NIDCustomerPriceGroup = f.NIDCustomerPriceGroup
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= 20260101 AND f.BillingDocumentDate <= 20261231
    GROUP BY pb.TProductBrand, cpg.TCustomerPriceGroup
), ranked AS (
    SELECT g.*, ROW_NUMBER() OVER (PARTITION BY g.MarcaProduto ORDER BY g.DescontoQuantidade ASC, g.GrupoPrecoCliente ASC) AS rn
    FROM grouped g
)
SELECT MarcaProduto, GrupoPrecoCliente, DescontoQuantidade
FROM ranked
WHERE rn <= 2
ORDER BY MarcaProduto ASC, DescontoQuantidade ASC, GrupoPrecoCliente ASC;

-- A07
-- Quais são as 2 famílias de produto com maior preço médio líquido por unidade dentro de cada organização de vendas em 2026?
WITH grouped AS (
    SELECT
        so.TSalesOrganization AS OrganizacaoVendas,
        pf.TProductFamily AS FamiliaProduto,
        SUM(f.NetAmount) / NULLIF(SUM(f.BillingQuantity), 0) AS PrecoMedioLiquidoPorUnidade
    FROM dbo.F_Invoice f
    JOIN dbo.D_SalesOrganization so ON so.NIDSalesOrganization = f.NIDSalesOrganization
    JOIN dbo.D_Product p ON p.NIDProduct = f.NIDProduct
    JOIN dbo.D_ProductFamily pf ON pf.NIDProductFamily = p.NIDProductFamily
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= 20260101 AND f.BillingDocumentDate <= 20261231
    GROUP BY so.TSalesOrganization, pf.TProductFamily
    HAVING SUM(f.BillingQuantity) <> 0
), ranked AS (
    SELECT g.*, ROW_NUMBER() OVER (PARTITION BY g.OrganizacaoVendas ORDER BY g.PrecoMedioLiquidoPorUnidade DESC, g.FamiliaProduto ASC) AS rn
    FROM grouped g
)
SELECT OrganizacaoVendas, FamiliaProduto, PrecoMedioLiquidoPorUnidade
FROM ranked
WHERE rn <= 2
ORDER BY OrganizacaoVendas ASC, PrecoMedioLiquidoPorUnidade DESC, FamiliaProduto ASC;

-- A08
-- Quais são os 3 clientes com maior crescimento absoluto de quantidade faturada dentro de cada região entre 2025 e 2026?
WITH grouped AS (
    SELECT
        r.TRegion AS Regiao,
        c.TCustomer AS Cliente,
        SUM(CASE WHEN f.BillingDocumentDate >= 20260101 AND f.BillingDocumentDate <= 20261231 THEN f.BillingQuantity ELSE 0 END)
      - SUM(CASE WHEN f.BillingDocumentDate >= 20250101 AND f.BillingDocumentDate <= 20251231 THEN f.BillingQuantity ELSE 0 END) AS CrescimentoAbsolutoQuantidade
    FROM dbo.F_Invoice f
    JOIN dbo.D_Region r ON r.NIDRegion = f.NIDRegion
    JOIN dbo.D_Customer c ON c.NIDCustomer = f.NIDPayerParty
    WHERE CAST(f.BillingDocumentDate / 10000 AS INT) IN (2025, 2026)
      AND f.BillingDocumentIsCancelled = 0
    GROUP BY r.TRegion, c.TCustomer
), ranked AS (
    SELECT g.*, ROW_NUMBER() OVER (PARTITION BY g.Regiao ORDER BY g.CrescimentoAbsolutoQuantidade DESC, g.Cliente ASC) AS rn
    FROM grouped g
)
SELECT Regiao, Cliente, CrescimentoAbsolutoQuantidade
FROM ranked
WHERE rn <= 3
ORDER BY Regiao ASC, CrescimentoAbsolutoQuantidade DESC, Cliente ASC;

-- A09
-- Qual a diferença entre o preço de lista e o valor líquido faturado por país e por mês em 2026?
WITH monthly_sales AS (
    SELECT
        DATEFROMPARTS(f.BillingDocumentDate / 10000, (f.BillingDocumentDate / 100) % 100, 1) AS Mes,
        co.TCountry AS Pais,
        SUM(f.ZLP1PriceList) - SUM(f.NetAmount) AS DiferencaPrecoListaVsLiquido
    FROM dbo.F_Invoice f
    JOIN dbo.D_Country co ON co.NIDCountry = f.NIDCountry
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= 20260101 AND f.BillingDocumentDate <= 20261231
    GROUP BY DATEFROMPARTS(f.BillingDocumentDate / 10000, (f.BillingDocumentDate / 100) % 100, 1), co.TCountry
)
SELECT Mes, Pais, DiferencaPrecoListaVsLiquido
FROM monthly_sales
ORDER BY Mes ASC, Pais ASC;

-- A10
-- Quais são os 2 canais de distribuição com maior taxa de cancelamento de documentos dentro de cada mês em 2026?
WITH docs AS (
    SELECT
        CAST((f.BillingDocumentDate / 100) % 100 AS INT) AS Mes,
        f.BillingDocument,
        f.NIDDistributionChannel,
        MAX(CASE WHEN f.BillingDocumentIsCancelled = 1 THEN 1 ELSE 0 END) AS DocumentoCancelado
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentDate >= 20260101 AND f.BillingDocumentDate <= 20261231
    GROUP BY CAST((f.BillingDocumentDate / 100) % 100 AS INT), f.BillingDocument, f.NIDDistributionChannel
), rates AS (
    SELECT
        d.Mes,
        dc.TDistributionChannel AS CanalDistribuicao,
        COUNT(*) AS TotalDocumentos,
        SUM(d.DocumentoCancelado) AS DocumentosCancelados,
        100.0 * SUM(d.DocumentoCancelado) / NULLIF(COUNT(*), 0) AS TaxaCancelamento
    FROM docs d
    JOIN dbo.D_DistributionChannel dc ON dc.NIDDistributionChannel = d.NIDDistributionChannel
    GROUP BY d.Mes, dc.TDistributionChannel
), ranked AS (
    SELECT r.*, ROW_NUMBER() OVER (PARTITION BY r.Mes ORDER BY r.TaxaCancelamento DESC, r.TotalDocumentos DESC, r.CanalDistribuicao ASC) AS rn
    FROM rates r
)
SELECT Mes, CanalDistribuicao, TotalDocumentos, DocumentosCancelados, TaxaCancelamento
FROM ranked
WHERE rn <= 2
ORDER BY Mes ASC, rn ASC;
