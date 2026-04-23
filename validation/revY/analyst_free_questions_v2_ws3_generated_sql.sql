-- B05
WITH recent_pairs AS (
    SELECT DISTINCT
        f.NIDSalesOrganization AS NIDSalesOrganization,
        f.NIDPayerParty AS NIDPayerParty
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -90, CAST(GETDATE() AS date)), 112))
),
inactive_pairs AS (
    SELECT DISTINCT
        f.NIDSalesOrganization AS NIDSalesOrganization,
        f.NIDPayerParty AS NIDPayerParty
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -270, CAST(GETDATE() AS date)), 112))
      AND f.BillingDocumentDate < CONVERT(int, CONVERT(char(8), DATEADD(day, -90, CAST(GETDATE() AS date)), 112))
),
reactivated_pairs AS (
    SELECT rp.NIDSalesOrganization, rp.NIDPayerParty
    FROM recent_pairs rp
    WHERE NOT EXISTS (
        SELECT 1
        FROM inactive_pairs iw
        WHERE iw.NIDSalesOrganization = rp.NIDSalesOrganization
          AND iw.NIDPayerParty = rp.NIDPayerParty
    )
)
SELECT
    d.TSalesOrganization AS OrganizacaoVendas,
    e.TCustomer AS Cliente
FROM reactivated_pairs rp
JOIN dbo.D_SalesOrganization d ON d.NIDSalesOrganization = rp.NIDSalesOrganization
JOIN dbo.D_Customer e ON e.NIDCustomer = rp.NIDPayerParty
ORDER BY OrganizacaoVendas ASC, Cliente ASC;

-- B16
WITH history_pairs AS (
    SELECT DISTINCT
        f.NIDDistributionChannel AS NIDDistributionChannel,
        f.NIDPayerParty AS NIDPayerParty
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -270, CAST(GETDATE() AS date)), 112))
      AND f.BillingDocumentDate < CONVERT(int, CONVERT(char(8), DATEADD(day, -90, CAST(GETDATE() AS date)), 112))
),
recent_pairs AS (
    SELECT DISTINCT
        f.NIDDistributionChannel AS NIDDistributionChannel,
        f.NIDPayerParty AS NIDPayerParty
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -90, CAST(GETDATE() AS date)), 112))
),
lost_pairs AS (
    SELECT hp.NIDDistributionChannel, hp.NIDPayerParty
    FROM history_pairs hp
    WHERE NOT EXISTS (
        SELECT 1
        FROM recent_pairs rp
        WHERE rp.NIDDistributionChannel = hp.NIDDistributionChannel
          AND rp.NIDPayerParty = hp.NIDPayerParty
    )
)
SELECT
    d.TDistributionChannel AS CanalDistribuicao,
    e.TCustomer AS Cliente
FROM lost_pairs lp
JOIN dbo.D_DistributionChannel d ON d.NIDDistributionChannel = lp.NIDDistributionChannel
JOIN dbo.D_Customer e ON e.NIDCustomer = lp.NIDPayerParty
ORDER BY CanalDistribuicao ASC, Cliente ASC;
