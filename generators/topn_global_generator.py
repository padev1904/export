import re
from dataclasses import dataclass

@dataclass
class ParsedTopNGlobal:
    entity: str
    measure: str
    time_scope: str
    year: int | None
    top_n: int


class TopNGlobalGenerator:
    """Gerador universal para top-N global sem partição e sem filtro cruzado."""

    def parse(self, question: str) -> ParsedTopNGlobal:
        q = question.strip().rstrip('?')
        ql = q.lower()

        top_match = re.search(r'quais são os\s+(\d+)\s+', ql)
        top_n = int(top_match.group(1)) if top_match else 10

        if 'clientes' in ql:
            entity = 'customer'
        elif 'produtos' in ql:
            entity = 'product'
        elif 'marcas' in ql:
            entity = 'brand'
        else:
            raise ValueError('Entidade não suportada para top_n_global.')

        if 'preço médio líquido por unidade' in ql or 'preco medio liquido por unidade' in ql:
            measure = 'avg_net_price_per_unit'
        elif 'número de documentos de faturação distintos' in ql or 'numero de documentos de faturacao distintos' in ql:
            measure = 'distinct_billing_documents'
        elif 'desconto promocional total' in ql or 'desconto promocional' in ql:
            measure = 'promo_total'
        elif 'diferença entre preço de lista e valor líquido faturado' in ql or 'diferenca entre preco de lista e valor liquido faturado' in ql:
            measure = 'list_minus_net'
        elif 'margem bruta' in ql:
            measure = 'gross_margin'
        elif 'vendas comerciais líquidas' in ql or 'vendas comerciais liquidas' in ql:
            measure = 'net_commercial_sales'
        elif 'quantidade faturada' in ql:
            measure = 'billing_quantity'
        elif 'faturação' in ql or 'valor líquido faturado' in ql or 'valor liquido faturado' in ql:
            measure = 'net_amount'
        else:
            raise ValueError('Métrica não suportada para top_n_global.')

        year_match = re.search(r'em\s+(20\d{2})', ql)
        if year_match:
            time_scope = 'explicit_year'
            year = int(year_match.group(1))
        elif 'ano atual' in ql:
            time_scope = 'current_year'
            year = None
        elif 'últimos 12 meses' in ql or 'ultimos 12 meses' in ql:
            time_scope = 'last_12_months'
            year = None
        else:
            raise ValueError('Âmbito temporal não suportado.')

        return ParsedTopNGlobal(entity=entity, measure=measure, time_scope=time_scope, year=year, top_n=top_n)

    def generate(self, question: str) -> str:
        p = self.parse(question)

        if p.entity == 'customer':
            joins = "JOIN dbo.D_Customer c\n    ON f.NIDPayerParty = c.NIDCustomer"
            label = 'c.TCustomer'
            alias = 'Cliente'
            group_by = 'c.TCustomer'
        elif p.entity == 'product':
            joins = "JOIN dbo.D_Product p\n    ON f.NIDProduct = p.NIDProduct"
            label = 'p.TProduct'
            alias = 'Produto'
            group_by = 'p.TProduct'
        elif p.entity == 'brand':
            joins = (
                "JOIN dbo.D_Product p\n    ON f.NIDProduct = p.NIDProduct\n"
                "JOIN dbo.D_ProductBrand pb\n    ON p.NIDProductBrand = pb.NIDProductBrand"
            )
            label = 'pb.TProductBrand'
            alias = 'MarcaProduto'
            group_by = 'pb.TProductBrand'
        else:
            raise ValueError('Entidade inválida.')

        where = ["f.BillingDocumentIsCancelled = 0"]
        if p.time_scope == 'explicit_year':
            where.append(f"f.BillingDocumentDate / 10000 = {p.year}")
        elif p.time_scope == 'current_year':
            where.append("f.BillingDocumentDate / 10000 = YEAR(GETDATE())")
        elif p.time_scope == 'last_12_months':
            where.append("f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, 1, EOMONTH(GETDATE(), -12)), 112))")

        if p.measure in {'gross_margin', 'net_commercial_sales'}:
            where.append("f.IsItAnAdditionalCalculatedRecord = 1")

        measure_sql = {
            'net_amount': ("SUM(f.NetAmount) AS ValorLiquidoFaturado", "ValorLiquidoFaturado", None),
            'billing_quantity': ("SUM(f.BillingQuantity) AS QuantidadeFaturada", "QuantidadeFaturada", None),
            'gross_margin': ("SUM(f.GrossMargin) AS MargemBruta", "MargemBruta", None),
            'net_commercial_sales': ("SUM(f.NetCommercialSales) AS VendasComerciaisLiquidas", "VendasComerciaisLiquidas", None),
            'list_minus_net': ("SUM(f.ZLP1PriceList) - SUM(f.NetAmount) AS DiferencaPrecoListaVsLiquido", "DiferencaPrecoListaVsLiquido", None),
            'promo_total': ("SUM(f.ZDPRPromotional + f.ZCPRPromotionalCampaign + f.REA1PromotionalDiscount) AS DescontoPromocionalTotal", "DescontoPromocionalTotal", None),
            'distinct_billing_documents': ("COUNT(DISTINCT f.BillingDocument) AS NumeroDocumentos", "NumeroDocumentos", None),
            'avg_net_price_per_unit': (
                "SUM(f.NetAmount) AS ValorLiquidoFaturado,\n    SUM(f.BillingQuantity) AS QuantidadeFaturada,\n    SUM(f.NetAmount) / NULLIF(SUM(f.BillingQuantity), 0) AS PrecoMedioLiquidoUnitario",
                "PrecoMedioLiquidoUnitario",
                "HAVING SUM(f.BillingQuantity) <> 0",
            ),
        }
        select_measure, order_alias, having = measure_sql[p.measure]

        order_dir = 'DESC'
        if p.measure == 'promo_total':
            order_dir = 'ASC'

        sql = (
            f"SELECT TOP {p.top_n}\n"
            f"    {label} AS {alias},\n"
            f"    {select_measure}\n"
            f"FROM dbo.F_Invoice f\n"
            f"{joins}\n"
            f"WHERE " + "\n  AND ".join(where) + "\n"
            f"GROUP BY {group_by}\n"
        )
        if having:
            sql += f"{having}\n"
        sql += f"ORDER BY {order_alias} {order_dir};"
        return sql
