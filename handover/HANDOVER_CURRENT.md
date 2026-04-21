# HANDOVER CURRENT

## RETOMA RÁPIDA
- última revisão fechada: revR
- última família fechada: top_n_global
- benchmark fechado: 212/268
- backlog aberto: 56/268
- próxima prioridade: top_n
- próximos passos:
  1. fechar top_n
  2. correr regressão da família
  3. criar perguntas novas fora do benchmark
  4. recalcular a contagem global
  5. atualizar repositório canónico

## Nota de fork de sessão
Se houver divergência entre conversa e repositório, prevalece o repositório canónico.

Última consolidação: 2026-04-21 (revR top_n_global closed)

## Estado factual consolidado
- benchmark total: 268 perguntas
- benchmark fechado com evidência canónica sincronizada: 212/268
- backlog residual atual: 56/268

## Fecho desta revisão
- família fechada: top_n_global
- benchmark da família: 12/12 PASS
- generalização fora do benchmark: 6/6 PASS

## Contagens por bloco
- Q1-Q60: 60/60 fechadas
- Q61-Q150: 56 fechadas
- Q151-Q268: 96 fechadas

## Evidência canónica relevante
- generators/topn_global_generator.py
- validation/revR/topn_global_benchmark_validation.csv
- validation/revR/topn_global_generalization_eval.csv
- validation/revR/topn_global_generalization_cases.md
- validation/revR/topn_global_notes.md
- validation/revR/global_counts_after_revR.csv

## Próxima prioridade
1. top_n
2. cancellation
3. rank_within_partition
4. distinct_count
