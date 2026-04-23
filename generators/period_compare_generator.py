from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class PeriodCompareSpec:
    question: str
    measure_expr: str
    dimension_expr: Optional[str]
    dimension_alias: Optional[str]
    joins: Tuple[str, ...]
    extra_filters: Tuple[str, ...]
    comparison_shape: str  # monthly_grid | delta_by_dimension
    delta_mode: Optional[str] = None  # absolute | percent


def normalize(text: str) -> str:
    x = text.lower().strip()
    return x.translate(str.maketrans('áàâãéêíóôõúç', 'aaaaeeiooouc'))


def detect_measure(qn: str) -> tuple[str, bool]:
    if 'vendas comerciais liquidas' in qn or 'vendas comerciais líquidas' in qn:
        return 'f.NetCommercialSales', True
    if 'margem bruta' in qn:
        return 'f.GrossMargin', True
    if 'quantidade' in qn:
        return 'f.BillingQuantity', False
    return 'f.NetAmount', False


def detect_dimension(qn: str) -> tuple[Optional[str], Optional[str], Tuple[str, ...]]:
    if 'organizacao de vendas' in qn or 'organização de vendas' in qn:
        return (
            'so.TSalesOrganization',
            'OrganizacaoVendas',
            ('JOIN dbo.D_SalesOrganization so ON f.NIDSalesOrganization = so.NIDSalesOrganization',),
        )
    if 'canal de distribuicao' in qn or 'canal de distribuição' in qn:
        return (
            'dc.TDistributionChannel',
            'CanalDistribuicao',
            ('JOIN dbo.D_DistributionChannel dc ON f.NIDDistributionChannel = dc.NIDDistributionChannel',),
        )
    if 'tipo de documento de faturacao' in qn or 'tipo de documento de faturação' in qn:
        return (
            'bdt.TBillingDocumentType',
            'TipoDocumentoFaturacao',
            ('JOIN dbo.D_BillingDocumentType bdt ON f.NIDBillingDocumentType = bdt.NIDBillingDocumentType',),
        )
    if 'regiao' in qn or 'região' in qn:
        return (
            'f.NIDRegion',
            'Regiao',
            ('JOIN dbo.D_Region r ON f.NIDRegion = r.NIDRegion',),
        )
    if 'pais' in qn or 'país' in qn:
        return (
            'c.TCountry',
            'Pais',
            ('JOIN dbo.D_Country c ON f.NIDCountry = c.NIDCountry',),
        )
    if 'marca' in qn:
        return (
            'pb.TProductBrand',
            'MarcaProduto',
            (
                'JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct',
                'JOIN dbo.D_ProductBrand pb ON p.NIDProductBrand = pb.NIDProductBrand',
            ),
        )
    if 'familia de produto' in qn or 'família de produto' in qn or 'familia' in qn:
        return (
            'pf.TProductFamily',
            'FamiliaProduto',
            (
                'JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct',
                'JOIN dbo.D_ProductFamily pf ON p.NIDProductFamily = pf.NIDProductFamily',
            ),
        )
    return None, None, ()


def classify_question(question: str) -> PeriodCompareSpec:
    qn = normalize(question)
    measure_expr, needs_additional = detect_measure(qn)
    dimension_expr, dimension_alias, joins = detect_dimension(qn)

    filters = ['f.BillingDocumentIsCancelled = 0']
    if needs_additional:
        filters.append('f.IsItAnAdditionalCalculatedRecord = 1')

    if ('por mes' in qn or 'por mês' in qn) and '2025' in qn and '2026' in qn:
        return PeriodCompareSpec(
            question=question,
            measure_expr=measure_expr,
            dimension_expr='((f.BillingDocumentDate / 100) % 100)',
            dimension_alias='Mes',
            joins=(),
            extra_filters=tuple(filters),
            comparison_shape='monthly_grid',
        )

    delta_mode = 'absolute' if ('variacao absoluta' in qn or 'variação absoluta' in qn or 'crescimento absoluto' in qn) else 'percent'
    return PeriodCompareSpec(
        question=question,
        measure_expr=measure_expr,
        dimension_expr=dimension_expr,
        dimension_alias=dimension_alias,
        joins=joins,
        extra_filters=tuple(filters + ['f.BillingDocumentDate / 10000 IN (2025, 2026)']),
        comparison_shape='delta_by_dimension',
        delta_mode=delta_mode,
    )


def build_sql(spec: PeriodCompareSpec) -> str:
    if spec.comparison_shape == 'monthly_grid':
        alias_2025 = 'ValorLiquido2025' if spec.measure_expr == 'f.NetAmount' else 'Valor2025'
        alias_2026 = 'ValorLiquido2026' if spec.measure_expr == 'f.NetAmount' else 'Valor2026'
        return f"""SELECT
    {spec.dimension_expr} AS Mes,
    SUM(CASE WHEN f.BillingDocumentDate / 10000 = 2025 THEN {spec.measure_expr} ELSE 0 END) AS {alias_2025},
    SUM(CASE WHEN f.BillingDocumentDate / 10000 = 2026 THEN {spec.measure_expr} ELSE 0 END) AS {alias_2026}
FROM dbo.F_Invoice f
WHERE {' AND '.join(spec.extra_filters)}
GROUP BY {spec.dimension_expr}
ORDER BY Mes ASC;"""

    if spec.dimension_expr is None or spec.dimension_alias is None:
        raise ValueError(f'Dimensão não suportada para period_compare: {spec.question}')

    if spec.dimension_expr == 'f.NIDRegion':
        delta_expr = (
            'g.Valor2026 - g.Valor2025'
            if spec.delta_mode == 'absolute'
            else '100.0 * (g.Valor2026 - g.Valor2025) / NULLIF(g.Valor2025, 0)'
        )
        delta_alias = 'VariacaoAbsoluta' if spec.delta_mode == 'absolute' else 'VariacaoPercentual'
        return f"""WITH grouped AS (
    SELECT
        f.NIDRegion,
        SUM(CASE WHEN f.BillingDocumentDate / 10000 = 2025 THEN {spec.measure_expr} ELSE 0 END) AS Valor2025,
        SUM(CASE WHEN f.BillingDocumentDate / 10000 = 2026 THEN {spec.measure_expr} ELSE 0 END) AS Valor2026
    FROM dbo.F_Invoice f
    WHERE {' AND '.join(spec.extra_filters)}
    GROUP BY f.NIDRegion
    HAVING SUM(CASE WHEN f.BillingDocumentDate / 10000 = 2025 THEN {spec.measure_expr} ELSE 0 END) <> 0
        OR SUM(CASE WHEN f.BillingDocumentDate / 10000 = 2026 THEN {spec.measure_expr} ELSE 0 END) <> 0
)
SELECT
    r.TRegion AS Regiao,
    {delta_expr} AS {delta_alias}
FROM grouped g
JOIN dbo.D_Region r ON r.NIDRegion = g.NIDRegion
ORDER BY {delta_alias} DESC, Regiao ASC;"""

    delta_alias = 'VariacaoAbsoluta' if spec.delta_mode == 'absolute' else 'VariacaoPercentual'
    delta_expr = (
        f"SUM(CASE WHEN f.BillingDocumentDate / 10000 = 2026 THEN {spec.measure_expr} ELSE 0 END) - "
        f"SUM(CASE WHEN f.BillingDocumentDate / 10000 = 2025 THEN {spec.measure_expr} ELSE 0 END)"
        if spec.delta_mode == 'absolute'
        else
        f"100.0 * (SUM(CASE WHEN f.BillingDocumentDate / 10000 = 2026 THEN {spec.measure_expr} ELSE 0 END) - "
        f"SUM(CASE WHEN f.BillingDocumentDate / 10000 = 2025 THEN {spec.measure_expr} ELSE 0 END)) / "
        f"NULLIF(SUM(CASE WHEN f.BillingDocumentDate / 10000 = 2025 THEN {spec.measure_expr} ELSE 0 END), 0)"
    )

    return f"""SELECT
    {spec.dimension_expr} AS {spec.dimension_alias},
    {delta_expr} AS {delta_alias}
FROM dbo.F_Invoice f
{' '.join(spec.joins)}
WHERE {' AND '.join(spec.extra_filters)}
GROUP BY {spec.dimension_expr}
HAVING SUM(CASE WHEN f.BillingDocumentDate / 10000 = 2025 THEN {spec.measure_expr} ELSE 0 END) <> 0
    OR SUM(CASE WHEN f.BillingDocumentDate / 10000 = 2026 THEN {spec.measure_expr} ELSE 0 END) <> 0
ORDER BY {delta_alias} DESC, {spec.dimension_alias} ASC;"""
