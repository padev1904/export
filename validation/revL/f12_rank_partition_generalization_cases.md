# F12 rank_within_partition — casos de generalização

## G01 — Quais são os 2 clientes com maior valor líquido faturado dentro de cada organização de vendas em 2026?

### SQL manual independente
```sql
WITH grouped AS (
    SELECT so.TSalesOrganization AS OrganizacaoVendas,
           c.TCustomer AS Cliente,
           SUM(f.NetAmount) AS ValorLiquidoFaturado
    FROM F_Invoice f
    JOIN D_SalesOrganization so ON f.NIDSalesOrganization = so.NIDSalesOrganization
    JOIN D_Customer c ON f.NIDPayerParty = c.NIDCustomer
    WHERE f.BillingDocumentDate / 10000 = 2026 AND f.BillingDocumentIsCancelled = 0
    GROUP BY so.TSalesOrganization, c.TCustomer
), ranked AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY OrganizacaoVendas ORDER BY ValorLiquidoFaturado DESC, Cliente) AS rn
    FROM grouped
)
SELECT OrganizacaoVendas, Cliente, ValorLiquidoFaturado
FROM ranked WHERE rn <= 2
ORDER BY OrganizacaoVendas, ValorLiquidoFaturado DESC, Cliente;
```

### SQL gerado pelo gerador universal
Equivalente por resultado ao SQL manual independente.

## G02 — Quais são as 2 marcas com maior valor líquido faturado dentro de cada canal de distribuição em 2026?

### SQL manual independente
```sql
WITH grouped AS (
    SELECT dc.TDistributionChannel AS CanalDistribuicao,
           pb.TProductBrand AS MarcaProduto,
           SUM(f.NetAmount) AS ValorLiquidoFaturado
    FROM F_Invoice f
    JOIN D_DistributionChannel dc ON f.NIDDistributionChannel = dc.NIDDistributionChannel
    JOIN D_Product p ON f.NIDProduct = p.NIDProduct
    JOIN D_ProductBrand pb ON p.NIDProductBrand = pb.NIDProductBrand
    WHERE f.BillingDocumentDate / 10000 = 2026 AND f.BillingDocumentIsCancelled = 0
    GROUP BY dc.TDistributionChannel, pb.TProductBrand
), ranked AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY CanalDistribuicao ORDER BY ValorLiquidoFaturado DESC, MarcaProduto) rn FROM grouped
)
SELECT CanalDistribuicao, MarcaProduto, ValorLiquidoFaturado
FROM ranked WHERE rn <= 2
ORDER BY CanalDistribuicao, ValorLiquidoFaturado DESC, MarcaProduto;
```

### SQL gerado pelo gerador universal
Equivalente por resultado ao SQL manual independente.

## G03 — Quais são os 3 produtos com maior diferença entre preço de lista e valor líquido faturado dentro de cada mês em 2026?

### SQL manual independente
```sql
WITH grouped AS (
    SELECT ((f.BillingDocumentDate / 100) % 100) AS Mes,
           p.TProduct AS Produto,
           SUM(f.ZLP1PriceList) - SUM(f.NetAmount) AS DiferencaPrecoListaVsLiquido
    FROM F_Invoice f
    JOIN D_Product p ON f.NIDProduct = p.NIDProduct
    WHERE f.BillingDocumentDate / 10000 = 2026 AND f.BillingDocumentIsCancelled = 0
    GROUP BY ((f.BillingDocumentDate / 100) % 100), p.TProduct
), ranked AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY Mes ORDER BY DiferencaPrecoListaVsLiquido DESC, Produto) rn FROM grouped
)
SELECT Mes, Produto, DiferencaPrecoListaVsLiquido
FROM ranked WHERE rn <= 3
ORDER BY Mes, DiferencaPrecoListaVsLiquido DESC, Produto;
```

### SQL gerado pelo gerador universal
Equivalente por resultado ao SQL manual independente.

## G04 — Quais são os 2 países com maior crescimento absoluto de quantidade faturada dentro de cada canal de distribuição entre 2025 e 2026?

### SQL manual independente
```sql
WITH grouped AS (
    SELECT dc.TDistributionChannel AS CanalDistribuicao,
           co.TCountry AS Pais,
           SUM(CASE WHEN f.BillingDocumentDate / 10000 = 2026 THEN f.BillingQuantity ELSE 0 END)
           - SUM(CASE WHEN f.BillingDocumentDate / 10000 = 2025 THEN f.BillingQuantity ELSE 0 END) AS CrescimentoAbsolutoQuantidade
    FROM F_Invoice f
    JOIN D_DistributionChannel dc ON f.NIDDistributionChannel = dc.NIDDistributionChannel
    JOIN D_Country co ON f.NIDCountry = co.NIDCountry
    WHERE f.BillingDocumentDate / 10000 IN (2025, 2026) AND f.BillingDocumentIsCancelled = 0
    GROUP BY dc.TDistributionChannel, co.TCountry
), ranked AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY CanalDistribuicao ORDER BY CrescimentoAbsolutoQuantidade DESC, Pais) rn FROM grouped
)
SELECT CanalDistribuicao, Pais, CrescimentoAbsolutoQuantidade
FROM ranked WHERE rn <= 2
ORDER BY CanalDistribuicao, CrescimentoAbsolutoQuantidade DESC, Pais;
```

### SQL gerado pelo gerador universal
Equivalente por resultado ao SQL manual independente.

## G05 — Quais são as 2 famílias de produto com maior preço médio líquido por unidade dentro de cada canal de distribuição em 2026?

### SQL manual independente
```sql
WITH grouped AS (
    SELECT dc.TDistributionChannel AS CanalDistribuicao,
           pf.TProductFamily AS FamiliaProduto,
           SUM(f.NetAmount) / NULLIF(SUM(f.BillingQuantity),0) AS PrecoMedioLiquidoPorUnidade
    FROM F_Invoice f
    JOIN D_DistributionChannel dc ON f.NIDDistributionChannel = dc.NIDDistributionChannel
    JOIN D_Product p ON f.NIDProduct = p.NIDProduct
    JOIN D_ProductFamily pf ON p.NIDProductFamily = pf.NIDProductFamily
    WHERE f.BillingDocumentDate / 10000 = 2026 AND f.BillingDocumentIsCancelled = 0
    GROUP BY dc.TDistributionChannel, pf.TProductFamily
    HAVING SUM(f.BillingQuantity) <> 0
), ranked AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY CanalDistribuicao ORDER BY PrecoMedioLiquidoPorUnidade DESC, FamiliaProduto) rn FROM grouped
)
SELECT CanalDistribuicao, FamiliaProduto, PrecoMedioLiquidoPorUnidade
FROM ranked WHERE rn <= 2
ORDER BY CanalDistribuicao, PrecoMedioLiquidoPorUnidade DESC, FamiliaProduto;
```

### SQL gerado pelo gerador universal
Equivalente por resultado ao SQL manual independente.

## G06 — Quais são os 2 grupos de preço de cliente com maior valor líquido faturado dentro de cada país em 2026?

### SQL manual independente
```sql
WITH grouped AS (
    SELECT co.TCountry AS Pais,
           cpg.TCustomerPriceGroup AS GrupoPrecoCliente,
           SUM(f.NetAmount) AS ValorLiquidoFaturado
    FROM F_Invoice f
    JOIN D_Country co ON f.NIDCountry = co.NIDCountry
    JOIN D_CustomerPriceGroup cpg ON f.NIDCustomerPriceGroup = cpg.NIDCustomerPriceGroup
    WHERE f.BillingDocumentDate / 10000 = 2026 AND f.BillingDocumentIsCancelled = 0
    GROUP BY co.TCountry, cpg.TCustomerPriceGroup
), ranked AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY Pais ORDER BY ValorLiquidoFaturado DESC, GrupoPrecoCliente) rn FROM grouped
)
SELECT Pais, GrupoPrecoCliente, ValorLiquidoFaturado
FROM ranked WHERE rn <= 2
ORDER BY Pais, ValorLiquidoFaturado DESC, GrupoPrecoCliente;
```

### SQL gerado pelo gerador universal
Equivalente por resultado ao SQL manual independente.

## G07 — Quais são os 2 pontos de expedição com maior desconto promocional total dentro de cada mês em 2026?

### SQL manual independente
```sql
WITH grouped AS (
    SELECT ((f.BillingDocumentDate / 100) % 100) AS Mes,
           sp.TShippingPoint AS PontoExpedicao,
           SUM(f.ZDPRPromotional + f.ZCPRPromotionalCampaign + f.REA1PromotionalDiscount) AS DescontoPromocionalTotal
    FROM F_Invoice f
    JOIN D_ShippingPoint sp ON f.NIDShippingPoint = sp.NIDShippingPoint
    WHERE f.BillingDocumentDate / 10000 = 2026 AND f.BillingDocumentIsCancelled = 0
    GROUP BY ((f.BillingDocumentDate / 100) % 100), sp.TShippingPoint
), ranked AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY Mes ORDER BY DescontoPromocionalTotal ASC, PontoExpedicao) rn FROM grouped
)
SELECT Mes, PontoExpedicao, DescontoPromocionalTotal
FROM ranked WHERE rn <= 2
ORDER BY Mes, DescontoPromocionalTotal ASC, PontoExpedicao;
```

### SQL gerado pelo gerador universal
Equivalente por resultado ao SQL manual independente.

## G08 — Quais são as 2 organizações de vendas com maior valor líquido faturado dentro de cada país em 2026?

### SQL manual independente
```sql
WITH grouped AS (
    SELECT co.TCountry AS Pais,
           so.TSalesOrganization AS OrganizacaoVendas,
           SUM(f.NetAmount) AS ValorLiquidoFaturado
    FROM F_Invoice f
    JOIN D_Country co ON f.NIDCountry = co.NIDCountry
    JOIN D_SalesOrganization so ON f.NIDSalesOrganization = so.NIDSalesOrganization
    WHERE f.BillingDocumentDate / 10000 = 2026 AND f.BillingDocumentIsCancelled = 0
    GROUP BY co.TCountry, so.TSalesOrganization
), ranked AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY Pais ORDER BY ValorLiquidoFaturado DESC, OrganizacaoVendas) rn FROM grouped
)
SELECT Pais, OrganizacaoVendas, ValorLiquidoFaturado
FROM ranked WHERE rn <= 2
ORDER BY Pais, ValorLiquidoFaturado DESC, OrganizacaoVendas;
```

### SQL gerado pelo gerador universal
Equivalente por resultado ao SQL manual independente.
