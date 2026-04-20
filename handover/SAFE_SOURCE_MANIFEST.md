# SAFE SOURCE MANIFEST

## Finalidade
Inventário estrutural seguro das fontes locais usadas no projeto.
Este documento não replica dados de negócio brutos.

## Estrutura confirmada
- `training_data/ddl/`
- `training_data/documentation/`
- `training_data/example_queries/`

## Ficheiros relevantes confirmados
- `ddl/BIDB_NEW_DLL.sql`
- `ddl/build_output.txt`
- `ddl/f_invoice_distincts.csv`
- `documentation/01_source_truth_overrides.md`
- `documentation/02_dimension_tables.md`
- `documentation/03_dimension_columns.md`
- `documentation/04_f_invoice_columns.md`
- `documentation/05_fact_dimension_links.md`
- `documentation/06_join_rules_and_semantics.md`
- `documentation/07_guardrails_and_disallowed_assumptions.md`
- `documentation/business_rules.md`
- 45 ficheiros JSON de dimensão em `documentation/`
- `documentation/f_invoice_sample.csv`
- `example_queries/examples.sql`

## Factos estruturais confirmados
- `examples.sql` contém 268 perguntas
- existem 45 dimensões JSON
- existe amostra factual `f_invoice_sample.csv`

## Política de segurança
Não publicar neste repositório:
- ZIP original
- DDL completo copiado
- CSV/JSON brutos
- amostras de dados de negócio
- bases locais auxiliares

## Uso recomendado
Serve para:
- preservar memória estrutural
- apoiar handover
- justificar a proveniência do contexto
