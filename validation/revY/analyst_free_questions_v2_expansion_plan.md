# analyst free questions v2 — expansion plan

## Objetivo
Preparar uma próxima sessão de trabalho que amplie os geradores universais para responder ao lote `B01`–`B20` formulado em estilo de analista experiente, sem reabrir benchmark fechado.

## Estado factual de partida
- benchmark canónico fechado: `268/268`
- backlog benchmark-wide: `0/268`
- lote `analyst_free_questions_v2`: 20 perguntas fora do benchmark
- cobertura atual por execução local: `4/20`
- gap atual fora do benchmark neste lote: `16/20`

## Princípio orientador
Expandir por **capacidades semânticas reutilizáveis** e não pergunta a pergunta.

## Workstreams mínimos recomendados

### WS1 — Nested share / partition share
**Cobertura alvo:** `B03`, `B11`, `B19`

Capacidade a introduzir:
- quota de uma entidade dentro de uma partição explícita
- suporte a bucket temporal mensal quando aplicável
- suporte a janelas `current_year` e `last_12_months`
- suporte a métricas com `requires_additional`

Alvo técnico principal:
- `generators/percentage_share_generator.py`
- eventual helper novo em `generators/sqlserver_patterns.py`

### WS2 — Pareto dentro de partição
**Cobertura alvo:** `B01`

Capacidade a introduzir:
- Pareto cumulativo por entidade dentro de uma partição
- threshold local por partição
- janela `last_12_months`

Alvo técnico principal:
- `generators/pareto_generator.py`

### WS3 — Lifecycle segmentado com janelas parametrizáveis
**Cobertura alvo:** `B05`, `B16`

Capacidade a introduzir:
- reativados/perdidos por dimensão
- janelas configuráveis de atividade e inatividade
- distinção explícita entre período-alvo e lookback

Alvo técnico principal:
- `generators/lifecycle_generator.py`
- helpers temporais adicionais em `generators/sqlserver_patterns.py`

### WS4 — Rank within partition com métricas derivadas e multi-partição
**Cobertura alvo:** `B02`, `B08`, `B10`, `B12`, `B14`, `B18`

Capacidade a introduzir:
- ranking sobre métrica yoy same-month derivada
- ranking sobre delta de moving windows
- ranking em partições múltiplas (`mes + organizacao`, `mes + marca`, etc.)
- mixed-sign documents partitioned beyond month
- novas métricas derivadas como `net_weight_per_unit`

Alvo técnico principal:
- `generators/rank_partition_generator.py`
- possível extração incremental de helpers comuns em `generators/sqlserver_patterns.py`

### WS5 — Cancellation por dimensão indireta e bucket novo
**Cobertura alvo:** `B07`, `B20`

Capacidade a introduzir:
- cancelamento por dimensão indireta via produto (`marca`)
- bucket trimestral
- top-N de taxa de cancelamento por partição temporal trimestral

Alvo técnico principal:
- `generators/cancellation_generator.py`
- helper trimestral em `generators/sqlserver_patterns.py`

### WS6 — Period compare / avg-per-document extensions
**Cobertura alvo:** `B09`, `B15`

Capacidade a introduzir:
- ticket médio por documento com dimensão indireta + mês rolling
- `period_compare` por `region`
- filtro semântico para excluir grupos com ambos os períodos a zero

Alvo técnico principal:
- `generators/avg_per_document_generator.py`
- `generators/period_compare_generator.py`

## Ordem recomendada
1. WS4 — rank derived / multi-partition
2. WS1 — nested share
3. WS3 — lifecycle parametrizável
4. WS5 — cancellation indirect / quarter
5. WS6 — avg-per-document + period compare extensions
6. WS2 — pareto within partition

## Justificação da ordem
- WS4 e WS1 fecham o maior volume de perguntas com maior reutilização transversal
- WS3 cobre lifecycle real de analista sénior, hoje ainda estreito
- WS5 e WS6 completam gaps dimensionais/temporais específicos
- WS2 é conceptualmente isolado e pode entrar depois sem bloquear os restantes

## Artefactos que a próxima sessão deverá produzir
- SQL manual esperado por pergunta nova suportada
- SQL gerado pelo código real atualizado
- matriz de equivalência por execução
- notas curtas por workstream com capacidade nova introduzida
- atualização de `HANDOVER_CURRENT.md`, `ARTEFACTS_INDEX.md` e `CHANGELOG.md`

## Regra crítica
Não reabrir benchmark fechado. Toda esta expansão é **fora do benchmark** até nova decisão explícita em contrário.
