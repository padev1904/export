# monthly generalization candidate notes

## Objetivo
Expandir a validação fora do benchmark para os arquétipos mensais consolidados na camada técnica pós-`revY`, sem promover como validados casos ainda não executados.

## Estado destes casos
Os casos em `validation/revY/monthly_generalization_candidate_cases.csv` são **candidatos de validação**.
Não representam PASS/FAIL nem substituem validação por equivalência de resultado.

## Porque estes casos foram escolhidos
Cobrem precisamente os blocos que ganharam suporte ou consolidação recente no `temporal_generator`:
- mensal por `grupo de contas de cliente`
- mensal por `organização de vendas`
- mensal por `tipo de processamento de devolução`
- métrica mensal `list_minus_net`
- janelas mensais em `ano atual`, `ano corrente`, ano explícito e últimos 6 meses
- regra documental de `GrossMargin` com `IsItAnAdditionalCalculatedRecord = 1`

## Uso recomendado
1. gerar SQL com o gerador universal atual
2. construir SQL manual independente
3. comparar por equivalência de resultado
4. só depois registar PASS/FAIL canónico
