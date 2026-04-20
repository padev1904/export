from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from typing import Optional

CURRENT_DATE = date(2026, 4, 20)


def yyyymmdd(d: date) -> int:
    return int(d.strftime('%Y%m%d'))


def month_start(year: int, month: int) -> date:
    return date(year, month, 1)


def add_months(d: date, months: int) -> date:
    year = d.year + (d.month - 1 + months) // 12
    month = (d.month - 1 + months) % 12 + 1
    return date(year, month, 1)


def moving_window_start(months: int) -> int:
    start = add_months(month_start(CURRENT_DATE.year, CURRENT_DATE.month), -(months - 1))
    return yyyymmdd(start)


ENTITY_SPECS = {
    'customer': {
        'label_expr': 'd.TCustomer',
        'alias': 'Cliente',
        'joins_sqlserver': ['JOIN dbo.D_Customer d ON f.NIDPayerParty = d.NIDCustomer'],
        'joins_sqlite': ['JOIN D_Customer d ON f.NIDPayerParty = d.NIDCustomer'],
    },
    'product': {
        'label_expr': 'd.TProduct',
        'alias': 'Produto',
        'joins_sqlserver': ['JOIN dbo.D_Product d ON f.NIDProduct = d.NIDProduct'],
        'joins_sqlite': ['JOIN D_Product d ON f.NIDProduct = d.NIDProduct'],
    },
    'brand': {
        'label_expr': 'd.TProductBrand',
        'alias': 'MarcaProduto',
        'joins_sqlserver': [
            'JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct',
            'JOIN dbo.D_ProductBrand d ON p.NIDProductBrand = d.NIDProductBrand',
        ],
        'joins_sqlite': [
            'JOIN D_Product p ON f.NIDProduct = p.NIDProduct',
            'JOIN D_ProductBrand d ON p.NIDProductBrand = d.NIDProductBrand',
        ],
    },
    'family': {
        'label_expr': 'd.TProductFamily',
        'alias': 'FamiliaProduto',
        'joins_sqlserver': [
            'JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct',
            'JOIN dbo.D_ProductFamily d ON p.NIDProductFamily = d.NIDProductFamily',
        ],
        'joins_sqlite': [
            'JOIN D_Product p ON f.NIDProduct = p.NIDProduct',
            'JOIN D_ProductFamily d ON p.NIDProductFamily = d.NIDProductFamily',
        ],
    },
    'country': {
        'label_expr': 'd.TCountry',
        'alias': 'Pais',
        'joins_sqlserver': ['JOIN dbo.D_Country d ON f.NIDCountry = d.NIDCountry'],
        'joins_sqlite': ['JOIN D_Country d ON f.NIDCountry = d.NIDCountry'],
    },
    'channel': {
        'label_expr': 'd.TDistributionChannel',
        'alias': 'CanalDistribuicao',
        'joins_sqlserver': ['JOIN dbo.D_DistributionChannel d ON f.NIDDistributionChannel = d.NIDDistributionChannel'],
        'joins_sqlite': ['JOIN D_DistributionChannel d ON f.NIDDistributionChannel = d.NIDDistributionChannel'],
    },
}

MEASURE_SPECS = {
    'net_amount': {
        'expr': 'f.NetAmount',
        'alias': 'ValorLiquidoFaturado',
        'requires_additional': False,
    },
    'billing_quantity': {
        'expr': 'f.BillingQuantity',
        'alias': 'QuantidadeFaturada',
        'requires_additional': False,
    },
    'gross_margin': {
        'expr': 'f.GrossMargin',
        'alias': 'MargemBruta',
        'requires_additional': True,
    },
    'promo_total': {
        'expr': '(f.ZDPRPromotional + f.ZCPRPromotionalCampaign + f.REA1PromotionalDiscount)',
        'alias': 'DescontoPromocionalTotal',
        'requires_additional': False,
    },
}


@dataclass
class ParetoSpec:
    entity: str
    measure: str
    start_date_int: int
    requires_additional: bool = False
    threshold: float = 80.0
    original_question: Optional[str] = None


def normalize(text: str) -> str:
    x = text.lower().strip()
    repl = {
        'á': 'a', 'à': 'a', 'â': 'a', 'ã': 'a',
        'é': 'e', 'ê': 'e',
        'í': 'i',
        'ó': 'o', 'ô': 'o', 'õ': 'o',
        'ú': 'u', 'ç': 'c',
    }
    for a, b in repl.items():
        x = x.replace(a, b)
    return re.sub(r'\s+', ' ', x)


def parse_pareto_question(question: str) -> ParetoSpec:
    q = normalize(question)
    if 'marca' in q or 'marcas' in q:
        entity = 'brand'
    elif 'familia de produto' in q or 'familias de produto' in q or 'familia' in q or 'familias' in q:
        entity = 'family'
    elif 'canal de distribuicao' in q or 'canais' in q or 'canal' in q:
        entity = 'channel'
    elif 'paises' in q or 'pais' in q:
        entity = 'country'
    elif 'produtos' in q or 'produto' in q:
        entity = 'product'
    elif 'clientes' in q or 'cliente' in q:
        entity = 'customer'
    else:
        entity = 'customer'

    if 'desconto promocional' in q:
        measure = 'promo_total'
    elif 'margem bruta' in q:
        measure = 'gross_margin'
    elif 'quantidade' in q:
        measure = 'billing_quantity'
    else:
        measure = 'net_amount'

    if 'ultimo ano movel' in q or 'ultimos 12 meses' in q:
        start_date_int = moving_window_start(12)
    elif 'ultimos 6 meses' in q:
        start_date_int = moving_window_start(6)
    elif 'em 2026' in q or 'de 2026' in q:
        start_date_int = 20260101
    else:
        start_date_int = moving_window_start(12)

    return ParetoSpec(
        entity=entity,
        measure=measure,
        start_date_int=start_date_int,
        requires_additional=MEASURE_SPECS[measure]['requires_additional'],
        original_question=question,
    )


class ParetoGenerator:
    def _build_sql(self, spec: ParetoSpec, dialect: str = 'sqlserver', mode: str = 'canonical') -> str:
        entity = ENTITY_SPECS[spec.entity]
        measure = MEASURE_SPECS[spec.measure]
        label = entity['label_expr']
        alias = entity['alias']
        joins = '\n    '.join(entity['joins_sqlserver' if dialect == 'sqlserver' else 'joins_sqlite'])
        table_name = 'dbo.F_Invoice' if dialect == 'sqlserver' else 'F_Invoice'
        metric_alias = measure['alias']
        where = [
            f'f.BillingDocumentDate >= {spec.start_date_int}',
            'f.BillingDocumentIsCancelled = 0',
        ]
        if spec.start_date_int == 20260101:
            where.append('f.BillingDocumentDate <= 20261231')
        if spec.requires_additional:
            where.append('f.IsItAnAdditionalCalculatedRecord = 1')
        where_sql = '\n      AND '.join(where)

        if mode == 'legacy_benchmark':
            positive_guard = ''
            final_filter = f'WHERE PercentagemAcumulada <= {spec.threshold}'
            before_col = ''
        elif mode == 'canonical_no_positive_guard':
            positive_guard = ''
            final_filter = f'WHERE PercentagemAcumulada <= {spec.threshold} OR PercentagemAntes < {spec.threshold}'
            before_col = ',\n    PercentagemAntes'
        elif mode == 'canonical':
            positive_guard = f'\n    WHERE {metric_alias} > 0'
            final_filter = f'WHERE PercentagemAcumulada <= {spec.threshold} OR PercentagemAntes < {spec.threshold}'
            before_col = ',\n    PercentagemAntes'
        else:
            raise ValueError(mode)

        return f"""
WITH sales_by_entity AS (
    SELECT
        {label} AS {alias},
        SUM({measure['expr']}) AS {metric_alias}
    FROM {table_name} f
    {joins}
    WHERE {where_sql}
    GROUP BY {label}
),
filtered AS (
    SELECT *
    FROM sales_by_entity{positive_guard}
),
ranked AS (
    SELECT
        {alias},
        {metric_alias},
        SUM({metric_alias}) OVER (
            ORDER BY {metric_alias} DESC, {alias}
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS ValorAcumulado,
        SUM({metric_alias}) OVER () AS ValorTotal
    FROM filtered
),
scored AS (
    SELECT
        {alias},
        {metric_alias},
        ({metric_alias} * 100.0) / NULLIF(ValorTotal, 0) AS PercentagemIndividual,
        (ValorAcumulado * 100.0) / NULLIF(ValorTotal, 0) AS PercentagemAcumulada,
        ((ValorAcumulado - {metric_alias}) * 100.0) / NULLIF(ValorTotal, 0) AS PercentagemAntes
    FROM ranked
)
SELECT
    {alias},
    {metric_alias},
    PercentagemIndividual,
    PercentagemAcumulada{before_col}
FROM scored
{final_filter}
ORDER BY {metric_alias} DESC, {alias};
""".strip()

    def build_sqlserver_sql(self, spec: ParetoSpec, mode: str = 'canonical') -> str:
        return self._build_sql(spec=spec, dialect='sqlserver', mode=mode)

    def build_sqlite_sql(self, spec: ParetoSpec, mode: str = 'canonical') -> str:
        return self._build_sql(spec=spec, dialect='sqlite', mode=mode)
