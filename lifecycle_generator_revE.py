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
        if qn.startswith(('quais os', 'quais as', 'quais sao os', 'quais são os', 'quais sao as', 'quais são as')):
            operation = 'lost_list_by_dimension' if dimension else 'lost_list'
        return LifecycleSpec(
            entity=entity,
            operation=operation,
            recent_days=recent_days,
            dimension=dimension,
            original_question=question,
        )

    raise ValueError(f'Pergunta não suportada pela família lifecycle revE: {question}')

def build_lifecycle_sql(spec: LifecycleSpec) -> str:
    """
    Guardrails semânticos desta família:

    1) Filtrar sempre faturação válida:
       f.BillingDocumentIsCancelled = 0

    2) "Reativado" segue a semântica operacional usada no benchmark:
       a entidade tem atividade na janela recente
       E não tem atividade na janela de inatividade imediatamente anterior.
       Nota: isto NÃO exige atividade anterior a essa janela de inatividade.

    3) "Perdido" usa default operacional universal:
       a entidade teve atividade antes do início da janela recente
       E não teve atividade na janela recente.

    4) Quando a pergunta é por organização de vendas, a semântica é por par
       (OrganizacaoVendas, Entidade), não apenas pela entidade global.

    5) O gerador emite T-SQL para SQL Server; não hardcode de QIDs.
    """
    entity_col = 'f.NIDPayerParty' if spec.entity == 'customer' else 'f.NIDProduct'
    entity_alias = 'NIDPayerParty' if spec.entity == 'customer' else 'NIDProduct'

    if spec.operation == 'first_purchase_monthly_count':
        metric_alias = 'ClientesNovos' if spec.entity == 'customer' else 'ProdutosNovos'
        return f"""WITH first_purchase AS (
    SELECT
        {entity_col} AS {entity_alias},
        MIN(f.BillingDocumentDate) AS PrimeiraCompraInt
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentIsCancelled = 0
    GROUP BY {entity_col}
)
SELECT
    DATEFROMPARTS(
        fp.PrimeiraCompraInt / 10000,
        (fp.PrimeiraCompraInt / 100) % 100,
        1
    ) AS Mes,
    COUNT(*) AS {metric_alias}
FROM first_purchase fp
WHERE fp.PrimeiraCompraInt >= CONVERT(int, CONVERT(char(8), DATEADD(day, 1, EOMONTH(GETDATE(), -{spec.moving_months})), 112))
GROUP BY DATEFROMPARTS(
    fp.PrimeiraCompraInt / 10000,
    (fp.PrimeiraCompraInt / 100) % 100,
    1
)
ORDER BY Mes ASC;"""

    if spec.dimension == 'sales_organization':
        join = "JOIN dbo.D_SalesOrganization so ON f.NIDSalesOrganization = so.NIDSalesOrganization"
        group_cols = "so.TSalesOrganization AS OrganizacaoVendas,\n        "
        reactivated_group_ref = "iw.OrganizacaoVendas = rc.OrganizacaoVendas AND "
        reactivated_group_out = "rc.OrganizacaoVendas,\n    "
        reactivated_count_group = "GROUP BY rc.OrganizacaoVendas\nORDER BY rc.OrganizacaoVendas ASC;"
        lost_group_ref = "r.OrganizacaoVendas = p.OrganizacaoVendas AND "
        lost_group_out = "p.OrganizacaoVendas,\n    "
        lost_count_group = "GROUP BY p.OrganizacaoVendas\nORDER BY p.OrganizacaoVendas ASC;"
        lost_order = f"ORDER BY p.OrganizacaoVendas ASC, p.{entity_alias} ASC;"
    else:
        join = ""
        group_cols = ""
        reactivated_group_ref = ""
        reactivated_group_out = ""
        reactivated_count_group = ""
        lost_group_ref = ""
        lost_group_out = ""
        lost_count_group = ""
        lost_order = f"ORDER BY p.{entity_alias} ASC;"

    if spec.operation.startswith('reactivated'):
        metric_alias = 'ClientesReativados' if spec.entity == 'customer' else 'ProdutosReativados'
        recent_days = spec.recent_days
        inactivity_days = spec.inactivity_days or 0

        sql = f"""WITH recent_entities AS (
    SELECT DISTINCT
        {group_cols}{entity_col} AS {entity_alias}
    FROM dbo.F_Invoice f
    {join}
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -{recent_days}, CAST(GETDATE() AS date)), 112))
),
inactive_window AS (
    SELECT DISTINCT
        {group_cols}{entity_col} AS {entity_alias}
    FROM dbo.F_Invoice f
    {join}
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -{recent_days + inactivity_days}, CAST(GETDATE() AS date)), 112))
      AND f.BillingDocumentDate < CONVERT(int, CONVERT(char(8), DATEADD(day, -{recent_days}, CAST(GETDATE() AS date)), 112))
)
SELECT
    {reactivated_group_out}"""

        if spec.operation == 'reactivated_count':
            if spec.dimension == 'sales_organization':
                sql += f"""COUNT(*) AS {metric_alias}
FROM recent_entities rc
WHERE NOT EXISTS (
    SELECT 1
    FROM inactive_window iw
    WHERE {reactivated_group_ref}iw.{entity_alias} = rc.{entity_alias}
)
{reactivated_count_group}"""
            else:
                sql += f"""COUNT(*) AS {metric_alias}
FROM recent_entities rc
WHERE NOT EXISTS (
    SELECT 1
    FROM inactive_window iw
    WHERE iw.{entity_alias} = rc.{entity_alias}
);"""
        else:
            prefix = reactivated_group_ref if spec.dimension == 'sales_organization' else ''
            order = ("rc.OrganizacaoVendas ASC, " if spec.dimension == 'sales_organization' else "") + f"rc.{entity_alias} ASC;"
            sql += f"""rc.{entity_alias}
FROM recent_entities rc
WHERE NOT EXISTS (
    SELECT 1
    FROM inactive_window iw
    WHERE {prefix}iw.{entity_alias} = rc.{entity_alias}
)
ORDER BY {order}"""
        return sql

    if spec.operation.startswith('lost'):
        recent_days = spec.recent_days
        sql = f"""WITH prior_entities AS (
    SELECT DISTINCT
        {group_cols}{entity_col} AS {entity_alias}
    FROM dbo.F_Invoice f
    {join}
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate < CONVERT(int, CONVERT(char(8), DATEADD(day, -{recent_days}, CAST(GETDATE() AS date)), 112))
),
recent_entities AS (
    SELECT DISTINCT
        {group_cols}{entity_col} AS {entity_alias}
    FROM dbo.F_Invoice f
    {join}
    WHERE f.BillingDocumentIsCancelled = 0
      AND f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, -{recent_days}, CAST(GETDATE() AS date)), 112))
)
SELECT
    {lost_group_out}"""

        metric_alias = 'ClientesPerdidos' if spec.entity == 'customer' else 'ProdutosPerdidos'

        if spec.operation == 'lost_count':
            if spec.dimension == 'sales_organization':
                sql += f"""COUNT(*) AS {metric_alias}
FROM prior_entities p
WHERE NOT EXISTS (
    SELECT 1
    FROM recent_entities r
    WHERE {lost_group_ref}r.{entity_alias} = p.{entity_alias}
)
{lost_count_group}"""
            else:
                sql += f"""COUNT(*) AS {metric_alias}
FROM prior_entities p
WHERE NOT EXISTS (
    SELECT 1
    FROM recent_entities r
    WHERE r.{entity_alias} = p.{entity_alias}
);"""
        elif spec.operation == 'lost_list_by_dimension':
            sql += f"""p.{entity_alias}
FROM prior_entities p
WHERE NOT EXISTS (
    SELECT 1
    FROM recent_entities r
    WHERE {lost_group_ref}r.{entity_alias} = p.{entity_alias}
)
{lost_order}"""
        else:
            sql += f"""p.{entity_alias}
FROM prior_entities p
WHERE NOT EXISTS (
    SELECT 1
    FROM recent_entities r
    WHERE r.{entity_alias} = p.{entity_alias}
)
{lost_order}"""
        return sql

    raise ValueError(f'Operação lifecycle não suportada: {spec.operation}')
