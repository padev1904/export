# RETOMA CHECKLIST

## Antes de continuar o projeto
1. ler `README.md`
2. ler `handover/HANDOVER_CURRENT.md`
3. ler `handover/CHANGELOG.md`
4. ler `handover/ARTEFACTS_INDEX.md`
5. confirmar `handover/SAFE_SOURCE_MANIFEST.md`
6. confirmar backlog atual em `HANDOVER_CURRENT.md`

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
6. manter o repositório canónico consistente com o estado real do trabalho

## Antes de fechar a revisão
1. produzir gerador canónico da família
2. produzir matriz benchmark da família
3. produzir matriz de generalização
4. produzir casos de generalização documentados
5. atualizar `HANDOVER_CURRENT.md`
6. acrescentar delta a `CHANGELOG.md`
7. atualizar `ARTEFACTS_INDEX.md`
8. rever se foi criada nova redundância documental

## Próximo alvo atualmente acordado
1. `F16_pareto_80`
2. `F12_rank_within_partition`
3. `F18_multi_metric_topn`
