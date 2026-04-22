# revY residual pattern consolidation scope

## Factos verificados
- o gap benchmark-wide explícito imediatamente anterior a `revY` tem `41 qid`
- esse gap foi fechado em `validation/revY/benchmark_residual_closure_validation.csv`
- a contagem global consolidada pós-`revY` é `268/268` fechadas e `0/268` abertas
- existe validação adicional fora do benchmark para os padrões residuais fechados: `10/10 PASS`

## Inferências operacionais para orientar refatoração
As categorias abaixo **não substituem** o benchmark canónico nem criam novas famílias factuais.
Servem apenas para orientar a consolidação técnica pós-`revY`.

### Agrupamento operacional do gap `41 qid`
- agregados promocionais: `Q74`, `Q89` -> `2`
- casos especiais/document logic/código técnico/câmbio: `Q76`, `Q77`, `Q81` -> `3`
- `time_series` mensal por dimensão direta ou indireta: `Q86`, `Q100`, `Q114`, `Q122`, `Q137`, `Q138` -> `6`
- `avg_per_document` por dimensão e/ou mês: `Q118`, `Q143`, `Q218`, `Q219`, `Q220` -> `5`
- cancelamento mensal por dimensão: `Q144` -> `1`
- `top_n_global` com `last_12_months` ou `current_year`: `Q180`, `Q181`, `Q183`, `Q184`, `Q186`, `Q187`, `Q224`, `Q225`, `Q226` -> `9`
- `rank_within_partition` com `last_12_months` ou `current_year`: `Q191`, `Q192`, `Q193`, `Q194`, `Q195`, `Q196` -> `6`
- `lifecycle` com janelas móveis: `Q206`, `Q208`, `Q211`, `Q212`, `Q213`, `Q214`, `Q215`, `Q216`, `Q217` -> `9`

## Implicações técnicas
1. a maior parte do fecho `revY` concentra-se em semântica temporal/janelas móveis, `lifecycle`, `top_n_global`, `rank_within_partition` e `avg_per_document`
2. o próximo bloco técnico útil não é reabrir famílias já fechadas, mas consolidar os padrões temporais residuais agora cobertos numa camada reutilizável
3. qualquer alteração na camada técnica deve preservar validação por equivalência de resultado e não reabrir benchmark fechado sem evidência de regressão

## Próxima subtarefa técnica recomendada
1. unificar normalização temporal reutilizável para:
   - `current_year`
   - `last_12_months`
   - `last_6_months`
   - `last_90_days`
   - `previous_90_days`
2. isolar um bloco reutilizável de `avg_per_document`
3. consolidar variantes temporais em `top_n_global`, `rank_within_partition`, `lifecycle`, `time_series` e cancelamento mensal por dimensão
4. manter validação fora do benchmark em paralelo para travar overfit
