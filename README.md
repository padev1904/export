# Universal T-SQL handover repository

Repositório de continuidade do projeto de geração universal de T-SQL para SQL Server.

## Objetivo
Preservar contexto, decisões, estado validado, backlog e artefactos seguros do projeto, sem publicar dados de negócio brutos.

## Estado atual resumido
- benchmark: 268 perguntas
- revD, revE, revK, revL, revM, revN e revO sincronizados
- revP fecha grouped_aggregate em generators e validation/revP
- benchmark fechado com evidência canónica sincronizada: 187/268
- backlog residual consolidado: 81/268
- próxima prioridade operacional: percentage_share, depois top_n_global, top_n e cancellation
