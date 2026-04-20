# Handover atualizado — revE — 2026-04-20

## Factos verificados nesta revisão

- Foi consultado o repositório público `padev1904/export`; o estado acessível confirmado continua a ser o bootstrap seguro do handover e da política de não publicação do ZIP bruto.
- A família seguinte trabalhada foi `F17_lifecycle`, conforme backlog recomendado.
- O subconjunto explícito do benchmark para `F17_lifecycle` é:
  - Q207 — primeira compra mensal no último ano móvel
  - Q209 — clientes reativados nos últimos 30 dias após 180 dias sem compras
  - Q210 — duplicado semântico de Q209 com formulação alternativa
- Foi construído um gerador universal `lifecycle_generator_revE.py` com:
  - classificador por semântica
  - extração de slots
  - síntese T-SQL por padrão
  - guardrails explícitos da família

## Subpadrões semânticos fechados em revE

1. `first_purchase_monthly_count`
   - entidade: cliente ou produto
   - semântica: primeira compra/venda histórica, agregada por mês
   - janela: último ano móvel por defeito

2. `reactivated_count`
   - entidade: cliente ou produto
   - semântica operacional: atividade recente e ausência de atividade na janela de inatividade imediatamente anterior
   - compatível com benchmark Q209/Q210
   - nota: não exige atividade anterior à janela de inatividade

3. `reactivated_list`
   - variante listagem da lógica anterior

4. `lost_count`
   - entidade: cliente ou produto
   - semântica operacional: atividade antes da janela recente e ausência de atividade na janela recente

5. `lost_list` / `lost_list_by_dimension`
   - variante listagem
   - por dimensão: semântica por par `(Dimensao, Entidade)`

## Slots obrigatórios e opcionais

### Obrigatórios
- `entity` = customer | product
- `operation`
- `recent_days` quando aplicável
- `inactivity_days` quando aplicável
- `moving_months` quando aplicável

### Opcionais
- `dimension` = sales_organization
- `output_shape` implícito na operação (count, list, monthly_count)

## Guardrails e defaults

- faturação válida: `f.BillingDocumentIsCancelled = 0`
- `reativado` default: 30 dias recentes + 180 dias de inatividade anterior
- `perdido` default: 90 dias recentes
- quando a pergunta é por organização de vendas, o raciocínio é por par `(OrganizacaoVendas, Entidade)`
- nenhuma regra desta família depende de `GrossMargin` ou `NetCommercialSales`, logo não se aplica por defeito o filtro `IsItAnAdditionalCalculatedRecord = 1`

## Validação medida

### Benchmark da família
- perguntas testadas: 3
- PASS: 3
- FAIL: 0

### Generalização fora do benchmark
- casos novos testados: 8
- PASS: 8
- FAIL: 0

### Regressão final da família após último ajuste
- total reexecutado nesta revisão: 11
- PASS: 11
- FAIL: 0

## Casos novos fora do benchmark usados
- G01 produtos reativados 30/180
- G02 clientes perdidos 90 dias por organização de vendas
- G03 contagem de clientes perdidos 60 dias
- G04 produtos com primeira venda mensal no último ano móvel
- G05 produtos reativados no último mês após 120 dias sem vendas
- G06 clientes reativados 45/120
- G07 clientes reativados 30/180 por organização de vendas
- G08 produtos perdidos 75 dias

## Discrepâncias relevantes

- Não foram encontradas discrepâncias de resultado nesta revisão; benchmark da família e casos novos passaram integralmente.
- A divergência antiga Q1–Q60 vs matriz factual mantém-se fora do âmbito desta revisão e continua por reconciliar.

## Próximo backlog recomendado
1. `F16_pareto_80`
2. `F12_rank_within_partition`
3. `F18_multi_metric_topn`
