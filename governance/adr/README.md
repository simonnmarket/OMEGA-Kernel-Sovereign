# Architecture Decision Records (ADR) — OMEGA Kernel Sovereign V6

Registro formal de decisões arquiteturais. Cada ADR documenta **Contexto, Decisão, Status,
Consequências** e (quando aplicável) **Supersede** e **Resolve (BUG)**.

**Autoridade documental:** PSA (`OMEGA-PSA-AUDIT-WORKSPACE`) · **Espelho técnico:** este diretório.

## Índice

| ADR | Título | Status | Supersede |
|-----|--------|--------|-----------|
| ADR-001 | Congelamento Prudencial | ✅ Aceito | — |
| ADR-002 | Launcher Legacy | ⬛ Supersedido | — |
| ADR-003 | Proibição Fallback Sintético | 🟡 Pendente (V6) | — |
| ADR-004 | Eliminação 8 Filtros PASS | 🟡 Pendente (V6) | — |
| ADR-005 | Segregação de ambientes | 🟡 Pendente (V6) | — |
| ADR-006 | Padronização Chave RSI | 🟡 Pendente (V6) | — |
| ADR-007 | Reconstrução Soberana V6 | ✅ Aprovado | ADR-002 |
| **ADR-008** | **Runtime Soberano** | ✅ Aceito (GATE-0) | — |
| **ADR-009** | **Launcher Soberano** | ✅ Aceito (GATE-0) | ADR-002 |
| **ADR-010** | **Fluxo Soberano** | ✅ Aceito (GATE-0) | — |
| **ADR-011** | **Ambiente Soberano** | ✅ Aceito (GATE-0) | complementa ADR-005 |
| **ADR-012** | **Plano Mestre de Execução V6** | ✅ Aceito | mapeamento 5→6 MIGs |

## Mapeamento DEC ↔ ADR

| DEC | ADR |
|-----|-----|
| DEC-1 | ADR-001 |
| DEC-2 | ADR-007 |
| DEC-6 / DEC-GATE0-* | ADR-008..011 |
| DEC-15 | ADR-012 |
