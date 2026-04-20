from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import re
import unicodedata

@dataclass
class LifecycleSpec:
    family: str = 'F17_lifecycle'
    entity: str = 'customer'      # customer | product
    operation: str = ''           # first_purchase_monthly_count | reactivated_count | reactivated_list | lost_count | lost_list | lost_list_by_dimension
    recent_days: Optional[int] = None
    inactivity_days: Optional[int] = None
    moving_months: Optional[int] = None
    dimension: Optional[str] = None
    original_question: str = ''

def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    text = re.sub(r'\s+', ' ', text)
    return text

def detect_entity(qn: str) -> str:
    if 'produto' in qn or 'produtos' in qn:
        return 'product'
    return 'customer'

def extract_days(qn: str, default_recent: Optional[int] = None, default_inactive: Optional[int] = None) -> tuple[Optional[int], Optional[int]]:
    recent = default_recent
    inactive = default_inactive

    m_recent = re.search(r'ultim[oa]s? (\d+) dias', qn)
    if m_recent:
        recent = int(m_recent.group(1))
    elif 'ultimo mes' in qn or 'ultimo mês' in qn:
        recent = 30

    for pattern in [
        r'apos pelo menos (\d+) dias sem (?:compras|vendas)',
        r'apos (\d+) dias sem (?:compras|vendas)',
        r'considerando (\d+) dias de inatividade anterior',
    ]:
        m = re.search(pattern, qn)
        if m:
            inactive = int(m.group(1))
            break

    return recent, inactive

def classify_lifecycle(question: str) -> LifecycleSpec:
    qn = normalize_text(question)
    entity = detect_entity(qn)
    dimension = 'sales_organization' if ('organizacao de vendas' in qn or 'organização de vendas' in qn) else None

    if 'primeira compra' in qn or 'primeira venda' in qn:
        return LifecycleSpec(
            entity=entity,
            operation='first_purchase_monthly_count',
            moving_months=12,
            original_question=question,
        )

    if 'reativad' in qn:
        recent_days, inactivity_days = extract_days(qn, default_recent=30, default_inactive=180)
        operation = 'reactivated_count'
        if qn.startswith(('quais os', 'quais as', 'quais sao os', 'quais são os', 'quais sao as', 'quais são as')):
            operation = 'reactivated_list'
        return LifecycleSpec(
            entity=entity,
            operation=operation,
            recent_days=recent_days,
            inactivity_days=inactivity_days,
            dimension=dimension,
            original_question=question,
        )

    if 'perdid' in qn:
        recent_days, _ = extract_days(qn, default_recent=90, default_inactive=None)
        operation = 'lost_count'
        if dimension:
            operation = 'lost_list_by_dimension'
        elif qn.startswith(('quais os', 'quais as', 'quais sao os', 'quais são os', 'quais sao as', 'quais são as')):
            operation = 'lost_list'
        return LifecycleSpec(
            entity=entity,
            operation=operation,
            recent_days=recent_days,
            dimension=dimension,
            original_question=question,
        )

    raise ValueError(f'Pergunta lifecycle não suportada: {question}')

def entity_column(entity: str) -> str:
    return 'f.NIDProduct' if entity == 'product' else 'f.NIDPayerParty'

def entity_alias(entity: str) -> str:
    return 'NIDProduct' if entity == 'product' else 'NIDPayerParty'

def build_lifecycle_sql(spec: LifecycleSpec) -> str:
    ent_col = entity_column(spec.entity)
    ent_alias = entity_alias(spec.entity)

    if spec.operation == 'first_purchase_monthly_count':
        return f"""
WITH first_activity AS (
    SELECT
        {ent_col} AS {ent_alias},
        MIN(f.MonthStart) AS FirstMonth
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentIsCancelled = 0
    GROUP BY {ent_col}
), last_12 AS (
    SELECT FirstMonth
    FROM first_activity
    WHERE FirstMonth >= DATE('2026-04-20', '-11 months', 'start of month')
)
SELECT
    FirstMonth AS Mes,
    COUNT(*) AS NumeroEntidadesPrimeiraAtividade
FROM last_12
GROUP BY FirstMonth
ORDER BY Mes ASC;
""".strip()

    if spec.operation in ('reactivated_count', 'reactivated_list'):
        recent = spec.recent_days or 30
        inactive = spec.inactivity_days or 180
        select_list = 'COUNT(*) AS NumeroEntidadesReativadas' if spec.operation == 'reactivated_count' else f'rc.{ent_alias}'
        order_by = '' if spec.operation == 'reactivated_count' else f'\nORDER BY rc.{ent_alias} ASC'
        return f"""
WITH recent_entities AS (
    SELECT DISTINCT
        {ent_col} AS {ent_alias}
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -{recent}, CAST(GETDATE() AS date)), 112))
),
inactive_window AS (
    SELECT DISTINCT
        {ent_col} AS {ent_alias}
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -{recent + inactive}, CAST(GETDATE() AS date)), 112))
      AND f.BillingDocumentDate < CONVERT(int, CONVERT(char(8), DATEADD(day, -{recent}, CAST(GETDATE() AS date)), 112))
)
SELECT
    {select_list}
FROM recent_entities rc
WHERE NOT EXISTS (
    SELECT 1
    FROM inactive_window iw
    WHERE iw.{ent_alias} = rc.{ent_alias}
){order_by};
""".strip()

    if spec.operation in ('lost_count', 'lost_list'):
        recent = spec.recent_days or 90
        select_list = 'COUNT(*) AS NumeroEntidadesPerdidas' if spec.operation == 'lost_count' else f'pe.{ent_alias}'
        order_by = '' if spec.operation == 'lost_count' else f'\nORDER BY pe.{ent_alias} ASC'
        return f"""
WITH prior_entities AS (
    SELECT DISTINCT
        {ent_col} AS {ent_alias}
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate < CONVERT(int, CONVERT(char(8), DATEADD(day, -{recent}, CAST(GETDATE() AS date)), 112))
),
recent_entities AS (
    SELECT DISTINCT
        {ent_col} AS {ent_alias}
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -{recent}, CAST(GETDATE() AS date)), 112))
)
SELECT
    {select_list}
FROM prior_entities pe
WHERE NOT EXISTS (
    SELECT 1
    FROM recent_entities re
    WHERE re.{ent_alias} = pe.{ent_alias}
){order_by};
""".strip()

    if spec.operation == 'lost_list_by_dimension':
        recent = spec.recent_days or 90
        return f"""
WITH historical_pairs AS (
    SELECT DISTINCT
        so.TSalesOrganization AS OrganizacaoVendas,
        {ent_col} AS {ent_alias}
    FROM dbo.F_Invoice f
    JOIN dbo.D_SalesOrganization so
      ON f.NIDSalesOrganization = so.NIDSalesOrganization
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate < CONVERT(int, CONVERT(char(8), DATEADD(day, -{recent}, CAST(GETDATE() AS date)), 112))
),
recent_pairs AS (
    SELECT DISTINCT
        so.TSalesOrganization AS OrganizacaoVendas,
        {ent_col} AS {ent_alias}
    FROM dbo.F_Invoice f
    JOIN dbo.D_SalesOrganization so
      ON f.NIDSalesOrganization = so.NIDSalesOrganization
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -{recent}, CAST(GETDATE() AS date)), 112))
)
SELECT
    hp.OrganizacaoVendas,
    hp.{ent_alias}
FROM historical_pairs hp
WHERE NOT EXISTS (
    SELECT 1
    FROM recent_pairs rp
    WHERE rp.OrganizacaoVendas = hp.OrganizacaoVendas
      AND rp.{ent_alias} = hp.{ent_alias}
)
ORDER BY hp.OrganizacaoVendas ASC, hp.{ent_alias} ASC;
""".strip()

    raise ValueError(spec)
