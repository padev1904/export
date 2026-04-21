# Cancellation — perguntas novas fora do benchmark

## C01
- Pergunta: Qual a taxa de cancelamento de documentos por organização de vendas em 2026?
- Operação: rate_by_dimension
- Resultado: PASS

## C02
- Pergunta: Qual a taxa de cancelamento de documentos por país em 2026?
- Operação: rate_by_dimension
- Resultado: PASS

## C03
- Pergunta: Qual a taxa de cancelamento de documentos por canal de distribuição e por mês em 2026?
- Operação: rate_by_month_and_dimension
- Resultado: PASS

## C04
- Pergunta: Quais são os 3 tipos de documento de faturação com maior taxa de cancelamento de documentos em 2026?
- Operação: top_rate_global
- Resultado: PASS

## C05
- Pergunta: Quais são os 2 canais de distribuição com maior taxa de cancelamento de documentos dentro de cada mês em 2026?
- Operação: top_rate_within_month
- Resultado: PASS

## C06
- Pergunta: Qual a taxa de cancelamento de documentos por organização de vendas e por canal de distribuição em 2026?
- Operação: rate_by_two_dimensions
- Resultado: PASS
