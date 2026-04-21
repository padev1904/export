from __future__ import annotations
from dataclasses import dataclass
import re
import unicodedata

CURRENT_YEAR = 2026

@dataclass
class TopNSpec:
    archetype: str
    top_n: int | None
    year: int | None = None
    year_a: int | None = None
    year_b: int | None = None
    threshold: int | None = None
    metric: str | None = None

def normalize(text: str) -> str:
    text = text.lower().strip().rstrip('?')
    text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    return text

class TopNGenerator:
    """
    Gerador universal para o residual canónico da família top_n:
    - documentos com mais de N linhas
    - combinações cliente-produto top-N por faturação
    - crescimento absoluto por cliente entre dois anos
    - documentos com linhas positivas e negativas
    - top-N documentos mistos por valor líquido absoluto
    """

    def parse(self, question: str) -> TopNSpec:
        q = normalize(question)
        top_match = re.search(r'\b(?:os|as)\s+(\d+)\b', q)
        top_n = int(top_match.group(1)) if top_match else None

        m = re.search(r'documentos de faturacao com mais de (\d+) linhas (?:em|no) (20\d{2}|ano atual)', q)
        if m:
            year = CURRENT_YEAR if m.group(2) == 'ano atual' else int(m.group(2))
            return TopNSpec(
                archetype='document_more_than_n_lines',
                top_n=top_n or 20,
                year=year,
                threshold=int(m.group(1)),
            )

        m = re.search(r'(\d+)\s+combinacoes cliente-produto com maior (?:valor liquido faturado|faturacao) (?:em|no) (20\d{2}|ano atual)', q)
        if m:
            year = CURRENT_YEAR if m.group(2) == 'ano atual' else int(m.group(2))
            return TopNSpec(
                archetype='customer_product_combo_net_amount',
                top_n=int(m.group(1)),
                year=year,
                metric='net_amount',
            )

        m = re.search(r'clientes com maior crescimento absoluto de (valor liquido faturado|quantidade faturada) de (20\d{2}) para (20\d{2})', q)
        if m:
            metric = 'net_amount' if 'valor liquido faturado' in m.group(1) else 'billing_quantity'
            return TopNSpec(
                archetype='customer_growth_absolute',
                top_n=top_n or 20,
                year_a=int(m.group(2)),
                year_b=int(m.group(3)),
                metric=metric,
            )

        m = re.search(r'documentos de faturacao tem simultaneamente linhas positivas e negativas (?:em|no) (20\d{2}|ano atual)', q)
        if m:
            year = CURRENT_YEAR if m.group(1) == 'ano atual' else int(m.group(1))
            return TopNSpec(
                archetype='mixed_sign_documents',
                top_n=top_n or 50,
                year=year,
            )

        m = re.search(r'(\d+)\s+documentos de faturacao com maior valor liquido absoluto(?: total)? (?:em|no) (20\d{2}|ano atual) entre os que tem simultaneamente linhas positivas e negativas', q)
        if m:
            year = CURRENT_YEAR if m.group(2) == 'ano atual' else int(m.group(2))
            return TopNSpec(
                archetype='mixed_sign_documents_abs_total',
                top_n=int(m.group(1)),
                year=year,
            )

        raise ValueError(f'Pergunta fora do residual top_n: {question}')

    def generate(self, question: str) -> str:
        p = self.parse(question)

        if p.archetype == 'document_more_than_n_lines':
            return f"""SELECT TOP {p.top_n}
    f.BillingDocument,
    COUNT(*) AS NumeroLinhas
FROM dbo.F_Invoice f
WHERE f.BillingDocumentDate / 10000 = {p.year}
GROUP BY f.BillingDocument
HAVING COUNT(*) > {p.threshold}
ORDER BY NumeroLinhas DESC, f.BillingDocument;"""

        if p.archetype == 'customer_product_combo_net_amount':
            return f"""SELECT TOP {p.top_n}
    c.TCustomer AS Cliente,
    p.TProduct AS Produto,
    SUM(f.NetAmount) AS ValorLiquidoFaturado
FROM dbo.F_Invoice f
JOIN dbo.D_Customer c
    ON f.NIDPayerParty = c.NIDCustomer
JOIN dbo.D_Product p
    ON f.NIDProduct = p.NIDProduct
WHERE f.BillingDocumentDate / 10000 = {p.year}
  AND f.BillingDocumentIsCancelled = 0
GROUP BY c.TCustomer, p.TProduct
ORDER BY ValorLiquidoFaturado DESC, c.TCustomer, p.TProduct;"""

        if p.archetype == 'customer_growth_absolute':
            alias = 'CrescimentoAbsoluto' if p.metric == 'net_amount' else 'CrescimentoAbsolutoQuantidade'
            measure_expr = 'f.NetAmount' if p.metric == 'net_amount' else 'f.BillingQuantity'
            return f"""SELECT TOP {p.top_n}
    c.TCustomer AS Cliente,
    SUM(CASE WHEN f.BillingDocumentDate / 10000 = {p.year_b} THEN {measure_expr} ELSE 0 END)
    - SUM(CASE WHEN f.BillingDocumentDate / 10000 = {p.year_a} THEN {measure_expr} ELSE 0 END) AS {alias}
FROM dbo.F_Invoice f
JOIN dbo.D_Customer c
    ON f.NIDPayerParty = c.NIDCustomer
WHERE f.BillingDocumentDate / 10000 IN ({p.year_a}, {p.year_b})
  AND f.BillingDocumentIsCancelled = 0
GROUP BY c.TCustomer
ORDER BY {alias} DESC, c.TCustomer;"""

        if p.archetype == 'mixed_sign_documents':
            return f"""SELECT TOP {p.top_n}
    f.BillingDocument,
    MIN(f.NetAmount) AS ValorMinimoLinha,
    MAX(f.NetAmount) AS ValorMaximoLinha
FROM dbo.F_Invoice f
WHERE f.BillingDocumentDate / 10000 = {p.year}
GROUP BY f.BillingDocument
HAVING MIN(f.NetAmount) < 0
   AND MAX(f.NetAmount) > 0
ORDER BY f.BillingDocument;"""

        if p.archetype == 'mixed_sign_documents_abs_total':
            return f"""SELECT TOP {p.top_n}
    f.BillingDocument,
    ABS(SUM(f.NetAmount)) AS ValorLiquidoAbsolutoTotal
FROM dbo.F_Invoice f
WHERE f.BillingDocumentDate / 10000 = {p.year}
  AND f.BillingDocumentIsCancelled = 0
GROUP BY f.BillingDocument
HAVING MIN(f.NetAmount) < 0
   AND MAX(f.NetAmount) > 0
ORDER BY ValorLiquidoAbsolutoTotal DESC, f.BillingDocument;"""

        raise ValueError(p.archetype)
