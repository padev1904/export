-- B09
WITH document_totals AS (
    SELECT
        CAST(f.BillingDocumentDate / 100 AS INT) AS Mes,
        cag.TCustomerAccountGroup AS GrupoContasCliente,
        f.BillingDocument,
        SUM(f.NetAmount) AS ValorDocumento
    FROM dbo.F_Invoice f
    JOIN dbo.D_Customer c ON f.NIDPayerParty = c.NIDCustomer
    JOIN dbo.D_CustomerAccountGroup cag ON c.NIDCustomerAccountGroup = cag.NIDCustomerAccountGroup
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, 1, EOMONTH(CAST(GETDATE() AS date), -6)), 112))
    GROUP BY CAST(f.BillingDocumentDate / 100 AS INT), cag.TCustomerAccountGroup, f.BillingDocument
)
SELECT
    Mes,
    GrupoContasCliente,
    AVG(ValorDocumento) AS TicketMedioPorDocumento
FROM document_totals
GROUP BY Mes, GrupoContasCliente
ORDER BY Mes ASC, GrupoContasCliente ASC;

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
    HAVING SUM(CASE WHEN f.BillingDocumentDate / 10000 = 2025 THEN f.NetAmount ELSE 0 END) <> 0
        OR SUM(CASE WHEN f.BillingDocumentDate / 10000 = 2026 THEN f.NetAmount ELSE 0 END) <> 0
)
SELECT
    r.TRegion AS Regiao,
    100.0 * (g.Valor2026 - g.Valor2025) / NULLIF(g.Valor2025, 0) AS VariacaoPercentual
FROM grouped g
JOIN dbo.D_Region r ON r.NIDRegion = g.NIDRegion
ORDER BY VariacaoPercentual DESC, Regiao ASC;
