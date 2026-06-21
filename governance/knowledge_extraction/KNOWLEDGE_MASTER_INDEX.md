# KNOWLEDGE_MASTER_INDEX

**ID:** KMI-V6 · **FASE 1.5 — Extração de Conhecimento** · **Emenda CFO-01** · **Atualizado:** 2026-06-22

> Ponto de entrada rastreável do conhecimento do V5.5. **Taxonomia canônica: BUG-001..010**
> (FND-xx / RT-xx viram referência histórica — deliberação CFO). Fonte de verdade: **Taskade**.

---

## Registries vinculados

| Registry | Arquivo | Conteúdo | Status |
|----------|---------|----------|--------|
| Bugs | `BUG_REGISTRY.csv` | BUG-001..010 (+ ref FND/RT, ADR, MIG) | ✅ canônico |
| Fixes | `FIX_REGISTRY.csv` | FMED-02..05B (05B = REFUTADO) | A validar |
| Decisões | `DECISION_REGISTRY.csv` | DEC-1..9 + DEC-GATE0-1..4 + mapping ADR | ✅ |
| Runtime | `RUNTIME_REGISTRY.csv` | motores, launchers, flags, ambientes | A validar |
| ADRs | `../adr/README.md` | ADR-008..011 (GATE-0) | ✅ |

---

## Bugs canônicos (BUG-001..010) — eixo de migração

| BUG | Sev | Decisão | Ref | ADR | MIG |
|-----|-----|---------|-----|-----|-----|
| BUG-001 | CRÍTICO | MIGRAR V6 | FND-11 | ADR-010 | MIG-1 |
| BUG-002 | CRÍTICO | MIGRAR V6 | FND-06 | ADR-010 | MIG-2 |
| BUG-003 | ALTO | MIGRAR V6 | FND-10 | ADR-010 | MIG-1 |
| BUG-004 | ALTO | MIGRAR V6 | FND-08 | ADR-009/011 | MIG-5 |
| BUG-005 | CRÍTICO | NÃO MIGRAR | RT-01 | ADR-008 | — |
| BUG-006 | ALTO | MIGRAR V6 | FND-04 | ADR-010 | MIG-5 |
| BUG-007 | CRÍTICO | NÃO MIGRAR | FND-01 | ADR-008 | — |
| BUG-008 | ALTO | NÃO MIGRAR | RT-02/03 | ADR-010 | — |
| BUG-009 | MÉDIO | MIGRAR V6 | FND-02 | ADR-011 | MIG-5 |
| BUG-010 | MÉDIO | MIGRAR V6 | FND-03 | ADR-011 | MIG-5 |

---

## Critério de saída (GATE-1.5)
- [ ] BUG_REGISTRY validado com evidência `arquivo:linha` no snapshot `OMEGA_V55_FROZEN`.
- [ ] FIX/RUNTIME registries fechados.
- [ ] KMI revisado e aprovado no Taskade.
