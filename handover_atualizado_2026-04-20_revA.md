# Handover atualizado — 2026-04-20 revA

## Âmbito e política de segurança
Este handover foi atualizado nesta sessão para permitir retoma noutra conversa sem depender da janela de contexto.
Não inclui o `training_data.zip` nem dados de negócio brutos.
Inclui apenas documentação derivada, inventário estrutural, regras estáveis e backlog operacional.

## Factos verificados nesta sessão
- O ZIP local `training_data.zip` existe e contém `ddl/`, `documentation/` e `example_queries/`.
- O ZIP contém 8 ficheiros Markdown documentais, 45 ficheiros JSON de dimensões, `f_invoice_sample.csv` e `examples.sql`.
- `examples.sql` contém 268 blocos `-- Question:`.
- O ficheiro `q61_q150_family_map.csv` cobre 90 perguntas (Q61–Q150).
- Os hold-outs anexos nesta sessão têm 12 perguntas em `v1` e 12 perguntas em `v2`.

## Regras estabilizadas validadas
- Âncora central: dbo.F_Invoice.
- Para faturação/vendas, aplicar por defeito BillingDocumentIsCancelled = 0, exceto em perguntas de cancelamento.
- Valor líquido faturado: SUM(f.NetAmount).
- Preço de lista: SUM(f.ZLP1PriceList).
- Desconto de quantidade: SUM(f.ZDQ1QtyDiscount).
- Desconto promocional total: SUM(f.ZDPRPromotional + f.ZCPRPromotionalCampaign + f.REA1PromotionalDiscount).
- Preço médio líquido por unidade: SUM(f.NetAmount) / NULLIF(SUM(f.BillingQuantity), 0).
- Peso líquido médio por unidade: SUM(f.ItemNetWeight) / NULLIF(SUM(f.BillingQuantity), 0).
- GrossMargin e NetCommercialSales: default operacional prudente com IsItAnAdditionalCalculatedRecord = 1 quando relevante.
- Marcas/famílias/tipos de material: resolver via D_Product.
- Grupo de contas/condição de expedição/zona de transporte/geografia de cliente: resolver via D_Customer.
- Quotas e taxas percentuais devem sair em escala 0–100.
- Taxa de cancelamento: consolidar primeiro ao nível de BillingDocument.
- Top N dentro de cada partição em SQL Server: ROW_NUMBER() OVER (PARTITION BY ...) e filtro exterior rn <= N.

## Guardrails operacionais validados
- Não ligar F_Invoice diretamente a D_MaterialType, D_ProductBrand ou D_ProductFamily; usar via D_Product.
- Não ligar F_Invoice diretamente a D_ShippingCondition, D_TranspZone ou D_CustomerAccountGroup; usar via D_Customer.
- Não usar D_MaterialCircana no treino inicial nem D_SDDocumentCategory_lixo como dimensão preferida.
- Não substituir grupo de contas de cliente por grupo de cliente.
- Não substituir condição de expedição por shipping point nem zona de transporte por sales district.
- Não devolver IDs técnicos NID... quando existe descrição legível T....
- Não tratar códigos de negócio como chaves surrogate da F_Invoice; para organização/canal filtrar pelos códigos da dimensão.
- Não usar LIMIT/FETCH FIRST/QUALIFY em SQL Server.
- Não calcular métricas 'por documento' diretamente ao nível da linha; consolidar primeiro por BillingDocument.

## Estado reconstituído
- O objetivo de arquitetura continua a ser: classificador de família → extrator de slots → grounding → gerador SQL por família → validação por equivalência de resultado.
- O foco imediato continua a ser fechar Q61–Q150 antes de avançar para Q151–Q268.
- As famílias dominantes em Q61–Q150 são:
  - rank_within_partition: 27
  - grouped_aggregate: 13
  - top_n: 12
  - percentage_share: 10
  - cancellation: 8
  - time_series: 6
  - distinct_count: 4
  - period_compare: 4
  - avg_per_document: 3
  - other: 2
  - window_trend: 1

## Divergências factuais abertas
1. O handover narrativo e o `project_state_log_v1` resumem Q1–Q60 como fechado em 60/60.
2. A matriz factual `tsql_pass_matrix_q1_q60_v2.csv` anexada nesta sessão mostra:
   - NO_GENERATOR: 2
   - PASS: 58
3. Perguntas ainda não fechadas na matriz factual:
   - Q32: NO_GENERATOR — Quais são os produtos com mais valor líquido faturado em 2026 para o cliente Cliente Exemplo?
   - Q34: NO_GENERATOR — Quais são os clientes com mais valor líquido faturado em 2026 para o produto Produto Exemplo?

## Interpretação operacional recomendada
- Até reconciliação por execução/comparação real, a verdade operacional deve seguir a matriz factual e não o resumo narrativo.
- Isso implica tratar Q32 e Q34 como backlog vivo, não como trabalho encerrado.

## Prioridade de execução recomendada
1. Reconciliar Q32 e Q34.
2. Fechar Q61–Q150 por equivalência de resultado, começando por:
   - rank_within_partition
   - percentage_share
   - cancellation
   - period_compare
3. Só depois consolidar casos especiais e avançar para Q151–Q268.
4. Manter hold-out fora do benchmark como barreira anti-memorização.

## O que atualizar no próximo handover
- contagem real de perguntas fechadas por equivalência de resultado
- novas correções universalizadas por família
- discrepâncias novas entre resumo narrativo e matrizes factuais
- lista de perguntas hold-out executadas vs apenas desenhadas

## Ficheiros-base desta sessão que convém manter no GitHub
- `Handover.txt`
- `project_state_log_v1.md.txt`
- `Family-Strategy-Matrix-v1.md.txt`
- `q61_q150_generator_playbook_v1.md.txt`
- `q61_q150_family_map.csv.txt`
- `tsql_pass_matrix_q1_q60_v2.csv.txt`
- `holdout_questions_v1.csv.txt`
- `holdout_questions_v2.csv.txt`
- este handover derivado atualizado
