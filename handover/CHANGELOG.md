# CHANGELOG

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
