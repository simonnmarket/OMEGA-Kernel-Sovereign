# ALLOW-LIST DE MIGRAÇÃO (FASE 3) — DEC-3

**ID:** MIG-ALLOWLIST-V6 · **Regra:** contrato → interface → teste → implementação (CFO-02)
**Atualizado:** 2026-06-22 (ratificação CFO — MIG-5 como Execution Engine independente)

> Migrar **apenas** os componentes abaixo, **um a um**, cada um passando por GATE-3
> (contrato + interface + teste verde + aprovação Taskade). **Proibido copiar em massa.**

| ID | Componente | Resolve (BUG) | ADR | Contrato | Interface | Teste | Aprovado | Status |
|----|-----------|---------------|-----|:--------:|:---------:|:-----:|:--------:|--------|
| MIG-1 | Indicator Engine | BUG-001 (RSI key) + BUG-003 (8 filtros PASS) | ADR-010 | ⬜ | ⬜ | ⬜ | ⬜ | PENDENTE |
| MIG-2 | Market Data Engine | BUG-002 (fallback sintético) | ADR-010 | ⬜ | ⬜ | ⬜ | ⬜ | PENDENTE |
| MIG-3 | Position Manager | — | — | ⬜ | ⬜ | ⬜ | ⬜ | PENDENTE |
| MIG-4 | Risk Manager | sizing/risco (níveis de SL/TP) | ADR-010 | ⬜ | ⬜ | ⬜ | ⬜ | PENDENTE |
| MIG-5 | **Execution Engine (Order Manager)** | BUG-006 (SL/TP), BUG-004 (gating) | ADR-009/010/011 | ⬜ | ⬜ | ⬜ | ⬜ | PENDENTE |

## MIG-5 — Execution Engine (trilha independente, ratificada CFO)
Não pode ser absorvido em MIG-3/MIG-4. Escopo obrigatório:
- [ ] `trade_mode` (validação DEMO/CONTEST/REAL)
- [ ] `OMEGA_ENV` gating (guard DEMO×REAL — anti BUG-004/FND-08)
- [ ] Order routing
- [ ] SL/TP derivados do sinal/risco (anti BUG-006/FND-04)
- [ ] Execution guards
- [ ] **Kill switch**

## Regra de bloqueio
Nenhum componente entra no `main` sem **todas** as colunas marcadas.
GATE-DEMO (execução em conta DEMO) só após MIG-1..5 completos.
