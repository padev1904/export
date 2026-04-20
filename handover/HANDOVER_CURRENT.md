# HANDOVER CURRENT

Última consolidação documental: 2026-04-20 (revF documental)

## 1) Âmbito
Projeto de geração universal de T-SQL para SQL Server, com foco em:
- classificação por família
- extração de slots semânticos
- grounding ao esquema real
- geração de SQL por família
- validação por equivalência de resultado
- controlo de generalização fora do benchmark

## 2) Fontes confirmadas
O conjunto-base local contém:
- `ddl/`
- `documentation/`
- `example_queries/`
- 45 ficheiros JSON de dimensão
- `f_invoice_sample.csv`
- `examples.sql` com 268 perguntas

## 3) Regras estabilizadas
### Regras transversais
- tabela âncora: `dbo.F_Invoice`
- por defeito, faturação válida: `f.BillingDocumentIsCancelled = 0`
- exceção: perguntas sobre cancelamentos

### Métricas estabilizadas
- valor líquido faturado: `SUM(f.NetAmount)`
- quantidade faturada: `SUM(f.BillingQuantity)`
- preço de lista: `SUM(f.ZLP1PriceList)`
- desconto de quantidade: `SUM(f.ZDQ1QtyDiscount)`
- desconto promocional total: `SUM(f.ZDPRPromotional + f.ZCPRPromotionalCampaign + f.REA1PromotionalDiscount)`
- preço médio líquido por unidade: `SUM(f.NetAmount) / NULLIF(SUM(f.BillingQuantity), 0)`
- peso líquido médio por unidade: `SUM(f.ItemNetWeight) / NULLIF(SUM(f.BillingQuantity), 0)`

### Regras documentais
- `GrossMargin` e `NetCommercialSales`: aplicar `f.IsItAnAdditionalCalculatedRecord = 1` quando relevante
- percentagens e quotas: escala `0-100`
- divisões: usar sempre `NULLIF`
- comparações entre períodos por entidade: excluir linhas onde ambos os períodos são zero, quando isso for ruído
- Pareto 80%: usar fronteira antes/depois, não filtro simplista
- ticket médio por documento: agregar primeiro por `BillingDocument`, só depois `AVG`

### Grounding estável
- marca / família / tipo de material: via `D_Product`
- grupo de contas / condição de expedição / zona de transporte / geografia cliente: via `D_Customer`

## 4) Divergências abertas
### Q1-Q60
Existe divergência factual entre:
- resumo narrativo antigo: 60/60
- matriz factual anexada: 58 PASS + 2 NO_GENERATOR

Perguntas remanescentes na matriz factual:
- Q32
- Q34

Até reconciliação por execução real, a verdade operacional deve seguir a matriz factual.

## 5) Estado validado por família
### Temporal / comparações / janela (revD)
Estado validado:
- emulador parcial T-SQL orientado ao benchmark
- 268/268 SQL de referência executados no emulador
- gerador temporal revD validado em 43 perguntas do benchmark
- equivalência semântica: 43/43 PASS
- equivalência estrita de grelha: 39/43 PASS
- generalização fora do benchmark: 8/8 PASS

Famílias/padrões cobertos em revD:
- `F15_window_trend`
- `F13_period_compare`
- `F11_percentage_share`
- `F10_avg_per_document`

### Lifecycle (revE)
Subconjunto explícito do benchmark:
- Q207
- Q209
- Q210

Estado validado:
- benchmark da família: 3/3 PASS
- generalização fora do benchmark: 8/8 PASS
- regressão final da família em revE: 11/11 PASS

Semântica operacional fechada:
- `reactivated`: atividade recente + ausência de atividade na janela de inatividade imediatamente anterior
- `lost`: atividade anterior + ausência de atividade na janela recente
- por dimensão: semântica por par `(Dimensao, Entidade)`

Subpadrões fechados:
- `first_purchase_monthly_count`
- `reactivated_count`
- `reactivated_list`
- `lost_count`
- `lost_list`
- `lost_list_by_dimension`

## 6) Método obrigatório para cada nova família
1. formalizar a semântica da família
2. definir slots obrigatórios e opcionais
3. fixar guardrails e defaults
4. construir gerador universal sem hardcode de perguntas
5. validar no subconjunto do benchmark dessa família
6. reexecutar tudo o que já tinha passado nessa família
7. criar novas perguntas fora do benchmark
8. escrever SQL manual independente para essas perguntas
9. comparar resultado do SQL manual com o SQL do gerador na `f_invoice_sample`
10. atualizar handover, changelog e índice de artefactos

## 7) Prioridade atual
1. `F16_pareto_80`
2. `F12_rank_within_partition`
3. `F18_multi_metric_topn`

## 8) Artefactos de trabalho já gerados fora do repositório
### revD
- `temporal_generator_revD.py`
- `tsql_emulator_benchmark_exec_revD.csv`
- `temporal_generator_revD_benchmark_validation.csv`
- `temporal_generator_revD_generalization_eval.csv`
- `temporal_generator_revD_generalization_cases.md`

### revE
- `lifecycle_generator_revE.py`
- `lifecycle_benchmark_validation_revE.csv`
- `lifecycle_generalization_eval_revE.csv`
- `lifecycle_generalization_cases_revE.md`

## 9) Regra de higiene documental
No repositório deve existir:
- um único `HANDOVER_CURRENT.md`
- um único `CHANGELOG.md`
- um único `SAFE_SOURCE_MANIFEST.md`
- um único `RETOMA_CHECKLIST.md`

As revisões (`revD`, `revE`, etc.) devem viver sobretudo em:
- `validation/revD/`
- `validation/revE/`
- `generators/`
