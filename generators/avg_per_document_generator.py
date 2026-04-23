from sqlserver_patterns import build_avg_document_cte, explicit_year_predicate, rolling_months_predicate, year_month_bucket_expr


class AvgPerDocumentGenerator:
    def _n(self, text):
        q = text.lower().strip().rstrip('?')
        for a, b in [('á','a'),('à','a'),('â','a'),('ã','a'),('é','e'),('ê','e'),('í','i'),('ó','o'),('ô','o'),('õ','o'),('ú','u'),('ç','c')]:
            q = q.replace(a, b)
        return q

    def generate(self, question):
        q = self._n(question)

        if ('ultimos 6 meses' in q or 'ultimo semestre movel' in q) and 'grupo de contas' in q and 'por mes' in q:
            cte = build_avg_document_cte(
                cte_name='document_totals',
                select_dimensions=[
                    (year_month_bucket_expr(), 'Mes'),
                    ('cag.TCustomerAccountGroup', 'GrupoContasCliente'),
                ],
                joins=[
                    'JOIN dbo.D_Customer c ON f.NIDPayerParty = c.NIDCustomer',
                    'JOIN dbo.D_CustomerAccountGroup cag ON c.NIDCustomerAccountGroup = cag.NIDCustomerAccountGroup',
                ],
                where_filters=['f.BillingDocumentIsCancelled = 0', rolling_months_predicate(6)],
                value_alias='ValorDocumento',
            )
            return f"""{cte}
SELECT
    dt.Mes,
    dt.GrupoContasCliente,
    AVG(dt.ValorDocumento) AS TicketMedioPorDocumento
FROM document_totals dt
GROUP BY dt.Mes, dt.GrupoContasCliente
ORDER BY dt.Mes ASC, dt.GrupoContasCliente ASC;"""

        if 'ultimos 6 meses' in q or 'ultimo semestre movel' in q:
            cte = build_avg_document_cte(
                cte_name='document_totals',
                select_dimensions=[(year_month_bucket_expr(), 'BillingYearMonth')],
                joins=[],
                where_filters=['f.BillingDocumentIsCancelled = 0', rolling_months_predicate(6)],
            )
            return f"""{cte}
SELECT
    DATEFROMPARTS(dt.BillingYearMonth / 100, dt.BillingYearMonth % 100, 1) AS Mes,
    AVG(dt.ValorDocumento) AS TicketMedioPorDocumento
FROM document_totals dt
GROUP BY dt.BillingYearMonth
ORDER BY dt.BillingYearMonth ASC;"""

        if 'grupo de cliente' in q:
            expr, alias, val = 'cg.TCustomerGroup', 'GrupoCliente', 'ValorLiquidoDocumento'
            joins = ['JOIN dbo.D_CustomerGroup cg\n    ON f.NIDCustomerGroup = cg.NIDCustomerGroup']
        elif 'organizacao de vendas' in q:
            expr, alias, val = 'so.TSalesOrganization', 'OrganizacaoVendas', 'ValorDocumento'
            joins = ['JOIN dbo.D_SalesOrganization so\n    ON f.NIDSalesOrganization = so.NIDSalesOrganization']
        elif 'canal de distribuicao' in q:
            expr, alias, val = 'dc.TDistributionChannel', 'CanalDistribuicao', 'ValorDocumento'
            joins = ['JOIN dbo.D_DistributionChannel dc\n    ON f.NIDDistributionChannel = dc.NIDDistributionChannel']
        else:
            raise ValueError('unsupported dimension')

        cte = build_avg_document_cte(
            cte_name='docs',
            select_dimensions=[(expr, alias)],
            joins=joins,
            where_filters=[explicit_year_predicate(2026), 'f.BillingDocumentIsCancelled = 0'],
            value_alias=val,
        )
        return f"""{cte}
SELECT
    d.{alias},
    AVG(d.{val}) AS ValorMedioLiquidoPorDocumento
FROM docs d
GROUP BY d.{alias}
ORDER BY ValorMedioLiquidoPorDocumento DESC;"""
