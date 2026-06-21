# Architecture Decision Records (ADR) — OMEGA OS

Registro formal de decisões arquiteturais. Cada ADR documenta **Contexto, Decisão, Status,
Consequências** e (quando aplicável) **Supersede** e **Resolve (BUG/FND)** para rastreamento
bidirecional com o `BUG_REGISTRY` e o `DECISION_REGISTRY` (Taskade = fonte de verdade).

## Índice

| ADR | Título | Status | Supersede | Origem |
|-----|--------|--------|-----------|--------|
| ADR-001 | (reservado no Taskade) | — | — | Taskade |
| ADR-002 | Launcher Legacy | ⬛ Supersedido por ADR-009 | — | Taskade |
| ADR-003 | Proibição de Fallback Sintético | 🟡 Pendente (V6) | — | Taskade |
| ADR-004 | Eliminação dos 8 Filtros PASS | 🟡 Pendente (V6) | — | Taskade |
| ADR-005 | Segregação dev/test/demo/exec | 🟡 Pendente (V6) | — | Taskade |
| ADR-006 | Padronização de Chave RSI | 🟡 Pendente (V6) | — | Taskade |
| ADR-007 | Reconstrução Soberana V6 | ✅ Aprovado | ADR-002 | Taskade |
| **ADR-008** | **Runtime Soberano** | ✅ Aceito (GATE-0) | — | GATE-0-DECL-V6 |
| **ADR-009** | **Launcher Soberano** | ✅ Aceito (GATE-0) | ADR-002 | GATE-0-DECL-V6 |
| **ADR-010** | **Fluxo Soberano** | ✅ Aceito (GATE-0) | — | GATE-0-DECL-V6 |
| **ADR-011** | **Ambiente Soberano** | ✅ Aceito (GATE-0) | — (complementa ADR-005) | GATE-0-DECL-V6 |

> ADR-001..007 são canônicos no Taskade; aqui ficam como referência. ADR-008..011 nascem da
> ratificação do GATE-0 (Ata do Conselho 2026-06-22).

## Mapeamento DEC ↔ ADR (a consolidar no Sync PR / TASK-0018)
| DEC | ADR relacionado |
|-----|-----------------|
| DEC-1 (congelar V5.5) | ADR-001 |
| DEC-2 (criar V6) | ADR-007 |
| DEC-6 (GATE-0) | ADR-008..011 |
