# F16_pareto_80 — benchmark subset notes revJ

## Perguntas benchmark identificadas
- Q203
- Q204
- Q205

## Observação factual
As três perguntas têm SQL oráculo equivalente:
- agregação por cliente
- últimos 12 meses
- `BillingDocumentIsCancelled = 0`
- cálculo de acumulado e total
- filtro final simplista `PercentagemAcumulada <= 80`

## Risco de overfit
Se o gerador universal copiar esta forma literalmente:
- passa o subconjunto benchmark atual
- mas falha a semântica Pareto de fronteira em casos onde a linha de corte ultrapassa 80%

## Decisão canónica recomendada
Separar:
1. compatibilidade benchmark
2. semântica universal

Na camada universal:
- usar `PercentagemAcumulada <= 80 OR PercentagemAnterior < 80`

Na validação:
- registar explicitamente quando o benchmark legado usa a forma simplista
- não promover esse detalhe a regra universal
