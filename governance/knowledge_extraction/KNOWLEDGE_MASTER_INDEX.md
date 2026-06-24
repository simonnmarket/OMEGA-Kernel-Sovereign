# KNOWLEDGE_MASTER_INDEX

**ID:** KMI-V6 · **FASE 1.5 — Extração de Conhecimento** · **Atualizado:** 2026-06-24

> Taxonomia canônica: **BUG-001..010** (FND/RT = referência histórica forense).
> Fonte documental: **PSA** (`OMEGA-PSA-AUDIT-WORKSPACE`). Espelho técnico: repo V6.

---

## Registries vinculados

| Registry | Arquivo | Status |
|----------|---------|--------|
| Bugs | `BUG_REGISTRY.csv` | ✅ canônico (6 MIGs) |
| Fixes | `FIX_REGISTRY.csv` | A validar |
| Decisões | `DECISION_REGISTRY.csv` | ✅ (incl. DEC-15) |
| Runtime | `RUNTIME_REGISTRY.csv` | A validar |
| ADRs | `../adr/README.md` | ✅ (ADR-008..012) |
| Sync | `../SYNC_LOG.md` | ✅ |

---

## Bugs canônicos — eixo de migração (6 MIGs)

| BUG | Sev | Decisão | Ref | MIG |
|-----|-----|---------|-----|-----|
| BUG-001 | CRÍTICO | MIGRAR V6 | FND-11 | MIG-1 |
| BUG-002 | CRÍTICO | MIGRAR V6 | FND-06 | MIG-2 |
| BUG-003 | ALTO | MIGRAR V6 | FND-10 | MIG-1 |
| BUG-004 | ALTO | MIGRAR V6 | FND-08 | MIG-6 |
| BUG-005 | CRÍTICO | NÃO MIGRAR | RT-01 | — |
| BUG-006 | ALTO | MIGRAR V6 | FND-04 | MIG-4 |
| BUG-007 | CRÍTICO | NÃO MIGRAR | FND-01 | — |
| BUG-008 | ALTO | NÃO MIGRAR | RT-02/03 | — |
| BUG-009 | MÉDIO | MIGRAR V6 | FND-02 | MIG-6 |
| BUG-010 | MÉDIO | MIGRAR V6 | FND-03 | MIG-6 |

---

## Critério de saída (GATE-1.5)

- [ ] BUG_REGISTRY validado com evidência `arquivo:linha` no snapshot `OMEGA_V55_FROZEN`.
- [ ] FIX/RUNTIME registries fechados.
- [ ] KMI revisado e aprovado no PSA workspace.
