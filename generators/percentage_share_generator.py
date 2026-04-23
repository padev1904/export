
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List
from unicodedata import normalize

from sqlserver_patterns import (
    build_named_time_predicate,
    current_month_start_date_sql,
    dedupe_joins,
    int_date_expr,
    next_month_start_date_sql,
    year_month_bucket_expr,
)


def norm(text: str) -> str:
    s = normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii').lower()
    return ' '.join(s.split())


@dataclass
class Spec:
    measure_kind: str
    output_kind: str
    entity: Optional[str] = None
    partition: Optional[str] = None
    needs_additional: bool = False
    time_scope: str = 'explicit_year'
    year: int | None = 2026
    original_question: str = ''


ENTITY_MAP = {
    'marca': {
        'select': 'pb.TProductBrand',
        'group': 'pb.TProductBrand',
        'joins': [
            'JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct',
            'JOIN dbo.D_ProductBrand pb ON p.NIDProductBrand = pb.NIDProductBrand',
        ],
        'label': 'MarcaProduto',
    },
    'familia': {
        'select': 'pf.TProductFamily',
        'group': 'pf.TProductFamily',
        'joins': [
            'JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct',
            'JOIN dbo.D_ProductFamily pf ON p.NIDProductFamily = pf.NIDProductFamily',
        ],
        'label': 'FamiliaProduto',
    },
    'produto': {
        'select': 'p.TProduct',
        'group': 'p.TProduct',
        'joins': ['JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct'],
        'label': 'Produto',
    },
    'organizacao_vendas': {
        'select': 'so.TSalesOrganization',
        'group': 'so.TSalesOrganization',
        'joins': ['JOIN dbo.D_SalesOrganization so ON f.NIDSalesOrganization = so.NIDSalesOrganization'],
        'label': 'OrganizacaoVendas',
    },
    'canal': {
        'select': 'dc.TDistributionChannel',
        'group': 'dc.TDistributionChannel',
        'joins': ['JOIN dbo.D_DistributionChannel dc ON f.NIDDistributionChannel = dc.NIDDistributionChannel'],
        'label': 'CanalDistribuicao',
    },
    'pais': {
        'select': 'co.TCountry',
        'group': 'co.TCountry',
        'joins': ['JOIN dbo.D_Country co ON f.NIDCountry = co.NIDCountry'],
        'label': 'Pais',
    },
    'regiao': {
        'select': 'r.TRegion',
        'group': 'r.TRegion',
        'joins': ['JOIN dbo.D_Region r ON f.NIDRegion = r.NIDRegion'],
        'label': 'Regiao',
    },
    'mes': {
        'select': year_month_bucket_expr(),
        'group': year_month_bucket_expr(),
        'joins': [],
        'label': 'Mes',
    },
}


def classify(question: str) -> Spec:
    q = norm(question)
    needs_additional = ('margem bruta' in q) or ('vendas comerciais liquidas' in q) or ('net commercial sales' in q)
    has_current_year = ('ano atual' in q) or ('ano corrente' in q) or ('este ano' in q)
    has_last_12m = 'ultimos 12 meses' in q or 'ultimo ano movel' in q
    has_month = ('por mes' in q) or ('mensal' in q)

    if 'quota' in q or 'percentagem' in q or 'peso' in q:
        if 'desconto promocional' in q:
            if has_month:
                return Spec('promo_over_billing', 'ratio', entity='mes', time_scope='last_6_months', year=None, original_question=question)
        if 'preco medio liquido por unidade' in q:
            if 'por marca' in q:
                return Spec('net_price_per_unit', 'ratio', entity='marca', original_question=question)
            if 'por produto' in q:
                return Spec('net_price_per_unit', 'ratio', entity='produto', original_question=question)
            if 'por familia de produto e por marca' in q or 'por familia e por marca' in q:
                return Spec('net_price_per_unit', 'ratio_nested', entity='marca', partition='familia', original_question=question)
        if 'peso liquido medio por unidade' in q:
            return Spec('net_weight_per_unit', 'ratio', entity='produto', original_question=question)
        if 'margem bruta por marca' in q:
            return Spec('gross_margin_share', 'share', entity='marca', needs_additional=True, original_question=question)
        if 'quantidade faturada de cada familia de produto' in q:
            return Spec('billing_quantity_share', 'share', entity='familia', original_question=question)
        if 'faturacao de cada marca dentro da sua familia' in q:
            return Spec('net_amount_share_partition', 'share_partition', entity='marca', partition='familia', original_question=question)
        if 'margem bruta de cada marca dentro da sua familia' in q:
            return Spec('gross_margin_share_partition', 'share_partition', entity='marca', partition='familia', needs_additional=True, original_question=question)
        if 'vendas comerciais liquidas de cada marca dentro da organizacao de vendas' in q:
            return Spec('net_commercial_sales_share_partition', 'share_partition', entity='marca', partition='organizacao_vendas', needs_additional=True, original_question=question)
        if 'valor liquido faturado de cada organizacao de vendas em cada mes' in q:
            return Spec('net_amount_share_partition', 'share_partition_2d', entity='organizacao_vendas', partition='mes', original_question=question)
        if 'valor liquido faturado de cada marca dentro da sua familia e por mes' in q:
            return Spec('net_amount_share_partition_2d', 'share_partition_2d_nested', entity='marca', partition='familia', original_question=question)
        if (
            ('quota de valor liquido faturado de cada organizacao de vendas' in q or 'percentagem do valor liquido faturado de cada organizacao de vendas' in q)
            and 'dentro de cada canal de distribuicao' in q
            and has_month
            and has_current_year
        ):
            return Spec('net_amount_share_partition_2d', 'share_partition_2d_nested', entity='organizacao_vendas', partition='canal', time_scope='current_year', year=None, original_question=question)
        if (
            ('percentagem da margem bruta de cada marca' in q or 'quota da margem bruta de cada marca' in q)
            and ('dentro da respetiva familia' in q or 'dentro da sua familia' in q)
            and has_month
            and has_current_year
        ):
            return Spec('gross_margin_share_partition_2d', 'share_partition_2d_nested', entity='marca', partition='familia', needs_additional=True, time_scope='current_year', year=None, original_question=question)
        if 'faturacao do mes atual pertence a cada canal' in q or 'mes atual pertence a cada canal de distribuicao' in q:
            return Spec('net_amount_share', 'share', entity='canal', time_scope='current_month', year=None, original_question=question)
        if 'ultimos 12 meses por regiao' in q:
            return Spec('net_amount_share', 'share', entity='regiao', time_scope='last_12_months', year=None, original_question=question)
        if 'cada pais dentro de cada organizacao de vendas em 2026' in q:
            return Spec('net_amount_share_partition', 'share_partition', entity='pais', partition='organizacao_vendas', original_question=question)
        if (
            ('quota de faturacao de cada pais' in q or 'percentagem da faturacao de cada pais' in q or 'quota de valor liquido faturado de cada pais' in q)
            and 'dentro de cada organizacao de vendas' in q
            and has_last_12m
        ):
            return Spec('net_amount_share_partition', 'share_partition', entity='pais', partition='organizacao_vendas', time_scope='last_12_months', year=None, original_question=question)
    raise ValueError(f'Pergunta fora do gerador percentage_share: {question}')


def base_filters(spec: Spec) -> List[str]:
    filters: List[str] = []
    if spec.time_scope in {'explicit_year', 'current_year', 'last_12_months', 'last_6_months'}:
        filters.append(build_named_time_predicate(spec.time_scope, year=spec.year))
    elif spec.time_scope == 'current_month':
        filters += [
            f'f.BillingDocumentDate >= {int_date_expr(current_month_start_date_sql())}',
            f'f.BillingDocumentDate < {int_date_expr(next_month_start_date_sql())}',
        ]
    else:
        raise ValueError(f'unsupported time scope: {spec.time_scope}')
    filters.append('f.BillingDocumentIsCancelled = 0')
    if spec.needs_additional:
        filters.append('f.IsItAnAdditionalCalculatedRecord = 1')
    return filters


def measure_sql(spec: Spec) -> tuple[str, str]:
    if spec.measure_kind in {'net_amount_share', 'net_amount_share_partition', 'net_amount_share_partition_2d'}:
        return 'SUM(f.NetAmount)', 'ValorLiquidoFaturado'
    if spec.measure_kind in {'gross_margin_share', 'gross_margin_share_partition', 'gross_margin_share_partition_2d'}:
        return 'SUM(f.GrossMargin)', 'MargemBruta'
    if spec.measure_kind == 'billing_quantity_share':
        return 'SUM(f.BillingQuantity)', 'QuantidadeFaturada'
    if spec.measure_kind == 'net_commercial_sales_share_partition':
        return 'SUM(f.NetCommercialSales)', 'VendasComerciaisLiquidas'
    raise ValueError(spec.measure_kind)


def render_sql(spec: Spec) -> str:
    if spec.output_kind == 'ratio':
        if spec.measure_kind == 'net_price_per_unit':
            ent = ENTITY_MAP[spec.entity]
            joins = '\n    '.join(ent['joins'])
            filters = '\n      AND '.join(base_filters(spec))
            return f"""
SELECT
    {ent['select']} AS {ent['label']},
    SUM(f.NetAmount) / NULLIF(SUM(f.BillingQuantity), 0) AS PrecoMedioLiquidoPorUnidade
FROM dbo.F_Invoice f
    {joins}
WHERE {filters}
GROUP BY {ent['group']}
HAVING SUM(f.BillingQuantity) <> 0
ORDER BY PrecoMedioLiquidoPorUnidade DESC, {ent['label']} ASC;
""".strip()
        if spec.measure_kind == 'net_weight_per_unit':
            ent = ENTITY_MAP[spec.entity]
            joins = '\n    '.join(ent['joins'])
            filters = '\n      AND '.join(base_filters(spec))
            return f"""
SELECT
    {ent['select']} AS {ent['label']},
    SUM(f.ItemNetWeight) / NULLIF(SUM(f.BillingQuantity), 0) AS PesoLiquidoMedioPorUnidade
FROM dbo.F_Invoice f
    {joins}
WHERE {filters}
GROUP BY {ent['group']}
HAVING SUM(f.BillingQuantity) <> 0
ORDER BY PesoLiquidoMedioPorUnidade DESC, {ent['label']} ASC;
""".strip()
        if spec.measure_kind == 'promo_over_billing':
            ent = ENTITY_MAP[spec.entity]
            filters = '\n      AND '.join(base_filters(spec))
            return f"""
SELECT
    {ent['select']} AS {ent['label']},
    SUM(f.NetAmount) AS ValorLiquidoFaturado,
    SUM(f.ZDPRPromotional + f.ZCPRPromotionalCampaign + f.REA1PromotionalDiscount) AS DescontoPromocionalTotal,
    (SUM(f.ZDPRPromotional + f.ZCPRPromotionalCampaign + f.REA1PromotionalDiscount) * 100.0) / NULLIF(SUM(f.NetAmount), 0) AS PercentagemDescontoPromocional
FROM dbo.F_Invoice f
WHERE {filters}
GROUP BY {ent['group']}
ORDER BY {ent['label']} ASC;
""".strip()

    if spec.output_kind == 'ratio_nested':
        ent = ENTITY_MAP[spec.entity]
        part = ENTITY_MAP[spec.partition]
        joins = dedupe_joins(part['joins'] + ent['joins'])
        filters = '\n      AND '.join(base_filters(spec))
        return f"""
SELECT
    {part['select']} AS {part['label']},
    {ent['select']} AS {ent['label']},
    SUM(f.NetAmount) / NULLIF(SUM(f.BillingQuantity), 0) AS PrecoMedioLiquidoPorUnidade
FROM dbo.F_Invoice f
    {'\n    '.join(joins)}
WHERE {filters}
GROUP BY {part['group']}, {ent['group']}
HAVING SUM(f.BillingQuantity) <> 0
ORDER BY {part['label']} ASC, PrecoMedioLiquidoPorUnidade DESC, {ent['label']} ASC;
""".strip()

    if spec.output_kind == 'share':
        ent = ENTITY_MAP[spec.entity]
        joins = '\n    '.join(ent['joins'])
        filters = '\n      AND '.join(base_filters(spec))
        measure_expr, measure_alias = measure_sql(spec)
        return f"""
WITH base AS (
    SELECT
        {ent['select']} AS {ent['label']},
        {measure_expr} AS {measure_alias}
    FROM dbo.F_Invoice f
        {joins}
    WHERE {filters}
    GROUP BY {ent['group']}
)
SELECT
    {ent['label']},
    {measure_alias},
    ({measure_alias} * 100.0) / NULLIF(SUM({measure_alias}) OVER (), 0) AS Percentagem
FROM base
ORDER BY Percentagem DESC, {ent['label']} ASC;
""".strip()

    if spec.output_kind == 'share_partition':
        ent = ENTITY_MAP[spec.entity]
        part = ENTITY_MAP[spec.partition]
        joins = dedupe_joins(part['joins'] + ent['joins'])
        filters = '\n      AND '.join(base_filters(spec))
        measure_expr, measure_alias = measure_sql(spec)
        return f"""
WITH base AS (
    SELECT
        {part['select']} AS {part['label']},
        {ent['select']} AS {ent['label']},
        {measure_expr} AS {measure_alias}
    FROM dbo.F_Invoice f
        {'\n        '.join(joins)}
    WHERE {filters}
    GROUP BY {part['group']}, {ent['group']}
)
SELECT
    {part['label']},
    {ent['label']},
    {measure_alias},
    ({measure_alias} * 100.0) / NULLIF(SUM({measure_alias}) OVER (PARTITION BY {part['label']}), 0) AS Percentagem
FROM base
ORDER BY {part['label']} ASC, Percentagem DESC, {ent['label']} ASC;
""".strip()

    if spec.output_kind == 'share_partition_2d':
        ent = ENTITY_MAP[spec.entity]
        part = ENTITY_MAP[spec.partition]
        joins = dedupe_joins(part['joins'] + ent['joins'])
        filters = '\n      AND '.join(base_filters(spec))
        measure_expr, measure_alias = measure_sql(spec)
        return f"""
WITH base AS (
    SELECT
        {part['select']} AS {part['label']},
        {ent['select']} AS {ent['label']},
        {measure_expr} AS {measure_alias}
    FROM dbo.F_Invoice f
        {'\n        '.join(joins)}
    WHERE {filters}
    GROUP BY {part['group']}, {ent['group']}
)
SELECT
    {part['label']},
    {ent['label']},
    {measure_alias},
    ({measure_alias} * 100.0) / NULLIF(SUM({measure_alias}) OVER (PARTITION BY {part['label']}), 0) AS Percentagem
FROM base
ORDER BY {part['label']} ASC, Percentagem DESC, {ent['label']} ASC;
""".strip()

    if spec.output_kind == 'share_partition_2d_nested':
        ent = ENTITY_MAP[spec.entity]
        part = ENTITY_MAP[spec.partition]
        joins = dedupe_joins(part['joins'] + ent['joins'])
        filters = '\n      AND '.join(base_filters(spec))
        measure_expr, measure_alias = measure_sql(spec)
        return f"""
WITH base AS (
    SELECT
        {ENTITY_MAP['mes']['select']} AS {ENTITY_MAP['mes']['label']},
        {part['select']} AS {part['label']},
        {ent['select']} AS {ent['label']},
        {measure_expr} AS {measure_alias}
    FROM dbo.F_Invoice f
        {'\n        '.join(joins)}
    WHERE {filters}
    GROUP BY {ENTITY_MAP['mes']['group']}, {part['group']}, {ent['group']}
)
SELECT
    Mes,
    {part['label']},
    {ent['label']},
    {measure_alias},
    ({measure_alias} * 100.0) / NULLIF(SUM({measure_alias}) OVER (PARTITION BY Mes, {part['label']}), 0) AS Percentagem
FROM base
ORDER BY Mes ASC, {part['label']} ASC, Percentagem DESC, {ent['label']} ASC;
""".strip()

    raise ValueError(spec)


def generate_sql(question: str) -> str:
    spec = classify(question)
    return render_sql(spec)
