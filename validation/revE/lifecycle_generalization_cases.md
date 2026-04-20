# Lifecycle generalization cases — revE

Casos fora do benchmark usados para validar generalização da família `F17_lifecycle`.

Semântica operacional adotada:
- `reativado`: atividade recente e ausência de atividade na janela de inatividade imediatamente anterior;
- `perdido`: atividade antes da janela recente e ausência de atividade na janela recente;
- por organização de vendas: semântica por par `(OrganizacaoVendas, Entidade)`.

## Resultado global
- total de casos novos: 8
- total `PASS`: 8
- total `FAIL`: 0

## Casos
| case_id | pergunta | operação | entidade | dimensão | status |
|---|---|---|---|---|---|
| G01 | Quais os produtos reativados nos últimos 30 dias após 180 dias sem vendas? | reactivated_list | product | - | PASS |
| G02 | Quais os clientes perdidos nos últimos 90 dias por organização de vendas? | lost_list_by_dimension | customer | sales_organization | PASS |
| G03 | Quantos clientes perdidos existem nos últimos 60 dias? | lost_count | customer | - | PASS |
| G04 | Mostra o número mensal de produtos com primeira venda no último ano móvel. | first_purchase_monthly_count | product | - | PASS |
| G05 | Quantos produtos foram reativados no último mês após 120 dias sem vendas? | reactivated_count | product | - | PASS |
| G06 | Quais os clientes reativados nos últimos 45 dias após 120 dias sem compras? | reactivated_list | customer | - | PASS |
| G07 | Quantos clientes foram reativados nos últimos 30 dias após 180 dias sem compras por organização de vendas? | reactivated_count | customer | sales_organization | PASS |
| G08 | Quais os produtos perdidos nos últimos 75 dias? | lost_list | product | - | PASS |

## Notas
- os resultados foram comparados entre SQL manual independente e SQL do gerador universal
- todas as comparações devolveram equivalência de resultado na `f_invoice_sample`
- o detalhe tabular completo encontra-se resumido em `validation/revE/lifecycle_generalization_eval.csv`
