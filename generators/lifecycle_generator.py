from dataclasses import dataclass
import re

from sqlserver_patterns import int_date_expr, previous_days_window_predicates, trailing_days_predicate


@dataclass
class LifecycleSpec:
    entity: str = 'customer'
    operation: str = ''
    recent_days: int | None = None
    inactivity_days: int | None = None
    dimension: str | None = None


def normalize_text(text: str) -> str:
    q = text.lower().strip()
    for a, b in [('á','a'),('à','a'),('â','a'),('ã','a'),('é','e'),('ê','e'),('í','i'),('ó','o'),('ô','o'),('õ','o'),('ú','u'),('ç','c')]:
        q = q.replace(a, b)
    return ' '.join(q.split())


def detect_entity(q: str) -> str:
    return 'product' if 'produto' in q or 'produtos' in q else 'customer'


def extract_days(q: str, default_recent=None, default_inactive=None):
    recent = default_recent
    inactive = default_inactive
    m = re.search(r'ultim[oa]s? (\d+) dias', q)
    if m:
        recent = int(m.group(1))
    for pattern in [
        r'apos pelo menos (\d+) dias sem (?:compras|vendas|atividade)',
        r'apos (\d+) dias sem (?:compras|vendas|atividade)',
    ]:
        m2 = re.search(pattern, q)
        if m2:
            inactive = int(m2.group(1))
            break
    return recent, inactive


def classify_lifecycle(question: str) -> LifecycleSpec:
    q = normalize_text(question)
    entity = detect_entity(q)
    dimension = 'sales_organization' if 'organizacao de vendas' in q else None

    if 'primeira compra' in q or 'primeira venda' in q or 'clientes novos' in q or 'primeira vez' in q:
        return LifecycleSpec(entity=entity, operation='first_purchase_monthly_count', recent_days=12)

    if 'reativad' in q or 'voltaram a comprar' in q:
        recent, inactive = extract_days(q, 30, 180)
        return LifecycleSpec(entity=entity, operation='reactivated_count', recent_days=recent, inactivity_days=inactive, dimension=dimension)

    if 'sem vendas nos ultimos' in q or 'nao tiveram vendas nos ultimos' in q or 'sem faturacao nos 90 dias mais recentes' in q or 'sem qualquer venda nos ultimos' in q:
        return LifecycleSpec(entity=entity, operation='no_recent_sales_list', recent_days=90)

    if 'perdid' in q or 'perdemos' in q or 'bloco anterior de 90 dias' in q or '90 a 180 dias' in q:
        return LifecycleSpec(entity=entity, operation='lost_count' if not dimension else 'lost_list_by_dimension', recent_days=90, dimension=dimension)

    raise ValueError('Pergunta lifecycle nao suportada')


def entity_column(entity: str) -> str:
    return 'f.NIDProduct' if entity == 'product' else 'f.NIDPayerParty'


def entity_alias(entity: str) -> str:
    return 'NIDProduct' if entity == 'product' else 'NIDPayerParty'


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
        inactive = spec.inactivity_days or 180
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
      AND f.BillingDocumentDate >= {int_date_expr(f'DATEADD(day, -{recent + inactive}, CAST(GETDATE() AS date))')}
      AND f.BillingDocumentDate < {int_date_expr(f'DATEADD(day, -{recent}, CAST(GETDATE() AS date))')}
)
SELECT COUNT(*) AS NumeroEntidadesReativadas
FROM recent_entities rc
WHERE NOT EXISTS (
    SELECT 1 FROM inactive_window iw WHERE iw.{ent_alias} = rc.{ent_alias}
);
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

    if spec.operation == 'lost_list_by_dimension':
        recent = spec.recent_days or 90
        prev_lower, prev_upper = previous_days_window_predicates(recent)
        return f"""
WITH historical_pairs AS (
    SELECT DISTINCT so.TSalesOrganization AS OrganizacaoVendas, {ent_col} AS {ent_alias}
    FROM dbo.F_Invoice f
    JOIN dbo.D_SalesOrganization so ON f.NIDSalesOrganization = so.NIDSalesOrganization
    WHERE f.BillingDocumentIsCancelled = 0
      AND {prev_lower}
      AND {prev_upper}
),
recent_pairs AS (
    SELECT DISTINCT so.TSalesOrganization AS OrganizacaoVendas, {ent_col} AS {ent_alias}
    FROM dbo.F_Invoice f
    JOIN dbo.D_SalesOrganization so ON f.NIDSalesOrganization = so.NIDSalesOrganization
    WHERE f.BillingDocumentIsCancelled = 0
      AND {trailing_days_predicate(recent)}
)
SELECT hp.OrganizacaoVendas, hp.{ent_alias}
FROM historical_pairs hp
WHERE NOT EXISTS (
    SELECT 1 FROM recent_pairs rp WHERE rp.OrganizacaoVendas = hp.OrganizacaoVendas AND rp.{ent_alias} = hp.{ent_alias}
)
ORDER BY hp.OrganizacaoVendas ASC, hp.{ent_alias} ASC;
""".strip()

    raise ValueError('unsupported lifecycle operation')
