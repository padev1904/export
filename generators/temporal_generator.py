from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import re

from sqlserver_patterns import (
    CURRENT_DATE_SQL,
    build_named_time_predicate,
    current_month_start_date_sql,
    date_window_predicates,
    dedupe_joins,
    inclusive_upper_bound_predicate,
    month_start_date_expr,
    next_month_start_date_sql,
    previous_month_start_date_sql,
    same_month_last_year_start_date_sql,
)

DIMENSIONS = {
    'channel': (
        'dc.TDistributionChannel',
        'CanalDistribuicao',
        ['JOIN dbo.D_DistributionChannel dc ON f.NIDDistributionChannel = dc.NIDDistributionChannel'],
    ),
    'sales_organization': (
        'so.TSalesOrganization',
        'OrganizacaoVendas',
        ['JOIN dbo.D_SalesOrganization so ON f.NIDSalesOrganization = so.NIDSalesOrganization'],
    ),
    'customer_account_group': (
        'cag.TCustomerAccountGroup',
        'GrupoContasCliente',
        [
            'JOIN dbo.D_Customer c ON f.NIDPayerParty = c.NIDCustomer',
            'JOIN dbo.D_CustomerAccountGroup cag ON c.NIDCustomerAccountGroup = cag.NIDCustomerAccountGroup',
        ],
    ),
    'return_item_processing_type': (
        'ript.TReturnItemProcessingType',
        'TipoProcessamentoDevolucao',
        ['JOIN dbo.D_ReturnItemProcessingType ript ON f.NIDReturnItemProcessingType = ript.NIDReturnItemProcessingType'],
    ),
    'region': (
        'r.TRegion',
        'Regiao',
        ['JOIN dbo.D_Region r ON f.NIDRegion = r.NIDRegion'],
    ),
    'country': (
        'co.TCountry',
        'Pais',
        ['JOIN dbo.D_Country co ON f.NIDCountry = co.NIDCountry'],
    ),
    'brand': (
        'pb.TProductBrand',
        'MarcaProduto',
        [
            'JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct',
            'JOIN dbo.D_ProductBrand pb ON p.NIDProductBrand = pb.NIDProductBrand',
        ],
    ),
    'family': (
        'pf.TProductFamily',
        'FamiliaProduto',
        [
            'JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct',
            'JOIN dbo.D_ProductFamily pf ON p.NIDProductFamily = pf.NIDProductFamily',
        ],
    ),
    'material_type': (
        'mt.TMaterialType',
        'TipoMaterial',
        [
            'JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct',
            'JOIN dbo.D_MaterialType mt ON p.NIDMaterialType = mt.NIDMaterialType',
        ],
    ),
}

MEASURES = {
    'net_amount': ('f.NetAmount', 'ValorLiquidoFaturado', False),
    'billing_quantity': ('f.BillingQuantity', 'QuantidadeFaturada', False),
    'gross_margin': ('f.GrossMargin', 'MargemBruta', True),
    'promo_total': (
        '(f.ZDPRPromotional + f.ZCPRPromotionalCampaign + f.REA1PromotionalDiscount)',
        'DescontoPromocionalTotal',
        False,
    ),
    'list_minus_net': (
        'SUM(f.ZLP1PriceList) - SUM(f.NetAmount)',
        'DiferencaPrecoListaVsLiquido',
        False,
    ),
}


@dataclass
class SemanticSpec:
    family: str
    operation: str
    measure: str
    dimension: Optional[str] = None
    time_scope: Optional[str] = None
    year: Optional[int] = None
    ranking: Optional[str] = None
    original_question: Optional[str] = None


def normalize_q(q: str) -> str:
    x = q.lower().strip()
    for a, b in [('á', 'a'), ('à', 'a'), ('â', 'a'), ('ã', 'a'), ('é', 'e'), ('ê', 'e'), ('í', 'i'), ('ó', 'o'), ('ô', 'o'), ('õ', 'o'), ('ú', 'u'), ('ç', 'c')]:
        x = x.replace(a, b)
    return ' '.join(x.split())


def detect_measure(qn: str) -> str:
    if 'diferenca entre preco de lista e valor liquido faturado' in qn or 'diferenca entre o preco de lista e o valor liquido faturado' in qn:
        return 'list_minus_net'
    if 'desconto promocional' in qn or 'descontos promocionais' in qn:
        return 'promo_total'
    if 'margem bruta' in qn:
        return 'gross_margin'
    if 'quantidade' in qn:
        return 'billing_quantity'
    return 'net_amount'


def detect_dimension(qn: str) -> Optional[str]:
    if 'grupo de contas do cliente' in qn or 'grupo de contas de cliente' in qn:
        return 'customer_account_group'
    if 'tipo de processamento de devolucao' in qn:
        return 'return_item_processing_type'
    if 'organizacao de vendas' in qn:
        return 'sales_organization'
    if 'familia de produto' in qn or 'familia' in qn:
        return 'family'
    if 'tipo de material' in qn:
        return 'material_type'
    if 'canal' in qn:
        return 'channel'
    if 'regiao' in qn:
        return 'region'
    if 'pais' in qn:
        return 'country'
    if 'marca' in qn:
        return 'brand'
    return None


def detect_year(qn: str) -> Optional[int]:
    m = re.search(r'\b(20\d{2})\b', qn)
    return int(m.group(1)) if m else None


def classify_question(question: str) -> SemanticSpec:
    qn = normalize_q(question)
    measure = detect_measure(qn)
    dim = detect_dimension(qn)
    year = detect_year(qn)
    if 'ticket medio' in qn or 'valor medio por documento' in qn:
        return SemanticSpec('F10_avg_per_document', 'monthly_avg_per_document', 'net_amount', None, 'last_6_months', original_question=question)
    if 'mes atual face ao mesmo mes do ano anterior' in qn or 'mes corrente com o mesmo mes do ano passado' in qn or 'entre este mes e o mesmo mes do ano anterior' in qn:
        return SemanticSpec('F13_period_compare', 'yoy_same_month_by_dimension', measure, dim, 'month_vs_same_month_last_year', original_question=question)
    if ('mes atual versus o mes anterior' in qn) or ('mes corrente com a do mes anterior' in qn) or ('este mes e no mes passado' in qn):
        return SemanticSpec('F13_period_compare', 'current_vs_previous_month', measure, None, 'current_vs_previous_month', original_question=question)
    if 'variacao percentual mensal' in qn or 'variacao mes contra mes' in qn or 'variou em percentagem' in qn:
        return SemanticSpec('F15_window_trend', 'mom_pct_change', measure, dim, 'last_6_months', original_question=question)
    if 'media movel' in qn or 'rolling average' in qn:
        return SemanticSpec('F15_window_trend', 'rolling_avg_3m', measure, dim, 'recent_with_history', original_question=question)
    if 'ytd' in qn or ('ano corrente' in qn and 'acumulado' in qn) or 'acumulado mensal' in qn:
        return SemanticSpec('F15_window_trend', 'ytd', measure, dim, 'current_year', original_question=question)
    if ('peso do desconto promocional total sobre a faturacao' in qn) or ('percentagem de desconto promocional face a faturacao' in qn) or ('taxa de desconto promocional mensal' in qn):
        return SemanticSpec('F11_percentage_share', 'monthly_ratio_to_billing', 'promo_total', dim, 'last_6_months', original_question=question)
    if 'por mes' in qn and year is not None:
        return SemanticSpec('F09_time_series_monthly', 'monthly_trend', measure, dim, 'explicit_year', year=year, original_question=question)
    if ('evolucao mensal' in qn) or ('mes a mes' in qn) or ('evoluiu mensalmente' in qn) or ('por mes nos ultimos 6 meses' in qn) or ('por mes no ultimo semestre movel' in qn):
        return SemanticSpec('F15_window_trend', 'monthly_trend', measure, dim, 'last_6_months', original_question=question)
    raise ValueError(f'Pergunta nao suportada pelo gerador temporal: {question}')


def _parts(dimension: Optional[str]):
    if not dimension:
        return '', '', [], '', ''
    expr, alias, joins = DIMENSIONS[dimension]
    return expr, alias, joins, f',\n        {expr} AS {alias}', f', {expr}'


def _join_sql(joins):
    block = '\n'.join(dedupe_joins(joins))
    return f'{block}\n' if block else ''


def _sel(alias: str) -> str:
    return f',\n    s.{alias}' if alias else ''


def _ord(alias: str) -> str:
    return f', s.{alias}' if alias else ''


def _time_filters(spec: SemanticSpec):
    if spec.time_scope == 'explicit_year':
        if spec.year is None:
            raise ValueError('year required for explicit_year monthly trend')
        return [build_named_time_predicate('explicit_year', year=spec.year)]
    if spec.time_scope == 'last_6_months':
        return [build_named_time_predicate('last_6_months'), inclusive_upper_bound_predicate(CURRENT_DATE_SQL)]
    if spec.time_scope == 'recent_with_history':
        return [build_named_time_predicate('recent_with_history'), inclusive_upper_bound_predicate(CURRENT_DATE_SQL)]
    if spec.time_scope == 'current_year':
        return [build_named_time_predicate('current_year'), inclusive_upper_bound_predicate(CURRENT_DATE_SQL)]
    raise ValueError(f'unsupported time scope: {spec.time_scope}')


def _monthly_aggregate_expr(measure_key: str, measure_expr: str) -> str:
    if measure_key == 'list_minus_net':
        return measure_expr
    return f'SUM({measure_expr})'


def build_sql(spec: SemanticSpec) -> str:
    measure_expr, measure_alias, needs_additional = MEASURES[spec.measure]
    filters = ['f.BillingDocumentIsCancelled = 0']
    if needs_additional:
        filters.append('f.IsItAnAdditionalCalculatedRecord = 1')
    dim_expr, dim_alias, joins, dim_select, dim_group = _parts(spec.dimension)
    join_sql = _join_sql(joins)
    month_expr = month_start_date_expr()

    if spec.operation == 'monthly_trend':
        where_sql = ' AND\n      '.join(filters + _time_filters(spec))
        aggregate_expr = _monthly_aggregate_expr(spec.measure, measure_expr)
        return f"""WITH monthly_sales AS (
    SELECT
        {month_expr} AS Mes{dim_select},
        {aggregate_expr} AS {measure_alias}
    FROM dbo.F_Invoice f
    {join_sql}WHERE {where_sql}
    GROUP BY {month_expr}{dim_group}
)
SELECT
    s.Mes{_sel(dim_alias)},
    s.{measure_alias}
FROM monthly_sales s
ORDER BY s.Mes ASC{_ord(dim_alias)};"""

    if spec.operation == 'monthly_avg_per_document':
        where_sql = ' AND\n      '.join(['f.BillingDocumentIsCancelled = 0'] + _time_filters(spec))
        return f"""WITH docs AS (
    SELECT
        {month_expr} AS Mes,
        f.BillingDocument,
        SUM(f.NetAmount) AS ValorDocumento
    FROM dbo.F_Invoice f
    WHERE {where_sql}
    GROUP BY {month_expr}, f.BillingDocument
)
SELECT
    d.Mes,
    AVG(d.ValorDocumento) AS TicketMedioPorDocumento
FROM docs d
GROUP BY d.Mes
ORDER BY d.Mes ASC;"""

    if spec.operation == 'current_vs_previous_month':
        current_start = current_month_start_date_sql()
        prev_start = previous_month_start_date_sql()
        next_start = next_month_start_date_sql()
        lower, upper = date_window_predicates(prev_start, next_start)
        c1, c2 = date_window_predicates(current_start, next_start)
        where_sql = ' AND\n      '.join(filters + [lower, upper])
        return f"""WITH base AS (
    SELECT
        CASE WHEN {c1} AND {c2} THEN 'MesAtual' ELSE 'MesAnterior' END AS Periodo,
        {measure_expr} AS metric
    FROM dbo.F_Invoice f
    WHERE {where_sql}
)
SELECT
    b.Periodo,
    SUM(b.metric) AS {measure_alias}
FROM base b
GROUP BY b.Periodo
ORDER BY CASE WHEN b.Periodo = 'MesAnterior' THEN 1 ELSE 2 END;"""

    if spec.operation == 'mom_pct_change':
        where_sql = ' AND\n      '.join(filters + _time_filters(spec))
        part = f'PARTITION BY s.{dim_alias} ' if dim_alias else ''
        return f"""WITH monthly_sales AS (
    SELECT
        {month_expr} AS Mes{dim_select},
        SUM({measure_expr}) AS {measure_alias}
    FROM dbo.F_Invoice f
    {join_sql}WHERE {where_sql}
    GROUP BY {month_expr}{dim_group}
)
SELECT
    s.Mes{_sel(dim_alias)},
    s.{measure_alias},
    LAG(s.{measure_alias}) OVER ({part}ORDER BY s.Mes) AS ValorMesAnterior,
    CASE
        WHEN LAG(s.{measure_alias}) OVER ({part}ORDER BY s.Mes) IS NULL THEN NULL
        WHEN LAG(s.{measure_alias}) OVER ({part}ORDER BY s.Mes) = 0 THEN NULL
        ELSE ((s.{measure_alias} - LAG(s.{measure_alias}) OVER ({part}ORDER BY s.Mes)) * 100.0) / NULLIF(LAG(s.{measure_alias}) OVER ({part}ORDER BY s.Mes), 0)
    END AS VariacaoPercentual
FROM monthly_sales s
ORDER BY s.Mes ASC{_ord(dim_alias)};"""

    if spec.operation == 'rolling_avg_3m':
        where_sql = ' AND\n      '.join(filters + _time_filters(spec))
        part = f'PARTITION BY s.{dim_alias} ' if dim_alias else ''
        return f"""WITH monthly_sales AS (
    SELECT
        {month_expr} AS Mes{dim_select},
        SUM({measure_expr}) AS {measure_alias}
    FROM dbo.F_Invoice f
    {join_sql}WHERE {where_sql}
    GROUP BY {month_expr}{dim_group}
)
SELECT
    s.Mes{_sel(dim_alias)},
    s.{measure_alias},
    AVG(s.{measure_alias}) OVER ({part}ORDER BY s.Mes ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS MediaMovel3Meses
FROM monthly_sales s
ORDER BY s.Mes ASC{_ord(dim_alias)};"""

    if spec.operation == 'ytd':
        where_sql = ' AND\n      '.join(filters + _time_filters(spec))
        part = f'PARTITION BY s.{dim_alias} ' if dim_alias else ''
        return f"""WITH monthly_sales AS (
    SELECT
        {month_expr} AS Mes{dim_select},
        SUM({measure_expr}) AS {measure_alias}
    FROM dbo.F_Invoice f
    {join_sql}WHERE {where_sql}
    GROUP BY {month_expr}{dim_group}
)
SELECT
    s.Mes{_sel(dim_alias)},
    s.{measure_alias},
    SUM(s.{measure_alias}) OVER ({part}ORDER BY s.Mes ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS {measure_alias}YTD
FROM monthly_sales s
ORDER BY s.Mes ASC{_ord(dim_alias)};"""

    if spec.operation == 'monthly_ratio_to_billing':
        where_sql = ' AND\n      '.join(['f.BillingDocumentIsCancelled = 0'] + _time_filters(spec))
        return f"""WITH monthly_totals AS (
    SELECT
        {month_expr} AS Mes{dim_select},
        SUM(f.NetAmount) AS ValorLiquidoFaturado,
        SUM(f.ZDPRPromotional + f.ZCPRPromotionalCampaign + f.REA1PromotionalDiscount) AS DescontoPromocionalTotal
    FROM dbo.F_Invoice f
    {join_sql}WHERE {where_sql}
    GROUP BY {month_expr}{dim_group}
)
SELECT
    s.Mes{_sel(dim_alias)},
    s.ValorLiquidoFaturado,
    s.DescontoPromocionalTotal,
    CASE WHEN s.ValorLiquidoFaturado = 0 THEN NULL ELSE (s.DescontoPromocionalTotal * 100.0) / NULLIF(s.ValorLiquidoFaturado, 0) END AS PercentagemDescontoPromocional
FROM monthly_totals s
ORDER BY s.Mes ASC{_ord(dim_alias)};"""

    if spec.operation == 'yoy_same_month_by_dimension':
        if not spec.dimension:
            raise ValueError('dimension required')
        current_start = current_month_start_date_sql()
        next_start = next_month_start_date_sql()
        same_last = same_month_last_year_start_date_sql()
        c1, c2 = date_window_predicates(current_start, next_start)
        p1, p2 = date_window_predicates(same_last, current_start)
        grouped_join_sql = _join_sql(joins)
        return f"""WITH grouped AS (
    SELECT
        {dim_expr} AS {dim_alias},
        SUM(CASE WHEN {c1} AND {c2} THEN {measure_expr} ELSE 0 END) AS ValorMesAtual,
        SUM(CASE WHEN {p1} AND {p2} THEN {measure_expr} ELSE 0 END) AS ValorMesmoMesAnoAnterior
    FROM dbo.F_Invoice f
    {grouped_join_sql}WHERE {' AND '.join(filters)}
    GROUP BY {dim_expr}
)
SELECT
    g.{dim_alias},
    g.ValorMesAtual,
    g.ValorMesmoMesAnoAnterior,
    CASE WHEN g.ValorMesmoMesAnoAnterior = 0 THEN NULL ELSE ((g.ValorMesAtual - g.ValorMesmoMesAnoAnterior) * 100.0) / NULLIF(g.ValorMesmoMesAnoAnterior, 0) END AS VariacaoPercentual
FROM grouped g
WHERE g.ValorMesAtual <> 0 OR g.ValorMesmoMesAnoAnterior <> 0
ORDER BY VariacaoPercentual DESC, g.{dim_alias} ASC;"""

    raise ValueError(spec)
