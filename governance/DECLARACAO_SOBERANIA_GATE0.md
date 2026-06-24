# DECLARAÇÃO FORMAL DE SOBERANIA — GATE-0

**ID:** GATE-0-DECL-V6 · **Repositório:** OMEGA-KERNEL-SOVEREIGN · **Status:** ✅ RATIFICADO (Ata do Conselho 2026-06-22)

> Emenda CFO-03 (OBRIGATÓRIA). As 4 respostas abaixo foram ratificadas por unanimidade.
> Formalizadas nos ADR-008..011.

---

## As 4 perguntas soberanas (ratificadas)

### 1. Qual é o **runtime soberano**? → ADR-008
- **Canônico:** um único runtime — o processo do launcher soberano (ADR-009), composto pelos
  módulos do pipeline V6 (ADR-010), sob um `OMEGA_ENV` (ADR-011).
- **Proibição:** motores paralelos. Legacy = NÃO MIGRAR (BUG-005/007), só no `OMEGA_V55_FROZEN`.

### 2. Qual é o **launcher soberano**? → ADR-009
- **Canônico:** `deployment/omega_run.py` (único).
- **Gating:** exige `OMEGA_ENV` explícito (`--env`); sem ele, **recusa iniciar** (fail-closed).
- **Proibição:** múltiplos launchers, `*_24x7.ps1`, variantes `*_final_fix*`, injeção de flags.

### 3. Qual é o **fluxo soberano**? → ADR-010
- **Canônico:** `data → indicators → strategy → risk → execution → telemetry`.
- **Regras:** fail-closed ⇒ HOLD; sem dados sintéticos; SL/TP do sinal (MIG-4/MIG-6);
  guards + kill switch (MIG-6); chaves de indicador padronizadas por contrato (MIG-1).

### 4. Qual é o **ambiente soberano**? → ADR-011
- **Canônico:** `OMEGA_ENV ∈ {dev, test, demo, exec}`, explícito, isolado por ambiente.
- **Regras:** precedência `arquivo > env` (ou `env` com gating auditado); guard DEMO×REAL no
  Execution Engine — MIG-6 (condição sine qua non do CFO).

---

## Ratificação (TASK-0015)

| Papel | Status | Observação |
|-------|--------|------------|
| CEO | ✅ RATIFICADO | Arquitetura soberana validada |
| CTO / Tech Lead | ✅ RATIFICADO | Responsável técnico do draft |
| CFO | ✅ RATIFICADO | Guard DEMO×REAL é condição sine qua non |
| CQO | ✅ RATIFICADO | fail-closed, sem sintéticos, chaves padronizadas |
| COO | ✅ RATIFICADO | Launcher único + isolamento OMEGA_ENV |

**GATE-0 APROVADO E VIGENTE.**

---

## Vínculo de governança
- Fonte documental: **PSA** (`OMEGA-PSA-AUDIT-WORKSPACE`).
- Fluxo: Conselho → PSA → Especificação → AIC → Implementação → Teste → Merge.
- Decisões: **DEC-GATE0-1..4 ↔ ADR-008..011** · Plano Mestre: **DEC-15 ↔ ADR-012**.
