# FORK RECOVERY PROTOCOL

## Objetivo
Este projeto pode ser retomado a partir de um fork de sessão criado pela edição de uma instrução antiga da conversa.

Nesses casos, a conversa atual pode estar desfasada do estado real mais recente do trabalho.

A fonte de verdade é sempre o repositório canónico, não a memória da conversa.

## Regra principal
Se houver divergência entre:
- histórico da conversa
- mensagens antigas da sessão
- instruções reutilizadas em forks
- estado documentado no repositório

prevalece sempre o repositório canónico.

## Procedimento obrigatório de retoma
Ao entrar numa sessão que possa ser um fork:

1. consultar o repositório canónico
2. ler pela seguinte ordem:
   - `handover/HANDOVER_CURRENT.md`
   - `handover/RETOMA_CHECKLIST.md`
   - `handover/ARTEFACTS_INDEX.md`
   - `handover/CHANGELOG.md`
3. reconstruir o estado real do projeto a partir desses ficheiros
4. identificar:
   - última revisão fechada
   - última família fechada
   - benchmark fechado atual
   - backlog residual atual
   - próxima prioridade operacional
5. prosseguir a partir desse ponto, sem repetir trabalho já fechado
6. atualizar novamente o repositório no fim da revisão

## Regras de execução
- não assumir que a conversa atual contém o progresso mais recente
- não assumir que uma instrução antiga representa o estado atual
- não confiar em resumos narrativos antigos se o repositório disser outra coisa
- não criar novas árvores documentais paralelas
- manter apenas a árvore canónica do repositório atualizada

## Regra de conflito
Se a conversa disser uma coisa e `HANDOVER_CURRENT.md` disser outra, seguir `HANDOVER_CURRENT.md`.

Se `HANDOVER_CURRENT.md` e a evidência técnica canónica divergirem, seguir a evidência técnica canónica e corrigir o handover.

## Evidência técnica canónica
A evidência técnica válida deve viver apenas em:
- `generators/`
- `validation/rev*/`
- `handover/`
- `repo_structure/`

## Objetivo operacional
Garantir continuidade correta mesmo quando o utilizador faz fork da sessão recuando para um ponto muito anterior da conversa.
