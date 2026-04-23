-- B09
WITH docs AS (
    SELECT
        CAST(f.BillingDocumentDate / 100 AS INT) AS Mes,
        c.NIDCustomerAccountGroup,
        f.BillingDocument,
        SUM(f.NetAmount) AS ValorDocumento
    FROM dbo.F_Invoice f
    JOIN dbo.D_Customer c ON f.NIDPayerParty = c.NIDCustomer
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, 1, EOMONTH(CAST(GETDATE() AS date), -6)), 112))
    GROUP BY CAST(f.BillingDocumentDate / 100 AS INT), c.NIDCustomerAccountGroup, f.BillingDocument
)
SELECT
    d.Mes,
    cag.TCustomerAccountGroup AS GrupoContasCliente,
    AVG(d.ValorDocumento) AS TicketMedioPorDocumento
FROM docs d
JOIN dbo.D_CustomerAccountGroup cag ON cag.NIDCustomerAccountGroup = d.NIDCustomerAccountGroup
GROUP BY d.Mes, cag.TCustomerAccountGroup
ORDER BY d.Mes, GrupoContasCliente;

-- B15
WITH grouped AS (
    SELECT
        f.NIDRegion,
        SUM(CASE WHEN f.BillingDocumentDate / 10000 = 2025 THEN f.NetAmount ELSE 0 END) AS Valor2025,
        SUM(CASE WHEN f.BillingDocumentDate / 10000 = 2026 THEN f.NetAmount ELSE 0 END) AS Valor2026
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate / 10000 IN (2025, 2026)
    GROUP BY f.NIDRegion
)
SELECT
    r.TRegion AS Regiao,
    100.0 * (g.Valor2026 - g.Valor2025) / NULLIF(g.Valor2025, 0) AS VariacaoPercentual
FROM grouped g
JOIN dbo.D_Region r ON r.NIDRegion = g.NIDRegion
WHERE g.Valor2025 <> 0 OR g.Valor2026 <> 0
ORDER BY VariacaoPercentual DESC, Regiao;
