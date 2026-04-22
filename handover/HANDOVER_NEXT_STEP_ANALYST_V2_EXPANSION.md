# HANDOVER NEXT STEP — analyst_free_questions_v2 expansion

## Contexto
Existe um novo lote de 20 perguntas fora do benchmark (`B01`–`B20`) formulado em linguagem de analista sénior, sem partir do catálogo de famílias técnicas.

## Estado já confirmado
- lote criado em `validation/revY/analyst_free_questions_v2.csv`
- 4 perguntas executadas com equivalência confirmada na base aceite `f_invoice_sample.csv`
- 16 perguntas bloqueadas por gap real de capacidade dos geradores atuais

## Objetivo da próxima sessão
Ampliar a camada técnica canónica para responder progressivamente às 16 perguntas ainda bloqueadas, em blocos de capacidade reutilizável.

## Entrada obrigatória
1. `handover/FORK_RECOVERY_PROTOCOL.md`
2. `handover/HANDOVER_CURRENT.md`
3. `handover/HANDOVER_NEXT_STEP_ANALYST_V2_EXPANSION.md`
4. `validation/revY/analyst_free_questions_v2.csv`
5. `validation/revY/analyst_free_questions_v2_gap_matrix.csv`
6. `validation/revY/analyst_free_questions_v2_expansion_plan.md`

## Primeira subtarefa recomendada
Atacar `WS4` do plano de expansão (`rank derived / multi-partition`), porque fecha o maior volume de perguntas do lote `B` com maior reutilização transversal.

## Saída mínima esperada da próxima sessão
- atualização do(s) gerador(es) visado(s)
- SQL manual independente para as perguntas cobertas nessa sessão
- SQL gerado pelo código real atualizado
- execução local e comparação por equivalência
- atualização de `HANDOVER_CURRENT.md`, `ARTEFACTS_INDEX.md` e `CHANGELOG.md`

## Regra crítica
Não reabrir benchmark fechado. Esta linha permanece fora do benchmark salvo decisão explícita em contrário.
