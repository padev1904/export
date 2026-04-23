-- B01
WITH grouped AS (
    SELECT
        f.NIDDistributionChannel,
        f.NIDPayerParty,
        SUM(f.NetAmount) AS ValorLiquidoFaturado
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, 1, EOMONTH(CAST(GETDATE() AS date), -12)), 112))
      AND f.BillingDocumentIsCancelled = 0
    GROUP BY f.NIDDistributionChannel, f.NIDPayerParty
), filtered AS (
    SELECT *
    FROM grouped
    WHERE ValorLiquidoFaturado > 0
), ranked AS (
    SELECT
        g.NIDDistributionChannel,
        g.NIDPayerParty,
        g.ValorLiquidoFaturado,
        SUM(g.ValorLiquidoFaturado) OVER (
            PARTITION BY g.NIDDistributionChannel
            ORDER BY g.ValorLiquidoFaturado DESC, g.NIDPayerParty
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS ValorAcumulado,
        SUM(g.ValorLiquidoFaturado) OVER (PARTITION BY g.NIDDistributionChannel) AS ValorTotal
    FROM filtered g
), scored AS (
    SELECT
        r.NIDDistributionChannel,
        r.NIDPayerParty,
        r.ValorLiquidoFaturado,
        (r.ValorLiquidoFaturado * 100.0) / NULLIF(r.ValorTotal, 0) AS PercentagemIndividual,
        (r.ValorAcumulado * 100.0) / NULLIF(r.ValorTotal, 0) AS PercentagemAcumulada,
        ((r.ValorAcumulado - r.ValorLiquidoFaturado) * 100.0) / NULLIF(r.ValorTotal, 0) AS PercentagemAntes
    FROM ranked r
)
SELECT
    dc.TDistributionChannel AS CanalDistribuicao,
    c.TCustomer AS Cliente,
    s.ValorLiquidoFaturado,
    s.PercentagemIndividual,
    s.PercentagemAcumulada,
    s.PercentagemAntes
FROM scored s
JOIN dbo.D_DistributionChannel dc ON dc.NIDDistributionChannel = s.NIDDistributionChannel
JOIN dbo.D_Customer c ON c.NIDCustomer = s.NIDPayerParty
WHERE s.PercentagemAcumulada <= 80 OR s.PercentagemAntes < 80
ORDER BY CanalDistribuicao, s.ValorLiquidoFaturado DESC, Cliente;
