# analyst_free_questions_v2 — WS3 notes

## Âmbito
Fecho do workstream `WS3 — lifecycle segmentado com janelas parametrizáveis` na linha fora do benchmark `analyst_free_questions_v2`.

## Perguntas cobertas nesta passagem
- B05
- B16

## Capacidades sincronizadas na camada técnica canónica
- lifecycle por dimensão direta (`organizacao de vendas`, `canal de distribuicao`)
- janelas parametrizáveis de período-alvo e lookback
- reativados por dimensão com janela de inatividade
- perdidos por dimensão com janela histórica explícita
- operação interna por IDs com projeção de labels apenas no fim

## Evidência de validação
- base aceite: `training_data/documentation/f_invoice_sample.csv`
- motor de execução: `sqlite_local_translated_from_tsql`
- equivalência confirmada em reexecução com o código canónico gravado: `2/2`
- `generators/lifecycle_generator.py` ficou sincronizado antes desta reexecução final

## Regra de perímetro
- esta passagem permanece **fora do benchmark**
- não altera o estado canónico `268/268`
