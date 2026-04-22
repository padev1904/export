# post-revY temporal consolidation notes

## Objetivo
Consolidar em camada técnica canónica as variantes temporais ainda dispersas em `topn_global` e `rank_partition`, reaproveitando `generators/sqlserver_patterns.py`, sem reabrir benchmark já fechado.

## Âmbito desta passagem
- atualização de `generators/sqlserver_patterns.py`
- atualização de `generators/topn_global_generator.py`
- atualização de `generators/rank_partition_generator.py`
- validação dirigida em `validation/revY/post_closure_temporal_consolidation_validation.csv`

## Factos verificados nesta passagem
- o estado factual canónico do repositório continua a apontar para `268/268` fechadas e `0/268` abertas
- esta passagem não introduz nova contagem benchmark-wide nem reabre `period_compare`
- a camada técnica passa a reutilizar predicados temporais canónicos para:
  - `explicit_year`
  - `current_year`
  - `last_12_months`
- `topn_global` passa a reconhecer variantes linguísticas fechadas em `revY` como:
  - `último ano móvel`
  - `ano corrente`
  - `este ano`
  - verbos como `mais faturaram` / `venderam mais unidades`
- `rank_partition` passa a reconhecer variantes temporais e de formulação equivalentes das perguntas fechadas em `revY`, incluindo:
  - `por região`
  - `por canal`
  - `para cada região`
  - `dentro de cada canal`
  - `último ano móvel`
  - `ano corrente`
  - `este ano`

## Limite desta validação
A validação registada nesta passagem é **dirigida** e **semanticamente orientada** sobre parsing e shape SQL dos padrões tocados.
Não substitui uma futura validação benchmark-wide por equivalência de resultado caso a camada técnica seja refatorada mais profundamente.

## Cobertura dirigida desta passagem
- `Q180`, `Q181`, `Q183`, `Q184`, `Q186`, `Q187`, `Q224`, `Q225`, `Q226`
- `Q191`, `Q192`, `Q193`, `Q194`, `Q195`, `Q196`

## Próxima subtarefa recomendada
1. avaliar consolidação semelhante para variantes temporais ainda dispersas em `time_series` e cancelamento mensal por dimensão
2. manter validação fora do benchmark em paralelo para travar overfit
3. só promover nova revisão factual benchmark-wide se houver evidência documental explícita de regressão ou nova validação total
