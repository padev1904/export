# F18 multi_metric_topn — revM

## Método aplicado
1. semântica
2. slots/guardrails
3. gerador universal
4. subset benchmark
5. regressão integral da família
6. perguntas novas fora do benchmark com SQL manual independente
7. atualização canónica do repositório

## Âmbito coberto em F18
Família tratada como um todo, não apenas o bloco Q248-Q253.

### Subset benchmark incluído
- Q58, Q59
- Q75, Q90
- Q188, Q189, Q190
- Q248, Q249, Q250
- Q251, Q252, Q253

Total: 13 perguntas.

## Slots semânticos
- `top_n`
- `entity` = customer | product | brand | family | material_type
- `metrics`
- `time_scope` = year_2026 | current_year | last_12_months
- `order_metrics`

## Guardrails
- filtro base: `f.BillingDocumentIsCancelled = 0`
- se a métrica envolver `GrossMargin` ou `NetCommercialSales`, aplicar também:
  - `f.IsItAnAdditionalCalculatedRecord = 1`
- preço médio líquido unitário:
  - `SUM(f.NetAmount) / NULLIF(SUM(f.BillingQuantity), 0)`
- para rácios unitários:
  - `HAVING SUM(f.BillingQuantity) <> 0`
- joins:
  - customer → `D_Customer`
  - product → `D_Product`
  - brand/family/material type → via `D_Product`

## Defaults semânticos quando a pergunta não explicita N
- customer + gross_margin → top 10
- product + net_commercial_sales → top 10
- brand + net_commercial_sales + gross_margin → top 15
- product + avg_net_price_unit → top 20
- product + cost_total + gross_margin → top 20

## Resultado benchmark
- PASS: 13/13
- regressões após ajuste final: 0 no subset F18

## Resultado generalização fora do benchmark
- PASS: 8/8
- SQL manual independente usado como oráculo alternativo

## Nota metodológica
O executor local usado para validação continua a ser o emulador parcial T-SQL sobre SQLite. Para este subset F18, a validação foi feita por execução real dos SQL de referência e dos SQL gerados.
