# RETOMA CHECKLIST

## Antes de continuar o projeto
1. ler `README.md`
2. ler `handover/HANDOVER_CURRENT.md`
3. ler `handover/CHANGELOG.md`
4. ler `handover/ARTEFACTS_INDEX.md`
5. confirmar `validation/revO/global_benchmark_counts.csv`
6. confirmar `validation/revO/global_benchmark_residual_summary.csv`
7. confirmar `validation/revO/backlog_residual_real.md`

## Antes de trabalhar nova família
1. identificar subconjunto do benchmark da família
2. formalizar a semântica
3. definir slots
4. definir defaults e guardrails
5. confirmar se já existe gerador canónico anterior
6. confirmar se o repositório já está sincronizado com o estado técnico mais recente

## Durante a implementação
1. não hardcode de perguntas do benchmark
2. separar parsing, grounding e síntese SQL
3. usar SQL manual independente nos casos novos
4. medir equivalência de resultado, não elegância
5. reexecutar tudo o que já tinha passado nessa família
6. recalcular a contagem global real após fechar a família
7. manter o repositório canónico consistente com o estado real do trabalho

## Próximo alvo atualmente acordado
1. fechar `grouped_aggregate`
2. fechar `percentage_share`
3. fechar `top_n_global`
4. fechar `top_n`
5. atualizar a contagem global real após cada revisão
