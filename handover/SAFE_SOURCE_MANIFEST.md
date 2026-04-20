# Safe source manifest

## Incluído apenas como inventário estrutural
Origem local analisada: `training_data.zip`

### Estrutura verificada
- `training_data/ddl/`
- `training_data/documentation/`
- `training_data/example_queries/`

### Ficheiros relevantes verificados no ZIP
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

## Política de segurança
Este manifesto não replica dados de negócio, conteúdos CSV, JSON, DDL completo nem amostras factuais. Serve apenas para:
- provar a existência e composição da fonte
- apoiar handover
- evitar perda de memória estrutural
