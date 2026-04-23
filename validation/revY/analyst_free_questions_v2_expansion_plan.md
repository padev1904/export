# analyst free questions v2 — expansion plan

## Objetivo
Preparar as próximas sessões de trabalho que ampliem os geradores universais para responder ao lote `B01`–`B20` formulado em estilo de analista experiente, sem reabrir benchmark fechado.

## Estado factual de partida
- benchmark canónico fechado: `268/268`
- backlog benchmark-wide: `0/268`
- lote `analyst_free_questions_v2`: 20 perguntas fora do benchmark
- cobertura canónica atual por execução/comparação de resultados: `20/20`
- gap atual fora do benchmark neste lote: `0/20`
- `WS1` fechado canonicamente em `2026-04-23`
- `WS2` fechado canonicamente em `2026-04-23`
- `WS3` fechado canonicamente em `2026-04-23`
- `WS4` fechado canonicamente em `2026-04-23`
- `WS5` fechado canonicamente em `2026-04-23`
- `WS6` fechado canonicamente em `2026-04-23`

## Princípio orientador
Expandir por **capacidades semânticas reutilizáveis** e não pergunta a pergunta.

## Estado dos workstreams

### WS1 — Nested share / partition share
**Cobertura fechada:** `B03`, `B11`, `B19`

### WS2 — Pareto dentro de partição
**Cobertura fechada:** `B01`

### WS3 — Lifecycle segmentado com janelas parametrizáveis
**Cobertura fechada:** `B05`, `B16`

### WS4 — Rank within partition com métricas derivadas e multi-partição
**Cobertura fechada:** `B02`, `B08`, `B10`, `B12`, `B14`, `B18`

### WS5 — Cancellation por dimensão indireta e bucket novo
**Cobertura fechada:** `B07`, `B20`

### WS6 — Period compare / avg-per-document extensions
**Cobertura fechada:** `B09`, `B15`

## Conclusão operacional
O lote `analyst_free_questions_v2` fica agora totalmente fechado por equivalência de resultado na base aceite, sem alterar o estado canónico do benchmark principal.

## Próximo uso recomendado
- não reabrir `analyst_free_questions_v2` sem regressão documental explícita
- preparar novo lote cego fora do benchmark
- ou executar regressão dirigida adicional sobre a camada técnica canónica consolidada

## Artefactos que a próxima sessão deverá produzir
- novo lote fora do benchmark ou nova regressão dirigida
- SQL manual esperado para os novos casos
- SQL gerado pelo código real atualizado
- matriz de equivalência por execução
- notas curtas do novo bloco
- atualização de `HANDOVER_CURRENT.md`, `ARTEFACTS_INDEX.md` e `CHANGELOG.md`

## Regra crítica
Não reabrir benchmark fechado. `analyst_free_questions_v2` fica agora fechado como linha canónica **fora do benchmark** até nova decisão explícita em contrário.
