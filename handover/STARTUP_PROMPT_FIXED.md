# STARTUP PROMPT FIXED

Usar sempre esta prompt, sem alterações:

```text
Consulta o repositório canónico `https://github.com/padev1904/export.git`.

Esta sessão pode ser um fork criado pela edição de uma instrução antiga.
Não assumes que a conversa atual contém o estado mais recente.
A fonte de verdade é o repositório.

Lê e segue, por esta ordem:
1. `handover/FORK_RECOVERY_PROTOCOL.md`
2. `handover/HANDOVER_CURRENT.md`
3. `handover/RETOMA_CHECKLIST.md`
4. `handover/ARTEFACTS_INDEX.md`
5. `handover/CHANGELOG.md`

Depois reconstitui o estado real, identifica a próxima prioridade em aberto a partir da documentação canónica do repositório e prossegue sem duplicar trabalho já fechado.

Se houver divergência entre conversa e repositório, prevalece o repositório.
```

## Regra
- esta prompt é fixa
- não deve ser reescrita em cada revisão
- o contexto mutável e os próximos passos devem existir apenas na documentação canónica do repositório
