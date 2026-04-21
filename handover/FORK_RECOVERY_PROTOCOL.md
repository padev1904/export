# FORK RECOVERY PROTOCOL

## Objetivo
Este projeto pode ser retomado a partir de um fork de sessão criado pela edição de uma instrução antiga da conversa.

Nesses casos, a conversa atual pode estar desfasada do estado real mais recente do trabalho.

A fonte de verdade é sempre o repositório canónico, não a memória da conversa.

## Regra principal
Se houver divergência entre conversa e repositório, prevalece sempre o repositório canónico.

## Prompt de arranque
A prompt de arranque é fixa.
Não deve transportar contexto mutável nem próximos passos variáveis.
A versão canónica da prompt fixa vive em:
- `handover/STARTUP_PROMPT_FIXED.md`

## Procedimento obrigatório de retoma
1. consultar o repositório canónico
2. ler por esta ordem:
   - `handover/FORK_RECOVERY_PROTOCOL.md`
   - `handover/HANDOVER_CURRENT.md`
   - `handover/RETOMA_CHECKLIST.md`
   - `handover/ARTEFACTS_INDEX.md`
   - `handover/CHANGELOG.md`
3. reconstruir o estado real do projeto
4. identificar última revisão, última família fechada, benchmark fechado, backlog aberto e próxima prioridade
5. prosseguir sem repetir trabalho já fechado
6. atualizar o repositório no fim da revisão

## Regra obrigatória no fim de cada resposta
No final de cada resposta de progresso, incluir sempre a secção:
`Próximos passos para a prompt de arranque`

Essa secção não serve para alterar a prompt.
Serve apenas para indicar o que a documentação canónica do repositório deve refletir no próximo arranque.

Essa secção deve indicar:
1. ficheiros a reler no repositório
2. última família fechada
3. benchmark fechado e backlog aberto
4. próxima prioridade operacional
5. subtarefa concreta seguinte

## Objetivo operacional
Garantir continuidade correta mesmo quando o utilizador faz fork da sessão recuando para um ponto muito anterior da conversa.
