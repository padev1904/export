from __future__ import annotations

from dataclasses import dataclass
import re


def normalize_q(q: str) -> str:
    x = q.lower().strip()
    rep = str.maketrans('áàâãéêíóôõúç', 'aaaaeeiooouc')
    return ' '.join(x.translate(rep).split())


ENTITY_MAP = [
    (
        'organizacoes de vendas',
        (
            'f.NIDSalesOrganization',
            'so.TSalesOrganization',
            ['JOIN dbo.D_SalesOrganization so ON d.EntityKey = so.NIDSalesOrganization'],
            'OrganizacaoVendas',
        ),
    ),
    (
        'organizacao de vendas',
        (
            'f.NIDSalesOrganization',
            'so.TSalesOrganization',
            ['JOIN dbo.D_SalesOrganization so ON d.EntityKey = so.NIDSalesOrganization'],
            'OrganizacaoVendas',
        ),
    ),
    (
        'canais de distribuicao',
        (
            'f.NIDDistributionChannel',
            'dc.TDistributionChannel',
            ['JOIN dbo.D_DistributionChannel dc ON d.EntityKey = dc.NIDDistributionChannel'],
            'CanalDistribuicao',
        ),
    ),
    (
        'canal de distribuicao',
        (
            'f.NIDDistributionChannel',
            'dc.TDistributionChannel',
            ['JOIN dbo.D_DistributionChannel dc ON d.EntityKey = dc.NIDDistributionChannel'],
            'CanalDistribuicao',
        ),
    ),
    (
        'clientes',
        (
            'f.NIDPayerParty',
            'c.TCustomer',
            ['JOIN dbo.D_Customer c ON d.EntityKey = c.NIDCustomer'],
            'Cliente',
        ),
    ),
    (
        'produtos',
        (
            'f.NIDProduct',
            'p.TProduct',
            ['JOIN dbo.D_Product p ON d.EntityKey = p.NIDProduct'],
            'Produto',
        ),
    ),
    (
        'paises',
        (
            'f.NIDCountry',
            'co.TCountry',
            ['JOIN dbo.D_Country co ON d.EntityKey = co.NIDCountry'],
            'Pais',
        ),
    ),
    (
        'pais',
        (
            'f.NIDCountry',
            'co.TCountry',
            ['JOIN dbo.D_Country co ON d.EntityKey = co.NIDCountry'],
            'Pais',
        ),
    ),
]


@dataclass
class Spec:
    family: str = 'F05_distinct_count'
    mode: str = 'grouped'
    entity_key_expr: str = ''
    entity_label_expr: str = ''
    joins: list[str] | None = None
    entity_alias: str = ''
    count_alias: str = 'NumeroDocumentos'
    threshold: int | None = None
    top_n: int | None = None
    year: int = 2026


def detect_year(qn: str) -> int:
    if 'ano atual' in qn:
        return 2026
    m = re.search(r'(20\d{2})', qn)
    return int(m.group(1)) if m else 2026


def classify(question: str) -> Spec:
    qn = normalize_q(question)

    entity = None
    for phrase, values in ENTITY_MAP:
        if phrase in qn:
            entity = values
            break
    if entity is None:
        raise ValueError(f'Entity not detected: {question}')

    entity_key_expr, entity_label_expr, joins, entity_alias = entity
    spec = Spec(
        entity_key_expr=entity_key_expr,
        entity_label_expr=entity_label_expr,
        joins=joins,
        entity_alias=entity_alias,
        year=detect_year(qn),
    )

    if 'com mais de ' in qn:
        spec.mode = 'threshold'
        spec.threshold = int(re.search(r'com mais de (\d+)', qn).group(1))
        spec.count_alias = 'NumeroDocumentosFaturacao'
        return spec

    if 'presentes em mais de ' in qn:
        spec.mode = 'threshold'
        spec.threshold = int(re.search(r'presentes em mais de (\d+)', qn).group(1))
        spec.count_alias = 'NumeroDocumentosFaturacao'
        return spec

    m = re.search(r'quais sao (?:os|as) (\d+)', qn)
    if m and 'maior numero de documentos de faturacao distintos' in qn:
        spec.mode = 'top_n'
        spec.top_n = int(m.group(1))
        return spec

    spec.mode = 'grouped'
    return spec


def build_sql(spec: Spec) -> str:
    prefix = f'SELECT TOP ({spec.top_n})' if spec.mode == 'top_n' else 'SELECT'

    sql = f"""WITH distinct_docs AS (
    SELECT DISTINCT
        f.BillingDocument,
        {spec.entity_key_expr} AS EntityKey
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentDate / 10000 = {spec.year}
      AND f.BillingDocumentIsCancelled = 0
)
{prefix}
    {spec.entity_label_expr} AS {spec.entity_alias},
    COUNT(*) AS {spec.count_alias}
FROM distinct_docs d
{' '.join(spec.joins or [])}
GROUP BY {spec.entity_label_expr}"""

    if spec.mode == 'threshold':
        sql += f"\nHAVING COUNT(*) > {spec.threshold}"

    sql += f"\nORDER BY {spec.count_alias} DESC, {spec.entity_alias};"
    return sql
