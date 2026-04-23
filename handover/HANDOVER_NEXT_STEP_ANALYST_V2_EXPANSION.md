# HANDOVER NEXT STEP — analyst_free_questions_v2 expansion

## Contexto
Existe um novo lote de 20 perguntas fora do benchmark (`B01`–`B20`) formulado em linguagem de analista sénior, sem partir do catálogo de famílias técnicas.

## Estado já confirmado
- lote criado em `validation/revY/analyst_free_questions_v2.csv`
- cobertura por execução local confirmada em `10/20`
- gap remanescente fora do benchmark neste lote: `10/20`
- `WS4` fechado por equivalência local em:
  - `B02`
  - `B08`
  - `B10`
  - `B12`
  - `B14`
  - `B18`

## Objetivo da próxima sessão
Ampliar a camada técnica canónica para responder progressivamente às 10 perguntas ainda bloqueadas, em blocos de capacidade reutilizável.

## Entrada obrigatória
1. `handover/FORK_RECOVERY_PROTOCOL.md`
2. `handover/HANDOVER_CURRENT.md`
3. `handover/HANDOVER_NEXT_STEP_ANALYST_V2_EXPANSION.md`
4. `validation/revY/analyst_free_questions_v2.csv`
5. `validation/revY/analyst_free_questions_v2_gap_matrix.csv`
6. `validation/revY/analyst_free_questions_v2_expansion_plan.md`
7. `validation/revY/analyst_free_questions_v2_ws4_equivalence_eval.csv`
8. `validation/revY/analyst_free_questions_v2_ws4_notes.md`

## Primeira subtarefa recomendada
Atacar `WS1` do plano de expansão (`nested share / partition share`), porque é agora o workstream remanescente com maior cobertura imediata e maior reutilização transversal.

## Saída mínima esperada da próxima sessão
- atualização do(s) gerador(es) visado(s)
- SQL manual independente para as perguntas cobertas nessa sessão
- SQL gerado pelo código real atualizado
- execução local e comparação por equivalência
- atualização de `HANDOVER_CURRENT.md`, `ARTEFACTS_INDEX.md` e `CHANGELOG.md`

## Regra crítica
Não reabrir benchmark fechado. Esta linha permanece fora do benchmark salvo decisão explícita em contrário.
