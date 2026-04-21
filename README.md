# Universal T-SQL handover repository

Repositório de continuidade do projeto de geração universal de T-SQL para SQL Server.

## Objetivo
Preservar contexto, decisões, estado validado, backlog e artefactos seguros do projeto, sem publicar dados de negócio brutos.

## Política de segurança
Não carregar para este repositório:
- `training_data.zip`
- CSV/JSON/DDLs brutos do projeto
- bases SQLite intermédias
- dumps com dados de negócio

Podem ser carregados:
- documentação derivada
- handover corrente
- changelog
- manifesto estrutural das fontes
- geradores universais
- matrizes de validação e resultados agregados
- casos de generalização com SQL manual independente

## Fonte de verdade documental
1. `handover/HANDOVER_CURRENT.md`
2. `handover/CHANGELOG.md`
3. `handover/SAFE_SOURCE_MANIFEST.md`
4. `handover/RETOMA_CHECKLIST.md`
5. `handover/ARTEFACTS_INDEX.md`
6. `repo_structure/REPO_STRUCTURE_CANONICAL.md`

## Convenção recomendada
- um único handover corrente
- um único changelog
- um único manifesto de fontes
- um único índice de artefactos
- geradores canónicos por família em `generators/`
- validações por revisão em `validation/revX/`

## Estado atual resumido
- benchmark: 268 perguntas
- emulador parcial T-SQL orientado ao benchmark validado com 268/268 SQL de referência executados
- `revD` técnico sincronizado no repositório em `generators/` e `validation/revD/`
- `revE` técnico sincronizado no repositório para `F17_lifecycle` em `generators/` e `validation/revE/`
- `revK` técnico sincronizado no repositório para `F16_pareto_80` em `generators/` e `validation/revK/`
- `revL` técnico sincronizado no repositório para `F12_rank_within_partition` em `generators/` e `validation/revL/`
- `revM` técnico sincronizado no repositório para `F18_multi_metric_topn` em `generators/` e `validation/revM/`
- `revN` técnico sincronizado no repositório para reconciliação explícita de `Q32/Q34` em `generators/` e `validation/revN/`
- próxima prioridade operacional: calcular backlog residual real pós-`Q32/Q34` e consolidar a contagem global final do benchmark
