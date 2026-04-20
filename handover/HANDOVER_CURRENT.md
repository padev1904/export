# HANDOVER CURRENT

Última consolidação: 2026-04-20 (revJ F16_pareto_80 started)

## 1) Âmbito
Projeto de geração universal de T-SQL para SQL Server, com foco em:
- classificação por família
- extração de slots semânticos
- grounding ao esquema real
- geração de SQL por família
- validação por equivalência de resultado
- controlo de generalização fora do benchmark
- sincronização canónica de artefactos seguros no repositório

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

### Pareto 80 (revJ em progresso)
Subconjunto benchmark identificado:
- Q203
- Q204
- Q205

Factos verificados:
- os três SQL oráculo são equivalentes
- os três usam filtro simplista `PercentagemAcumulada <= 80`
- a regra documental canónica do projeto exige fronteira antes/depois
- na `f_invoice_sample`, quando se restringe a contribuições positivas, a regra simplista seleciona 10 entidades e a regra canónica seleciona 11

Estado revJ:
- especificação canónica inicial fechada
- `generators/pareto_generator.py` criado
- `validation/revJ/pareto_benchmark_subset.csv` criado
- `validation/revJ/pareto_benchmark_notes.md` criado
- falta ainda validação executável da família e casos novos fora do benchmark

## 6) Estado do repositório canónico
### Já sincronizado no repositório
- `generators/temporal_generator.py`
- `generators/lifecycle_generator.py`
- `generators/pareto_generator.py`
- `validation/revD/tsql_emulator_benchmark_exec.csv`
- `validation/revD/temporal_benchmark_validation.csv`
- `validation/revD/temporal_generalization_eval.csv`
- `validation/revD/temporal_generalization_cases.md`
- `validation/revE/lifecycle_benchmark_validation.csv`
- `validation/revE/lifecycle_generalization_eval.csv`
- `validation/revE/lifecycle_generalization_cases.md`
- `validation/revJ/pareto_benchmark_subset.csv`
- `validation/revJ/pareto_benchmark_notes.md`
- documentação canónica em `handover/` e `repo_structure/`

## 7) Método obrigatório para cada nova família
1. formalizar a semântica da família
2. definir slots obrigatórios e opcionais
3. fixar guardrails e defaults
4. construir gerador universal sem hardcode de perguntas
5. validar no subconjunto do benchmark dessa família
6. reexecutar tudo o que já tinha passado nessa família
7. criar novas perguntas fora do benchmark
8. escrever SQL manual independente para essas perguntas
9. comparar resultado do SQL manual com o SQL do gerador na `f_invoice_sample`
10. atualizar `HANDOVER_CURRENT.md`, `CHANGELOG.md`, `ARTEFACTS_INDEX.md` e `RETOMA_CHECKLIST.md`

## 8) Prioridade atual
1. fechar `F16_pareto_80`
2. depois `F12_rank_within_partition`
3. depois `F18_multi_metric_topn`

## 9) Regras de higiene documental
No repositório deve existir:
- um único `HANDOVER_CURRENT.md`
- um único `CHANGELOG.md`
- um único `SAFE_SOURCE_MANIFEST.md`
- um único `RETOMA_CHECKLIST.md`
- um único `ARTEFACTS_INDEX.md`

As revisões (`revD`, `revE`, etc.) devem viver sobretudo em:
- `validation/revD/`
- `validation/revE/`
- `validation/revJ/`
- `generators/`

Não manter no repositório:
- ZIPs de handover
- handovers por revisão fora da árvore canónica
- cópias redundantes do mesmo estado em múltiplos caminhos
