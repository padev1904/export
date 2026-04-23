-- B01
WITH sales_by_entity AS (
    SELECT
        f.NIDDistributionChannel AS NIDDistributionChannel,
        f.NIDPayerParty AS NIDPayerParty,
        SUM(f.NetAmount) AS ValorLiquidoFaturado
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, 1, EOMONTH(CAST(GETDATE() AS date), -12)), 112))
      AND f.BillingDocumentIsCancelled = 0
    GROUP BY f.NIDDistributionChannel, f.NIDPayerParty
),
filtered AS (
    SELECT *
    FROM sales_by_entity
    WHERE ValorLiquidoFaturado > 0
),
ranked AS (
    SELECT
        *,
        SUM(ValorLiquidoFaturado) OVER (
            PARTITION BY NIDDistributionChannel
            ORDER BY ValorLiquidoFaturado DESC, NIDPayerParty
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS ValorAcumulado,
        SUM(ValorLiquidoFaturado) OVER (PARTITION BY NIDDistributionChannel) AS ValorTotal
    FROM filtered
),
scored AS (
    SELECT
        *,
        (ValorLiquidoFaturado * 100.0) / NULLIF(ValorTotal, 0) AS PercentagemIndividual,
        (ValorAcumulado * 100.0) / NULLIF(ValorTotal, 0) AS PercentagemAcumulada,
        ((ValorAcumulado - ValorLiquidoFaturado) * 100.0) / NULLIF(ValorTotal, 0) AS PercentagemAntes
    FROM ranked
)
SELECT
    pd.TDistributionChannel AS CanalDistribuicao,
    d.TCustomer AS Cliente,
    s.ValorLiquidoFaturado,
    s.PercentagemIndividual,
    s.PercentagemAcumulada,
    s.PercentagemAntes
FROM scored s
JOIN dbo.D_DistributionChannel pd ON pd.NIDDistributionChannel = s.NIDDistributionChannel
JOIN dbo.D_Customer d ON d.NIDCustomer = s.NIDPayerParty
WHERE s.PercentagemAcumulada <= 80
   OR s.PercentagemAntes < 80
ORDER BY CanalDistribuicao ASC, s.ValorLiquidoFaturado DESC, Cliente;
