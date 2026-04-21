
import re
from dataclasses import dataclass

@dataclass
class ParsedQuery:
    target_entity: str
    filter_entity: str
    filter_mode: str
    filter_value: str
    measure: str
    year: int
    top_n: int

class TopNCrossFilterGenerator:
    """
    Gerador universal para perguntas do arquétipo:
    - produtos top-N por valor líquido para um cliente
    - clientes top-N por valor líquido para um produto
    com filtro por label ou por código.
    """

    def parse(self, question: str) -> ParsedQuery:
        q = question.strip().rstrip('?')
        q_low = q.lower()

        if 'valor líquido faturado' not in q_low and 'valor liquido faturado' not in q_low:
            raise ValueError('Pergunta fora do arquétipo: métrica não suportada.')

        top_match = re.search(r'quais são os\s+(\d+)\s+', q_low)
        top_n = int(top_match.group(1)) if top_match else 10

        year_match = re.search(r'em\s+(20\d{2})', q_low)
        if not year_match:
            raise ValueError('Ano não identificado.')
        year = int(year_match.group(1))

        target_entity = None
        filter_entity = None
        filter_mode = None
        filter_value = None

        m = re.search(r'quais são os produtos com mais valor líquido faturado em\s+20\d{2}\s+para o cliente com código\s+(.+)$', q, re.I)
        if m:
            target_entity='product'; filter_entity='customer'; filter_mode='code'; filter_value=m.group(1).strip();
        m = m or re.search(r'quais são os produtos com mais valor líquido faturado em\s+20\d{2}\s+para o cliente\s+(.+)$', q, re.I)
        if m and target_entity is None:
            target_entity='product'; filter_entity='customer'; filter_mode='label'; filter_value=m.group(1).strip();
        m = m or re.search(r'quais são os clientes com mais valor líquido faturado em\s+20\d{2}\s+para o produto com código\s+(.+)$', q, re.I)
        if m and target_entity is None:
            target_entity='customer'; filter_entity='product'; filter_mode='code'; filter_value=m.group(1).strip();
        m = m or re.search(r'quais são os clientes com mais valor líquido faturado em\s+20\d{2}\s+para o produto\s+(.+)$', q, re.I)
        if m and target_entity is None:
            target_entity='customer'; filter_entity='product'; filter_mode='label'; filter_value=m.group(1).strip();

        if target_entity is None:
            raise ValueError('Pergunta fora do arquétipo suportado.')

        return ParsedQuery(
            target_entity=target_entity,
            filter_entity=filter_entity,
            filter_mode=filter_mode,
            filter_value=filter_value,
            measure='net_amount',
            year=year,
            top_n=top_n,
        )

    def generate(self, question: str) -> str:
        p = self.parse(question)

        if p.target_entity == 'product':
            select_entity = 'p.TProduct AS Produto'
            group_entity = 'p.TProduct'
            filter_join = 'JOIN dbo.D_Customer c\n    ON f.NIDPayerParty = c.NIDCustomer\nJOIN dbo.D_Product p\n    ON f.NIDProduct = p.NIDProduct'
            filter_col = 'c.CCustomer' if p.filter_mode == 'code' else 'c.TCustomer'
        else:
            select_entity = 'c.TCustomer AS Cliente'
            group_entity = 'c.TCustomer'
            filter_join = 'JOIN dbo.D_Customer c\n    ON f.NIDPayerParty = c.NIDCustomer\nJOIN dbo.D_Product p\n    ON f.NIDProduct = p.NIDProduct'
            filter_col = 'p.CProduct' if p.filter_mode == 'code' else 'p.TProduct'

        filter_value = p.filter_value.replace("'", "''")

        sql = f"""SELECT TOP {p.top_n}
    {select_entity},
    SUM(f.NetAmount) AS ValorLiquidoFaturado
FROM dbo.F_Invoice f
{filter_join}
WHERE f.BillingDocumentDate / 10000 = {p.year}
  AND {filter_col} = '{filter_value}'
  AND f.BillingDocumentIsCancelled = 0
GROUP BY {group_entity}
ORDER BY ValorLiquidoFaturado DESC;"""
        return sql
