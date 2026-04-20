# CHANGELOG

## 2026-04-20 — revK pareto closure
- fechamento canónico da família `F16_pareto_80`
- promoção de `generators/pareto_generator.py` para a versão canónica `revK`
- validação executável do subset benchmark `Q203/Q204/Q205`
- compatibilidade com benchmark legado: `3/3 PASS`
- medição explícita do impacto da fronteira antes/depois e do guardrail de contributos positivos
- criação de `validation/revK/f16_pareto_benchmark_validation.csv`
- criação de `validation/revK/f16_pareto_family_regression.csv`
- criação de `validation/revK/f16_pareto_generalization_eval.csv`
- criação de `validation/revK/f16_pareto_generalization_cases.md`
- criação de `validation/revK/f16_pareto_notes.md`
- generalização fora do benchmark com SQL manual independente: `8/8 PASS`
- regressão integral da família em `revK`: `14/14 PASS`
- atualização de `HANDOVER_CURRENT.md`, `CHANGELOG.md`, `ARTEFACTS_INDEX.md`, `RETOMA_CHECKLIST.md` e `README.md`
- `validation/revJ/` deixa de ser a referência canónica de Pareto e é removido para evitar redundância

## 2026-04-20 — revJ pareto start
- início canónico da família `F16_pareto_80`
- criação de `generators/pareto_generator.py`
- criação de `validation/revJ/pareto_benchmark_subset.csv`
- criação de `validation/revJ/pareto_benchmark_notes.md`
- atualização de `HANDOVER_CURRENT.md` para refletir `revJ` em progresso
- formalização explícita da divergência entre benchmark Pareto legado e semântica canónica de fronteira

## 2026-04-20 — revI lifecycle sync completion
- sincronização técnica de `revE` a partir do ficheiro `handover_pack_2026-04-20_revE.zip` fornecido pelo utilizador
- criação de `generators/lifecycle_generator.py`
- criação de `validation/revE/lifecycle_benchmark_validation.csv`
- criação de `validation/revE/lifecycle_generalization_eval.csv`
- criação de `validation/revE/lifecycle_generalization_cases.md` em formato canónico resumido
- remoção de `validation/revE/PENDING_SYNC_NOTE.md`
- atualização de `README.md`, `HANDOVER_CURRENT.md`, `RETOMA_CHECKLIST.md` e `ARTEFACTS_INDEX.md`
- o repositório fica sincronizado, à data, para `revD` e `revE`

## 2026-04-20 — revH handover consolidation
- atualização de `HANDOVER_CURRENT.md` para refletir o estado canónico real do repositório
- atualização de `README.md` com distinção entre `revD` sincronizado e `revE` ainda pendente de sincronização técnica nesta sessão
- atualização de `RETOMA_CHECKLIST.md` para priorizar a sincronização técnica de `revE` antes de novas famílias
- manutenção explícita da divergência factual Q1-Q60 (Q32/Q34) no handover corrente
- reforço das regras de higiene documental e de não retenção de ZIPs/handovers redundantes

## 2026-04-20 — revG technical sync
- sincronização da camada técnica canónica disponível nesta sessão
- criação de `generators/temporal_generator.py`
- criação de `validation/revD/tsql_emulator_benchmark_exec.csv`
- criação de `validation/revD/temporal_benchmark_validation.csv`
- criação de `validation/revD/temporal_generalization_eval.csv`
- criação de `validation/revD/temporal_generalization_cases.md`
- criação de `validation/revE/PENDING_SYNC_NOTE.md`
- `revE` continua documentado, mas pendente de sincronização técnica nesta sessão por ausência dos ficheiros locais correspondentes

## 2026-04-20 — revF documental
- consolidação da estrutura documental canónica
- eliminação de redundâncias entre README, state reconstructed e handovers por revisão
- criação de `HANDOVER_CURRENT.md`
- criação de `RETOMA_CHECKLIST.md`
- criação de `ARTEFACTS_INDEX.md`
- criação de lista explícita de documentos redundantes a remover

## 2026-04-20 — revE
- fechamento da família `F17_lifecycle`
- benchmark da família: 3/3 PASS
- generalização fora do benchmark: 8/8 PASS
- regressão final da família em revE: 11/11 PASS
- semântica operacional de `reactivated` e `lost` formalizada

## 2026-04-20 — revD
- emulador parcial T-SQL orientado ao benchmark operacional
- execução de 268/268 SQL de referência do benchmark
- validação executável do gerador temporal
- benchmark temporal: 43/43 PASS por equivalência semântica
- generalização temporal fora do benchmark: 8/8 PASS

## 2026-04-20 — revA
- bootstrap do repositório
- política explícita de não publicação do ZIP bruto
- reconstrução inicial do estado do projeto
- inventário estrutural seguro das fontes
- registo da divergência factual Q1-Q60
