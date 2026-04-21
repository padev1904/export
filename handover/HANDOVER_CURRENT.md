# HANDOVER CURRENT

Última consolidação: 2026-04-21 (revN Q32/Q34 reconciled)

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
A divergência factual antiga fica agora reconciliada por execução real:
- `Q32`: PASS
- `Q34`: PASS

Observação importante:
- os oráculos de benchmark de `Q32/Q34` usam labels de exemplo inexistentes nas dimensões reais (`Cliente Exemplo`, `Produto Exemplo`)
- por isso, o resultado esperado é conjunto vazio
- a equivalência foi validada por execução real de oráculo e gerador

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

### Pareto 80 (revK)
Subconjunto benchmark validado:
- Q203
- Q204
- Q205

Estado validado:
- compatibilidade executável com benchmark legado: 3/3 PASS
- generalização fora do benchmark com SQL manual independente: 8/8 PASS
- regressão integral da família nesta revisão: 14/14 PASS

Semântica operacional fechada:
- usar fronteira antes/depois: `PercentagemAcumulada <= 80 OR PercentagemAntes < 80`
- aplicar guardrail de contributos positivos antes do ranking: excluir entidades com métrica agregada `<= 0`
- manter um modo separado de compatibilidade com benchmark legado apenas para comparação histórica

### Rank within partition (revL)
Subconjunto benchmark validado:
- 27 perguntas classificadas como `rank_within_partition` em `Q61-Q150`

Estado validado:
- benchmark da família: 27/27 PASS por equivalência semântica
- equivalência estrita de grelha: 26/27
- regressão integral da família nesta revisão: 27/27 PASS
- generalização fora do benchmark com SQL manual independente: 8/8 PASS

Semântica operacional fechada:
- agregar primeiro por `(partição, entidade)`
- só depois aplicar `ROW_NUMBER() OVER (PARTITION BY ... ORDER BY métrica DESC, entidade)`
- desempate estável por entidade
- quando a métrica é rácio, calcular o rácio agregado antes do ranking
- em cancelamentos, granularizar primeiro ao nível `BillingDocument`

### Multi metric top-N (revM)
Subconjunto benchmark validado:
- Q58
- Q59
- Q75
- Q90
- Q188
- Q189
- Q190
- Q248
- Q249
- Q250
- Q251
- Q252
- Q253

Estado validado:
- benchmark da família: 13/13 PASS por equivalência semântica
- regressão integral da família nesta revisão: 13/13 PASS
- generalização fora do benchmark com SQL manual independente: 8/8 PASS

Semântica operacional fechada:
- top-N global por entidade com uma ou várias métricas ordenadoras
- quando a métrica envolve `GrossMargin` ou `NetCommercialSales`, aplicar `IsItAnAdditionalCalculatedRecord = 1`
- quando a métrica é `avg_net_price_unit`, calcular sempre `SUM(NetAmount) / NULLIF(SUM(BillingQuantity), 0)`
- aplicar `HAVING SUM(BillingQuantity) <> 0` nas perguntas de preço médio unitário
- suportar entidades `customer`, `product`, `brand`, `family`, `material_type`
- suportar time scopes `year_2026`, `current_year`, `last_12_months`
- usar defaults semânticos de `top_n` por arquétipo quando a pergunta não explicita N

### Top-N com filtro cruzado (revN)
Subconjunto benchmark validado:
- Q32
- Q34

Estado validado:
- benchmark da família: 2/2 PASS por equivalência de resultado
- generalização fora do benchmark com SQL manual independente: 6/6 PASS

Semântica operacional fechada:
- `produtos ... para o cliente X` -> agrupar por produto, filtrar cliente
- `clientes ... para o produto Y` -> agrupar por cliente, filtrar produto
- suporte a filtro por `label` e por `código`
- resolver slots: entidade alvo, entidade filtro, modo do filtro, valor do filtro, ano, top_n
- aplicar sempre `BillingDocumentIsCancelled = 0`

## 6) Estado do repositório canónico
### Já sincronizado no repositório
- `generators/temporal_generator.py`
- `generators/lifecycle_generator.py`
- `generators/pareto_generator.py`
- `generators/rank_partition_generator.py`
- `generators/f18_multi_metric_topn_generator.py`
- `generators/topn_cross_filter_generator.py`
- `validation/revD/tsql_emulator_benchmark_exec.csv`
- `validation/revD/temporal_benchmark_validation.csv`
- `validation/revD/temporal_generalization_eval.csv`
- `validation/revD/temporal_generalization_cases.md`
- `validation/revE/lifecycle_benchmark_validation.csv`
- `validation/revE/lifecycle_generalization_eval.csv`
- `validation/revE/lifecycle_generalization_cases.md`
- `validation/revK/f16_pareto_benchmark_validation.csv`
- `validation/revK/f16_pareto_family_regression.csv`
- `validation/revK/f16_pareto_generalization_eval.csv`
- `validation/revK/f16_pareto_generalization_cases.md`
- `validation/revK/f16_pareto_notes.md`
- `validation/revL/f12_rank_partition_benchmark_validation.csv`
- `validation/revL/f12_rank_partition_family_regression.csv`
- `validation/revL/f12_rank_partition_generalization_eval.csv`
- `validation/revL/f12_rank_partition_generalization_cases.md`
- `validation/revL/f12_rank_partition_notes.md`
- `validation/revM/f18_multi_metric_topn_benchmark_validation.csv`
- `validation/revM/f18_multi_metric_topn_generalization_cases.md`
- `validation/revM/f18_multi_metric_topn_notes.md`
- `validation/revN/q32_q34_benchmark_validation.csv`
- `validation/revN/q32_q34_regression_slice.csv`
- `validation/revN/q32_q34_generalization_eval.csv`
- `validation/revN/q32_q34_generalization_cases.md`
- `validation/revN/q32_q34_notes.md`
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
1. calcular backlog residual real pós-`Q32/Q34`
2. consolidar a contagem global real do benchmark já fechado
3. fechar os agrupamentos residuais por família/problema
4. limpeza final de redundâncias documentais, mantendo apenas a árvore canónica

## 9) Regras de higiene documental
No repositório deve existir:
- um único `HANDOVER_CURRENT.md`
- um único `CHANGELOG.md`
- um único `SAFE_SOURCE_MANIFEST.md`
- um único `RETOMA_CHECKLIST.md`
- um único `ARTEFACTS_INDEX.md`

As revisões devem viver sobretudo em:
- `validation/revD/`
- `validation/revE/`
- `validation/revK/`
- `validation/revL/`
- `validation/revM/`
- `validation/revN/`
- `generators/`

Não manter no repositório:
- ZIPs de handover
- handovers por revisão fora da árvore canónica
- checklists por revisão fora da árvore canónica
- cópias redundantes do mesmo estado em múltiplos caminhos
- ficheiros intermédios supersedidos quando já exista a versão canónica sincronizada
- qualquer ficheiro bruto derivado diretamente do ZIP original
