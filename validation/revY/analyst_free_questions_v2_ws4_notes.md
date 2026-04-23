# analyst_free_questions_v2 — WS4 notes

## Âmbito
Fecho do workstream `WS4 — rank within partition com métricas derivadas e multi-partição` na linha fora do benchmark `analyst_free_questions_v2`.

## Perguntas cobertas nesta passagem
- B02
- B08
- B10
- B12
- B14
- B18

## Capacidades sincronizadas na camada técnica canónica
- ranking por múltiplas chaves de partição (`mes + organizacao`, `mes + marca`)
- ranking sobre métrica derivada `list_minus_net`
- ranking sobre métrica derivada `promo_discount_total`
- ranking sobre nova métrica derivada `net_weight_per_unit`
- ranking sobre delta móvel `ultimos 90 dias` vs `90 dias anteriores`
- ranking documental `mixed-sign` por partição não mensal
- ranking sobre yoy same-month para `GrossMargin` com `requires_additional`

## Evidência de validação
- base aceite: `training_data/documentation/f_invoice_sample.csv`
- motor de execução: `sqlite_local_translated_from_tsql`
- equivalência confirmada em reexecução com o código canónico gravado: `6/6`
- `generators/rank_partition_generator.py` ficou sincronizado antes desta reexecução final

## Regra de perímetro
- esta passagem permanece **fora do benchmark**
- não altera o estado canónico `268/268`

## Nota de interpretação operacional
- `B12` não explicita `N` no texto canónico da pergunta.
- A interpretação mantida no código canónico é devolver o conjunto ordenado por partição, sem corte `TOP N`, preservando ranking interno.

## Observação sobre a amostra
- `B02` devolveu `0` linhas na base aceite atual; a equivalência manual vs gerado foi ainda assim confirmada (`0 = 0`).
