# OMEGA-KERNEL-SOVEREIGN

**OMEGA Kernel Sovereign — Institutional Trading System with Multi-Strategy Global Orchestrator and Adaptive Risk Management**

> Repositório soberano (V6). Reconstrução controlada após congelamento do V5.5 como evidência
> forense (`OMEGA_V55_FROZEN`).

**Autoridade documental:** PSA → `OMEGA-PSA-AUDIT-WORKSPACE`  
**Autoridade técnica:** AIC → este repositório

---

## Princípios não-negociáveis (soberania)

1. **Um único runtime soberano.** Proibido motores/launchers paralelos.
2. **Sem dados sintéticos no fluxo de decisão.** Falha de dados ⇒ `HOLD`.
3. **Ordem alinhada ao sinal.** SL/TP derivam do sinal (MIG-4/MIG-6).
4. **Um único launcher** com gating explícito (`OMEGA_ENV`).
5. **Telemetria com IDs rastreáveis** ponta a ponta.
6. **Contratos antes de código** (CFO-02).

## Segregação PSA ↔ AIC

| Repo | Autoridade | Escreve |
|------|------------|---------|
| `OMEGA-Kernel-Sovereign` | AIC | Somente AIC |
| `OMEGA-PSA-AUDIT-WORKSPACE` | PSA | Somente PSA |

Comunicação formal: **SYNC-IN / SYNC-OUT** (`governance/SYNC_PROTOCOL.md`).

## Governança (resumo)

| Gate | Significado |
|------|-------------|
| GATE-0 | Soberania ratificada (`DECLARACAO_SOBERANIA_GATE0.md`) |
| GATE-0 GOVERNANÇA | ETAPA 0 fechada (ADR-012, SYNC, 6 MIGs) |
| GATE-1 | V5.5 congelado read-only |
| GATE-1.5 | Registries validados |
| GATE-2 | V6 bootstrap em `dev` |
| GATE-MIG1..6 | Trilhas MIG-1..6 (ADR-012) |
| GATE-DEMO | Após MIG-1..6 |

**Fluxo oficial:**

```
Conselho → PSA → Especificação → AIC → Implementação → Teste → Merge → Deploy
```

Alteração fora deste fluxo: **STATUS = NÃO OFICIAL**.

## Proteção Git (CFO-04)

- Proibido: push direto em `main`, commit sem Task ID, merge sem CI.
- Obrigatório: PR + teste automático + aprovação documental PSA.

## Estrutura

```
OMEGA-KERNEL-SOVEREIGN/
├── governance/      # ADRs, SYNC, registries, GATE-0
├── architecture/    # topologia soberana
├── contracts/       # contratos antes da implementação
├── runtime/         # dev | test | demo | exec
├── strategy/ execution/ telemetry/ tests/ audit/ deployment/
└── archive/
```

## Status atual

- **ETAPA 0 — Governança:** ✅ CONCLUÍDA (commit `7f15073`, CFO-RAT-20260624-002).
- **GATE-0 GOVERNANÇA:** ✅ FECHADO (2026-06-24).
- **Próximo:** TASK-0021 — MIG-1 Charter (PSA prepara; implementação 🔒 bloqueada).
