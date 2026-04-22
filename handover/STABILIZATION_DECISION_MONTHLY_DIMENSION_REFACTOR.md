# STABILIZATION DECISION — monthly dimension refactor

## Factos verificados
- o benchmark canónico permanece fechado em `268/268`
- o backlog factual permanece `0/268`
- a linha fora do benchmark `MG01`–`MG08` ficou aceite com `PASS` em `validation/revY/monthly_generalization_eval.csv`
- a cobertura técnica recente já consolidou os blocos mensais relevantes em `generators/temporal_generator.py`

## Inferência operacional
A refatoração adicional para extrair um novo bloco reutilizável de "mensal por dimensão" tem **baixo valor incremental imediato**.

## Decisão desta sessão
- **não avançar agora** com nova refatoração estrutural do `temporal_generator`
- considerar esse trabalho apenas se surgir uma destas condições:
  1. regressão documental ou semântica
  2. novo conjunto material de casos mensais que torne a abstração claramente vantajosa
  3. duplicação técnica adicional noutros geradores que beneficie de unificação real

## Justificação
- o estado funcional está estabilizado
- não existe backlog benchmark-wide aberto
- a generalização mensal fora do benchmark já ficou aceite nesta sessão
- nova refatoração nesta fase aumenta risco estrutural com retorno limitado

## Regra prática para próximas sessões
Na ausência de evidência nova, tratar o bloco mensal atual como **congelado por estabilização**.
