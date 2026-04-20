# Lifecycle generalization cases — revE

Casos fora do benchmark usados para validar generalização da família `F17_lifecycle`.

Semântica operacional adotada:
- `reativado`: atividade recente e ausência de atividade na janela de inatividade imediatamente anterior;
- `perdido`: atividade antes da janela recente e ausência de atividade na janela recente;
- por organização de vendas: semântica por par `(OrganizacaoVendas, Entidade)`.

## G01 — Quais os produtos reativados nos últimos 30 dias após 180 dias sem vendas?

- operação: `reactivated_list`
- entidade: `product`
- dimensão: `nenhuma`
- janela recente: `30 dias`
- janela de inatividade: `180 dias`
- meses móveis: `-`
- resultado: `PASS` (ok)
- linhas devolvidas pelo SQL manual: `47`
- linhas devolvidas pelo gerador: `47`

### SQL manual independente
```sql
WITH recent_products AS (
    SELECT DISTINCT NIDProduct
    FROM dbo.F_Invoice
    WHERE BillingDocumentIsCancelled = 0
      AND BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -30, CAST(GETDATE() AS date)), 112))
),
prior_180 AS (
    SELECT DISTINCT NIDProduct
    FROM dbo.F_Invoice
    WHERE BillingDocumentIsCancelled = 0
      AND BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -210, CAST(GETDATE() AS date)), 112))
      AND BillingDocumentDate < CONVERT(int, CONVERT(char(8), DATEADD(day, -30, CAST(GETDATE() AS date)), 112))
)
SELECT rp.NIDProduct
FROM recent_products rp
EXCEPT
SELECT p180.NIDProduct
FROM prior_180 p180
ORDER BY NIDProduct ASC;
```

### SQL do gerador
```sql
WITH recent_entities AS (
    SELECT DISTINCT
        f.NIDProduct AS NIDProduct
    FROM dbo.F_Invoice f
    
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -30, CAST(GETDATE() AS date)), 112))
),
inactive_window AS (
    SELECT DISTINCT
        f.NIDProduct AS NIDProduct
    FROM dbo.F_Invoice f
    
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -210, CAST(GETDATE() AS date)), 112))
      AND f.BillingDocumentDate < CONVERT(int, CONVERT(char(8), DATEADD(day, -30, CAST(GETDATE() AS date)), 112))
)
SELECT
    rc.NIDProduct
FROM recent_entities rc
WHERE NOT EXISTS (
    SELECT 1
    FROM inactive_window iw
    WHERE iw.NIDProduct = rc.NIDProduct
)
ORDER BY rc.NIDProduct ASC;
```

## G02 — Quais os clientes perdidos nos últimos 90 dias por organização de vendas?

- operação: `lost_list_by_dimension`
- entidade: `customer`
- dimensão: `sales_organization`
- janela recente: `90 dias`
- janela de inatividade: `- dias`
- meses móveis: `-`
- resultado: `PASS` (ok)
- linhas devolvidas pelo SQL manual: `52`
- linhas devolvidas pelo gerador: `52`

### SQL manual independente
```sql
WITH historical_pairs AS (
    SELECT DISTINCT
        so.TSalesOrganization AS OrganizacaoVendas,
        f.NIDPayerParty
    FROM dbo.F_Invoice f
    JOIN dbo.D_SalesOrganization so
      ON f.NIDSalesOrganization = so.NIDSalesOrganization
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate < CONVERT(int, CONVERT(char(8), DATEADD(day, -90, CAST(GETDATE() AS date)), 112))
),
recent_pairs AS (
    SELECT DISTINCT
        so.TSalesOrganization AS OrganizacaoVendas,
        f.NIDPayerParty
    FROM dbo.F_Invoice f
    JOIN dbo.D_SalesOrganization so
      ON f.NIDSalesOrganization = so.NIDSalesOrganization
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -90, CAST(GETDATE() AS date)), 112))
)
SELECT hp.OrganizacaoVendas, hp.NIDPayerParty
FROM historical_pairs hp
EXCEPT
SELECT rp.OrganizacaoVendas, rp.NIDPayerParty
FROM recent_pairs rp
ORDER BY OrganizacaoVendas ASC, NIDPayerParty ASC;
```

### SQL do gerador
```sql
WITH prior_entities AS (
    SELECT DISTINCT
        so.TSalesOrganization AS OrganizacaoVendas,
        f.NIDPayerParty AS NIDPayerParty
    FROM dbo.F_Invoice f
    JOIN dbo.D_SalesOrganization so ON f.NIDSalesOrganization = so.NIDSalesOrganization
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate < CONVERT(int, CONVERT(char(8), DATEADD(day, -90, CAST(GETDATE() AS date)), 112))
),
recent_entities AS (
    SELECT DISTINCT
        so.TSalesOrganization AS OrganizacaoVendas,
        f.NIDPayerParty AS NIDPayerParty
    FROM dbo.F_Invoice f
    JOIN dbo.D_SalesOrganization so ON f.NIDSalesOrganization = so.NIDSalesOrganization
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -90, CAST(GETDATE() AS date)), 112))
)
SELECT
    p.OrganizacaoVendas,
    p.NIDPayerParty
FROM prior_entities p
WHERE NOT EXISTS (
    SELECT 1
    FROM recent_entities r
    WHERE r.OrganizacaoVendas = p.OrganizacaoVendas AND r.NIDPayerParty = p.NIDPayerParty
)
ORDER BY p.OrganizacaoVendas ASC, p.NIDPayerParty ASC;
```

## G03 — Quantos clientes perdidos existem nos últimos 60 dias?

- operação: `lost_count`
- entidade: `customer`
- dimensão: `nenhuma`
- janela recente: `60 dias`
- janela de inatividade: `- dias`
- meses móveis: `-`
- resultado: `PASS` (ok)
- linhas devolvidas pelo SQL manual: `1`
- linhas devolvidas pelo gerador: `1`

### SQL manual independente
```sql
WITH previous_customers AS (
    SELECT DISTINCT NIDPayerParty
    FROM dbo.F_Invoice
    WHERE BillingDocumentIsCancelled = 0
      AND BillingDocumentDate < CONVERT(int, CONVERT(char(8), DATEADD(day, -60, CAST(GETDATE() AS date)), 112))
),
current_customers AS (
    SELECT DISTINCT NIDPayerParty
    FROM dbo.F_Invoice
    WHERE BillingDocumentIsCancelled = 0
      AND BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -60, CAST(GETDATE() AS date)), 112))
)
SELECT COUNT(*) AS ClientesPerdidos
FROM (
    SELECT NIDPayerParty FROM previous_customers
    EXCEPT
    SELECT NIDPayerParty FROM current_customers
) x;
```

### SQL do gerador
```sql
WITH prior_entities AS (
    SELECT DISTINCT
        f.NIDPayerParty AS NIDPayerParty
    FROM dbo.F_Invoice f
    
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate < CONVERT(int, CONVERT(char(8), DATEADD(day, -60, CAST(GETDATE() AS date)), 112))
),
recent_entities AS (
    SELECT DISTINCT
        f.NIDPayerParty AS NIDPayerParty
    FROM dbo.F_Invoice f
    
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -60, CAST(GETDATE() AS date)), 112))
)
SELECT
    COUNT(*) AS ClientesPerdidos
FROM prior_entities p
WHERE NOT EXISTS (
    SELECT 1
    FROM recent_entities r
    WHERE r.NIDPayerParty = p.NIDPayerParty
);
```

## G04 — Mostra o número mensal de produtos com primeira venda no último ano móvel.

- operação: `first_purchase_monthly_count`
- entidade: `product`
- dimensão: `nenhuma`
- janela recente: `- dias`
- janela de inatividade: `- dias`
- meses móveis: `12`
- resultado: `PASS` (ok)
- linhas devolvidas pelo SQL manual: `12`
- linhas devolvidas pelo gerador: `12`

### SQL manual independente
```sql
SELECT
    DATEFROMPARTS(
        MIN_DATE / 10000,
        (MIN_DATE / 100) % 100,
        1
    ) AS Mes,
    COUNT(*) AS ProdutosNovos
FROM (
    SELECT
        NIDProduct,
        MIN(BillingDocumentDate) AS MIN_DATE
    FROM dbo.F_Invoice
    WHERE BillingDocumentIsCancelled = 0
    GROUP BY NIDProduct
) p
WHERE MIN_DATE >= CONVERT(int, CONVERT(char(8), DATEADD(day, 1, EOMONTH(GETDATE(), -12)), 112))
GROUP BY DATEFROMPARTS(
    MIN_DATE / 10000,
    (MIN_DATE / 100) % 100,
    1
)
ORDER BY Mes ASC;
```

### SQL do gerador
```sql
WITH first_purchase AS (
    SELECT
        f.NIDProduct AS NIDProduct,
        MIN(f.BillingDocumentDate) AS PrimeiraCompraInt
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentIsCancelled = 0
    GROUP BY f.NIDProduct
)
SELECT
    DATEFROMPARTS(
        fp.PrimeiraCompraInt / 10000,
        (fp.PrimeiraCompraInt / 100) % 100,
        1
    ) AS Mes,
    COUNT(*) AS ProdutosNovos
FROM first_purchase fp
WHERE fp.PrimeiraCompraInt >= CONVERT(int, CONVERT(char(8), DATEADD(day, 1, EOMONTH(GETDATE(), -12)), 112))
GROUP BY DATEFROMPARTS(
    fp.PrimeiraCompraInt / 10000,
    (fp.PrimeiraCompraInt / 100) % 100,
    1
)
ORDER BY Mes ASC;
```

## G05 — Quantos produtos foram reativados no último mês após 120 dias sem vendas?

- operação: `reactivated_count`
- entidade: `product`
- dimensão: `nenhuma`
- janela recente: `30 dias`
- janela de inatividade: `120 dias`
- meses móveis: `-`
- resultado: `PASS` (ok)
- linhas devolvidas pelo SQL manual: `1`
- linhas devolvidas pelo gerador: `1`

### SQL manual independente
```sql
WITH recent_products AS (
    SELECT DISTINCT NIDProduct
    FROM dbo.F_Invoice
    WHERE BillingDocumentIsCancelled = 0
      AND BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -30, CAST(GETDATE() AS date)), 112))
),
inactive_products AS (
    SELECT DISTINCT NIDProduct
    FROM dbo.F_Invoice
    WHERE BillingDocumentIsCancelled = 0
      AND BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -150, CAST(GETDATE() AS date)), 112))
      AND BillingDocumentDate < CONVERT(int, CONVERT(char(8), DATEADD(day, -30, CAST(GETDATE() AS date)), 112))
)
SELECT COUNT(*) AS ProdutosReativados
FROM (
    SELECT NIDProduct FROM recent_products
    EXCEPT
    SELECT NIDProduct FROM inactive_products
) z;
```

### SQL do gerador
```sql
WITH recent_entities AS (
    SELECT DISTINCT
        f.NIDProduct AS NIDProduct
    FROM dbo.F_Invoice f
    
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -30, CAST(GETDATE() AS date)), 112))
),
inactive_window AS (
    SELECT DISTINCT
        f.NIDProduct AS NIDProduct
    FROM dbo.F_Invoice f
    
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -150, CAST(GETDATE() AS date)), 112))
      AND f.BillingDocumentDate < CONVERT(int, CONVERT(char(8), DATEADD(day, -30, CAST(GETDATE() AS date)), 112))
)
SELECT
    COUNT(*) AS ProdutosReativados
FROM recent_entities rc
WHERE NOT EXISTS (
    SELECT 1
    FROM inactive_window iw
    WHERE iw.NIDProduct = rc.NIDProduct
);
```

## G06 — Quais os clientes reativados nos últimos 45 dias após 120 dias sem compras?

- operação: `reactivated_list`
- entidade: `customer`
- dimensão: `nenhuma`
- janela recente: `45 dias`
- janela de inatividade: `120 dias`
- meses móveis: `-`
- resultado: `PASS` (ok)
- linhas devolvidas pelo SQL manual: `13`
- linhas devolvidas pelo gerador: `13`

### SQL manual independente
```sql
WITH recent_customers AS (
    SELECT DISTINCT NIDPayerParty
    FROM dbo.F_Invoice
    WHERE BillingDocumentIsCancelled = 0
      AND BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -45, CAST(GETDATE() AS date)), 112))
),
inactive_customers AS (
    SELECT DISTINCT NIDPayerParty
    FROM dbo.F_Invoice
    WHERE BillingDocumentIsCancelled = 0
      AND BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -165, CAST(GETDATE() AS date)), 112))
      AND BillingDocumentDate < CONVERT(int, CONVERT(char(8), DATEADD(day, -45, CAST(GETDATE() AS date)), 112))
)
SELECT NIDPayerParty
FROM recent_customers
EXCEPT
SELECT NIDPayerParty
FROM inactive_customers
ORDER BY NIDPayerParty ASC;
```

### SQL do gerador
```sql
WITH recent_entities AS (
    SELECT DISTINCT
        f.NIDPayerParty AS NIDPayerParty
    FROM dbo.F_Invoice f
    
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -45, CAST(GETDATE() AS date)), 112))
),
inactive_window AS (
    SELECT DISTINCT
        f.NIDPayerParty AS NIDPayerParty
    FROM dbo.F_Invoice f
    
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -165, CAST(GETDATE() AS date)), 112))
      AND f.BillingDocumentDate < CONVERT(int, CONVERT(char(8), DATEADD(day, -45, CAST(GETDATE() AS date)), 112))
)
SELECT
    rc.NIDPayerParty
FROM recent_entities rc
WHERE NOT EXISTS (
    SELECT 1
    FROM inactive_window iw
    WHERE iw.NIDPayerParty = rc.NIDPayerParty
)
ORDER BY rc.NIDPayerParty ASC;
```

## G07 — Quantos clientes foram reativados nos últimos 30 dias após 180 dias sem compras por organização de vendas?

- operação: `reactivated_count`
- entidade: `customer`
- dimensão: `sales_organization`
- janela recente: `30 dias`
- janela de inatividade: `180 dias`
- meses móveis: `-`
- resultado: `PASS` (ok)
- linhas devolvidas pelo SQL manual: `1`
- linhas devolvidas pelo gerador: `1`

### SQL manual independente
```sql
WITH recent_pairs AS (
    SELECT DISTINCT
        so.TSalesOrganization AS OrganizacaoVendas,
        f.NIDPayerParty
    FROM dbo.F_Invoice f
    JOIN dbo.D_SalesOrganization so
      ON f.NIDSalesOrganization = so.NIDSalesOrganization
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -30, CAST(GETDATE() AS date)), 112))
),
inactive_pairs AS (
    SELECT DISTINCT
        so.TSalesOrganization AS OrganizacaoVendas,
        f.NIDPayerParty
    FROM dbo.F_Invoice f
    JOIN dbo.D_SalesOrganization so
      ON f.NIDSalesOrganization = so.NIDSalesOrganization
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -210, CAST(GETDATE() AS date)), 112))
      AND f.BillingDocumentDate < CONVERT(int, CONVERT(char(8), DATEADD(day, -30, CAST(GETDATE() AS date)), 112))
)
SELECT OrganizacaoVendas, COUNT(*) AS ClientesReativados
FROM (
    SELECT OrganizacaoVendas, NIDPayerParty FROM recent_pairs
    EXCEPT
    SELECT OrganizacaoVendas, NIDPayerParty FROM inactive_pairs
) r
GROUP BY OrganizacaoVendas
ORDER BY OrganizacaoVendas ASC;
```

### SQL do gerador
```sql
WITH recent_entities AS (
    SELECT DISTINCT
        so.TSalesOrganization AS OrganizacaoVendas,
        f.NIDPayerParty AS NIDPayerParty
    FROM dbo.F_Invoice f
    JOIN dbo.D_SalesOrganization so ON f.NIDSalesOrganization = so.NIDSalesOrganization
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -30, CAST(GETDATE() AS date)), 112))
),
inactive_window AS (
    SELECT DISTINCT
        so.TSalesOrganization AS OrganizacaoVendas,
        f.NIDPayerParty AS NIDPayerParty
    FROM dbo.F_Invoice f
    JOIN dbo.D_SalesOrganization so ON f.NIDSalesOrganization = so.NIDSalesOrganization
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -210, CAST(GETDATE() AS date)), 112))
      AND f.BillingDocumentDate < CONVERT(int, CONVERT(char(8), DATEADD(day, -30, CAST(GETDATE() AS date)), 112))
)
SELECT
    rc.OrganizacaoVendas,
    COUNT(*) AS ClientesReativados
FROM recent_entities rc
WHERE NOT EXISTS (
    SELECT 1
    FROM inactive_window iw
    WHERE iw.OrganizacaoVendas = rc.OrganizacaoVendas AND iw.NIDPayerParty = rc.NIDPayerParty
)
GROUP BY rc.OrganizacaoVendas
ORDER BY rc.OrganizacaoVendas ASC;
```

## G08 — Quais os produtos perdidos nos últimos 75 dias?

- operação: `lost_list`
- entidade: `product`
- dimensão: `nenhuma`
- janela recente: `75 dias`
- janela de inatividade: `- dias`
- meses móveis: `-`
- resultado: `PASS` (ok)
- linhas devolvidas pelo SQL manual: `204`
- linhas devolvidas pelo gerador: `204`

### SQL manual independente
```sql
WITH before_cutoff AS (
    SELECT DISTINCT NIDProduct
    FROM dbo.F_Invoice
    WHERE BillingDocumentIsCancelled = 0
      AND BillingDocumentDate < CONVERT(int, CONVERT(char(8), DATEADD(day, -75, CAST(GETDATE() AS date)), 112))
),
after_cutoff AS (
    SELECT DISTINCT NIDProduct
    FROM dbo.F_Invoice
    WHERE BillingDocumentIsCancelled = 0
      AND BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -75, CAST(GETDATE() AS date)), 112))
)
SELECT NIDProduct
FROM before_cutoff
EXCEPT
SELECT NIDProduct
FROM after_cutoff
ORDER BY NIDProduct ASC;
```

### SQL do gerador
```sql
WITH prior_entities AS (
    SELECT DISTINCT
        f.NIDProduct AS NIDProduct
    FROM dbo.F_Invoice f
    
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate < CONVERT(int, CONVERT(char(8), DATEADD(day, -75, CAST(GETDATE() AS date)), 112))
),
recent_entities AS (
    SELECT DISTINCT
        f.NIDProduct AS NIDProduct
    FROM dbo.F_Invoice f
    
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -75, CAST(GETDATE() AS date)), 112))
)
SELECT
    p.NIDProduct
FROM prior_entities p
WHERE NOT EXISTS (
    SELECT 1
    FROM recent_entities r
    WHERE r.NIDProduct = p.NIDProduct
)
ORDER BY p.NIDProduct ASC;
```
