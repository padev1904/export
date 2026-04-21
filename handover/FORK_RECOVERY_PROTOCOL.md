# FORK RECOVERY PROTOCOL

## Objetivo
Este projeto pode ser retomado a partir de um fork de sessão criado pela edição de uma instrução antiga da conversa.

Nesses casos, a conversa atual pode estar desfasada do estado real mais recente do trabalho.

A fonte de verdade é sempre o repositório canónico, não a memória da conversa.

## Regra principal
Se houver divergência entre conversa e repositório, prevalece sempre o repositório canónico.

## Procedimento obrigatório de retoma
1. consultar o repositório canónico
2. ler por esta ordem:
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

Essa secção deve indicar:
1. ficheiros a ler no repositório no próximo arranque
2. última família fechada
3. benchmark fechado e backlog aberto
4. próxima prioridade operacional
5. subtarefa concreta seguinte

## Objetivo operacional
Garantir continuidade correta mesmo quando o utilizador faz fork da sessão recuando para um ponto muito anterior da conversa.
