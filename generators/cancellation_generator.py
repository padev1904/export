from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import re

@dataclass
class CancellationSpec:
    family: str
    operation: str
    year: int
    dimension: Optional[str] = None
    secondary_dimension: Optional[str] = None
    top_n: Optional[int] = None
    include_counts: bool = True
    original_question: Optional[str] = None

DIMENSIONS = {
    "billing_document_type": {"nid":"NIDBillingDocumentType","table":"dbo.D_BillingDocumentType","pk":"NIDBillingDocumentType","text":"TBillingDocumentType","alias":"TipoDocumentoFaturacao"},
    "distribution_channel": {"nid":"NIDDistributionChannel","table":"dbo.D_DistributionChannel","pk":"NIDDistributionChannel","text":"TDistributionChannel","alias":"CanalDistribuicao"},
    "sales_organization": {"nid":"NIDSalesOrganization","table":"dbo.D_SalesOrganization","pk":"NIDSalesOrganization","text":"TSalesOrganization","alias":"OrganizacaoVendas"},
    "country": {"nid":"NIDCountry","table":"dbo.D_Country","pk":"NIDCountry","text":"TCountry","alias":"Pais"},
}

def normalize_q(q:str)->str:
    x=q.lower().strip()
    for a,b in [('á','a'),('à','a'),('â','a'),('ã','a'),('é','e'),('ê','e'),('í','i'),('ó','o'),('ô','o'),('õ','o'),('ú','u'),('ç','c')]:
        x=x.replace(a,b)
    return ' '.join(x.split())

def detect_year(qn:str)->int:
    m=re.search(r'(20\d{2})', qn)
    return int(m.group(1)) if m else 2026

def detect_top_n(qn:str)->Optional[int]:
    m=re.search(r'quais sao os (\d+)', qn)
    return int(m.group(1)) if m else None

def detect_dims(qn:str):
    candidates=[]
    patterns=[
        ('billing_document_type',['tipo de documento de faturacao','tipos de documento de faturacao']),
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

def classify_question(question:str)->CancellationSpec:
    qn=normalize_q(question)
    year=detect_year(qn); top_n=detect_top_n(qn)
    d1,d2=detect_dims(qn)
    if 'quantos documentos cancelados existem por mes' in qn:
        return CancellationSpec('cancellation','cancelled_docs_by_month',year, original_question=question)
    if 'tipos de documento de faturacao com mais documentos cancelados' in qn:
        return CancellationSpec('cancellation','top_cancelled_docs_by_dimension',year,dimension='billing_document_type',top_n=top_n or 10,original_question=question)
    if 'com maior taxa de cancelamento de documentos dentro de cada mes' in qn and d1=='sales_organization':
        return CancellationSpec('cancellation','top_rate_within_month',year,dimension='sales_organization',top_n=top_n or 2,original_question=question)
    if 'com maior taxa de cancelamento de documentos dentro de cada mes' in qn and d1=='distribution_channel':
        return CancellationSpec('cancellation','top_rate_within_month',year,dimension='distribution_channel',top_n=top_n or 2,original_question=question)
    if 'com maior taxa de cancelamento de documentos' in qn and d1=='billing_document_type':
        return CancellationSpec('cancellation','top_rate_global',year,dimension='billing_document_type',top_n=top_n or 10,original_question=question)
    if 'taxa de cancelamento de documentos' in qn and 'por mes' in qn and d1=='billing_document_type':
        return CancellationSpec('cancellation','rate_by_month_and_dimension',year,dimension='billing_document_type',include_counts=True,original_question=question)
    if 'taxa de cancelamento de documentos' in qn and 'por mes' in qn and d1=='distribution_channel':
        return CancellationSpec('cancellation','rate_by_month_and_dimension',year,dimension='distribution_channel',include_counts=True,original_question=question)
    if 'taxa de cancelamento de documentos' in qn and 'por mes' in qn:
        return CancellationSpec('cancellation','rate_by_month',year,original_question=question)
    if 'taxa de cancelamento de documentos' in qn and d1 and d2:
        return CancellationSpec('cancellation','rate_by_two_dimensions',year,dimension=d1,secondary_dimension=d2,include_counts=True,original_question=question)
    if 'taxa de cancelamento de documentos' in qn and d1:
        include_counts = False if d1=='billing_document_type' else True
        return CancellationSpec('cancellation','rate_by_dimension',year,dimension=d1,include_counts=include_counts,original_question=question)
    raise ValueError(f'Unsupported cancellation question: {question}')

def _dim_sql(dim_key:str, table_alias:str='d'):
    meta=DIMENSIONS[dim_key]
    return meta, f"JOIN {meta['table']} {table_alias} ON {table_alias}.{meta['pk']} = x.{meta['nid']}"

def generate_sql(spec:CancellationSpec)->str:
    y=spec.year
    if spec.operation=='cancelled_docs_by_month':
        return f"""SELECT
    (f.BillingDocumentDate / 100) % 100 AS Mes,
    COUNT(DISTINCT f.BillingDocument) AS DocumentosCancelados
FROM dbo.F_Invoice f
WHERE f.BillingDocumentDate / 10000 = {y}
  AND f.BillingDocumentIsCancelled = 1
GROUP BY (f.BillingDocumentDate / 100) % 100
ORDER BY Mes;"""
    if spec.operation=='top_cancelled_docs_by_dimension':
        m=DIMENSIONS[spec.dimension]
        return f"""SELECT TOP ({spec.top_n})
    d.{m['text']} AS {m['alias']},
    COUNT(DISTINCT f.BillingDocument) AS DocumentosCancelados
FROM dbo.F_Invoice f
JOIN {m['table']} d
    ON f.{m['nid']} = d.{m['pk']}
WHERE f.BillingDocumentDate / 10000 = {y}
  AND f.BillingDocumentIsCancelled = 1
GROUP BY d.{m['text']}
ORDER BY DocumentosCancelados DESC, {m['alias']};"""
    if spec.operation=='rate_by_month':
        return f"""WITH docs AS (
    SELECT
        (f.BillingDocumentDate / 100) % 100 AS Mes, f.BillingDocument, MAX(CASE WHEN f.BillingDocumentIsCancelled = 1 THEN 1 ELSE 0 END) AS DocumentoCancelado
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentDate / 10000 = {y}
    GROUP BY (f.BillingDocumentDate / 100) % 100, f.BillingDocument
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
        f.BillingDocument, f.{m['nid']}, MAX(CASE WHEN f.BillingDocumentIsCancelled = 1 THEN 1 ELSE 0 END) AS DocumentoCancelado
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentDate / 10000 = {y}
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
        (f.BillingDocumentDate / 100) % 100 AS Mes, f.BillingDocument, f.{m['nid']}, MAX(CASE WHEN f.BillingDocumentIsCancelled = 1 THEN 1 ELSE 0 END) AS DocumentoCancelado
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentDate / 10000 = {y}
    GROUP BY (f.BillingDocumentDate / 100) % 100, f.BillingDocument, f.{m['nid']}
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
    if spec.operation=='rate_by_two_dimensions':
        m1=DIMENSIONS[spec.dimension]; m2=DIMENSIONS[spec.secondary_dimension]
        return f"""WITH docs AS (
    SELECT
        f.BillingDocument, f.{m1['nid']}, f.{m2['nid']}, MAX(CASE WHEN f.BillingDocumentIsCancelled = 1 THEN 1 ELSE 0 END) AS DocumentoCancelado
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentDate / 10000 = {y}
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
        f.BillingDocument, f.{m['nid']}, MAX(CASE WHEN f.BillingDocumentIsCancelled = 1 THEN 1 ELSE 0 END) AS DocumentoCancelado
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentDate / 10000 = {y}
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
        (f.BillingDocumentDate / 100) % 100 AS Mes,
        f.BillingDocument,
        f.{m['nid']},
        MAX(CASE WHEN f.BillingDocumentIsCancelled = 1 THEN 1 ELSE 0 END) AS DocumentoCancelado
    FROM dbo.F_Invoice f
    WHERE f.BillingDocumentDate / 10000 = {y}
    GROUP BY (f.BillingDocumentDate / 100) % 100, f.BillingDocument, f.{m['nid']}
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
    raise ValueError(f'Unsupported operation: {spec.operation}')
