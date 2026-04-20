# Manifesto seguro de fontes — 2026-04-20 revA

## Objetivo
Registar o que foi verificado localmente sem publicar dados brutos.

## Estrutura validada do ZIP
- `training_data/ddl/`
- `training_data/documentation/`
- `training_data/example_queries/`

## Conteúdo validado
- DDL principal: `training_data/ddl/BIDB_NEW_DLL.sql`
- Output auxiliar de build: `training_data/ddl/build_output.txt`
- Distintos da facto: `training_data/ddl/f_invoice_distincts.csv`
- Documentação Markdown: 8 ficheiros
- Dimensões JSON: 45 ficheiros
- Amostra da facto: `training_data/documentation/f_invoice_sample.csv`
- Benchmark SQL: `training_data/example_queries/examples.sql`

## Documentação Markdown validada
- `01_source_truth_overrides.md`
- `02_dimension_tables.md`
- `03_dimension_columns.md`
- `04_f_invoice_columns.md`
- `05_fact_dimension_links.md`
- `06_join_rules_and_semantics.md`
- `07_guardrails_and_disallowed_assumptions.md`
- `business_rules.md`

## Validações efetuadas
- Contagem de perguntas em `examples.sql`: 268
- Existência de `f_invoice_sample.csv`: sim
- Existência de `examples.sql`: sim

## Política
Este manifesto não deve ser confundido com publicação da fonte.
Não inclui:
- CSVs brutos
- JSONs de dimensão
- DDL completo
- amostras de linhas
- conteúdo do benchmark
