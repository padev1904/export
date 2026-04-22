from __future__ import annotations

from typing import Iterable, Sequence, Tuple

CURRENT_DATE_SQL = 'CAST(GETDATE() AS date)'


def int_date_expr(date_expr: str) -> str:
    return f"CONVERT(int, CONVERT(char(8), {date_expr}, 112))"


def explicit_year_predicate(year: int, column: str = 'f.BillingDocumentDate') -> str:
    return f"{column} / 10000 = {year}"


def current_year_predicate(column: str = 'f.BillingDocumentDate') -> str:
    return f"{column} / 10000 = YEAR(GETDATE())"


def rolling_months_start_date_sql(months: int, anchor_date_sql: str = CURRENT_DATE_SQL) -> str:
    return f"DATEADD(day, 1, EOMONTH({anchor_date_sql}, -{months}))"


def rolling_months_predicate(
    months: int,
    column: str = 'f.BillingDocumentDate',
    anchor_date_sql: str = CURRENT_DATE_SQL,
) -> str:
    return f"{column} >= {int_date_expr(rolling_months_start_date_sql(months, anchor_date_sql))}"


def trailing_days_predicate(
    days: int,
    column: str = 'f.BillingDocumentDate',
    anchor_date_sql: str = CURRENT_DATE_SQL,
) -> str:
    return f"{column} >= {int_date_expr(f'DATEADD(day, -{days}, {anchor_date_sql})')}"


def previous_days_window_predicates(
    days: int,
    column: str = 'f.BillingDocumentDate',
    anchor_date_sql: str = CURRENT_DATE_SQL,
) -> Tuple[str, str]:
    return (
        f"{column} >= {int_date_expr(f'DATEADD(day, -{days * 2}, {anchor_date_sql})')}",
        f"{column} < {int_date_expr(f'DATEADD(day, -{days}, {anchor_date_sql})')}",
    )


def month_bucket_expr(column: str = 'f.BillingDocumentDate') -> str:
    return f"CAST(({column} / 100) % 100 AS INT)"


def build_named_time_predicate(
    time_scope: str,
    *,
    year: int | None = None,
    column: str = 'f.BillingDocumentDate',
    anchor_date_sql: str = CURRENT_DATE_SQL,
) -> str:
    if time_scope == 'explicit_year':
        if year is None:
            raise ValueError('year is required for explicit_year')
        return explicit_year_predicate(year, column)
    if time_scope == 'current_year':
        return current_year_predicate(column)
    if time_scope == 'last_12_months':
        return rolling_months_predicate(12, column, anchor_date_sql)
    raise ValueError(f'unsupported time scope: {time_scope}')


def dedupe_joins(joins: Iterable[str]) -> Tuple[str, ...]:
    out: list[str] = []
    seen: set[str] = set()
    for join in joins:
        if join not in seen:
            out.append(join)
            seen.add(join)
    return tuple(out)


def build_avg_document_cte(
    *,
    cte_name: str,
    select_dimensions: Sequence[tuple[str, str]],
    joins: Sequence[str],
    where_filters: Sequence[str],
    value_alias: str = 'ValorDocumento',
    document_value_expr: str = 'SUM(f.NetAmount)',
    from_clause: str = 'dbo.F_Invoice f',
) -> str:
    dimension_select = ',\n        '.join(f'{expr} AS {alias}' for expr, alias in select_dimensions)
    select_prefix = f'{dimension_select},\n        ' if dimension_select else ''
    group_exprs = ', '.join(expr for expr, _ in select_dimensions)
    group_prefix = f'{group_exprs}, ' if group_exprs else ''
    join_block = '\n'.join(dedupe_joins(joins))
    join_sql = f'{join_block}\n' if join_block else ''
    where_sql = ' AND\n      '.join(where_filters)
    return f"""WITH {cte_name} AS (
    SELECT
        {select_prefix}f.BillingDocument,
        {document_value_expr} AS {value_alias}
    FROM {from_clause}
    {join_sql}WHERE {where_sql}
    GROUP BY {group_prefix}f.BillingDocument
)"""