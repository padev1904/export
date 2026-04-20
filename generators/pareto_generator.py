"""
Canonical Pareto 80 generator — revJ
Initial universal generator for F16_pareto_80.

Scope of this revision:
- global pareto by entity
- optional partitioned pareto
- threshold default 80
- canonical boundary logic with PercentagemAnterior
- optional positive-contribution guardrail
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class ParetoSlots:
    entity_label_expr: str
    entity_group_expr: str
    measure_expr: str
    from_and_joins_sql: str
    where_clauses: List[str]
    partition_exprs: List[str] = field(default_factory=list)
    threshold_percent: float = 80.0
    positive_contribution_only: bool = False
    include_individual_percent: bool = True
    include_cumulative_percent: bool = True


def build_pareto_sql(slots: ParetoSlots) -> str:
    partition_cols = ", ".join(slots.partition_exprs)
    partition_group = (partition_cols + ", ") if partition_cols else ""
    partition_select = (partition_cols + ",\n        ") if partition_cols else ""
    partition_by = f"PARTITION BY {partition_cols} " if partition_cols else ""
    where_sql = "\n      AND ".join(slots.where_clauses) if slots.where_clauses else "1=1"

    positive_filter = ""
    if slots.positive_contribution_only:
        positive_filter = "\n    WHERE Valor > 0"

    select_cols = []
    if partition_cols:
        select_cols.append(partition_cols)
    select_cols.append("Entidade")
    select_cols.append("Valor")
    if slots.include_individual_percent:
        select_cols.append("PercentagemIndividual")
    if slots.include_cumulative_percent:
        select_cols.append("PercentagemAcumulada")
    select_sql = ",\n    ".join(select_cols)

    order_prefix = (partition_cols + ", ") if partition_cols else ""

    sql = f"""
WITH entity_sales AS (
    SELECT
        {partition_select}{slots.entity_label_expr} AS Entidade,
        {slots.measure_expr} AS Valor
    {slots.from_and_joins_sql}
    WHERE {where_sql}
    GROUP BY {partition_group}{slots.entity_group_expr}
),
entity_sales_filtered AS (
    SELECT *
    FROM entity_sales{positive_filter}
),
ranked AS (
    SELECT
        {partition_select}Entidade,
        Valor,
        SUM(Valor) OVER (
            {partition_by}ORDER BY Valor DESC, Entidade
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS ValorAcumulado,
        SUM(Valor) OVER ({partition_by.rstrip()}) AS ValorTotal
    FROM entity_sales_filtered
),
scored AS (
    SELECT
        {partition_select}Entidade,
        Valor,
        Valor * 100.0 / NULLIF(ValorTotal, 0) AS PercentagemIndividual,
        ValorAcumulado * 100.0 / NULLIF(ValorTotal, 0) AS PercentagemAcumulada,
        (ValorAcumulado - Valor) * 100.0 / NULLIF(ValorTotal, 0) AS PercentagemAnterior
    FROM ranked
)
SELECT
    {select_sql}
FROM scored
WHERE PercentagemAcumulada <= {slots.threshold_percent}
   OR PercentagemAnterior < {slots.threshold_percent}
ORDER BY {order_prefix}Valor DESC, Entidade;
""".strip()
    return sql


def build_customer_last_12m_pareto_sql() -> str:
    slots = ParetoSlots(
        entity_label_expr="c.TCustomer",
        entity_group_expr="c.TCustomer",
        measure_expr="SUM(f.NetAmount)",
        from_and_joins_sql="FROM dbo.F_Invoice f\n    JOIN dbo.D_Customer c ON f.NIDPayerParty = c.NIDCustomer",
        where_clauses=[
            "f.BillingDocumentIsCancelled = 0",
            "f.BillingDocumentDate >= CONVERT(int, CONVERT(char(8), DATEADD(day, 1, EOMONTH(GETDATE(), -12)), 112))",
        ],
        partition_exprs=[],
        threshold_percent=80.0,
        positive_contribution_only=False,
    )
    return build_pareto_sql(slots)
