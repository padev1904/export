# post-revY refactor notes

## Objetivo
Consolidar em camada técnica canónica padrões temporais residuais já fechados em `revY`, sem reabrir benchmark fechado.

## Âmbito desta passagem
- criação de `generators/sqlserver_patterns.py`
- criação de `generators/avg_per_document_generator.py` em versão funcional mínima
- atualização de `generators/lifecycle_generator.py` para sintaxe e janelas temporais coerentes com T-SQL
- validação dirigida de perguntas benchmark afetadas em `validation/revY/post_closure_refactor_semantic_validation.csv`

## Factos verificados nesta passagem
- o benchmark canónico continua fechado em `268/268`
- esta passagem não identificou evidência documental de regressão benchmark-wide
- a validação dirigida desta consolidação cobre:
  - `Q118`, `Q143`, `Q218`, `Q219`, `Q220`
  - `Q206`, `Q208`, `Q211`, `Q212`, `Q213`, `Q214`, `Q215`, `Q216`, `Q217`

## Limite desta validação
A validação registada nesta passagem é **dirigida** e **semanticamente orientada** sobre os padrões tocados.
Não substitui uma futura validação benchmark-wide por equivalência de resultado caso a camada técnica venha a ser refatorada mais profundamente.

## Próxima subtarefa recomendada
1. ligar explicitamente o novo gerador `avg_per_document` ao classificador/orquestração canónica quando essa camada existir no repositório
2. avaliar consolidação semelhante para variantes temporais ainda dispersas em `topn_global` e `rank_partition`
3. manter validação fora do benchmark em paralelo para travar overfit
