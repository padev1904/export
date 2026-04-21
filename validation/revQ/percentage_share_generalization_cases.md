# Percentage share — generalization cases (revQ)

## PS01 — PASS

**Pergunta:** Que percentagem da faturação do mês atual pertence a cada canal de distribuição?

**Semântica alvo:**
- família: `percentage_share`
- medida base: `SUM(NetAmount)`
- partição: total global do mês atual
- entidade: canal de distribuição
- saída: percentagem 0–100

**SQL manual independente:**
```sql
WITH base AS (
    SELECT
        dc.TDistributionChannel AS CanalDistribuicao,
        SUM(f.NetAmount) AS ValorLiquidoFaturado
    FROM F_Invoice f
    JOIN D_DistributionChannel dc ON f.NIDDistributionChannel = dc.NIDDistributionChannel
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= 20260401
      AND f.BillingDocumentDate < 20260501
    GROUP BY dc.TDistributionChannel
)
SELECT
    CanalDistribuicao,
    ValorLiquidoFaturado,
    (ValorLiquidoFaturado * 100.0) / NULLIF(SUM(ValorLiquidoFaturado) OVER (), 0) AS Percentagem
FROM base
ORDER BY Percentagem DESC, CanalDistribuicao ASC;
```

**Resultado:** equivalente ao SQL do gerador universal.

---

## PS02 — PASS

**Pergunta:** Mostra a quota da faturação dos últimos 12 meses por região.

**Semântica alvo:**
- família: `percentage_share`
- medida base: `SUM(NetAmount)`
- janela temporal: últimos 12 meses
- entidade: região
- saída: quota global 0–100

**SQL manual independente:**
```sql
WITH base AS (
    SELECT
        r.TRegion AS Regiao,
        SUM(f.NetAmount) AS ValorLiquidoFaturado
    FROM F_Invoice f
    JOIN D_Region r ON f.NIDRegion = r.NIDRegion
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= 20250421
      AND f.BillingDocumentDate <= 20260420
    GROUP BY r.TRegion
)
SELECT
    Regiao,
    ValorLiquidoFaturado,
    (ValorLiquidoFaturado * 100.0) / NULLIF(SUM(ValorLiquidoFaturado) OVER (), 0) AS Percentagem
FROM base
ORDER BY Percentagem DESC, Regiao ASC;
```

**Resultado:** equivalente ao SQL do gerador universal.

---

## PS03 — PASS

**Pergunta:** Qual o preço médio líquido por unidade faturada por marca em 2026, ignorando marcas com quantidade total zero?

**Semântica alvo:**
- família: `percentage_share`
- subtipo: rácio agregado `SUM(NetAmount) / SUM(BillingQuantity)`
- entidade: marca
- exclusão obrigatória: denominador total zero

**SQL manual independente:**
```sql
SELECT
    pb.TProductBrand AS MarcaProduto,
    SUM(f.NetAmount) / NULLIF(SUM(f.BillingQuantity), 0) AS PrecoMedioLiquidoPorUnidade
FROM F_Invoice f
JOIN D_Product p ON f.NIDProduct = p.NIDProduct
JOIN D_ProductBrand pb ON p.NIDProductBrand = pb.NIDProductBrand
WHERE f.BillingDocumentIsCancelled = 0
  AND f.BillingDocumentDate >= 20260101
  AND f.BillingDocumentDate <= 20261231
GROUP BY pb.TProductBrand
HAVING SUM(f.BillingQuantity) <> 0
ORDER BY PrecoMedioLiquidoPorUnidade DESC, MarcaProduto ASC;
```

**Resultado:** equivalente ao SQL do gerador universal.

---

## PS04 — PASS

**Pergunta:** Qual a percentagem de margem bruta por marca em 2026 usando só registos adicionais calculados?

**Semântica alvo:**
- família: `percentage_share`
- medida: `SUM(GrossMargin)`
- filtro documental adicional: `IsItAnAdditionalCalculatedRecord = 1`
- entidade: marca
- saída: percentagem global 0–100

**SQL manual independente:**
```sql
WITH base AS (
    SELECT
        pb.TProductBrand AS MarcaProduto,
        SUM(f.GrossMargin) AS MargemBruta
    FROM F_Invoice f
    JOIN D_Product p ON f.NIDProduct = p.NIDProduct
    JOIN D_ProductBrand pb ON p.NIDProductBrand = pb.NIDProductBrand
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.IsItAnAdditionalCalculatedRecord = 1
      AND f.BillingDocumentDate >= 20260101
      AND f.BillingDocumentDate <= 20261231
    GROUP BY pb.TProductBrand
)
SELECT
    MarcaProduto,
    MargemBruta,
    (MargemBruta * 100.0) / NULLIF(SUM(MargemBruta) OVER (), 0) AS Percentagem
FROM base
ORDER BY Percentagem DESC, MarcaProduto ASC;
```

**Resultado:** equivalente ao SQL do gerador universal.

---

## PS05 — PASS

**Pergunta:** Qual a quota de faturação de cada país dentro de cada organização de vendas em 2026?

**Semântica alvo:**
- família: `percentage_share`
- medida: `SUM(NetAmount)`
- partição: organização de vendas
- entidade: país
- saída: percentagem dentro da partição

**SQL manual independente:**
```sql
WITH base AS (
    SELECT
        s.TSalesOrganization AS OrganizacaoVendas,
        c.TCountry AS Pais,
        SUM(f.NetAmount) AS ValorLiquidoFaturado
    FROM F_Invoice f
    JOIN D_SalesOrganization s ON f.NIDSalesOrganization = s.NIDSalesOrganization
    JOIN D_Country c ON f.NIDCountry = c.NIDCountry
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= 20260101
      AND f.BillingDocumentDate <= 20261231
    GROUP BY s.TSalesOrganization, c.TCountry
)
SELECT
    OrganizacaoVendas,
    Pais,
    ValorLiquidoFaturado,
    (ValorLiquidoFaturado * 100.0) / NULLIF(SUM(ValorLiquidoFaturado) OVER (PARTITION BY OrganizacaoVendas), 0) AS Percentagem
FROM base
ORDER BY OrganizacaoVendas ASC, Percentagem DESC, Pais ASC;
```

**Resultado:** equivalente ao SQL do gerador universal.

---

## PS06 — PASS

**Pergunta:** Qual a percentagem do desconto promocional total sobre a faturação por mês nos últimos 6 meses?

**Semântica alvo:**
- família: `percentage_share`
- numerador: `SUM(ZDPRPromotional + ZCPRPromotionalCampaign + REA1PromotionalDiscount)`
- denominador: `SUM(NetAmount)`
- bucket temporal: mês
- janela temporal: últimos 6 meses

**SQL manual independente:**
```sql
SELECT
    CAST(f.BillingDocumentDate / 100 AS INT) AS Mes,
    SUM(f.NetAmount) AS ValorLiquidoFaturado,
    SUM(f.ZDPRPromotional + f.ZCPRPromotionalCampaign + f.REA1PromotionalDiscount) AS DescontoPromocionalTotal,
    (SUM(f.ZDPRPromotional + f.ZCPRPromotionalCampaign + f.REA1PromotionalDiscount) * 100.0)
        / NULLIF(SUM(f.NetAmount), 0) AS PercentagemDescontoPromocional
FROM F_Invoice f
WHERE f.BillingDocumentIsCancelled = 0
  AND f.BillingDocumentDate >= 20251021
  AND f.BillingDocumentDate <= 20260420
GROUP BY CAST(f.BillingDocumentDate / 100 AS INT)
ORDER BY Mes ASC;
```

**Resultado:** equivalente ao SQL do gerador universal.
