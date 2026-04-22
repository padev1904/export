# post-revY time series and cancellation consolidation notes

## Objetivo
Consolidar em camada técnica canónica os padrões temporais ainda dispersos em `temporal_generator.py` e os padrões mensais de `cancellation_generator.py`, sem reabrir benchmark fechado.

## Âmbito desta passagem
- atualização de `generators/sqlserver_patterns.py`
- atualização de `generators/temporal_generator.py`
- atualização de `generators/cancellation_generator.py`
- validação dirigida em `validation/revY/post_closure_timeseries_cancellation_consolidation_validation.csv`

## Factos verificados nesta passagem
- o repositório continua a refletir `268/268` fechadas e `0/268` abertas
- esta passagem não reabre `period_compare` nem cria nova revisão benchmark-wide
- `sqlserver_patterns.py` passa a expor helpers temporais reutilizáveis para:
  - `last_6_months`
  - `recent_with_history`
  - upper bound até `GETDATE()`
  - janelas de mês atual / mês anterior / mesmo mês do ano anterior
  - bucket mensal como `DATEFROMPARTS(...)`
- `cancellation_generator.py` deixa de repetir manualmente o filtro anual e o bucket mensal
- `temporal_generator.py` deixa de depender de datas Python hardcoded e de colunas auxiliares locais como `MonthStart`/`BillingYear`

## Limite desta validação
A validação registada nesta passagem é **dirigida** e **semanticamente orientada**.
Não substitui uma futura validação benchmark-wide por equivalência de resultado.

## Cobertura dirigida desta passagem
### Casos confirmados sobre os padrões tocados
- `Q61`
- `Q62`
- `Q86`
- `Q104`
- `Q125`
- `Q138`
- `Q144`

### Casos explicitamente fora do âmbito deste gerador temporal consolidado
Os seguintes exemplos continuam a depender de geradores/famílias próprios ou de consolidação posterior mais ampla, pelo que **não** foram promovidos como cobertura desta passagem:
- `Q100`
- `Q114`
- `Q122`
- `Q137`

## Próxima subtarefa recomendada
1. consolidar os restantes casos mensais por dimensão ainda fora do âmbito do `temporal_generator` atual
2. manter validação fora do benchmark em paralelo para travar overfit
3. só promover nova revisão factual benchmark-wide se houver evidência documental explícita de regressão ou nova validação total
