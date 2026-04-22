# analyst free questions v1 — notes

## Objetivo
Criar um novo conjunto de 10 perguntas fora do benchmark, formuladas em linguagem natural de analista de negócio, sem partir do catálogo de famílias como critério de formulação.

## Regra metodológica desta passagem
As perguntas foram desenhadas a partir da documentação de:
- campos de `F_Invoice`
- tabelas dimensão
- ligações facto-dimensão
- regras de join e semântica

A formulação das perguntas foi feita antes da verificação do encaixe técnico nos geradores.

## Execução realizada
Para cada pergunta:
1. foi escrito um SQL manual independente
2. foi produzido o SQL gerado a partir do código real dos geradores universais já estabilizados
3. ambos os SQL foram executados localmente sobre a base reconstruída a partir de:
   - `training_data/documentation/f_invoice_sample.csv`
   - dimensões `.json` necessárias
4. a execução foi feita num motor SQLite local após tradução mecânica do subconjunto T-SQL necessário para execução local
5. os resultados foram comparados por equivalência de dataframe ordenado

## Limite desta evidência
Esta validação é fora do benchmark.
Mantém a decisão operacional já registada no repositório de que `f_invoice_sample.csv` é suficiente para esta linha de validação fora do benchmark.

## Resultado
- 10/10 equivalentes entre SQL manual e SQL gerado
- complexidade variada de média a muito elevada
