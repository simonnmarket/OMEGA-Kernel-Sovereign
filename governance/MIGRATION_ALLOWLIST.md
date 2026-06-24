# ALLOW-LIST DE MIGRAÇÃO (FASE 3) — DEC-3 / DEC-15

**ID:** MIG-ALLOWLIST-V6 · **Regra:** contrato → interface → teste → implementação (CFO-02)
**Atualizado:** 2026-06-24 (CFO-RAT-20260623-03 — modelo oficial **6 MIGs**, ADR-012)

> Migrar **apenas** os componentes abaixo, **um a um**, cada um passando por GATE-3
> (contrato + interface + teste verde + aprovação PSA). **Proibido copiar em massa.**

| ID | Componente | Resolve (BUG) | ADR | Contrato | Interface | Teste | Aprovado PSA | Status |
|----|-----------|---------------|-----|:--------:|:---------:|:-----:|:------------:|--------|
| MIG-1 | Indicator Engine | BUG-001 + BUG-003 | ADR-010 | ⬜ | ⬜ | ⬜ | ⬜ | PENDENTE |
| MIG-2 | Market Data Engine | BUG-002 | ADR-010 | ⬜ | ⬜ | ⬜ | ⬜ | PENDENTE |
| MIG-3 | Position Manager | — | — | ⬜ | ⬜ | ⬜ | ⬜ | PENDENTE |
| MIG-4 | Risk Engine | BUG-006 (SL/TP do sinal) | ADR-010 | ⬜ | ⬜ | ⬜ | ⬜ | PENDENTE |
| MIG-5 | Signal Validation Layer | (arquitetural) | ADR-012 | ⬜ | ⬜ | ⬜ | ⬜ | PENDENTE |
| MIG-6 | **Execution Engine Sovereign** | BUG-004, BUG-009, BUG-010 | ADR-009/011/012 | ⬜ | ⬜ | ⬜ | ⬜ | PENDENTE |

## MIG-6 — Execution Engine Sovereign (trilha independente, ratificada CFO)

Não pode ser absorvido em MIG-3/MIG-4/MIG-5. Escopo obrigatório:
- [ ] Order Manager
- [ ] `trade_mode` (validação DEMO/CONTEST/REAL)
- [ ] `OMEGA_ENV` gating (guard DEMO×REAL — anti BUG-004)
- [ ] Broker Connector
- [ ] Order routing
- [ ] Execution guards
- [ ] **Kill switch**
- [ ] Estado sem lockfiles/flags órfãos (anti BUG-009/010)

## Regra de bloqueio

Nenhum componente entra no `main` sem **todas** as colunas marcadas.
GATE-DEMO só após MIG-1..6 completos (ADR-012).
