from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import re

from sqlserver_patterns import explicit_year_predicate, month_bucket_expr


@dataclass
class CancellationSpec:
    family: str
    operation: str
    year: Optional[int] = 2026
    time_scope: str = 'explicit_year'
    dimension: Optional[str] = None
    secondary_dimension: Optional[str] = None
    top_n: Optional[int] = None
    include_counts: bool = True
    original_question: Optional[str] = None


DIMENSIONS = {
    'billing_document_type': {'nid':'NIDBillingDocumentType','table':'dbo.D_BillingDocumentType','pk':'NIDBillingDocumentType','text':'TBillingDocumentType','alias':'TipoDocumentoFaturacao'},
    'distribution_channel': {'nid':'NIDDistributionChannel','table':'dbo.D_DistributionChannel','pk':'NIDDistributionChannel','text':'TDistributionChannel','alias':'CanalDistribuicao'},
    'sales_organization': {'nid':'NIDSalesOrganization','table':'dbo.D_SalesOrganization','pk':'NIDSalesOrganization','text':'TSalesOrganization','alias':'OrganizacaoVendas'},
    'country': {'nid':'NIDCountry','table':'dbo.D_Country','pk':'NIDCountry','text':'TCountry','alias':'Pais'},
}


def normalize_q(q:str)->str:
    x=q.lower().strip()
    for a,b in [('á','a'),('à','a'),('â','a'),('ã','a'),('é','e'),('ê','e'),('í','i'),('ó','o'),('ô','o'),('õ','o'),('ú','u'),('ç','c')]:
        x=x.replace(a,b)
    return ' '.join(x.split())


def detect_year(qn:str)->tuple[Optional[int], str]:
    if 'ano atual' in qn or 'ano corrente' in qn or 'este ano' in qn:
        return None, 'current_year'
    m=re.search(r'(20\d{2})', qn)
    return (int(m.group(1)), 'explicit_year') if m else (2026, 'explicit_year')


def detect_top_n(qn:str)->Optional[int]:
    m=re.search(r'quais sao os (\d+)', qn)
    return int(m.group(1)) if m else None


def detect_dims(qn:str):
    candidates=[]
    patterns=[
        ('billing_document_type',['tipo de documento de faturacao','tipos de documento de faturacao']),
        ('product_brand',['marca','marcas']),
        ('distribution_channel',['canal de distribuicao','canais de distribuicao']),
        ('sales_organization',['organizacao de vendas','organizacoes de vendas']),
        ('country',['pais'])
    ]
    for key, pats in patterns:
        pos_list=[qn.find(p) for p in pats if qn.find(p)!=-1]
        if pos_list:
            candidates.append((min(pos_list), key))
    candidates=sorted(candidates, key=lambda x: x[0])
    primary=candidates[0][1] if len(candidates)>=1 else None
    secondary=candidates[1][1] if len(candidates)>=2 else None
    return primary, secondary


def year_filter_sql(spec: CancellationSpec) -> str:
    if spec.time_scope == 'current_year':
        return 'f.BillingDocumentDate / 10000 = YEAR(GETDATE())'
    return explicit_year_predicate(spec.year or 2026)


def quarter_bucket_expr(column: str = 'f.BillingDocumentDate') -> str:
    return f"CAST((((CAST(({column} / 100) AS INT) % 100) - 1) / 3) + 1 AS INT)"


def classify_question(question:str)->CancellationSpec:
    qn=normalize_q(question)
    year, time_scope = detect_year(qn)
    top_n=detect_top_n(qn)
    d1,d2=detect_dims(qn)
    if 'quantos documentos cancelados existem por mes' in qn:
        return CancellationSpec('cancellation','cancelled_docs_by_month',year,time_scope=time_scope, original_question=question)
    if 'tipos de documento de faturacao com mais documentos cancelados' in qn:
        return CancellationSpec('cancellation','top_cancelled_docs_by_dimension',year,time_scope=time_scope,dimension='billing_document_type',top_n=top_n or 10,original_question=question)
    if 'com maior taxa de cancelamento de documentos dentro de cada trimestre' in qn and d1=='distribution_channel':
        return CancellationSpec('cancellation','top_rate_within_quarter',year,time_scope=time_scope,dimension='distribution_channel',top_n=top_n or 3,original_question=question)
    if 'com maior taxa de cancelamento de documentos dentro de cada mes' in qn and d1=='sales_organization':
        return CancellationSpec('cancellation','top_rate_within_month',year,time_scope=time_scope,dimension='sales_organization',top_n=top_n or 2,original_question=question)
    if 'com maior taxa de cancelamento de documentos dentro de cada mes' in qn and d1=='distribution_channel':
        return CancellationSpec('cancellation','top_rate_within_month',year,time_scope=time_scope,dimension='distribution_channel',top_n=top_n or 2,original_question=question)
    if 'com maior taxa de cancelamento de documentos' in qn and d1=='billing_document_type':
        return CancellationSpec('cancellation','top_rate_global',year,time_scope=time_scope,dimension='billing_document_type',top_n=top_n or 10,original_question=question)
    if 'taxa de cancelamento de documentos' in qn and 'por mes' in qn and d1=='billing_document_type':
        return CancellationSpec('cancellation','rate_by_month_and_dimension',year,time_scope=time_scope,dimension='billing_document_type',include_counts=True,original_question=question)
    if 'taxa de cancelamento de documentos' in qn and 'por mes' in qn and d1=='distribution_channel':
        return CancellationSpec('cancellation','rate_by_month_and_dimension',year,time_scope=time_scope,dimension='distribution_channel',include_counts=True,original_question=question)
    if 'taxa de cancelamento de documentos' in qn and 'por mes' in qn and d1=='product_brand':
        return CancellationSpec('cancellation','rate_by_month_and_dimension_indirect',year,time_scope=time_scope,dimension='product_brand',include_counts=True,original_question=question)
    if 'taxa de cancelamento de documentos' in qn and 'por mes' in qn:
        return CancellationSpec('cancellation','rate_by_month',year,time_scope=time_scope,original_question=question)
    if 'taxa de cancelamento de documentos' in qn and d1 and d2:
        return CancellationSpec('cancellation','rate_by_two_dimensions',year,time_scope=time_scope,dimension=d1,secondary_dimension=d2,include_counts=True,original_question=question)
    if 'taxa de cancelamento de documentos' in qn and d1:
        include_counts = False if d1=='billing_document_type' else True
        return CancellationSpec('cancellation','rate_by_dimension',year,time_scope=time_scope,dimension=d1,include_counts=include_counts,original_question=question)
    raise ValueError(f'Unsupported cancellation question: {question}')


def generate_sql(spec:CancellationSpec)->str:
    year_filter = year_filter_sql(spec)
    month_expr = month_bucket_expr()
    if spec.operation=='cancelled_docs_by_month':
        return f"""SELECT
    {month_expr} AS Mes,
    COUNT(DISTINCT f.BillingDocument) AS DocumentosCancelados
FROM dbo.F_Invoice f
WHERE {year_filter}
  AND f.BillingDocumentIsCancelled = 1
GROUP BY {month_expr}
ORDER BY Mes;"""

    if spec.operation=='top_cancelled_docs_by_dimension':
        m=DIMENSIONS[spec.dimension]
        return f"""SELECT TOP ({spec.top_n})
    d.{m['text']} AS {m['alias']},
    COUNT(DISTINCT f.BillingDocument) AS DocumentosCancelados
FROM dbo.F_Invoice f
JOIN {m['table']} d
    ON f.{m['nid']} = d.{m['pk']}
WHERE {year_filter}
  AND f.BillingDocumentIsCancelled = 1
GROUP BY d.{m['text']}
ORDER BY DocumentosCancelados DESC, {m['alias']};"""

    if spec.operation=='rate_by_month':
        return f"""WITH docs AS (
    SELECT
        {month_expr} AS Mes,
        f.BillingDocument,
        MAX(CASE WHEN f.BillingDocumentIsCancelled = 1 THEN 1 ELSE 0 END) AS DocumentoCancelado
    FROM dbo.F_Invoice f
    WHERE {year_filter}
    GROUP BY {month_expr}, f.BillingDocument
)
SELECT
    x.Mes,
    COUNT(*) AS TotalDocumentos,
    SUM(x.DocumentoCancelado) AS DocumentosCancelados,
    100.0 * SUM(x.DocumentoCancelado) / NULLIF(COUNT(*), 0) AS TaxaCancelamento
FROM docs x
GROUP BY x.Mes
ORDER BY x.Mes;"""

    if spec.operation=='rate_by_dimension':
        m=DIMENSIONS[spec.dimension]
        select_counts = "\n    COUNT(*) AS TotalDocumentos,\n    SUM(x.DocumentoCancelado) AS DocumentosCancelados," if spec.include_counts else ""
        return f"""WITH docs AS (
    SELECT
        f.BillingDocument,
        f.{m['nid']},
        MAX(CASE WHEN f.BillingDocumentIsCancelled = 1 THEN 1 ELSE 0 END) AS DocumentoCancelado
    FROM dbo.F_Invoice f
    WHERE {year_filter}
    GROUP BY f.BillingDocument, f.{m['nid']}
)
SELECT
    d.{m['text']} AS {m['alias']},{select_counts}
    100.0 * SUM(x.DocumentoCancelado) / NULLIF(COUNT(*), 0) AS TaxaCancelamento
FROM docs x
JOIN {m['table']} d ON d.{m['pk']} = x.{m['nid']}
GROUP BY d.{m['text']}
ORDER BY TaxaCancelamento DESC{', TotalDocumentos DESC' if spec.include_counts else ''}, {m['alias']};"""

    if spec.operation=='rate_by_month_and_dimension':
        m=DIMENSIONS[spec.dimension]
        return f"""WITH docs AS (
    SELECT
        {month_expr} AS Mes,
        f.BillingDocument,
        f.{m['nid']},
        MAX(CASE WHEN f.BillingDocumentIsCancelled = 1 THEN 1 ELSE 0 END) AS DocumentoCancelado
    FROM dbo.F_Invoice f
    WHERE {year_filter}
    GROUP BY {month_expr}, f.BillingDocument, f.{m['nid']}
)
SELECT
    x.Mes,
    d.{m['text']} AS {m['alias']},
    COUNT(*) AS TotalDocumentos,
    SUM(x.DocumentoCancelado) AS DocumentosCancelados,
    100.0 * SUM(x.DocumentoCancelado) / NULLIF(COUNT(*), 0) AS TaxaCancelamento
FROM docs x
JOIN {m['table']} d ON d.{m['pk']} = x.{m['nid']}
GROUP BY x.Mes, d.{m['text']}
ORDER BY x.Mes, TaxaCancelamento DESC, TotalDocumentos DESC, {m['alias']};"""

    if spec.operation=='rate_by_month_and_dimension_indirect':
        return f"""WITH docs AS (
    SELECT
        {month_expr} AS Mes,
        f.BillingDocument,
        p.NIDProductBrand,
        MAX(CASE WHEN f.BillingDocumentIsCancelled = 1 THEN 1 ELSE 0 END) AS DocumentoCancelado
    FROM dbo.F_Invoice f
    JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct
    WHERE {year_filter}
    GROUP BY {month_expr}, f.BillingDocument, p.NIDProductBrand
)
SELECT
    x.Mes,
    pb.TProductBrand AS MarcaProduto,
    COUNT(*) AS TotalDocumentos,
    SUM(x.DocumentoCancelado) AS DocumentosCancelados,
    100.0 * SUM(x.DocumentoCancelado) / NULLIF(COUNT(*), 0) AS TaxaCancelamento
FROM docs x
JOIN dbo.D_ProductBrand pb ON pb.NIDProductBrand = x.NIDProductBrand
GROUP BY x.Mes, pb.TProductBrand
ORDER BY x.Mes, TaxaCancelamento DESC, TotalDocumentos DESC, MarcaProduto;"""

    if spec.operation=='rate_by_two_dimensions':
        m1=DIMENSIONS[spec.dimension]; m2=DIMENSIONS[spec.secondary_dimension]
        return f"""WITH docs AS (
    SELECT
        f.BillingDocument,
        f.{m1['nid']},
        f.{m2['nid']},
        MAX(CASE WHEN f.BillingDocumentIsCancelled = 1 THEN 1 ELSE 0 END) AS DocumentoCancelado
    FROM dbo.F_Invoice f
    WHERE {year_filter}
    GROUP BY f.BillingDocument, f.{m1['nid']}, f.{m2['nid']}
)
SELECT
    d1.{m1['text']} AS {m1['alias']},
    d2.{m2['text']} AS {m2['alias']},
    COUNT(*) AS TotalDocumentos,
    SUM(x.DocumentoCancelado) AS DocumentosCancelados,
    100.0 * SUM(x.DocumentoCancelado) / NULLIF(COUNT(*), 0) AS TaxaCancelamento
FROM docs x
JOIN {m1['table']} d1 ON d1.{m1['pk']} = x.{m1['nid']}
JOIN {m2['table']} d2 ON d2.{m2['pk']} = x.{m2['nid']}
GROUP BY d1.{m1['text']}, d2.{m2['text']}
ORDER BY TaxaCancelamento DESC, TotalDocumentos DESC, {m1['alias']}, {m2['alias']};"""

    if spec.operation=='top_rate_global':
        m=DIMENSIONS[spec.dimension]
        return f"""WITH docs AS (
    SELECT
        f.BillingDocument,
        f.{m['nid']},
        MAX(CASE WHEN f.BillingDocumentIsCancelled = 1 THEN 1 ELSE 0 END) AS DocumentoCancelado
    FROM dbo.F_Invoice f
    WHERE {year_filter}
    GROUP BY f.BillingDocument, f.{m['nid']}
)
SELECT TOP ({spec.top_n})
    d.{m['text']} AS {m['alias']},
    COUNT(*) AS TotalDocumentos,
    SUM(x.DocumentoCancelado) AS DocumentosCancelados,
    100.0 * SUM(x.DocumentoCancelado) / NULLIF(COUNT(*), 0) AS TaxaCancelamento
FROM docs x
JOIN {m['table']} d ON d.{m['pk']} = x.{m['nid']}
GROUP BY d.{m['text']}
ORDER BY TaxaCancelamento DESC, TotalDocumentos DESC, {m['alias']};"""

    if spec.operation=='top_rate_within_month':
        m=DIMENSIONS[spec.dimension]
        return f"""WITH docs AS (
    SELECT
        {month_expr} AS Mes,
        f.BillingDocument,
        f.{m['nid']},
        MAX(CASE WHEN f.BillingDocumentIsCancelled = 1 THEN 1 ELSE 0 END) AS DocumentoCancelado
    FROM dbo.F_Invoice f
    WHERE {year_filter}
    GROUP BY {month_expr}, f.BillingDocument, f.{m['nid']}
), grouped AS (
    SELECT
        x.Mes,
        d.{m['text']} AS {m['alias']},
        COUNT(*) AS TotalDocumentos,
        SUM(x.DocumentoCancelado) AS DocumentosCancelados,
        100.0 * SUM(x.DocumentoCancelado) / NULLIF(COUNT(*), 0) AS TaxaCancelamento
    FROM docs x
    JOIN {m['table']} d ON d.{m['pk']} = x.{m['nid']}
    GROUP BY x.Mes, d.{m['text']}
), ranked AS (
    SELECT
        g.*,
        ROW_NUMBER() OVER (
            PARTITION BY g.Mes
            ORDER BY g.TaxaCancelamento DESC, g.TotalDocumentos DESC, g.{m['alias']}
        ) AS rn
    FROM grouped g
)
SELECT
    Mes,
    {m['alias']},
    TotalDocumentos,
    DocumentosCancelados,
    TaxaCancelamento
FROM ranked
WHERE rn <= {spec.top_n}
ORDER BY Mes, rn;"""

    if spec.operation=='top_rate_within_quarter':
        m=DIMENSIONS[spec.dimension]
        quarter_expr = quarter_bucket_expr()
        return f"""WITH docs AS (
    SELECT
        {quarter_expr} AS Trimestre,
        f.BillingDocument,
        f.{m['nid']},
        MAX(CASE WHEN f.BillingDocumentIsCancelled = 1 THEN 1 ELSE 0 END) AS DocumentoCancelado
    FROM dbo.F_Invoice f
    WHERE {year_filter}
    GROUP BY {quarter_expr}, f.BillingDocument, f.{m['nid']}
), grouped AS (
    SELECT
        x.Trimestre,
        d.{m['text']} AS {m['alias']},
        COUNT(*) AS TotalDocumentos,
        SUM(x.DocumentoCancelado) AS DocumentosCancelados,
        100.0 * SUM(x.DocumentoCancelado) / NULLIF(COUNT(*), 0) AS TaxaCancelamento
    FROM docs x
    JOIN {m['table']} d ON d.{m['pk']} = x.{m['nid']}
    GROUP BY x.Trimestre, d.{m['text']}
), ranked AS (
    SELECT
        g.*,
        ROW_NUMBER() OVER (
            PARTITION BY g.Trimestre
            ORDER BY g.TaxaCancelamento DESC, g.TotalDocumentos DESC, g.{m['alias']}
        ) AS rn
    FROM grouped g
)
SELECT
    Trimestre,
    {m['alias']},
    TotalDocumentos,
    DocumentosCancelados,
    TaxaCancelamento
FROM ranked
WHERE rn <= {spec.top_n}
ORDER BY Trimestre, rn;"""

    raise ValueError(f'Unsupported operation: {spec.operation}')
