-- Manual oracle SQL for monthly generalization candidates MG01-MG08
-- These queries are independent validation references.
-- They are not benchmark PASS/FAIL evidence until executed and compared by result equivalence.

-- MG01
-- Qual o valor líquido faturado por grupo de contas de cliente e por mês no ano atual?
WITH monthly_sales AS (
    SELECT
        DATEFROMPARTS(f.BillingDocumentDate / 10000, (f.BillingDocumentDate / 100) % 100, 1) AS Mes,
        cag.TCustomerAccountGroup AS GrupoContasCliente,
        SUM(f.NetAmount) AS ValorLiquidoFaturado
    FROM dbo.F_Invoice f
    JOIN dbo.D_Customer c
        ON f.NIDPayerParty = c.NIDCustomer
    JOIN dbo.D_CustomerAccountGroup cag
        ON c.NIDCustomerAccountGroup = cag.NIDCustomerAccountGroup
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate / 10000 = YEAR(GETDATE())
      AND f.BillingDocumentDate <= CONVERT(int, CONVERT(char(8), CAST(GETDATE() AS date), 112))
    GROUP BY DATEFROMPARTS(f.BillingDocumentDate / 10000, (f.BillingDocumentDate / 100) % 100, 1), cag.TCustomerAccountGroup
)
SELECT Mes, GrupoContasCliente, ValorLiquidoFaturado
FROM monthly_sales
ORDER BY Mes ASC, GrupoContasCliente;

-- MG02
-- Qual a diferença entre preço de lista e valor líquido faturado por marca e por mês no ano atual?
WITH monthly_sales AS (
    SELECT
        DATEFROMPARTS(f.BillingDocumentDate / 10000, (f.BillingDocumentDate / 100) % 100, 1) AS Mes,
        pb.TProductBrand AS MarcaProduto,
        SUM(f.ZLP1PriceList) - SUM(f.NetAmount) AS DiferencaPrecoListaVsLiquido
    FROM dbo.F_Invoice f
    JOIN dbo.D_Product p
        ON f.NIDProduct = p.NIDProduct
    JOIN dbo.D_ProductBrand pb
        ON p.NIDProductBrand = pb.NIDProductBrand
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate / 10000 = YEAR(GETDATE())
      AND f.BillingDocumentDate <= CONVERT(int, CONVERT(char(8), CAST(GETDATE() AS date), 112))
    GROUP BY DATEFROMPARTS(f.BillingDocumentDate / 10000, (f.BillingDocumentDate / 100) % 100, 1), pb.TProductBrand
)
SELECT Mes, MarcaProduto, DiferencaPrecoListaVsLiquido
FROM monthly_sales
ORDER BY Mes ASC, MarcaProduto;

-- MG03
-- Qual o valor líquido faturado por tipo de processamento de devolução e por mês no ano corrente?
WITH monthly_sales AS (
    SELECT
        DATEFROMPARTS(f.BillingDocumentDate / 10000, (f.BillingDocumentDate / 100) % 100, 1) AS Mes,
        ript.TReturnItemProcessingType AS TipoProcessamentoDevolucao,
        SUM(f.NetAmount) AS ValorLiquidoFaturado
    FROM dbo.F_Invoice f
    JOIN dbo.D_ReturnItemProcessingType ript
        ON f.NIDReturnItemProcessingType = ript.NIDReturnItemProcessingType
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate / 10000 = YEAR(GETDATE())
      AND f.BillingDocumentDate <= CONVERT(int, CONVERT(char(8), CAST(GETDATE() AS date), 112))
    GROUP BY DATEFROMPARTS(f.BillingDocumentDate / 10000, (f.BillingDocumentDate / 100) % 100, 1), ript.TReturnItemProcessingType
)
SELECT Mes, TipoProcessamentoDevolucao, ValorLiquidoFaturado
FROM monthly_sales
ORDER BY Mes ASC, TipoProcessamentoDevolucao;

-- MG04
-- Qual o valor líquido faturado por mês e por organização de vendas no ano atual?
WITH monthly_sales AS (
    SELECT
        DATEFROMPARTS(f.BillingDocumentDate / 10000, (f.BillingDocumentDate / 100) % 100, 1) AS Mes,
        so.TSalesOrganization AS OrganizacaoVendas,
        SUM(f.NetAmount) AS ValorLiquidoFaturado
    FROM dbo.F_Invoice f
    JOIN dbo.D_SalesOrganization so
        ON f.NIDSalesOrganization = so.NIDSalesOrganization
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate / 10000 = YEAR(GETDATE())
      AND f.BillingDocumentDate <= CONVERT(int, CONVERT(char(8), CAST(GETDATE() AS date), 112))
    GROUP BY DATEFROMPARTS(f.BillingDocumentDate / 10000, (f.BillingDocumentDate / 100) % 100, 1), so.TSalesOrganization
)
SELECT Mes, OrganizacaoVendas, ValorLiquidoFaturado
FROM monthly_sales
ORDER BY Mes ASC, OrganizacaoVendas;

-- MG05
-- Qual a quantidade faturada por mês e por organização de vendas em 2025?
WITH monthly_sales AS (
    SELECT
        DATEFROMPARTS(f.BillingDocumentDate / 10000, (f.BillingDocumentDate / 100) % 100, 1) AS Mes,
        so.TSalesOrganization AS OrganizacaoVendas,
        SUM(f.BillingQuantity) AS QuantidadeFaturada
    FROM dbo.F_Invoice f
    JOIN dbo.D_SalesOrganization so
        ON f.NIDSalesOrganization = so.NIDSalesOrganization
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate / 10000 = 2025
    GROUP BY DATEFROMPARTS(f.BillingDocumentDate / 10000, (f.BillingDocumentDate / 100) % 100, 1), so.TSalesOrganization
)
SELECT Mes, OrganizacaoVendas, QuantidadeFaturada
FROM monthly_sales
ORDER BY Mes ASC, OrganizacaoVendas;

-- MG06
-- Qual a margem bruta por marca e por mês em 2026 considerando apenas registos adicionais calculados?
WITH monthly_sales AS (
    SELECT
        DATEFROMPARTS(f.BillingDocumentDate / 10000, (f.BillingDocumentDate / 100) % 100, 1) AS Mes,
        pb.TProductBrand AS MarcaProduto,
        SUM(f.GrossMargin) AS MargemBruta
    FROM dbo.F_Invoice f
    JOIN dbo.D_Product p
        ON f.NIDProduct = p.NIDProduct
    JOIN dbo.D_ProductBrand pb
        ON p.NIDProductBrand = pb.NIDProductBrand
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.IsItAnAdditionalCalculatedRecord = 1
      AND f.BillingDocumentDate / 10000 = 2026
    GROUP BY DATEFROMPARTS(f.BillingDocumentDate / 10000, (f.BillingDocumentDate / 100) % 100, 1), pb.TProductBrand
)
SELECT Mes, MarcaProduto, MargemBruta
FROM monthly_sales
ORDER BY Mes ASC, MarcaProduto;

-- MG07
-- Como evoluiu por mês nos últimos 6 meses o valor líquido faturado por grupo de contas de cliente?
WITH monthly_sales AS (
    SELECT
        DATEFROMPARTS(f.BillingDocumentDate / 10000, (f.BillingDocumentDate / 100) % 100, 1) AS Mes,
        cag.TCustomerAccountGroup AS GrupoContasCliente,
        SUM(f.NetAmount) AS ValorLiquidoFaturado
    FROM dbo.F_Invoice f
    JOIN dbo.D_Customer c
        ON f.NIDPayerParty = c.NIDCustomer
    JOIN dbo.D_CustomerAccountGroup cag
        ON c.NIDCustomerAccountGroup = cag.NIDCustomerAccountGroup
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, 1, EOMONTH(CAST(GETDATE() AS date), -6)), 112))
      AND f.BillingDocumentDate <= CONVERT(int, CONVERT(char(8), CAST(GETDATE() AS date), 112))
    GROUP BY DATEFROMPARTS(f.BillingDocumentDate / 10000, (f.BillingDocumentDate / 100) % 100, 1), cag.TCustomerAccountGroup
)
SELECT Mes, GrupoContasCliente, ValorLiquidoFaturado
FROM monthly_sales
ORDER BY Mes ASC, GrupoContasCliente;

-- MG08
-- Qual a diferença entre preço de lista e valor líquido faturado por organização de vendas e por mês em 2026?
WITH monthly_sales AS (
    SELECT
        DATEFROMPARTS(f.BillingDocumentDate / 10000, (f.BillingDocumentDate / 100) % 100, 1) AS Mes,
        so.TSalesOrganization AS OrganizacaoVendas,
        SUM(f.ZLP1PriceList) - SUM(f.NetAmount) AS DiferencaPrecoListaVsLiquido
    FROM dbo.F_Invoice f
    JOIN dbo.D_SalesOrganization so
        ON f.NIDSalesOrganization = so.NIDSalesOrganization
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate / 10000 = 2026
    GROUP BY DATEFROMPARTS(f.BillingDocumentDate / 10000, (f.BillingDocumentDate / 100) % 100, 1), so.TSalesOrganization
)
SELECT Mes, OrganizacaoVendas, DiferencaPrecoListaVsLiquido
FROM monthly_sales
ORDER BY Mes ASC, OrganizacaoVendas;
