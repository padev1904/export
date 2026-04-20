# F12 rank_within_partition notes

## Subconjunto benchmark validado
- 27 perguntas classificadas como `rank_within_partition` em `Q61-Q150`
- resultado: 27/27 PASS por equivalência semântica
- equivalência estrita de grelha: 26/27

## Subpadrões cobertos
- métrica simples `SUM(NetAmount)`
- crescimento absoluto 2025->2026
- variação percentual 2025->2026
- diferença `SUM(ZLP1PriceList) - SUM(NetAmount)`
- rácio `SUM(NetAmount) / NULLIF(SUM(BillingQuantity), 0)` com `HAVING SUM(BillingQuantity) <> 0`
- taxa de cancelamento com deduplicação ao nível `BillingDocument`
- documentos com linhas positivas e negativas e ranking por `ABS(SUM(NetAmount))`
- partições simples e compostas (`Mes + FamiliaProduto`)
- joins diretos e indiretos via `D_Product`

## Regras operacionais fixadas
- agregar primeiro por `(partição, entidade)`
- só depois aplicar `ROW_NUMBER() OVER (PARTITION BY ... ORDER BY métrica ..., entidade)`
- desempate estável por entidade no gerador canónico
- quando a métrica é rácio, calcular o rácio agregado antes do ranking
- em cancelamentos, granularizar primeiro ao nível `BillingDocument`

## Divergência estrutural remanescente
- Q108 difere apenas no alias da métrica:
  - oráculo: `DiferencaPrecoListaValorLiquido`
  - gerador: `DiferencaPrecoListaVsLiquido`
- equivalência semântica preservada

## Generalização fora do benchmark
- 8 casos novos
- 8/8 PASS por equivalência semântica
