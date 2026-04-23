# analyst_free_questions_v2 — WS5 notes

## Âmbito
Fecho do workstream `WS5 — cancellation por dimensão indireta e bucket novo` na linha fora do benchmark `analyst_free_questions_v2`.

## Perguntas cobertas nesta passagem
- B07
- B20

## Capacidades sincronizadas na camada técnica canónica
- taxa de cancelamento por dimensão indireta via produto (`marca`)
- suporte a `current_year` em cancelamentos fora do benchmark
- bucket trimestral em cancelamentos
- top-N de taxa de cancelamento por partição trimestral

## Evidência de validação
- base aceite: `training_data/documentation/f_invoice_sample.csv`
- motor de execução: `sqlite_local_translated_from_tsql`
- equivalência confirmada em reexecução com o código canónico gravado: `2/2`
- `generators/cancellation_generator.py` ficou sincronizado antes desta reexecução final

## Regra de perímetro
- esta passagem permanece **fora do benchmark**
- não altera o estado canónico `268/268`
