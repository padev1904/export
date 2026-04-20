from __future__ import annotations
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Optional

CURRENT_DATE = date(2026, 4, 20)

def yyyymmdd(d: date) -> int:
    return int(d.strftime('%Y%m%d'))

def add_months(d: date, months: int) -> date:
    year = d.year + (d.month - 1 + months) // 12
    month = (d.month - 1 + months) % 12 + 1
    day = min(d.day, [31,29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28,31,30,31,30,31,31,30,31,30,31][month - 1])
    return date(year, month, day)

def eomonth(d: date, offset: int = 0) -> date:
    m = add_months(d.replace(day=1), offset + 1)
    return m - timedelta(days=1)

LAST6_START = eomonth(CURRENT_DATE, -6) + timedelta(days=1)
LAST8_START = eomonth(CURRENT_DATE, -8) + timedelta(days=1)
CUR_MONTH_START = date(CURRENT_DATE.year, CURRENT_DATE.month, 1)
PREV_MONTH_START = add_months(CUR_MONTH_START, -1)
NEXT_MONTH_START = add_months(CUR_MONTH_START, 1)
SAME_MONTH_LAST_YEAR_START = date(CURRENT_DATE.year - 1, CURRENT_DATE.month, 1)
SAME_MONTH_LAST_YEAR_NEXT = add_months(SAME_MONTH_LAST_YEAR_START, 1)

DIMENSIONS = {
    'channel': {'select_label': 'd.TDistributionChannel', 'alias': 'CanalDistribuicao', 'joins': ['JOIN D_DistributionChannel d ON f.NIDDistributionChannel = d.NIDDistributionChannel']},
    'region': {'select_label': 'd.TRegion', 'alias': 'Regiao', 'joins': ['JOIN D_Region d ON f.NIDRegion = d.NIDRegion']},
    'country': {'select_label': 'd.TCountry', 'alias': 'Pais', 'joins': ['JOIN D_Country d ON f.NIDCountry = d.NIDCountry']},
    'brand': {'select_label': 'd.TProductBrand', 'alias': 'MarcaProduto', 'joins': ['JOIN D_Product p ON f.NIDProduct = p.NIDProduct', 'JOIN D_ProductBrand d ON p.NIDProductBrand = d.NIDProductBrand']},
    'family': {'select_label': 'd.TProductFamily', 'alias': 'FamiliaProduto', 'joins': ['JOIN D_Product p ON f.NIDProduct = p.NIDProduct', 'JOIN D_ProductFamily d ON p.NIDProductFamily = d.NIDProductFamily']},
    'material_type': {'select_label': 'd.TMaterialType', 'alias': 'TipoMaterial', 'joins': ['JOIN D_Product p ON f.NIDProduct = p.NIDProduct', 'JOIN D_MaterialType d ON p.NIDMaterialType = d.NIDMaterialType']},
}

MEASURES = {
    'net_amount': {'expr': 'f.NetAmount', 'alias': 'ValorLiquidoFaturado', 'needs_additional': False},
    'billing_quantity': {'expr': 'f.BillingQuantity', 'alias': 'QuantidadeFaturada', 'needs_additional': False},
    'gross_margin': {'expr': 'f.GrossMargin', 'alias': 'MargemBruta', 'needs_additional': True},
    'promo_total': {'expr': '(f.ZDPRPromotional + f.ZCPRPromotionalCampaign + f.REA1PromotionalDiscount)', 'alias': 'DescontoPromocionalTotal', 'needs_additional': False},
}

@dataclass
class SemanticSpec:
    family: str
    operation: str
    measure: str
    dimension: Optional[str] = None
    time_scope: Optional[str] = None
    ranking: Optional[str] = None
    original_question: Optional[str] = None

def normalize_q(q: str) -> str:
    x = q.lower().strip()
    for a, b in [('á','a'),('à','a'),('â','a'),('ã','a'),('é','e'),('ê','e'),('í','i'),('ó','o'),('ô','o'),('õ','o'),('ú','u'),('ç','c')]:
        x = x.replace(a, b)
    return x

def detect_measure(qn: str) -> str:
    if 'desconto promocional' in qn or 'descontos promocionais' in qn:
        return 'promo_total'
    if 'margem bruta' in qn:
        return 'gross_margin'
    if 'quantidade' in qn:
        return 'billing_quantity'
    return 'net_amount'

def detect_dimension(qn: str) -> Optional[str]:
    if 'canal' in qn:
        return 'channel'
    if 'regiao' in qn:
        return 'region'
    if 'pais' in qn:
        return 'country'
    if 'marca' in qn:
        return 'brand'
    if 'familia de produto' in qn or 'familia' in qn:
        return 'family'
    if 'tipo de material' in qn:
        return 'material_type'
    return None

def classify_question(question: str) -> SemanticSpec:
    qn = normalize_q(question)
    measure = detect_measure(qn)
    dim = detect_dimension(qn)
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
    if ('evolucao mensal' in qn) or ('mes a mes' in qn) or ('evoluiu mensalmente' in qn) or ('por mes nos ultimos 6 meses' in qn) or ('por mes no ultimo semestre movel' in qn):
        return SemanticSpec('F15_window_trend', 'monthly_trend', measure, dim, 'last_6_months', original_question=question)
    raise ValueError(f'Pergunta nao suportada pelo gerador revD: {question}')

def build_sql(spec: SemanticSpec) -> str:
    measure = MEASURES[spec.measure]
    filters = ['f.BillingDocumentIsCancelled = 0']
    if measure['needs_additional']:
        filters.append('f.IsItAnAdditionalCalculatedRecord = 1')
    joins = []
    dim_select = ''
    dim_order = ''
    if spec.dimension:
        d = DIMENSIONS[spec.dimension]
        joins.extend(d['joins'])
        dim_select = f"{d['select_label']} AS {d['alias']}, "
        dim_order = f", {d['alias']}"
    if spec.operation == 'monthly_trend':
        return f"""WITH base AS (
    SELECT
        f.MonthStart AS Mes,
        {dim_select}{measure['expr']} AS metric
    FROM F_Invoice f
    {' '.join(joins)}
    WHERE {' AND '.join(filters)}
      AND f.BillingDocumentDate >= {yyyymmdd(LAST6_START)}
      AND f.BillingDocumentDate <= {yyyymmdd(CURRENT_DATE)}
)
SELECT
    Mes,
    {f"{DIMENSIONS[spec.dimension]['alias']}, " if spec.dimension else ''}SUM(metric) AS {measure['alias']}
FROM base
GROUP BY Mes{f", {DIMENSIONS[spec.dimension]['alias']}" if spec.dimension else ''}
ORDER BY Mes ASC{dim_order};"""
    if spec.operation == 'monthly_avg_per_document':
        return f"""WITH docs AS (
    SELECT
        f.MonthStart AS Mes,
        f.BillingDocument,
        SUM(f.NetAmount) AS ValorDocumento
    FROM F_Invoice f
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= {yyyymmdd(LAST6_START)}
      AND f.BillingDocumentDate <= {yyyymmdd(CURRENT_DATE)}
    GROUP BY f.MonthStart, f.BillingDocument
)
SELECT
    Mes,
    AVG(ValorDocumento) AS TicketMedioPorDocumento
FROM docs
GROUP BY Mes
ORDER BY Mes ASC;"""
    if spec.operation == 'current_vs_previous_month':
        return f"""WITH base AS (
    SELECT
        CASE
            WHEN f.BillingDocumentDate >= {yyyymmdd(CUR_MONTH_START)} AND f.BillingDocumentDate < {yyyymmdd(NEXT_MONTH_START)} THEN 'MesAtual'
            WHEN f.BillingDocumentDate >= {yyyymmdd(PREV_MONTH_START)} AND f.BillingDocumentDate < {yyyymmdd(CUR_MONTH_START)} THEN 'MesAnterior'
            ELSE NULL
        END AS Periodo,
        {measure['expr']} AS metric
    FROM F_Invoice f
    WHERE {' AND '.join(filters)}
      AND f.BillingDocumentDate >= {yyyymmdd(PREV_MONTH_START)}
      AND f.BillingDocumentDate < {yyyymmdd(NEXT_MONTH_START)}
)
SELECT
    Periodo,
    SUM(metric) AS {measure['alias']}
FROM base
WHERE Periodo IS NOT NULL
GROUP BY Periodo
ORDER BY Periodo ASC;"""
    if spec.operation == 'mom_pct_change':
        dim_alias = DIMENSIONS[spec.dimension]['alias'] if spec.dimension else None
        part = f"PARTITION BY {dim_alias} " if dim_alias else ''
        sel_dim = f"{dim_alias},\n    " if dim_alias else ''
        return f"""WITH monthly_sales AS (
    SELECT
        f.MonthStart AS Mes,
        {dim_select}SUM({measure['expr']}) AS {measure['alias']}
    FROM F_Invoice f
    {' '.join(joins)}
    WHERE {' AND '.join(filters)}
      AND f.BillingDocumentDate >= {yyyymmdd(LAST6_START)}
      AND f.BillingDocumentDate <= {yyyymmdd(CURRENT_DATE)}
    GROUP BY f.MonthStart{f", {dim_alias}" if dim_alias else ''}
)
SELECT
    Mes,
    {sel_dim}{measure['alias']},
    LAG({measure['alias']}) OVER ({part}ORDER BY Mes) AS ValorMesAnterior,
    CASE
        WHEN LAG({measure['alias']}) OVER ({part}ORDER BY Mes) IS NULL THEN NULL
        WHEN LAG({measure['alias']}) OVER ({part}ORDER BY Mes) = 0 THEN NULL
        ELSE (({measure['alias']} - LAG({measure['alias']}) OVER ({part}ORDER BY Mes)) * 100.0) / NULLIF(LAG({measure['alias']}) OVER ({part}ORDER BY Mes), 0)
    END AS VariacaoPercentual
FROM monthly_sales
ORDER BY Mes ASC{dim_order};"""
    if spec.operation == 'rolling_avg_3m':
        dim_alias = DIMENSIONS[spec.dimension]['alias'] if spec.dimension else None
        part = f"PARTITION BY {dim_alias} " if dim_alias else ''
        sel_dim = f"{dim_alias},\n    " if dim_alias else ''
        return f"""WITH monthly_sales AS (
    SELECT
        f.MonthStart AS Mes,
        {dim_select}SUM({measure['expr']}) AS {measure['alias']}
    FROM F_Invoice f
    {' '.join(joins)}
    WHERE {' AND '.join(filters)}
      AND f.BillingDocumentDate >= {yyyymmdd(LAST8_START)}
      AND f.BillingDocumentDate <= {yyyymmdd(CURRENT_DATE)}
    GROUP BY f.MonthStart{f", {dim_alias}" if dim_alias else ''}
)
SELECT
    Mes,
    {sel_dim}{measure['alias']},
    AVG({measure['alias']}) OVER ({part}ORDER BY Mes ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS MediaMovel3Meses
FROM monthly_sales
ORDER BY Mes ASC{dim_order};"""
    if spec.operation == 'ytd':
        dim_alias = DIMENSIONS[spec.dimension]['alias'] if spec.dimension else None
        part = f"PARTITION BY {dim_alias} " if dim_alias else ''
        sel_dim = f"{dim_alias},\n    " if dim_alias else ''
        return f"""WITH monthly_sales AS (
    SELECT
        f.MonthStart AS Mes,
        {dim_select}SUM({measure['expr']}) AS {measure['alias']}
    FROM F_Invoice f
    {' '.join(joins)}
    WHERE {' AND '.join(filters)}
      AND f.BillingYear = {CURRENT_DATE.year}
      AND f.BillingDocumentDate <= {yyyymmdd(CURRENT_DATE)}
    GROUP BY f.MonthStart{f", {dim_alias}" if dim_alias else ''}
)
SELECT
    Mes,
    {sel_dim}{measure['alias']},
    SUM({measure['alias']}) OVER ({part}ORDER BY Mes ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS {measure['alias']}YTD
FROM monthly_sales
ORDER BY Mes ASC{dim_order};"""
    if spec.operation == 'monthly_ratio_to_billing':
        dim_alias = DIMENSIONS[spec.dimension]['alias'] if spec.dimension else None
        return f"""WITH monthly_totals AS (
    SELECT
        f.MonthStart AS Mes,
        {dim_select}SUM(f.NetAmount) AS ValorLiquidoFaturado,
        SUM({MEASURES['promo_total']['expr']}) AS DescontoPromocionalTotal
    FROM F_Invoice f
    {' '.join(joins)}
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= {yyyymmdd(LAST6_START)}
      AND f.BillingDocumentDate <= {yyyymmdd(CURRENT_DATE)}
    GROUP BY f.MonthStart{f", {dim_alias}" if dim_alias else ''}
)
SELECT
    Mes,
    {f"{dim_alias}, " if dim_alias else ''}ValorLiquidoFaturado,
    DescontoPromocionalTotal,
    (DescontoPromocionalTotal * 100.0) / NULLIF(ValorLiquidoFaturado, 0) AS PercentagemDescontoPromocional
FROM monthly_totals
ORDER BY Mes ASC{dim_order};"""
    if spec.operation == 'yoy_same_month_by_dimension':
        dim_alias = DIMENSIONS[spec.dimension]['alias']
        return f"""SELECT
    {DIMENSIONS[spec.dimension]['select_label']} AS {dim_alias},
    SUM(CASE WHEN f.BillingDocumentDate >= {yyyymmdd(CUR_MONTH_START)} AND f.BillingDocumentDate < {yyyymmdd(NEXT_MONTH_START)} THEN {measure['expr']} ELSE 0 END) AS ValorMesAtual,
    SUM(CASE WHEN f.BillingDocumentDate >= {yyyymmdd(SAME_MONTH_LAST_YEAR_START)} AND f.BillingDocumentDate < {yyyymmdd(SAME_MONTH_LAST_YEAR_NEXT)} THEN {measure['expr']} ELSE 0 END) AS ValorMesmoMesAnoAnterior,
    CASE
        WHEN SUM(CASE WHEN f.BillingDocumentDate >= {yyyymmdd(SAME_MONTH_LAST_YEAR_START)} AND f.BillingDocumentDate < {yyyymmdd(SAME_MONTH_LAST_YEAR_NEXT)} THEN {measure['expr']} ELSE 0 END) = 0 THEN NULL
        ELSE ((SUM(CASE WHEN f.BillingDocumentDate >= {yyyymmdd(CUR_MONTH_START)} AND f.BillingDocumentDate < {yyyymmdd(NEXT_MONTH_START)} THEN {measure['expr']} ELSE 0 END) - SUM(CASE WHEN f.BillingDocumentDate >= {yyyymmdd(SAME_MONTH_LAST_YEAR_START)} AND f.BillingDocumentDate < {yyyymmdd(SAME_MONTH_LAST_YEAR_NEXT)} THEN {measure['expr']} ELSE 0 END)) * 100.0) / NULLIF(SUM(CASE WHEN f.BillingDocumentDate >= {yyyymmdd(SAME_MONTH_LAST_YEAR_START)} AND f.BillingDocumentDate < {yyyymmdd(SAME_MONTH_LAST_YEAR_NEXT)} THEN {measure['expr']} ELSE 0 END), 0)
    END AS VariacaoPercentual
FROM F_Invoice f
{' '.join(joins)}
WHERE {' AND '.join(filters)}
GROUP BY {dim_alias}
HAVING ValorMesAtual <> 0 OR ValorMesmoMesAnoAnterior <> 0
ORDER BY VariacaoPercentual DESC, {dim_alias} ASC;"""
    raise ValueError(spec)
