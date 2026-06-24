# ADR-008 — Runtime Soberano

- **Status:** ✅ Aceito (ratificado no GATE-0, Ata do Conselho 2026-06-22)
- **Origem:** GATE-0-DECL-V6 · TASK-0011
- **Supersede:** — (complementa ADR-007)
- **Resolve (por exclusão/governança):** BUG-007 (FND-01, 2 motores paralelos), BUG-005 (RT-01, motor legacy não inicializa)

## Contexto
No V5.5 coexistiam **dois motores paralelos** (`shadow_loop.py` e `shadow_loop_v33_final.py`)
sem um runtime soberano declarado. Ninguém podia afirmar com 100% de certeza qual era o runtime
canônico — o código auditado nem sempre era o executado. Isso configurava um problema de
**governança** (BUG-007/FND-01), agravado pela falha de inicialização do motor legacy (BUG-005/RT-01).

## Decisão
Existe **um único runtime soberano**: o processo iniciado pelo launcher soberano (ADR-009),
composto **exclusivamente** pelos módulos do pipeline V6 (ADR-010), executando sob **um**
`OMEGA_ENV` (ADR-011).

- Os motores legacy são **NÃO MIGRAR** e permanecem apenas no `OMEGA_V55_FROZEN` (read-only).
- Nenhum motor/processo paralelo é permitido no V6.

## Consequências
- **(+)** Propriedade e rastreabilidade claras: 1 runtime, 1 verdade de execução.
- **(+)** Elimina a "arqueologia" de descobrir qual código roda.
- **(−)** Exige reconstruir os componentes via trilhas MIG-1..5 (não há atalho de "copiar tudo").
- **Dependência:** ADR-009 (launcher), ADR-010 (fluxo), ADR-011 (ambiente).
