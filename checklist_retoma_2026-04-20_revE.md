# Checklist de retoma — revE

## Estado mínimo para continuar sem perda de contexto
- usar `lifecycle_generator_revE.py` como base oficial da família `F17_lifecycle`
- considerar a semântica de `reativado` explicitamente alinhada com o benchmark:
  atividade recente + ausência de atividade na janela imediatamente anterior
- considerar a semântica de `perdido` como default operacional novo:
  atividade anterior + ausência de atividade recente
- preservar a política de não publicar o ZIP bruto nem dados de negócio

## Artefactos a carregar primeiro numa nova sessão
1. `handover_atualizado_2026-04-20_revE.md`
2. `lifecycle_generator_revE.py`
3. `lifecycle_benchmark_validation_revE.csv`
4. `lifecycle_generalization_eval_revE.csv`
5. `lifecycle_generalization_cases_revE.md`
6. `checklist_retoma_2026-04-20_revE.md`

## Validação já concluída
- benchmark lifecycle: 3/3 PASS
- generalização lifecycle: 8/8 PASS
- regressão final revE: 11/11 PASS

## Próximo alvo imediato
- `F16_pareto_80`

## Método a repetir
- formalizar semântica da família
- construir gerador universal
- correr benchmark da família
- reexecutar regressão da própria família
- criar perguntas novas fora do benchmark com SQL manual independente
- atualizar handover e pacote descarregável
