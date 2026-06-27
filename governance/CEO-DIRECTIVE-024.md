# CEO-DIRECTIVE-024 — Política Oficial de Isolamento de Workspaces

**ID:** CEO-DIRECTIVE-024  
**Data:** 2026-06-27  
**Emitido por:** CEO / Conselho  
**Base:** ADR-012 · CEO-DIRECTIVE-023A · DEC-GATE-MIG3-001  
**Status:** DIRETRIZ PERMANENTE — VIGENTE IMEDIATAMENTE

---

## Objetivo

Estabelecer fronteiras operacionais definitivas entre PSA e AIC, eliminando sobreposição de responsabilidades, conflitos de repositório e ciclos de sincronização indevidos.

---

## Workspaces oficiais

| Agente | Workspace | Escopo exclusivo |
|--------|-----------|------------------|
| **PSA** | `OMEGA-PSA-AUDIT-WORKSPACE` | Governança, ADRs, diretivas, pareceres, auditorias, planejamento |
| **AIC** | `OMEGA-Kernel-Sovereign` | Código, contratos, testes, branches, commits, merges, integração |

**Regra permanente:** PSA nunca altera diretamente o Kernel. AIC nunca altera diretamente o Workspace PSA.

---

## Fluxo institucional obrigatório

```
Conselho → PSA (documentação) → Deliberação → AIC (implementação)
→ SYNC-OUT → PSA (validação) → Deliberação Gate → Encerramento
```

Alterações arquiteturais: PSA produz → Conselho aprova → AIC reproduz no Kernel → PSA valida.

---

## Incidente MIG-3 — SOVEREIGN_TOPOLOGY.md

Classificação: **INCIDENTE OPERACIONAL DE FRONTEIRA ENTRE WORKSPACES**

- Sem impacto técnico, funcional ou arquitetural
- Sincronização residual: **exclusivamente AIC**
- Encerramento: após SYNC-OUT AIC da topologia atualizada

---

## Aplicação

Vigente para TASK-0024, MIG-5..6, DEMO, SHADOW, GATE-REAL e EXECUÇÃO REAL.

**Próximo marco:** TASK-0024 — MIG-4 Risk Engine Charter (PSA), após encerramento do incidente topologia.

---

**CEO / Conselho — Emitido e em vigor**
