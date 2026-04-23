# analyst_free_questions_v2 — WS1 notes

## Âmbito
Fecho do workstream `WS1 — nested share / partition share` na linha fora do benchmark `analyst_free_questions_v2`.

## Perguntas cobertas nesta passagem
- B03
- B11
- B19

## Capacidades sincronizadas na camada técnica canónica
- quota por entidade dentro de partição explícita
- quota por entidade dentro de partição com bucket mensal
- suporte a `current_year`
- suporte a `last_12_months`
- suporte a métricas com `requires_additional`
- quota por dimensão indireta via produto (`marca` dentro de `família`)

## Evidência de validação
- base aceite: `training_data/documentation/f_invoice_sample.csv`
- motor de execução: `sqlite_local_translated_from_tsql`
- equivalência confirmada em reexecução com o código canónico gravado: `3/3`
- `generators/percentage_share_generator.py` ficou sincronizado antes desta reexecução final

## Regra de perímetro
- esta passagem permanece **fora do benchmark**
- não altera o estado canónico `268/268`

## Observações operacionais
- `B03` passou a suportar quota por `organizacao de vendas` dentro de `canal de distribuicao` com bucket mensal em `current_year`
- `B11` passou a suportar share de `GrossMargin` por `marca` dentro de `familia` e por mês, com `IsItAnAdditionalCalculatedRecord = 1`
- `B19` passou a suportar quota por `pais` dentro de `organizacao de vendas` em janela `last_12_months`
