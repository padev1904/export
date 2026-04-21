from __future__ import annotations
from dataclasses import dataclass
import re
import unicodedata
from typing import List

CURRENT_YEAR = 2026
LAST_12M_START_YYYYMMDD = 20250501

@dataclass
class F18Spec:
    family: str
    top_n: int
    entity: str
    metrics: List[str]
    time_scope: str
    order_metrics: List[str]
    original_question: str

ENTITY_MAP = {
    'customer': {
        'label_expr':'c.TCustomer',
        'label_alias':'Cliente',
        'joins':['JOIN dbo.D_Customer c ON f.NIDPayerParty = c.NIDCustomer']
    },
    'product': {
        'label_expr':'p.TProduct',
        'label_alias':'Produto',
        'joins':['JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct']
    },
    'brand': {
        'label_expr':'pb.TProductBrand',
        'label_alias':'MarcaProduto',
        'joins':['JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct',
                 'JOIN dbo.D_ProductBrand pb ON p.NIDProductBrand = pb.NIDProductBrand']
    },
    'family': {
        'label_expr':'pf.TProductFamily',
        'label_alias':'FamiliaProduto',
        'joins':['JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct',
                 'JOIN dbo.D_ProductFamily pf ON p.NIDProductFamily = pf.NIDProductFamily']
    },
    'material_type': {
        'label_expr':'mt.TMaterialType',
        'label_alias':'TipoMaterial',
        'joins':['JOIN dbo.D_Product p ON f.NIDProduct = p.NIDProduct',
                 'JOIN dbo.D_MaterialType mt ON p.NIDMaterialType = mt.NIDMaterialType']
    },
}

METRIC_DEFS = {
    'gross_margin': {'expr':'SUM(f.GrossMargin)','alias':'MargemBruta','additional':True},
    'net_commercial_sales': {'expr':'SUM(f.NetCommercialSales)','alias':'VendasComerciaisLiquidas','additional':True},
    'cost_total': {'expr':'SUM(f.CostAmount)','alias':'CustoTotal','additional':False},
    'net_amount': {'expr':'SUM(f.NetAmount)','alias':'ValorLiquidoFaturado','additional':False},
    'billing_quantity': {'expr':'SUM(f.BillingQuantity)','alias':'QuantidadeFaturada','additional':False},
    'avg_net_price_unit': {'expr':'SUM(f.NetAmount) / NULLIF(SUM(f.BillingQuantity), 0)','alias':'PrecoMedioLiquidoUnitario','additional':False},
}

DEFAULT_TOP = {
    ('customer', ('gross_margin',)): 10,
    ('product', ('net_commercial_sales',)): 10,
    ('brand', ('net_commercial_sales', 'gross_margin')): 15,
    ('product', ('net_amount', 'billing_quantity', 'avg_net_price_unit')): 20,
    ('product', ('cost_total', 'gross_margin')): 20,
    ('family', ('gross_margin',)): 10,
    ('family', ('net_commercial_sales', 'gross_margin')): 10,
    ('material_type', ('gross_margin',)): 10,
}

def normalize(text: str) -> str:
    text = text.lower().strip()
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    return text

def extract_top_n(q: str) -> int | None:
    m = re.search(r'\btop\s+(\d+)\b', q)
    if m:
        return int(m.group(1))
    m = re.search(r'\b(\d+)\s+(produtos|clientes|marcas|familias|tipos)\b', q)
    if m:
        return int(m.group(1))
    return None

def classify_question(question: str) -> F18Spec:
    q = normalize(question)

    if 'clientes' in q or 'cliente' in q:
        entity = 'customer'
    elif 'marcas' in q or 'marca' in q:
        entity = 'brand'
    elif 'familias de produto' in q or 'familia de produto' in q or 'familias' in q:
        entity = 'family'
    elif 'tipos de material' in q or 'tipo de material' in q:
        entity = 'material_type'
    else:
        entity = 'product'

    if 'ultimos 12 meses' in q or 'ultimo ano movel' in q:
        time_scope = 'last_12_months'
    elif 'ano atual' in q or 'este ano' in q or 'ano corrente' in q:
        time_scope = 'current_year'
    elif '2026' in q:
        time_scope = 'year_2026'
    else:
        raise ValueError(f'Time scope nao suportado em F18: {question}')

    if 'preco medio liquido' in q or 'valor medio por unidade faturada' in q or 'preco medio liquido unitario' in q:
        metrics = ['net_amount', 'billing_quantity', 'avg_net_price_unit']
        order_metrics = ['avg_net_price_unit']
    elif 'vendas comerciais liquidas' in q:
        if 'margem bruta' in q:
            metrics = ['net_commercial_sales', 'gross_margin']
            order_metrics = ['net_commercial_sales', 'gross_margin']
        else:
            metrics = ['net_commercial_sales']
            order_metrics = ['net_commercial_sales']
    elif 'custo total' in q or ('custo' in q and 'margem bruta' in q):
        metrics = ['cost_total', 'gross_margin']
        order_metrics = ['gross_margin', 'cost_total']
    elif 'margem bruta' in q:
        metrics = ['gross_margin']
        order_metrics = ['gross_margin']
    else:
        raise ValueError(f'Metricas nao suportadas em F18: {question}')

    top_n = extract_top_n(q) or DEFAULT_TOP[(entity, tuple(metrics))]

    return F18Spec(
        family='F18_multi_metric_topn',
        top_n=top_n,
        entity=entity,
        metrics=metrics,
        time_scope=time_scope,
        order_metrics=order_metrics,
        original_question=question,
    )

def build_sql(spec: F18Spec) -> str:
    entity = ENTITY_MAP[spec.entity]
    select_cols = [f"{entity['label_expr']} AS {entity['label_alias']}"]
    for metric in spec.metrics:
        md = METRIC_DEFS[metric]
        select_cols.append(f"    {md['expr']} AS {md['alias']}")

    filters = ['f.BillingDocumentIsCancelled = 0']
    if any(METRIC_DEFS[m]['additional'] for m in spec.metrics):
        filters.append('f.IsItAnAdditionalCalculatedRecord = 1')

    if spec.time_scope == 'last_12_months':
        filters.append('f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, 1, EOMONTH(GETDATE(), -12)), 112))')
    elif spec.time_scope == 'current_year':
        filters.append('f.BillingDocumentDate / 10000 = YEAR(GETDATE())')
    elif spec.time_scope == 'year_2026':
        filters.append('f.BillingDocumentDate / 10000 = 2026')
    else:
        raise ValueError(spec.time_scope)

    having = ''
    if 'avg_net_price_unit' in spec.metrics:
        having = '\nHAVING SUM(f.BillingQuantity) <> 0'

    order_clause = ', '.join(f"{METRIC_DEFS[m]['alias']} DESC" for m in spec.order_metrics)

    sql = "SELECT TOP {top_n}\n    {cols}\nFROM dbo.F_Invoice f\n{joins}\nWHERE {where}\nGROUP BY {label}{having}\nORDER BY {order};".format(
        top_n=spec.top_n,
        cols=',\n'.join(select_cols),
        joins='\n'.join(entity['joins']),
        where='\n  AND '.join(filters),
        label=entity['label_expr'],
        having=having,
        order=order_clause,
    )
    return sql

def generate_sql(question: str) -> str:
    spec = classify_question(question)
    return build_sql(spec)
