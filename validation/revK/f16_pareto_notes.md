# F16 Pareto — notas revK

## Factos verificados
- Subset benchmark da família: Q203, Q204 e Q205.
- Compatibilidade com benchmark legado: 3/3 PASS.
- Regressão integral da família nesta revisão: 14/14 PASS.
- Casos novos fora do benchmark: 8/8 PASS.

## Semântica canónica adotada
- Fronteira correta antes/depois: incluir a entidade de corte quando `PercentagemAcumulada > 80` mas `PercentagemAntes < 80`.
- Guardrail de contributos positivos: excluir entidades com métrica agregada `<= 0` antes do ranking Pareto.
- Percentagens em escala 0-100.
- Ordenação estável por métrica descendente e label.

## Observação material
No subset legado Q203-Q205, a lógica do benchmark produz percentagens negativas na amostra móvel de 12 meses, porque o total agregado de `NetAmount` nesse horizonte é negativo. A semântica canónica com guardrail positivo remove esse comportamento degenerado e devolve um corte Pareto interpretável.
