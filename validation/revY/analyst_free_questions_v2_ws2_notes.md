# analyst_free_questions_v2 — WS2 notes

## Âmbito
Fecho do workstream `WS2 — Pareto dentro de partição` na linha fora do benchmark `analyst_free_questions_v2`.

## Perguntas cobertas nesta passagem
- B01

## Capacidades sincronizadas na camada técnica canónica
- Pareto cumulativo por entidade dentro de partição explícita
- threshold local por partição
- janela `last_12_months`
- operação interna por IDs com projeção de labels apenas no fim
- fronteira correta por `PercentagemAcumulada` e `PercentagemAntes`

## Evidência de validação
- base aceite: `training_data/documentation/f_invoice_sample.csv`
- motor de execução: `sqlite_local_translated_from_tsql`
- equivalência confirmada em reexecução com o código canónico gravado: `1/1`
- `generators/pareto_generator.py` ficou sincronizado antes desta reexecução final

## Regra de perímetro
- esta passagem permanece **fora do benchmark**
- não altera o estado canónico `268/268`
