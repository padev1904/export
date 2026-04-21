# Casos de generalização revN — top-N com filtro cruzado

## CF01
Quais são os produtos com mais valor líquido faturado em 2026 para o cliente MODELO CONTINENTE HIPERMERCADOS, SA?

### SQL manual independente
```sql
SELECT TOP 10 p.TProduct AS Produto, SUM(f.NetAmount) AS ValorLiquidoFaturado
FROM dbo.F_Invoice f
JOIN dbo.D_Customer c ON f.NIDPayerParty = c.NIDCustomer
JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct
WHERE f.BillingDocumentDate / 10000 = 2026
  AND c.TCustomer = 'MODELO CONTINENTE HIPERMERCADOS, SA'
  AND f.BillingDocumentIsCancelled = 0
GROUP BY p.TProduct
ORDER BY ValorLiquidoFaturado DESC;
```

### SQL do gerador universal
```sql
SELECT TOP 10
    p.TProduct AS Produto,
    SUM(f.NetAmount) AS ValorLiquidoFaturado
FROM dbo.F_Invoice f
JOIN dbo.D_Customer c
    ON f.NIDPayerParty = c.NIDCustomer
JOIN dbo.D_Product p
    ON f.NIDProduct = p.NIDProduct
WHERE f.BillingDocumentDate / 10000 = 2026
  AND c.TCustomer = 'MODELO CONTINENTE HIPERMERCADOS, SA'
  AND f.BillingDocumentIsCancelled = 0
GROUP BY p.TProduct
ORDER BY ValorLiquidoFaturado DESC;
```

Resultado: **PASS**

## CF02
Quais são os produtos com mais valor líquido faturado em 2026 para o cliente com código 13770?

Resultado: **PASS**

## CF03
Quais são os clientes com mais valor líquido faturado em 2026 para o produto MZ-ESPARGUETE 500g 10kg?

Resultado: **PASS**

## CF04
Quais são os clientes com mais valor líquido faturado em 2026 para o produto com código WM05010002?

Resultado: **PASS**

## CF05
Quais são os produtos com mais valor líquido faturado em 2026 para o cliente ITMP ALIMENTAR, S.A.?

Resultado: **PASS**

## CF06
Quais são os clientes com mais valor líquido faturado em 2026 para o produto MZ-ESPARGUETE box 500g 345kg?

Resultado: **PASS**
