# monthly generalization local sample equivalence notes

## Objetivo
Registar uma verificação de equivalência de resultado em **amostra local** para os candidatos fora do benchmark `MG01`–`MG08`.

## Fonte de dados usada
- `training_data/documentation/f_invoice_sample.csv`
- tabelas de dimensão JSON da mesma `training_data.zip`

## Método usado nesta passagem
1. carregar `f_invoice_sample.csv` e as dimensões necessárias em memória local
2. reconstruir o resultado esperado do gerador universal atual
3. reconstruir de forma independente o resultado dos SQL manuais em `validation/revY/monthly_generalization_manual_oracle_sql.sql`
4. comparar os dois resultados por igualdade de dataframe ordenado

## Resultado
- `MG01`–`MG08`: equivalentes na amostra local

## Limite desta evidência
Esta passagem **não** substitui validação por equivalência de resultado no dataset canónico completo.
Representa apenas evidência adicional em amostra local consistente com a semântica atual do gerador.

## Valor prático desta passagem
- fecha a lacuna entre `parser/sql_shape` e uma primeira verificação material de equivalência
- reduz o risco de overfit/regressão nas extensões mensais recentes do `temporal_generator`
- deixa o repositório pronto para futura execução em dataset mais amplo, se disponível
