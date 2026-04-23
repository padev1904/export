-- B05
WITH recent_pairs AS (
    SELECT DISTINCT
        f.NIDSalesOrganization,
        f.NIDPayerParty
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -90, CAST(GETDATE() AS date)), 112))
), inactive_pairs AS (
    SELECT DISTINCT
        f.NIDSalesOrganization,
        f.NIDPayerParty
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -270, CAST(GETDATE() AS date)), 112))
      AND f.BillingDocumentDate < CONVERT(int, CONVERT(char(8), DATEADD(day, -90, CAST(GETDATE() AS date)), 112))
)
SELECT
    so.TSalesOrganization AS OrganizacaoVendas,
    c.TCustomer AS Cliente
FROM recent_pairs rp
JOIN dbo.D_SalesOrganization so ON so.NIDSalesOrganization = rp.NIDSalesOrganization
JOIN dbo.D_Customer c ON c.NIDCustomer = rp.NIDPayerParty
WHERE NOT EXISTS (
    SELECT 1
    FROM inactive_pairs iw
    WHERE iw.NIDSalesOrganization = rp.NIDSalesOrganization
      AND iw.NIDPayerParty = rp.NIDPayerParty
)
ORDER BY OrganizacaoVendas, Cliente;

-- B16
WITH history_pairs AS (
    SELECT DISTINCT
        f.NIDDistributionChannel,
        f.NIDPayerParty
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -270, CAST(GETDATE() AS date)), 112))
      AND f.BillingDocumentDate < CONVERT(int, CONVERT(char(8), DATEADD(day, -90, CAST(GETDATE() AS date)), 112))
), recent_pairs AS (
    SELECT DISTINCT
        f.NIDDistributionChannel,
        f.NIDPayerParty
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -90, CAST(GETDATE() AS date)), 112))
)
SELECT
    dc.TDistributionChannel AS CanalDistribuicao,
    c.TCustomer AS Cliente
FROM history_pairs hp
JOIN dbo.D_DistributionChannel dc ON dc.NIDDistributionChannel = hp.NIDDistributionChannel
JOIN dbo.D_Customer c ON c.NIDCustomer = hp.NIDPayerParty
WHERE NOT EXISTS (
    SELECT 1
    FROM recent_pairs rp
    WHERE rp.NIDDistributionChannel = hp.NIDDistributionChannel
      AND rp.NIDPayerParty = hp.NIDPayerParty
)
ORDER BY CanalDistribuicao, Cliente;
