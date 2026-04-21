# rank_within_partition — generalization cases revU

## G01

Quais são os 4 produtos com maior valor líquido faturado dentro de cada canal de distribuição em 2026?

```sql
WITH grouped AS (
    SELECT
        dc.TDistributionChannel AS CanalDistribuicao,
        p.TProduct AS Produto,
        SUM(f.NetAmount) AS ValorLiquidoFaturado
    FROM F_Invoice f
    JOIN D_DistributionChannel dc ON f.NIDDistributionChannel = dc.NIDDistributionChannel
    JOIN D_Product p ON f.NIDProduct = p.NIDProduct
    WHERE CAST(f.BillingDocumentDate / 10000 AS INT) = 2026
      AND f.BillingDocumentIsCancelled = 0
    GROUP BY dc.TDistributionChannel, p.TProduct
), ranked AS (
    SELECT g.*, ROW_NUMBER() OVER (PARTITION BY CanalDistribuicao ORDER BY ValorLiquidoFaturado DESC, Produto) AS rn
    FROM grouped g
)
SELECT CanalDistribuicao, Produto, ValorLiquidoFaturado
FROM ranked
WHERE rn <= 4
ORDER BY CanalDistribuicao, ValorLiquidoFaturado DESC, Produto;
```

## G02

Quais são os 2 países com maior crescimento absoluto de valor líquido faturado dentro de cada organização de vendas entre 2025 e 2026?

```sql
WITH grouped AS (
    SELECT
        so.TSalesOrganization AS OrganizacaoVendas,
        co.TCountry AS Pais,
        SUM(CASE WHEN CAST(f.BillingDocumentDate / 10000 AS INT) = 2026 THEN f.NetAmount ELSE 0 END)
        - SUM(CASE WHEN CAST(f.BillingDocumentDate / 10000 AS INT) = 2025 THEN f.NetAmount ELSE 0 END) AS CrescimentoAbsoluto
    FROM F_Invoice f
    JOIN D_SalesOrganization so ON f.NIDSalesOrganization = so.NIDSalesOrganization
    JOIN D_Country co ON f.NIDCountry = co.NIDCountry
    WHERE CAST(f.BillingDocumentDate / 10000 AS INT) IN (2025, 2026)
      AND f.BillingDocumentIsCancelled = 0
    GROUP BY so.TSalesOrganization, co.TCountry
), ranked AS (
    SELECT g.*, ROW_NUMBER() OVER (PARTITION BY OrganizacaoVendas ORDER BY CrescimentoAbsoluto DESC, Pais) AS rn
    FROM grouped g
)
SELECT OrganizacaoVendas, Pais, CrescimentoAbsoluto
FROM ranked
WHERE rn <= 2
ORDER BY OrganizacaoVendas, CrescimentoAbsoluto DESC, Pais;
```

## G03

Quais são os 2 grupos de cliente com maior desconto promocional total dentro de cada mês em 2026?

```sql
WITH grouped AS (
    SELECT
        CAST((f.BillingDocumentDate / 100) % 100 AS INT) AS Mes,
        cg.TCustomerGroup AS GrupoCliente,
        SUM(f.ZDPRPromotional + f.ZCPRPromotionalCampaign + f.REA1PromotionalDiscount) AS DescontoPromocionalTotal
    FROM F_Invoice f
    JOIN D_CustomerGroup cg ON f.NIDCustomerGroup = cg.NIDCustomerGroup
    WHERE CAST(f.BillingDocumentDate / 10000 AS INT) = 2026
      AND f.BillingDocumentIsCancelled = 0
    GROUP BY CAST((f.BillingDocumentDate / 100) % 100 AS INT), cg.TCustomerGroup
), ranked AS (
    SELECT g.*, ROW_NUMBER() OVER (PARTITION BY Mes ORDER BY DescontoPromocionalTotal ASC, GrupoCliente) AS rn
    FROM grouped g
)
SELECT Mes, GrupoCliente, DescontoPromocionalTotal
FROM ranked
WHERE rn <= 2
ORDER BY Mes, DescontoPromocionalTotal ASC, GrupoCliente;
```

## G04

Quais são as 2 marcas com maior preço médio líquido por unidade dentro de cada família de produto em 2026?

```sql
WITH grouped AS (
    SELECT
        pf.TProductFamily AS FamiliaProduto,
        pb.TProductBrand AS MarcaProduto,
        SUM(f.NetAmount) / NULLIF(SUM(f.BillingQuantity), 0) AS PrecoMedioLiquidoPorUnidade
    FROM F_Invoice f
    JOIN D_Product p ON f.NIDProduct = p.NIDProduct
    JOIN D_ProductFamily pf ON p.NIDProductFamily = pf.NIDProductFamily
    JOIN D_ProductBrand pb ON p.NIDProductBrand = pb.NIDProductBrand
    WHERE CAST(f.BillingDocumentDate / 10000 AS INT) = 2026
      AND f.BillingDocumentIsCancelled = 0
    GROUP BY pf.TProductFamily, pb.TProductBrand
    HAVING SUM(f.BillingQuantity) <> 0
), ranked AS (
    SELECT g.*, ROW_NUMBER() OVER (PARTITION BY FamiliaProduto ORDER BY PrecoMedioLiquidoPorUnidade DESC, MarcaProduto) AS rn
    FROM grouped g
)
SELECT FamiliaProduto, MarcaProduto, PrecoMedioLiquidoPorUnidade
FROM ranked
WHERE rn <= 2
ORDER BY FamiliaProduto, PrecoMedioLiquidoPorUnidade DESC, MarcaProduto;
```

## G05

Quais são os 2 pontos de expedição com maior valor líquido faturado dentro de cada organização de vendas em 2026?

```sql
WITH grouped AS (
    SELECT
        so.TSalesOrganization AS OrganizacaoVendas,
        sp.TShippingPoint AS PontoExpedicao,
        SUM(f.NetAmount) AS ValorLiquidoFaturado
    FROM F_Invoice f
    JOIN D_SalesOrganization so ON f.NIDSalesOrganization = so.NIDSalesOrganization
    JOIN D_ShippingPoint sp ON f.NIDShippingPoint = sp.NIDShippingPoint
    WHERE CAST(f.BillingDocumentDate / 10000 AS INT) = 2026
      AND f.BillingDocumentIsCancelled = 0
    GROUP BY so.TSalesOrganization, sp.TShippingPoint
), ranked AS (
    SELECT g.*, ROW_NUMBER() OVER (PARTITION BY OrganizacaoVendas ORDER BY ValorLiquidoFaturado DESC, PontoExpedicao) AS rn
    FROM grouped g
)
SELECT OrganizacaoVendas, PontoExpedicao, ValorLiquidoFaturado
FROM ranked
WHERE rn <= 2
ORDER BY OrganizacaoVendas, ValorLiquidoFaturado DESC, PontoExpedicao;
```

## G06

Quais são os 2 tipos de lista de preços com maior diferença entre preço de lista e valor líquido faturado em cada mês de 2026?

```sql
WITH grouped AS (
    SELECT
        CAST((f.BillingDocumentDate / 100) % 100 AS INT) AS Mes,
        plt.TPriceListType AS TipoListaPrecos,
        SUM(f.ZLP1PriceList) - SUM(f.NetAmount) AS DiferencaPrecoListaVsLiquido
    FROM F_Invoice f
    JOIN D_PriceListType plt ON f.NIDPriceListType = plt.NIDPriceListType
    WHERE CAST(f.BillingDocumentDate / 10000 AS INT) = 2026
      AND f.BillingDocumentIsCancelled = 0
    GROUP BY CAST((f.BillingDocumentDate / 100) % 100 AS INT), plt.TPriceListType
), ranked AS (
    SELECT g.*, ROW_NUMBER() OVER (PARTITION BY Mes ORDER BY DiferencaPrecoListaVsLiquido DESC, TipoListaPrecos) AS rn
    FROM grouped g
)
SELECT Mes, TipoListaPrecos, DiferencaPrecoListaVsLiquido
FROM ranked
WHERE rn <= 2
ORDER BY Mes, DiferencaPrecoListaVsLiquido DESC, TipoListaPrecos;
```
