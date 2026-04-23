from dataclasses import dataclass
import re

from sqlserver_patterns import int_date_expr, previous_days_window_predicates, trailing_days_predicate


@dataclass
class LifecycleSpec:
    entity: str = 'customer'
    operation: str = ''
    recent_days: int | None = None
    inactivity_days: int | None = None
    lookback_days: int | None = None
    dimension: str | None = None


DIMENSIONS = {
    'sales_organization': {
        'nid': 'NIDSalesOrganization',
        'table': 'dbo.D_SalesOrganization',
        'pk': 'NIDSalesOrganization',
        'text': 'TSalesOrganization',
        'alias': 'OrganizacaoVendas',
    },
    'distribution_channel': {
        'nid': 'NIDDistributionChannel',
        'table': 'dbo.D_DistributionChannel',
        'pk': 'NIDDistributionChannel',
        'text': 'TDistributionChannel',
        'alias': 'CanalDistribuicao',
    },
}


def normalize_text(text: str) -> str:
    q = text.lower().strip()
    for a, b in [('á','a'),('à','a'),('â','a'),('ã','a'),('é','e'),('ê','e'),('í','i'),('ó','o'),('ô','o'),('õ','o'),('ú','u'),('ç','c')]:
        q = q.replace(a, b)
    return ' '.join(q.split())


def detect_entity(q: str) -> str:
    return 'product' if 'produto' in q or 'produtos' in q else 'customer'


def detect_dimension(q: str) -> str | None:
    if 'organizacao de vendas' in q:
        return 'sales_organization'
    if 'canal de distribuicao' in q:
        return 'distribution_channel'
    return None


def extract_recent_days(q: str, default: int) -> int:
    m = re.search(r'ultim[oa]s? (\d+) dias', q)
    return int(m.group(1)) if m else default


def extract_inactivity_days(q: str, default: int) -> int:
    for pattern in [
        r'apos pelo menos (\d+) dias sem (?:compras|vendas|atividade)',
        r'depois de (\d+) dias sem (?:compras|vendas|atividade)',
        r'considerando (\d+) dias de inatividade anterior',
    ]:
        m = re.search(pattern, q)
        if m:
            return int(m.group(1))
    return default


def extract_lookback_days(q: str, default: int) -> int:
    for pattern in [
        r'tinham compras nos (\d+) dias anteriores',
        r'compras nos (\d+) dias anteriores a esse periodo',
    ]:
        m = re.search(pattern, q)
        if m:
            return int(m.group(1))
    return default


def classify_lifecycle(question: str) -> LifecycleSpec:
    q = normalize_text(question)
    entity = detect_entity(q)
    dimension = detect_dimension(q)

    if 'primeira compra' in q or 'primeira venda' in q or 'clientes novos' in q or 'primeira vez' in q:
        return LifecycleSpec(entity=entity, operation='first_purchase_monthly_count', recent_days=12)

    if 'reativad' in q or 'voltaram a comprar' in q:
        recent = extract_recent_days(q, 30)
        inactivity = extract_inactivity_days(q, 180)
        if dimension:
            return LifecycleSpec(entity=entity, operation='reactivated_list_by_dimension', recent_days=recent, inactivity_days=inactivity, dimension=dimension)
        return LifecycleSpec(entity=entity, operation='reactivated_count', recent_days=recent, inactivity_days=inactivity)

    if 'sem vendas nos ultimos' in q or 'nao tiveram vendas nos ultimos' in q or 'sem faturacao nos 90 dias mais recentes' in q or 'sem qualquer venda nos ultimos' in q:
        return LifecycleSpec(entity=entity, operation='no_recent_sales_list', recent_days=90)

    if 'perdid' in q or 'perdemos' in q or 'bloco anterior de 90 dias' in q or '90 a 180 dias' in q:
        recent = extract_recent_days(q, 90)
        if dimension:
            lookback = extract_lookback_days(q, recent)
            return LifecycleSpec(entity=entity, operation='lost_list_by_dimension_windowed', recent_days=recent, lookback_days=lookback, dimension=dimension)
        return LifecycleSpec(entity=entity, operation='lost_count', recent_days=recent, lookback_days=recent)

    raise ValueError('Pergunta lifecycle nao suportada')


def entity_column(entity: str) -> str:
    return 'f.NIDProduct' if entity == 'product' else 'f.NIDPayerParty'


def entity_alias(entity: str) -> str:
    return 'NIDProduct' if entity == 'product' else 'NIDPayerParty'


def entity_dimension_table(entity: str) -> tuple[str, str, str, str]:
    if entity == 'product':
        return 'dbo.D_Product', 'NIDProduct', 'TProduct', 'Produto'
    return 'dbo.D_Customer', 'NIDCustomer', 'TCustomer', 'Cliente'


def build_lifecycle_sql(spec: LifecycleSpec) -> str:
    ent_col = entity_column(spec.entity)
    ent_alias = entity_alias(spec.entity)

    if spec.operation == 'first_purchase_monthly_count':
        return f"""
WITH first_purchase AS (
    SELECT
        {ent_col} AS {ent_alias},
        MIN(f.BillingDocumentDate) AS PrimeiraCompraInt
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentIsCancelled = 0
    GROUP BY {ent_col}
)
SELECT
    DATEFROMPARTS(fp.PrimeiraCompraInt / 10000, (fp.PrimeiraCompraInt / 100) % 100, 1) AS Mes,
    COUNT(*) AS NumeroEntidadesPrimeiraAtividade
FROM first_purchase fp
WHERE fp.PrimeiraCompraInt >= {int_date_expr('DATEADD(day, 1, EOMONTH(GETDATE(), -12))')}
GROUP BY DATEFROMPARTS(fp.PrimeiraCompraInt / 10000, (fp.PrimeiraCompraInt / 100) % 100, 1)
ORDER BY Mes ASC;
""".strip()

    if spec.operation == 'reactivated_count':
        recent = spec.recent_days or 30
        inactivity = spec.inactivity_days or 180
        return f"""
WITH recent_entities AS (
    SELECT DISTINCT {ent_col} AS {ent_alias}
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentIsCancelled = 0
      AND {trailing_days_predicate(recent)}
),
inactive_window AS (
    SELECT DISTINCT {ent_col} AS {ent_alias}
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= {int_date_expr(f'DATEADD(day, -{recent + inactivity}, CAST(GETDATE() AS date))')}
      AND f.BillingDocumentDate < {int_date_expr(f'DATEADD(day, -{recent}, CAST(GETDATE() AS date))')}
)
SELECT COUNT(*) AS NumeroEntidadesReativadas
FROM recent_entities rc
WHERE NOT EXISTS (
    SELECT 1 FROM inactive_window iw WHERE iw.{ent_alias} = rc.{ent_alias}
);
""".strip()

    if spec.operation == 'reactivated_list_by_dimension':
        recent = spec.recent_days or 90
        inactivity = spec.inactivity_days or 180
        dim = DIMENSIONS[spec.dimension]
        ent_table, ent_pk, ent_text, ent_label = entity_dimension_table(spec.entity)
        return f"""
WITH recent_pairs AS (
    SELECT DISTINCT
        f.{dim['nid']} AS {dim['nid']},
        {ent_col} AS {ent_alias}
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentIsCancelled = 0
      AND {trailing_days_predicate(recent)}
),
inactive_pairs AS (
    SELECT DISTINCT
        f.{dim['nid']} AS {dim['nid']},
        {ent_col} AS {ent_alias}
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= {int_date_expr(f'DATEADD(day, -{recent + inactivity}, CAST(GETDATE() AS date))')}
      AND f.BillingDocumentDate < {int_date_expr(f'DATEADD(day, -{recent}, CAST(GETDATE() AS date))')}
),
reactivated_pairs AS (
    SELECT rp.{dim['nid']}, rp.{ent_alias}
    FROM recent_pairs rp
    WHERE NOT EXISTS (
        SELECT 1
        FROM inactive_pairs iw
        WHERE iw.{dim['nid']} = rp.{dim['nid']}
          AND iw.{ent_alias} = rp.{ent_alias}
    )
)
SELECT
    d.{dim['text']} AS {dim['alias']},
    e.{ent_text} AS {ent_label}
FROM reactivated_pairs rp
JOIN {dim['table']} d ON d.{dim['pk']} = rp.{dim['nid']}
JOIN {ent_table} e ON e.{ent_pk} = rp.{ent_alias}
ORDER BY {dim['alias']} ASC, {ent_label} ASC;
""".strip()

    if spec.operation == 'lost_count':
        recent = spec.recent_days or 90
        prev_lower, prev_upper = previous_days_window_predicates(recent)
        return f"""
WITH previous_window AS (
    SELECT DISTINCT {ent_col} AS {ent_alias}
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentIsCancelled = 0
      AND {prev_lower}
      AND {prev_upper}
),
current_window AS (
    SELECT DISTINCT {ent_col} AS {ent_alias}
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentIsCancelled = 0
      AND {trailing_days_predicate(recent)}
)
SELECT COUNT(*) AS NumeroEntidadesPerdidas
FROM previous_window p
WHERE NOT EXISTS (
    SELECT 1 FROM current_window c WHERE c.{ent_alias} = p.{ent_alias}
);
""".strip()

    if spec.operation == 'no_recent_sales_list':
        recent = spec.recent_days or 90
        return f"""
WITH recent_products AS (
    SELECT DISTINCT f.NIDProduct
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentIsCancelled = 0
      AND {trailing_days_predicate(recent)}
)
SELECT p.TProduct AS Produto
FROM dbo.D_Product p
LEFT JOIN recent_products rp ON rp.NIDProduct = p.NIDProduct
WHERE rp.NIDProduct IS NULL
ORDER BY p.TProduct ASC;
""".strip()

    if spec.operation == 'lost_list_by_dimension_windowed':
        recent = spec.recent_days or 90
        lookback = spec.lookback_days or recent
        dim = DIMENSIONS[spec.dimension]
        ent_table, ent_pk, ent_text, ent_label = entity_dimension_table(spec.entity)
        return f"""
WITH history_pairs AS (
    SELECT DISTINCT
        f.{dim['nid']} AS {dim['nid']},
        {ent_col} AS {ent_alias}
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= {int_date_expr(f'DATEADD(day, -{recent + lookback}, CAST(GETDATE() AS date))')}
      AND f.BillingDocumentDate < {int_date_expr(f'DATEADD(day, -{recent}, CAST(GETDATE() AS date))')}
),
recent_pairs AS (
    SELECT DISTINCT
        f.{dim['nid']} AS {dim['nid']},
        {ent_col} AS {ent_alias}
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentIsCancelled = 0
      AND {trailing_days_predicate(recent)}
),
lost_pairs AS (
    SELECT hp.{dim['nid']}, hp.{ent_alias}
    FROM history_pairs hp
    WHERE NOT EXISTS (
        SELECT 1
        FROM recent_pairs rp
        WHERE rp.{dim['nid']} = hp.{dim['nid']}
          AND rp.{ent_alias} = hp.{ent_alias}
    )
)
SELECT
    d.{dim['text']} AS {dim['alias']},
    e.{ent_text} AS {ent_label}
FROM lost_pairs lp
JOIN {dim['table']} d ON d.{dim['pk']} = lp.{dim['nid']}
JOIN {ent_table} e ON e.{ent_pk} = lp.{ent_alias}
ORDER BY {dim['alias']} ASC, {ent_label} ASC;
""".strip()

    raise ValueError('unsupported lifecycle operation')
