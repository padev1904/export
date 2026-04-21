
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List
from unicodedata import normalize

CURRENT_DATE_INT = 20260420
YEAR_START_2026 = 20260101
YEAR_END_2026 = 20261231
MONTH_CURRENT_START = 20260401
MONTH_NEXT_START = 20260501
LAST12M_START = 20250421
LAST6M_START = 20251021


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
    time_scope: str = '2026'
    original_question: str = ''


ENTITY_MAP = {
    'marca': {
        'select': 'b.MarcaProduto',
        'group': 'b.MarcaProduto',
        'joins': [
            'JOIN D_Product p ON f.NIDProduct = p.NIDProduct',
            'JOIN D_ProductBrand pb ON p.NIDProductBrand = pb.NIDProductBrand',
        ],
        'label': 'MarcaProduto',
    },
    'familia': {
        'select': 'pf.TProductFamily',
        'group': 'pf.TProductFamily',
        'joins': [
            'JOIN D_Product p ON f.NIDProduct = p.NIDProduct',
            'JOIN D_ProductFamily pf ON p.NIDProductFamily = pf.NIDProductFamily',
        ],
        'label': 'FamiliaProduto',
    },
    'produto': {
        'select': 'p.TProduct',
        'group': 'p.TProduct',
        'joins': ['JOIN D_Product p ON f.NIDProduct = p.NIDProduct'],
        'label': 'Produto',
    },
    'organizacao_vendas': {
        'select': 's.TSalesOrganization',
        'group': 's.TSalesOrganization',
        'joins': ['JOIN D_SalesOrganization s ON f.NIDSalesOrganization = s.NIDSalesOrganization'],
        'label': 'OrganizacaoVendas',
    },
    'canal': {
        'select': 'dc.TDistributionChannel',
        'group': 'dc.TDistributionChannel',
        'joins': ['JOIN D_DistributionChannel dc ON f.NIDDistributionChannel = dc.NIDDistributionChannel'],
        'label': 'CanalDistribuicao',
    },
    'pais': {
        'select': 'c.TCountry',
        'group': 'c.TCountry',
        'joins': ['JOIN D_Country c ON f.NIDCountry = c.NIDCountry'],
        'label': 'Pais',
    },
    'regiao': {
        'select': 'r.TRegion',
        'group': 'r.TRegion',
        'joins': ['JOIN D_Region r ON f.NIDRegion = r.NIDRegion'],
        'label': 'Regiao',
    },
    'mes': {
        'select': 'CAST(f.BillingDocumentDate / 100 AS INT)',
        'group': 'CAST(f.BillingDocumentDate / 100 AS INT)',
        'joins': [],
        'label': 'Mes',
    },
}


def classify(question: str) -> Spec:
    q = norm(question)
    needs_additional = ('margem bruta' in q) or ('vendas comerciais liquidas' in q) or ('net commercial sales' in q)

    if 'quota' in q or 'percentagem' in q or 'peso' in q:
        if 'desconto promocional' in q:
            if 'por mes' in q or 'mensal' in q:
                return Spec('promo_over_billing', 'ratio', entity='mes', original_question=question)
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
        if 'faturacao do mes atual pertence a cada canal' in q or 'mes atual pertence a cada canal de distribuicao' in q:
            return Spec('net_amount_share', 'share', entity='canal', time_scope='current_month', original_question=question)
        if 'ultimos 12 meses por regiao' in q:
            return Spec('net_amount_share', 'share', entity='regiao', time_scope='last12m', original_question=question)
        if 'cada pais dentro de cada organizacao de vendas em 2026' in q:
            return Spec('net_amount_share_partition', 'share_partition', entity='pais', partition='organizacao_vendas', original_question=question)
    raise ValueError(f'Pergunta fora do gerador percentage_share: {question}')


def base_filters(spec: Spec) -> List[str]:
    filters = []
    if spec.time_scope == '2026':
        filters += [f'f.BillingDocumentDate >= {YEAR_START_2026}', f'f.BillingDocumentDate <= {YEAR_END_2026}']
    elif spec.time_scope == 'current_month':
        filters += [f'f.BillingDocumentDate >= {MONTH_CURRENT_START}', f'f.BillingDocumentDate < {MONTH_NEXT_START}']
    elif spec.time_scope == 'last12m':
        filters += [f'f.BillingDocumentDate >= {LAST12M_START}', f'f.BillingDocumentDate <= {CURRENT_DATE_INT}']
    elif spec.time_scope == 'last6m':
        filters += [f'f.BillingDocumentDate >= {LAST6M_START}', f'f.BillingDocumentDate <= {CURRENT_DATE_INT}']
    filters.append('f.BillingDocumentIsCancelled = 0')
    if spec.needs_additional:
        filters.append('f.IsItAnAdditionalCalculatedRecord = 1')
    return filters


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
FROM F_Invoice f
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
FROM F_Invoice f
    {joins}
WHERE {filters}
GROUP BY {ent['group']}
HAVING SUM(f.BillingQuantity) <> 0
ORDER BY PesoLiquidoMedioPorUnidade DESC, {ent['label']} ASC;
""".strip()
        if spec.measure_kind == 'promo_over_billing':
            ent = ENTITY_MAP[spec.entity]
            filters = '\n      AND '.join(base_filters(Spec(spec.measure_kind, spec.output_kind, entity='mes', time_scope='last6m', original_question=spec.original_question)))
            return f"""
SELECT
    {ent['select']} AS {ent['label']},
    SUM(f.NetAmount) AS ValorLiquidoFaturado,
    SUM(f.ZDPRPromotional + f.ZCPRPromotionalCampaign + f.REA1PromotionalDiscount) AS DescontoPromocionalTotal,
    (SUM(f.ZDPRPromotional + f.ZCPRPromotionalCampaign + f.REA1PromotionalDiscount) * 100.0) / NULLIF(SUM(f.NetAmount), 0) AS PercentagemDescontoPromocional
FROM F_Invoice f
WHERE {filters}
GROUP BY {ent['group']}
ORDER BY {ent['label']} ASC;
""".strip()
    if spec.output_kind == 'ratio_nested':
        ent = ENTITY_MAP[spec.entity]
        part = ENTITY_MAP[spec.partition]
        joins = []
        for j in part['joins'] + ent['joins']:
            if j not in joins:
                joins.append(j)
        filters = '\n      AND '.join(base_filters(spec))
        return f"""
SELECT
    {part['select']} AS {part['label']},
    {ent['select']} AS {ent['label']},
    SUM(f.NetAmount) / NULLIF(SUM(f.BillingQuantity), 0) AS PrecoMedioLiquidoPorUnidade
FROM F_Invoice f
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
        measure_expr = 'f.NetAmount'
        measure_alias = 'ValorLiquidoFaturado'
        if spec.measure_kind == 'gross_margin_share':
            measure_expr = 'f.GrossMargin'
            measure_alias = 'MargemBruta'
        elif spec.measure_kind == 'billing_quantity_share':
            measure_expr = 'f.BillingQuantity'
            measure_alias = 'QuantidadeFaturada'
        return f"""
WITH base AS (
    SELECT
        {ent['select']} AS {ent['label']},
        SUM({measure_expr}) AS {measure_alias}
    FROM F_Invoice f
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
        joins = []
        for j in part['joins'] + ent['joins']:
            if j not in joins:
                joins.append(j)
        filters = '\n      AND '.join(base_filters(spec))
        measure_expr = 'f.NetAmount'
        measure_alias = 'ValorLiquidoFaturado'
        if spec.measure_kind == 'gross_margin_share_partition':
            measure_expr = 'f.GrossMargin'
            measure_alias = 'MargemBruta'
        elif spec.measure_kind == 'net_commercial_sales_share_partition':
            measure_expr = 'f.NetCommercialSales'
            measure_alias = 'VendasComerciaisLiquidas'
        return f"""
WITH base AS (
    SELECT
        {part['select']} AS {part['label']},
        {ent['select']} AS {ent['label']},
        SUM({measure_expr}) AS {measure_alias}
    FROM F_Invoice f
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
        joins = []
        for j in part['joins'] + ent['joins']:
            if j not in joins:
                joins.append(j)
        filters = '\n      AND '.join(base_filters(spec))
        return f"""
WITH base AS (
    SELECT
        {part['select']} AS {part['label']},
        {ent['select']} AS {ent['label']},
        SUM(f.NetAmount) AS ValorLiquidoFaturado
    FROM F_Invoice f
        {'\n        '.join(joins)}
    WHERE {filters}
    GROUP BY {part['group']}, {ent['group']}
)
SELECT
    {part['label']},
    {ent['label']},
    ValorLiquidoFaturado,
    (ValorLiquidoFaturado * 100.0) / NULLIF(SUM(ValorLiquidoFaturado) OVER (PARTITION BY {part['label']}), 0) AS Percentagem
FROM base
ORDER BY {part['label']} ASC, Percentagem DESC, {ent['label']} ASC;
""".strip()
    if spec.output_kind == 'share_partition_2d_nested':
        ent = ENTITY_MAP[spec.entity]
        part = ENTITY_MAP[spec.partition]
        joins = []
        for j in part['joins'] + ent['joins']:
            if j not in joins:
                joins.append(j)
        filters = '\n      AND '.join(base_filters(spec))
        return f"""
WITH base AS (
    SELECT
        CAST(f.BillingDocumentDate / 100 AS INT) AS Mes,
        {part['select']} AS {part['label']},
        {ent['select']} AS {ent['label']},
        SUM(f.NetAmount) AS ValorLiquidoFaturado
    FROM F_Invoice f
        {'\n        '.join(joins)}
    WHERE {filters}
    GROUP BY CAST(f.BillingDocumentDate / 100 AS INT), {part['group']}, {ent['group']}
)
SELECT
    Mes,
    {part['label']},
    {ent['label']},
    ValorLiquidoFaturado,
    (ValorLiquidoFaturado * 100.0) / NULLIF(SUM(ValorLiquidoFaturado) OVER (PARTITION BY Mes, {part['label']}), 0) AS Percentagem
FROM base
ORDER BY Mes ASC, {part['label']} ASC, Percentagem DESC, {ent['label']} ASC;
""".strip()
    raise ValueError(spec)


def generate_sql(question: str) -> str:
    spec = classify(question)
    return render_sql(spec)
