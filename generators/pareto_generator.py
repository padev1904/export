from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date
from typing import Optional

CURRENT_DATE = date(2026, 4, 23)


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
        'id_expr': 'f.NIDPayerParty',
        'id_alias': 'NIDPayerParty',
        'lookup_table_sqlserver': 'dbo.D_Customer',
        'lookup_table_sqlite': 'D_Customer',
        'lookup_pk': 'NIDCustomer',
        'lookup_text': 'TCustomer',
        'label_alias': 'Cliente',
        'joins_sqlserver': [],
        'joins_sqlite': [],
    },
    'product': {
        'id_expr': 'f.NIDProduct',
        'id_alias': 'NIDProduct',
        'lookup_table_sqlserver': 'dbo.D_Product',
        'lookup_table_sqlite': 'D_Product',
        'lookup_pk': 'NIDProduct',
        'lookup_text': 'TProduct',
        'label_alias': 'Produto',
        'joins_sqlserver': [],
        'joins_sqlite': [],
    },
    'brand': {
        'id_expr': 'p.NIDProductBrand',
        'id_alias': 'NIDProductBrand',
        'lookup_table_sqlserver': 'dbo.D_ProductBrand',
        'lookup_table_sqlite': 'D_ProductBrand',
        'lookup_pk': 'NIDProductBrand',
        'lookup_text': 'TProductBrand',
        'label_alias': 'MarcaProduto',
        'joins_sqlserver': ['JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct'],
        'joins_sqlite': ['JOIN D_Product p ON f.NIDProduct = p.NIDProduct'],
    },
    'family': {
        'id_expr': 'p.NIDProductFamily',
        'id_alias': 'NIDProductFamily',
        'lookup_table_sqlserver': 'dbo.D_ProductFamily',
        'lookup_table_sqlite': 'D_ProductFamily',
        'lookup_pk': 'NIDProductFamily',
        'lookup_text': 'TProductFamily',
        'label_alias': 'FamiliaProduto',
        'joins_sqlserver': ['JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct'],
        'joins_sqlite': ['JOIN D_Product p ON f.NIDProduct = p.NIDProduct'],
    },
    'country': {
        'id_expr': 'f.NIDCountry',
        'id_alias': 'NIDCountry',
        'lookup_table_sqlserver': 'dbo.D_Country',
        'lookup_table_sqlite': 'D_Country',
        'lookup_pk': 'NIDCountry',
        'lookup_text': 'TCountry',
        'label_alias': 'Pais',
        'joins_sqlserver': [],
        'joins_sqlite': [],
    },
    'channel': {
        'id_expr': 'f.NIDDistributionChannel',
        'id_alias': 'NIDDistributionChannel',
        'lookup_table_sqlserver': 'dbo.D_DistributionChannel',
        'lookup_table_sqlite': 'D_DistributionChannel',
        'lookup_pk': 'NIDDistributionChannel',
        'lookup_text': 'TDistributionChannel',
        'label_alias': 'CanalDistribuicao',
        'joins_sqlserver': [],
        'joins_sqlite': [],
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
    partition: Optional[str] = None
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
    elif 'paises' in q or 'pais' in q:
        entity = 'country'
    elif 'produtos' in q or 'produto' in q:
        entity = 'product'
    elif 'clientes' in q or 'cliente' in q:
        entity = 'customer'
    else:
        entity = 'customer'

    partition = 'channel' if 'dentro de cada canal de distribuicao' in q or 'dentro de cada canal' in q else None

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
        partition=partition,
        start_date_int=start_date_int,
        requires_additional=MEASURE_SPECS[measure]['requires_additional'],
        original_question=question,
    )


class ParetoGenerator:
    def _build_sql(self, spec: ParetoSpec, dialect: str = 'sqlserver', mode: str = 'canonical') -> str:
        entity = ENTITY_SPECS[spec.entity]
        measure = MEASURE_SPECS[spec.measure]
        joins = list(entity['joins_sqlserver' if dialect == 'sqlserver' else 'joins_sqlite'])
        table_name = 'dbo.F_Invoice' if dialect == 'sqlserver' else 'F_Invoice'
        entity_lookup_table = entity['lookup_table_sqlserver' if dialect == 'sqlserver' else 'lookup_table_sqlite']
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

        partition_select = ''
        partition_group = ''
        partition_window = ''
        partition_total = ''
        partition_projection = ''
        partition_join = ''
        order_prefix = ''

        if spec.partition:
            partition = ENTITY_SPECS[spec.partition]
            joins.extend(partition['joins_sqlserver' if dialect == 'sqlserver' else 'joins_sqlite'])
            partition_lookup_table = partition['lookup_table_sqlserver' if dialect == 'sqlserver' else 'lookup_table_sqlite']
            partition_select = f"        {partition['id_expr']} AS {partition['id_alias']},\n"
            partition_group = f"{partition['id_expr']}, "
            partition_window = f"PARTITION BY {partition['id_alias']}\n            "
            partition_total = f"PARTITION BY {partition['id_alias']}"
            partition_projection = f"    pd.{partition['lookup_text']} AS {partition['label_alias']},\n"
            partition_join = f"JOIN {partition_lookup_table} pd ON pd.{partition['lookup_pk']} = s.{partition['id_alias']}\n"
            order_prefix = f"{partition['label_alias']} ASC, "

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
{partition_select}        {entity['id_expr']} AS {entity['id_alias']},
        SUM({measure['expr']}) AS {metric_alias}
    FROM {table_name} f
    {' '.join(joins)}
    WHERE {where_sql}
    GROUP BY {partition_group}{entity['id_expr']}
),
filtered AS (
    SELECT *
    FROM sales_by_entity{positive_guard}
),
ranked AS (
    SELECT
        *,
        SUM({metric_alias}) OVER (
            {partition_window}ORDER BY {metric_alias} DESC, {entity['id_alias']}
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS ValorAcumulado,
        SUM({metric_alias}) OVER ({partition_total}) AS ValorTotal
    FROM filtered
),
scored AS (
    SELECT
        *,
        ({metric_alias} * 100.0) / NULLIF(ValorTotal, 0) AS PercentagemIndividual,
        (ValorAcumulado * 100.0) / NULLIF(ValorTotal, 0) AS PercentagemAcumulada,
        ((ValorAcumulado - {metric_alias}) * 100.0) / NULLIF(ValorTotal, 0) AS PercentagemAntes
    FROM ranked
)
SELECT
{partition_projection}    d.{entity['lookup_text']} AS {entity['label_alias']},
    s.{metric_alias},
    s.PercentagemIndividual,
    s.PercentagemAcumulada{before_col}
FROM scored s
{partition_join}JOIN {entity_lookup_table} d ON d.{entity['lookup_pk']} = s.{entity['id_alias']}
{final_filter}
ORDER BY {order_prefix}s.{metric_alias} DESC, {entity['label_alias']};
""".strip()

    def build_sqlserver_sql(self, spec: ParetoSpec, mode: str = 'canonical') -> str:
        return self._build_sql(spec=spec, dialect='sqlserver', mode=mode)

    def build_sqlite_sql(self, spec: ParetoSpec, mode: str = 'canonical') -> str:
        return self._build_sql(spec=spec, dialect='sqlite', mode=mode)
