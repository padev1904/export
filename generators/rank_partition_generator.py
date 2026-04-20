from __future__ import annotations
from dataclasses import dataclass
import re


def normalize_q(q: str) -> str:
    x = q.lower().strip()
    rep = str.maketrans('áàâãéêíóôõúç', 'aaaaeeiooouc')
    return x.translate(rep)


PARTITIONS = {
    'pais': ('co.TCountry', ['JOIN D_Country co ON f.NIDCountry = co.NIDCountry'], 'Pais'),
    'organizacao de vendas': ('so.TSalesOrganization', ['JOIN D_SalesOrganization so ON f.NIDSalesOrganization = so.NIDSalesOrganization'], 'OrganizacaoVendas'),
    'familia de produto': ('pf.TProductFamily', ['JOIN D_Product p ON f.NIDProduct = p.NIDProduct', 'JOIN D_ProductFamily pf ON p.NIDProductFamily = pf.NIDProductFamily'], 'FamiliaProduto'),
    'canal de distribuicao': ('dc.TDistributionChannel', ['JOIN D_DistributionChannel dc ON f.NIDDistributionChannel = dc.NIDDistributionChannel'], 'CanalDistribuicao'),
    'mes': ('((f.BillingDocumentDate / 100) % 100)', [], 'Mes'),
    'marca': ('pb.TProductBrand', ['JOIN D_Product p ON f.NIDProduct = p.NIDProduct', 'JOIN D_ProductBrand pb ON p.NIDProductBrand = pb.NIDProductBrand'], 'MarcaProduto'),
}

ENTITIES = {
    'documentos de faturacao': ('f.BillingDocument', [], 'BillingDocument'),
    'grupos de preco de cliente': ('cpg.TCustomerPriceGroup', ['JOIN D_CustomerPriceGroup cpg ON f.NIDCustomerPriceGroup = cpg.NIDCustomerPriceGroup'], 'GrupoPrecoCliente'),
    'grupos de cliente': ('cg.TCustomerGroup', ['JOIN D_CustomerGroup cg ON f.NIDCustomerGroup = cg.NIDCustomerGroup'], 'GrupoCliente'),
    'pontos de expedicao': ('sp.TShippingPoint', ['JOIN D_ShippingPoint sp ON f.NIDShippingPoint = sp.NIDShippingPoint'], 'PontoExpedicao'),
    'organizacoes de vendas': ('so.TSalesOrganization', ['JOIN D_SalesOrganization so ON f.NIDSalesOrganization = so.NIDSalesOrganization'], 'OrganizacaoVendas'),
    'familias de produto': ('pf.TProductFamily', ['JOIN D_Product p ON f.NIDProduct = p.NIDProduct', 'JOIN D_ProductFamily pf ON p.NIDProductFamily = pf.NIDProductFamily'], 'FamiliaProduto'),
    'tipos de lista de precos': ('plt.TPriceListType', ['JOIN D_PriceListType plt ON f.NIDPriceListType = plt.NIDPriceListType'], 'TipoListaPrecos'),
    'clientes': ('c.TCustomer', ['JOIN D_Customer c ON f.NIDPayerParty = c.NIDCustomer'], 'Cliente'),
    'produtos': ('p.TProduct', ['JOIN D_Product p ON f.NIDProduct = p.NIDProduct'], 'Produto'),
    'marcas': ('pb.TProductBrand', ['JOIN D_Product p ON f.NIDProduct = p.NIDProduct', 'JOIN D_ProductBrand pb ON p.NIDProductBrand = pb.NIDProductBrand'], 'MarcaProduto'),
    'regioes': ('r.TRegion', ['JOIN D_Region r ON f.NIDRegion = r.NIDRegion'], 'Regiao'),
    'paises': ('co.TCountry', ['JOIN D_Country co ON f.NIDCountry = co.NIDCountry'], 'Pais'),
}


@dataclass
class Spec:
    family: str = 'F12_rank_within_partition'
    n: int = 0
    partition_keys: list | None = None
    entity_key: str = ''
    metric: str = ''
    years: tuple = (2026,)
    needs_valid_filter: bool = True


def detect_n(qn: str) -> int:
    m = re.search(r'quais sao os (\d+)|quais sao as (\d+)', qn)
    return int(next(g for g in m.groups() if g))


def alias_to_sql(alias: str):
    for expr, joins, al in PARTITIONS.values():
        if al == alias:
            return expr, joins
    for expr, joins, al in ENTITIES.values():
        if al == alias:
            return expr, joins
    raise KeyError(alias)


def dedupe(seq: list[str]) -> list[str]:
    out = []
    seen = set()
    for x in seq:
        if x not in seen:
            out.append(x)
            seen.add(x)
    return out


def classify(question: str) -> Spec:
    qn = normalize_q(question)
    spec = Spec(n=detect_n(qn), partition_keys=[])

    if 'dentro de cada familia de produto e por mes' in qn:
        spec.partition_keys = ['Mes', 'FamiliaProduto']
    elif 'dentro de cada pais' in qn:
        spec.partition_keys = ['Pais']
    elif 'em cada organizacao de vendas' in qn or 'dentro de cada organizacao de vendas' in qn:
        spec.partition_keys = ['OrganizacaoVendas']
    elif 'dentro de cada familia de produto' in qn:
        spec.partition_keys = ['FamiliaProduto']
    elif 'dentro de cada canal de distribuicao' in qn:
        spec.partition_keys = ['CanalDistribuicao']
    elif 'em cada mes' in qn or 'dentro de cada mes' in qn:
        spec.partition_keys = ['Mes']
    elif 'dentro de cada marca' in qn:
        spec.partition_keys = ['MarcaProduto']
    else:
        raise ValueError(f'Partition not detected: {question}')

    for phrase, alias in [
        ('documentos de faturacao', 'BillingDocument'),
        ('grupos de preco de cliente', 'GrupoPrecoCliente'),
        ('grupos de cliente', 'GrupoCliente'),
        ('pontos de expedicao', 'PontoExpedicao'),
        ('organizacoes de vendas', 'OrganizacaoVendas'),
        ('familias de produto', 'FamiliaProduto'),
        ('tipos de lista de precos', 'TipoListaPrecos'),
        ('clientes', 'Cliente'),
        ('produtos', 'Produto'),
        ('marcas', 'MarcaProduto'),
        ('regioes', 'Regiao'),
        ('paises', 'Pais'),
    ]:
        if phrase in qn:
            spec.entity_key = alias
            break
    if not spec.entity_key:
        raise ValueError(f'Entity not detected: {question}')

    if 'variacao percentual de valor liquido faturado' in qn:
        spec.metric = 'pct_change_net_amount'
        spec.years = (2025, 2026)
    elif 'crescimento absoluto de valor liquido faturado' in qn:
        spec.metric = 'growth_net_amount'
        spec.years = (2025, 2026)
    elif 'crescimento absoluto de quantidade faturada' in qn:
        spec.metric = 'growth_billing_quantity'
        spec.years = (2025, 2026)
    elif 'taxa de cancelamento de documentos' in qn:
        spec.metric = 'cancellation_rate'
        spec.needs_valid_filter = False
    elif 'valor liquido absoluto' in qn and 'linhas positivas e negativas' in qn:
        spec.metric = 'abs_document_net_amount_mixed_sign'
    elif 'diferenca entre preco de lista e valor liquido faturado' in qn:
        spec.metric = 'list_minus_net'
    elif 'preco medio liquido por unidade' in qn:
        spec.metric = 'avg_net_price_per_unit'
    elif 'desconto de quantidade' in qn:
        spec.metric = 'qty_discount'
    elif 'desconto promocional total' in qn:
        spec.metric = 'promo_discount_total'
    elif 'valor liquido faturado' in qn:
        spec.metric = 'net_amount'
    else:
        raise ValueError(f'Metric not detected: {question}')
    return spec


def build_sql(spec: Spec) -> str:
    part_exprs = []
    joins = []
    for alias in spec.partition_keys:
        expr, j = alias_to_sql(alias)
        part_exprs.append((expr, alias))
        joins.extend(j)
    ent_expr, ent_joins = alias_to_sql(spec.entity_key)
    joins.extend(ent_joins)
    joins = dedupe(joins)

    year_filter = 'f.BillingDocumentDate / 10000 = 2026' if spec.years == (2026,) else 'f.BillingDocumentDate / 10000 IN (2025, 2026)'
    filters = [year_filter]
    if spec.needs_valid_filter:
        filters.append('f.BillingDocumentIsCancelled = 0')
    where = ' AND\n      '.join(filters)

    part_select = ',\n        '.join([f'{expr} AS {alias}' for expr, alias in part_exprs])
    part_group = ', '.join([expr for expr, _ in part_exprs])
    part_cols = ', '.join([alias for _, alias in part_exprs])
    order_partition = ', '.join([f'r.{a}' for _, a in part_exprs])

    if spec.metric in {'net_amount', 'list_minus_net', 'qty_discount', 'promo_discount_total'}:
        metric_expr = {
            'net_amount': 'SUM(f.NetAmount)',
            'list_minus_net': 'SUM(f.ZLP1PriceList) - SUM(f.NetAmount)',
            'qty_discount': 'SUM(f.ZDQ1QtyDiscount)',
            'promo_discount_total': 'SUM(f.ZDPRPromotional + f.ZCPRPromotionalCampaign + f.REA1PromotionalDiscount)',
        }[spec.metric]
        metric_alias = {
            'net_amount': 'ValorLiquidoFaturado',
            'list_minus_net': 'DiferencaPrecoListaVsLiquido',
            'qty_discount': 'DescontoQuantidade',
            'promo_discount_total': 'DescontoPromocionalTotal',
        }[spec.metric]
        direction = 'ASC' if spec.metric in {'qty_discount', 'promo_discount_total'} else 'DESC'
        return f"""WITH grouped AS (
    SELECT
        {part_select},
        {ent_expr} AS {spec.entity_key},
        {metric_expr} AS {metric_alias}
    FROM F_Invoice f
    {' '.join(joins)}
    WHERE {where}
    GROUP BY {part_group}, {ent_expr}
), ranked AS (
    SELECT
        g.*,
        ROW_NUMBER() OVER (PARTITION BY {part_cols} ORDER BY {metric_alias} {direction}, {spec.entity_key}) AS rn
    FROM grouped g
)
SELECT
    {', '.join([f'r.{a}' for _, a in part_exprs])},
    r.{spec.entity_key},
    r.{metric_alias}
FROM ranked r
WHERE r.rn <= {spec.n}
ORDER BY {order_partition}, r.{metric_alias} {direction}, r.{spec.entity_key};"""

    if spec.metric == 'avg_net_price_per_unit':
        return f"""WITH grouped AS (
    SELECT
        {part_select},
        {ent_expr} AS {spec.entity_key},
        SUM(f.NetAmount) / NULLIF(SUM(f.BillingQuantity), 0) AS PrecoMedioLiquidoPorUnidade
    FROM F_Invoice f
    {' '.join(joins)}
    WHERE {where}
    GROUP BY {part_group}, {ent_expr}
    HAVING SUM(f.BillingQuantity) <> 0
), ranked AS (
    SELECT
        g.*,
        ROW_NUMBER() OVER (PARTITION BY {part_cols} ORDER BY PrecoMedioLiquidoPorUnidade DESC, {spec.entity_key}) AS rn
    FROM grouped g
)
SELECT
    {', '.join([f'r.{a}' for _, a in part_exprs])},
    r.{spec.entity_key},
    r.PrecoMedioLiquidoPorUnidade
FROM ranked r
WHERE r.rn <= {spec.n}
ORDER BY {order_partition}, r.PrecoMedioLiquidoPorUnidade DESC, r.{spec.entity_key};"""

    if spec.metric in {'growth_net_amount', 'growth_billing_quantity'}:
        metric_alias = 'CrescimentoAbsoluto' if spec.metric == 'growth_net_amount' else 'CrescimentoAbsolutoQuantidade'
        base_expr = 'f.NetAmount' if spec.metric == 'growth_net_amount' else 'f.BillingQuantity'
        return f"""WITH grouped AS (
    SELECT
        {part_select},
        {ent_expr} AS {spec.entity_key},
        SUM(CASE WHEN f.BillingDocumentDate / 10000 = 2026 THEN {base_expr} ELSE 0 END)
        - SUM(CASE WHEN f.BillingDocumentDate / 10000 = 2025 THEN {base_expr} ELSE 0 END) AS {metric_alias}
    FROM F_Invoice f
    {' '.join(joins)}
    WHERE {where}
    GROUP BY {part_group}, {ent_expr}
), ranked AS (
    SELECT
        g.*,
        ROW_NUMBER() OVER (PARTITION BY {part_cols} ORDER BY {metric_alias} DESC, {spec.entity_key}) AS rn
    FROM grouped g
)
SELECT
    {', '.join([f'r.{a}' for _, a in part_exprs])},
    r.{spec.entity_key},
    r.{metric_alias}
FROM ranked r
WHERE r.rn <= {spec.n}
ORDER BY {order_partition}, r.{metric_alias} DESC, r.{spec.entity_key};"""

    if spec.metric == 'pct_change_net_amount':
        return f"""WITH grouped AS (
    SELECT
        {part_select},
        {ent_expr} AS {spec.entity_key},
        SUM(CASE WHEN f.BillingDocumentDate / 10000 = 2025 THEN f.NetAmount ELSE 0 END) AS Valor2025,
        SUM(CASE WHEN f.BillingDocumentDate / 10000 = 2026 THEN f.NetAmount ELSE 0 END) AS Valor2026
    FROM F_Invoice f
    {' '.join(joins)}
    WHERE {where}
    GROUP BY {part_group}, {ent_expr}
), ranked AS (
    SELECT
        g.*,
        100.0 * (g.Valor2026 - g.Valor2025) / NULLIF(g.Valor2025, 0) AS VariacaoPercentual,
        ROW_NUMBER() OVER (
            PARTITION BY {part_cols}
            ORDER BY 100.0 * (g.Valor2026 - g.Valor2025) / NULLIF(g.Valor2025, 0) DESC, {spec.entity_key}
        ) AS rn
    FROM grouped g
)
SELECT
    {', '.join([f'r.{a}' for _, a in part_exprs])},
    r.{spec.entity_key},
    r.VariacaoPercentual
FROM ranked r
WHERE r.rn <= {spec.n}
ORDER BY {order_partition}, r.VariacaoPercentual DESC, r.{spec.entity_key};"""

    if spec.metric == 'cancellation_rate':
        return f"""WITH docs AS (
    SELECT
        ((f.BillingDocumentDate / 100) % 100) AS Mes,
        f.BillingDocument,
        f.NIDSalesOrganization,
        MAX(CASE WHEN f.BillingDocumentIsCancelled = 1 THEN 1 ELSE 0 END) AS DocumentoCancelado
    FROM F_Invoice f
    WHERE f.BillingDocumentDate / 10000 = 2026
    GROUP BY ((f.BillingDocumentDate / 100) % 100), f.BillingDocument, f.NIDSalesOrganization
), rates AS (
    SELECT
        d.Mes,
        so.TSalesOrganization AS OrganizacaoVendas,
        COUNT(*) AS TotalDocumentos,
        SUM(d.DocumentoCancelado) AS DocumentosCancelados,
        100.0 * SUM(d.DocumentoCancelado) / NULLIF(COUNT(*), 0) AS TaxaCancelamento
    FROM docs d
    JOIN D_SalesOrganization so ON d.NIDSalesOrganization = so.NIDSalesOrganization
    GROUP BY d.Mes, so.TSalesOrganization
), ranked AS (
    SELECT
        r.*,
        ROW_NUMBER() OVER (PARTITION BY r.Mes ORDER BY r.TaxaCancelamento DESC, r.TotalDocumentos DESC, r.OrganizacaoVendas) AS rn
    FROM rates r
)
SELECT
    r.Mes, r.OrganizacaoVendas, r.TotalDocumentos, r.DocumentosCancelados, r.TaxaCancelamento
FROM ranked r
WHERE r.rn <= {spec.n}
ORDER BY r.Mes, r.TaxaCancelamento DESC, r.TotalDocumentos DESC, r.OrganizacaoVendas;"""

    if spec.metric == 'abs_document_net_amount_mixed_sign':
        return f"""WITH docs AS (
    SELECT
        ((f.BillingDocumentDate / 100) % 100) AS Mes,
        f.BillingDocument,
        ABS(SUM(f.NetAmount)) AS ValorLiquidoTotal,
        MIN(f.NetAmount) AS ValorMinimoLinha,
        MAX(f.NetAmount) AS ValorMaximoLinha
    FROM F_Invoice f
    WHERE f.BillingDocumentDate / 10000 = 2026
      AND f.BillingDocumentIsCancelled = 0
    GROUP BY ((f.BillingDocumentDate / 100) % 100), f.BillingDocument
    HAVING MIN(f.NetAmount) < 0 AND MAX(f.NetAmount) > 0
), ranked AS (
    SELECT
        d.*,
        ROW_NUMBER() OVER (PARTITION BY d.Mes ORDER BY d.ValorLiquidoTotal DESC, d.BillingDocument) AS rn
    FROM docs d
)
SELECT
    r.Mes, r.BillingDocument, r.ValorLiquidoTotal, r.ValorMinimoLinha, r.ValorMaximoLinha
FROM ranked r
WHERE r.rn <= {spec.n}
ORDER BY r.Mes, r.ValorLiquidoTotal DESC, r.BillingDocument;"""

    raise ValueError(spec.metric)
