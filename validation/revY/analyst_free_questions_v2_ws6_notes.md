# analyst_free_questions_v2 — WS6 notes

## Âmbito
Fecho do workstream `WS6 — period compare / avg-per-document extensions` na linha fora do benchmark `analyst_free_questions_v2`.

## Perguntas cobertas nesta passagem
- B09
- B15

## Capacidades sincronizadas na camada técnica canónica
- ticket médio por documento com bucket mensal rolling e dimensão indireta via cliente (`grupo de contas`)
- extensão de `period_compare` para `region`
- preservação da exclusão semântica de grupos com ambos os períodos a zero
- operação interna por IDs para `region` com projeção de label no fim

## Evidência de validação
- base aceite: `training_data/documentation/f_invoice_sample.csv`
- motor de execução: `sqlite_local_translated_from_tsql`
- equivalência confirmada em reexecução com o código canónico gravado: `2/2`
- `generators/avg_per_document_generator.py` e `generators/period_compare_generator.py` ficaram sincronizados antes desta reexecução final

## Regra de perímetro
- esta passagem permanece **fora do benchmark**
- não altera o estado canónico `268/268`
