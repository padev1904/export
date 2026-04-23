from __future__ import annotations

from dataclasses import dataclass
import re

from sqlserver_patterns import (
    build_named_time_predicate,
    current_month_start_date_sql,
    dedupe_joins,
    explicit_year_predicate,
    int_date_expr,
    month_bucket_expr,
    next_month_start_date_sql,
    previous_days_window_predicates,
    same_month_last_year_start_date_sql,
    trailing_days_predicate,
)


def normalize_q(q: str) -> str:
    x = q.lower().strip()
    rep = str.maketrans('áàâãéêíóôõúç', 'aaaaeeiooouc')
    return x.translate(rep)


PARTITIONS = {
    'pais': ('co.TCountry', ['JOIN dbo.D_Country co ON f.NIDCountry = co.NIDCountry'], 'Pais'),
    'regiao': ('r.TRegion', ['JOIN dbo.D_Region r ON f.NIDRegion = r.NIDRegion'], 'Regiao'),
    'organizacao de vendas': ('so.TSalesOrganization', ['JOIN dbo.D_SalesOrganization so ON f.NIDSalesOrganization = so.NIDSalesOrganization'], 'OrganizacaoVendas'),
    'familia de produto': ('pf.TProductFamily', ['JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct', 'JOIN dbo.D_ProductFamily pf ON p.NIDProductFamily = pf.NIDProductFamily'], 'FamiliaProduto'),
    'canal de distribuicao': ('dc.TDistributionChannel', ['JOIN dbo.D_DistributionChannel dc ON f.NIDDistributionChannel = dc.NIDDistributionChannel'], 'CanalDistribuicao'),
    'canal': ('dc.TDistributionChannel', ['JOIN dbo.D_DistributionChannel dc ON f.NIDDistributionChannel = dc.NIDDistributionChannel'], 'CanalDistribuicao'),
    'mes': (month_bucket_expr(), [], 'Mes'),
    'marca': ('pb.TProductBrand', ['JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct', 'JOIN dbo.D_ProductBrand pb ON p.NIDProductBrand = pb.NIDProductBrand'], 'MarcaProduto'),
}

ENTITIES = {
    'documentos de faturacao': ('f.BillingDocument', [], 'BillingDocument'),
    'grupos de preco de cliente': ('cpg.TCustomerPriceGroup', ['JOIN dbo.D_CustomerPriceGroup cpg ON f.NIDCustomerPriceGroup = cpg.NIDCustomerPriceGroup'], 'GrupoPrecoCliente'),
    'grupos de cliente': ('cg.TCustomerGroup', ['JOIN dbo.D_CustomerGroup cg ON f.NIDCustomerGroup = cg.NIDCustomerGroup'], 'GrupoCliente'),
    'pontos de expedicao': ('sp.TShippingPoint', ['JOIN dbo.D_ShippingPoint sp ON f.NIDShippingPoint = sp.NIDShippingPoint'], 'PontoExpedicao'),
    'organizacoes de vendas': ('so.TSalesOrganization', ['JOIN dbo.D_SalesOrganization so ON f.NIDSalesOrganization = so.NIDSalesOrganization'], 'OrganizacaoVendas'),
    'familias de produto': ('pf.TProductFamily', ['JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct', 'JOIN dbo.D_ProductFamily pf ON p.NIDProductFamily = pf.NIDProductFamily'], 'FamiliaProduto'),
    'tipos de lista de precos': ('plt.TPriceListType', ['JOIN dbo.D_PriceListType plt ON f.NIDPriceListType = plt.NIDPriceListType'], 'TipoListaPrecos'),
    'clientes': ('c.TCustomer', ['JOIN dbo.D_Customer c ON f.NIDPayerParty = c.NIDCustomer'], 'Cliente'),
    'produtos': ('p.TProduct', ['JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct'], 'Produto'),
    'marcas': ('pb.TProductBrand', ['JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct', 'JOIN dbo.D_ProductBrand pb ON p.NIDProductBrand = pb.NIDProductBrand'], 'MarcaProduto'),
    'regioes': ('r.TRegion', ['JOIN dbo.D_Region r ON f.NIDRegion = r.NIDRegion'], 'Regiao'),
    'paises': ('co.TCountry', ['JOIN dbo.D_Country co ON f.NIDCountry = co.NIDCountry'], 'Pais'),
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
    requires_additional: bool = False
    time_scope: str = 'explicit_year'
    year: int | None = 2026


def detect_n(qn: str) -> int:
    patterns = [
        r'quais sao os (\d+)',
        r'quais sao as (\d+)',
        r'mostra o top (\d+)',
        r'quem sao os (\d+)',
        r'quais foram os (\d+)',
    ]
    for pattern in patterns:
        m = re.search(pattern, qn)
        if m:
            return int(m.group(1))
    return 0


def alias_to_sql(alias: str):
    for expr, joins, al in PARTITIONS.values():
        if al == alias:
            return expr, joins
    for expr, joins, al in ENTITIES.values():
        if al == alias:
            return expr, joins
    raise KeyError(alias)


def classify(question: str) -> Spec:
    qn = normalize_q(question)
    spec = Spec(n=detect_n(qn), partition_keys=[])

    if 'dentro de cada familia de produto e por mes' in qn or 'por mes dentro de cada familia de produto' in qn:
        spec.partition_keys = ['Mes', 'FamiliaProduto']
    elif 'dentro de cada organizacao de vendas e por mes' in qn or 'por mes dentro de cada organizacao de vendas' in qn:
        spec.partition_keys = ['Mes', 'OrganizacaoVendas']
    elif 'dentro de cada marca e por mes' in qn or 'por mes dentro de cada marca' in qn:
        spec.partition_keys = ['Mes', 'MarcaProduto']
    elif 'dentro de cada pais' in qn or 'por pais' in qn:
        spec.partition_keys = ['Pais']
    elif 'por regiao' in qn or 'para cada regiao' in qn:
        spec.partition_keys = ['Regiao']
    elif 'em cada organizacao de vendas' in qn or 'dentro de cada organizacao de vendas' in qn or 'por organizacao de vendas' in qn:
        spec.partition_keys = ['OrganizacaoVendas']
    elif 'dentro de cada familia de produto' in qn:
        spec.partition_keys = ['FamiliaProduto']
    elif 'dentro de cada canal de distribuicao' in qn or 'dentro de cada canal' in qn or 'por canal' in qn or 'para cada canal de distribuicao' in qn:
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

    year_match = re.search(r'em (20\d{2})', qn)
    if year_match:
        spec.time_scope = 'explicit_year'
        spec.year = int(year_match.group(1))
    elif 'entre o mes atual e o mesmo mes do ano anterior' in qn:
        spec.time_scope = 'current_month_vs_same_month_last_year'
        spec.year = None
    elif 'entre os ultimos 90 dias e os 90 dias anteriores' in qn:
        spec.time_scope = 'last_90_vs_previous_90'
        spec.year = None
    elif 'ano atual' in qn or 'ano corrente' in qn or 'este ano' in qn:
        spec.time_scope = 'current_year'
        spec.year = None
    elif 'ultimos 12 meses' in qn or 'ultimo ano movel' in qn:
        spec.time_scope = 'last_12_months'
        spec.year = None

    if 'registos adicionais calculados' in qn:
        spec.requires_additional = True

    if 'crescimento percentual de margem bruta' in qn:
        spec.metric = 'pct_growth_gross_margin_same_month_yoy'
        spec.requires_additional = True
    elif 'variacao percentual de valor liquido faturado' in qn:
        spec.metric = 'pct_change_net_amount'
        spec.years = (2025, 2026)
    elif 'crescimento absoluto de valor liquido faturado' in qn:
        spec.metric = 'growth_net_amount'
        spec.years = (2025, 2026)
    elif 'crescimento absoluto de quantidade faturada' in qn and spec.time_scope == 'last_90_vs_previous_90':
        spec.metric = 'growth_billing_quantity_last_90_vs_previous_90'
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
    elif 'peso liquido medio por unidade' in qn:
        spec.metric = 'net_weight_per_unit'
    elif 'desconto de quantidade' in qn:
        spec.metric = 'qty_discount'
    elif 'desconto promocional total' in qn:
        spec.metric = 'promo_discount_total'
    elif 'valor liquido faturado' in qn or 'faturacao' in qn or 'valor faturado' in qn or 'mais faturad' in qn or 'mais faturaram' in qn:
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
    joins = list(dedupe_joins(joins))

    part_select = ',\n        '.join([f'{expr} AS {alias}' for expr, alias in part_exprs])
    part_group = ', '.join([expr for expr, _ in part_exprs])
    part_cols = ', '.join([alias for _, alias in part_exprs])
    order_partition = ', '.join([f'r.{a}' for _, a in part_exprs])
    select_partition_cols = ',\n    '.join([f'r.{a}' for _, a in part_exprs])

    def build_where(default_time_scope: bool = True):
        filters = []
        if default_time_scope:
            if spec.metric in {'growth_net_amount', 'growth_billing_quantity', 'pct_change_net_amount'}:
                filters.append(f'CAST(f.BillingDocumentDate / 10000 AS INT) IN ({", ".join(str(y) for y in spec.years)})')
            elif spec.time_scope in {'explicit_year', 'current_year', 'last_12_months', 'last_6_months'}:
                filters.append(build_named_time_predicate(spec.time_scope, year=spec.year))
            else:
                raise ValueError(f'Unsupported default time scope for {spec.metric}: {spec.time_scope}')
        if spec.needs_valid_filter:
            filters.append('f.BillingDocumentIsCancelled = 0')
        if spec.requires_additional:
            filters.append('f.IsItAnAdditionalCalculatedRecord = 1')
        return ' AND\n      '.join(filters)

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
        where = build_where()
        return f"""WITH grouped AS (
    SELECT
        {part_select},
        {ent_expr} AS {spec.entity_key},
        {metric_expr} AS {metric_alias}
    FROM dbo.F_Invoice f
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
    {select_partition_cols},
    r.{spec.entity_key},
    r.{metric_alias}
FROM ranked r
WHERE r.rn <= {spec.n}
ORDER BY {order_partition}, r.{metric_alias} DESC, r.{spec.entity_key};"""

    if spec.metric == 'avg_net_price_per_unit':
        where = build_where()
        return f"""WITH grouped AS (
    SELECT
        {part_select},
        {ent_expr} AS {spec.entity_key},
        SUM(f.NetAmount) / NULLIF(SUM(f.BillingQuantity), 0) AS PrecoMedioLiquidoPorUnidade
    FROM dbo.F_Invoice f
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
    {select_partition_cols},
    r.{spec.entity_key},
    r.PrecoMedioLiquidoPorUnidade
FROM ranked r
WHERE r.rn <= {spec.n}
ORDER BY {order_partition}, r.PrecoMedioLiquidoPorUnidade DESC, r.{spec.entity_key};"""

    if spec.metric == 'net_weight_per_unit':
        where = build_where()
        return f"""WITH grouped AS (
    SELECT
        {part_select},
        {ent_expr} AS {spec.entity_key},
        SUM(f.ItemNetWeight) / NULLIF(SUM(f.BillingQuantity), 0) AS PesoLiquidoMedioPorUnidade
    FROM dbo.F_Invoice f
    {' '.join(joins)}
    WHERE {where}
    GROUP BY {part_group}, {ent_expr}
    HAVING SUM(f.BillingQuantity) <> 0
), ranked AS (
    SELECT
        g.*,
        ROW_NUMBER() OVER (PARTITION BY {part_cols} ORDER BY PesoLiquidoMedioPorUnidade DESC, {spec.entity_key}) AS rn
    FROM grouped g
)
SELECT
    {select_partition_cols},
    r.{spec.entity_key},
    r.PesoLiquidoMedioPorUnidade
FROM ranked r
WHERE r.rn <= {spec.n}
ORDER BY {order_partition}, r.PesoLiquidoMedioPorUnidade DESC, r.{spec.entity_key};"""

    if spec.metric in {'growth_net_amount', 'growth_billing_quantity'}:
        metric_alias = 'CrescimentoAbsoluto' if spec.metric == 'growth_net_amount' else 'CrescimentoAbsolutoQuantidade'
        base_expr = 'f.NetAmount' if spec.metric == 'growth_net_amount' else 'f.BillingQuantity'
        where = build_where()
        return f"""WITH grouped AS (
    SELECT
        {part_select},
        {ent_expr} AS {spec.entity_key},
        SUM(CASE WHEN {explicit_year_predicate(2026)} THEN {base_expr} ELSE 0 END)
        - SUM(CASE WHEN {explicit_year_predicate(2025)} THEN {base_expr} ELSE 0 END) AS {metric_alias}
    FROM dbo.F_Invoice f
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
    {select_partition_cols},
    r.{spec.entity_key},
    r.{metric_alias}
FROM ranked r
WHERE r.rn <= {spec.n}
ORDER BY {order_partition}, r.{metric_alias} DESC, r.{spec.entity_key};"""

    if spec.metric == 'growth_billing_quantity_last_90_vs_previous_90':
        current_90 = trailing_days_predicate(90)
        prev_90_start, prev_90_end = previous_days_window_predicates(90)
        filters = [trailing_days_predicate(180)]
        if spec.needs_valid_filter:
            filters.append('f.BillingDocumentIsCancelled = 0')
        where = ' AND\n      '.join(filters)
        return f"""WITH grouped AS (
    SELECT
        {part_select},
        {ent_expr} AS {spec.entity_key},
        SUM(CASE WHEN {current_90} THEN f.BillingQuantity ELSE 0 END) AS QuantidadeUltimos90Dias,
        SUM(CASE WHEN {prev_90_start} AND {prev_90_end} THEN f.BillingQuantity ELSE 0 END) AS Quantidade90DiasAnteriores,
        SUM(CASE WHEN {current_90} THEN f.BillingQuantity ELSE 0 END)
        - SUM(CASE WHEN {prev_90_start} AND {prev_90_end} THEN f.BillingQuantity ELSE 0 END) AS CrescimentoAbsolutoQuantidade
    FROM dbo.F_Invoice f
    {' '.join(joins)}
    WHERE {where}
    GROUP BY {part_group}, {ent_expr}
), ranked AS (
    SELECT
        g.*,
        ROW_NUMBER() OVER (PARTITION BY {part_cols} ORDER BY CrescimentoAbsolutoQuantidade DESC, {spec.entity_key}) AS rn
    FROM grouped g
)
SELECT
    {select_partition_cols},
    r.{spec.entity_key},
    r.QuantidadeUltimos90Dias,
    r.Quantidade90DiasAnteriores,
    r.CrescimentoAbsolutoQuantidade
FROM ranked r
WHERE r.rn <= {spec.n}
ORDER BY {order_partition}, r.CrescimentoAbsolutoQuantidade DESC, r.{spec.entity_key};"""

    if spec.metric == 'pct_change_net_amount':
        where = build_where()
        return f"""WITH grouped AS (
    SELECT
        {part_select},
        {ent_expr} AS {spec.entity_key},
        SUM(CASE WHEN {explicit_year_predicate(2025)} THEN f.NetAmount ELSE 0 END) AS Valor2025,
        SUM(CASE WHEN {explicit_year_predicate(2026)} THEN f.NetAmount ELSE 0 END) AS Valor2026
    FROM dbo.F_Invoice f
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
    {select_partition_cols},
    r.{spec.entity_key},
    r.VariacaoPercentual
FROM ranked r
WHERE r.rn <= {spec.n}
ORDER BY {order_partition}, r.VariacaoPercentual DESC, r.{spec.entity_key};"""

    if spec.metric == 'pct_growth_gross_margin_same_month_yoy':
        current_month_start = current_month_start_date_sql()
        next_month_start = next_month_start_date_sql()
        same_month_last_year_start = same_month_last_year_start_date_sql()
        same_month_last_year_next = f'DATEADD(month, 1, {same_month_last_year_start})'
        filters = [
            f'f.BillingDocumentDate >= {int_date_expr(same_month_last_year_start)}',
            f'f.BillingDocumentDate < {int_date_expr(next_month_start)}',
        ]
        if spec.needs_valid_filter:
            filters.append('f.BillingDocumentIsCancelled = 0')
        if spec.requires_additional:
            filters.append('f.IsItAnAdditionalCalculatedRecord = 1')
        where = ' AND\n      '.join(filters)
        return f"""WITH grouped AS (
    SELECT
        {part_select},
        {ent_expr} AS {spec.entity_key},
        SUM(CASE WHEN f.BillingDocumentDate >= {int_date_expr(current_month_start)} AND f.BillingDocumentDate < {int_date_expr(next_month_start)} THEN f.GrossMargin ELSE 0 END) AS MargemBrutaMesAtual,
        SUM(CASE WHEN f.BillingDocumentDate >= {int_date_expr(same_month_last_year_start)} AND f.BillingDocumentDate < {int_date_expr(same_month_last_year_next)} THEN f.GrossMargin ELSE 0 END) AS MargemBrutaMesmoMesAnoAnterior
    FROM dbo.F_Invoice f
    {' '.join(joins)}
    WHERE {where}
    GROUP BY {part_group}, {ent_expr}
), filtered AS (
    SELECT *
    FROM grouped
    WHERE MargemBrutaMesAtual <> 0 OR MargemBrutaMesmoMesAnoAnterior <> 0
), ranked AS (
    SELECT
        g.*,
        100.0 * (g.MargemBrutaMesAtual - g.MargemBrutaMesmoMesAnoAnterior) / NULLIF(g.MargemBrutaMesmoMesAnoAnterior, 0) AS CrescimentoPercentualMargemBruta,
        ROW_NUMBER() OVER (
            PARTITION BY {part_cols}
            ORDER BY 100.0 * (g.MargemBrutaMesAtual - g.MargemBrutaMesmoMesAnoAnterior) / NULLIF(g.MargemBrutaMesmoMesAnoAnterior, 0) DESC, {spec.entity_key}
        ) AS rn
    FROM filtered g
)
SELECT
    {select_partition_cols},
    r.{spec.entity_key},
    r.MargemBrutaMesAtual,
    r.MargemBrutaMesmoMesAnoAnterior,
    r.CrescimentoPercentualMargemBruta
FROM ranked r
WHERE r.rn <= {spec.n}
ORDER BY {order_partition}, r.CrescimentoPercentualMargemBruta DESC, r.{spec.entity_key};"""

    if spec.metric == 'cancellation_rate':
        return f"""WITH docs AS (
    SELECT
        {month_bucket_expr()} AS Mes,
        f.BillingDocument,
        f.NIDSalesOrganization,
        MAX(CASE WHEN f.BillingDocumentIsCancelled = 1 THEN 1 ELSE 0 END) AS DocumentoCancelado
    FROM dbo.F_Invoice f
    WHERE {explicit_year_predicate(2026)}
    GROUP BY {month_bucket_expr()}, f.BillingDocument, f.NIDSalesOrganization
), rates AS (
    SELECT
        d.Mes,
        so.TSalesOrganization AS OrganizacaoVendas,
        COUNT(*) AS TotalDocumentos,
        SUM(d.DocumentoCancelado) AS DocumentosCancelados,
        100.0 * SUM(d.DocumentoCancelado) / NULLIF(COUNT(*), 0) AS TaxaCancelamento
    FROM docs d
    JOIN dbo.D_SalesOrganization so ON d.NIDSalesOrganization = so.NIDSalesOrganization
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
        where = build_where()
        filter_sql = f'WHERE r.rn <= {spec.n}\n' if spec.n > 0 else ''
        return f"""WITH docs AS (
    SELECT
        {part_select},
        f.BillingDocument,
        ABS(SUM(f.NetAmount)) AS ValorLiquidoAbsolutoTotal,
        MIN(f.NetAmount) AS ValorMinimoLinha,
        MAX(f.NetAmount) AS ValorMaximoLinha
    FROM dbo.F_Invoice f
    {' '.join(joins)}
    WHERE {where}
    GROUP BY {part_group}, f.BillingDocument
    HAVING MIN(f.NetAmount) < 0 AND MAX(f.NetAmount) > 0
), ranked AS (
    SELECT
        d.*,
        ROW_NUMBER() OVER (PARTITION BY {part_cols} ORDER BY d.ValorLiquidoAbsolutoTotal DESC, d.BillingDocument) AS rn
    FROM docs d
)
SELECT
    {select_partition_cols},
    r.BillingDocument,
    r.ValorLiquidoAbsolutoTotal,
    r.ValorMinimoLinha,
    r.ValorMaximoLinha
FROM ranked r
{filter_sql}ORDER BY {order_partition}, r.ValorLiquidoAbsolutoTotal DESC, r.BillingDocument;"""

    raise ValueError(spec.metric)
