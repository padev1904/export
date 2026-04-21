# Top N notes — revS

## Fonte de verdade usada
- repositório canónico `padev1904/export`
- última revisão fechada antes desta: `revR`
- última família fechada antes desta: `top_n_global`
- benchmark fechado anterior: 212/268
- backlog aberto anterior: 56/268

## Delimitação factual do residual top_n
A família `top_n_global` já estava fechada em `revR`.
O gerador `f18_multi_metric_topn_generator.py` já cobre o subespaço multi-métrica.
A família `top_n_with_cross_filter` já tinha sido reconciliada anteriormente.
Combinando a evidência canónica com o mapeamento Q61-Q150, o residual factual desta revisão é:

- Q64
- Q67
- Q71
- Q79
- Q95
- Q110

## Arquétipos fechados nesta revisão
1. documentos com mais de N linhas
2. combinações cliente-produto top-N por faturação
3. crescimento absoluto por cliente entre dois anos
4. documentos com linhas positivas e negativas
5. top-N documentos mistos por valor líquido absoluto

## Resultado benchmark da família
- total coberto: 6
- PASS semântico: 6/6

## Generalização fora do benchmark
- total: 6
- PASS semântico: 6/6

## Contagem global após revS
- benchmark fechado anterior: 212/268
- adicional fechado nesta revisão: 6
- benchmark fechado após revS: 218/268
- backlog residual após revS: 50/268

## Regressão executada
A regressão desta família foi corrida sobre todas as questões do residual top_n cobertas nesta revisão:
Q64, Q67, Q71, Q79, Q95, Q110.
