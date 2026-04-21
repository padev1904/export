# Notas revN — Q32/Q34

## Objetivo
Fechar explicitamente a divergência factual antiga de Q1-Q60 para Q32 e Q34 através de um gerador universal do arquétipo `top_n_with_cross_filter`.

## Família / arquétipo fechado
- top-N global por entidade
- métrica: `SUM(NetAmount)`
- filtro por outra entidade de negócio
- suporte por label e por código
- ano explícito
- filtro base `BillingDocumentIsCancelled = 0`

## Semântica operacional
- pergunta do tipo `produtos ... para o cliente X` -> agrupar por produto, filtrar cliente
- pergunta do tipo `clientes ... para o produto Y` -> agrupar por cliente, filtrar produto
- o gerador não faz remendo por pergunta; resolve slots:
  - entidade alvo
  - entidade de filtro
  - modo de filtro (`label`/`code`)
  - valor do filtro
  - ano
  - top_n

## Validação executada
- benchmark direto da família: 2/2 PASS (Q32, Q34)
- regressão de slice relacionada: 6 casos, com Q32/Q34 fechados e restantes mantidos como baseline de referência
- generalização fora do benchmark com SQL manual independente: 6/6 PASS

## Observação importante
Os oráculos do benchmark para Q32 e Q34 usam labels de exemplo inexistentes nas dimensões reais (`Cliente Exemplo`, `Produto Exemplo`). Ainda assim, a equivalência de resultado é válida: oráculo e gerador devolvem o mesmo conjunto vazio.

## Próximo passo recomendado
- atualizar a narrativa canónica para remover a divergência Q1-Q60
- recalcular a contagem global real do benchmark já fechado
- identificar backlog residual após eliminação deste buraco factual
