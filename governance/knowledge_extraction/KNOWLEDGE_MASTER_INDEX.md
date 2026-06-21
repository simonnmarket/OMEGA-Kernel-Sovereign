# KNOWLEDGE_MASTER_INDEX

**ID:** KMI-V6 · **FASE 1.5 — Extração de Conhecimento** · **Emenda CFO-01 (OBRIGATÓRIA)** · **Status:** ⬜ EM PREENCHIMENTO

> Objetivo: inventariar **tudo o que já foi descoberto** no V5.5 antes de qualquer migração,
> para que o V6 **não reconstrua o mesmo erro**. Este índice é o ponto de entrada rastreável
> para os 4 registries abaixo. Fonte de verdade: **Taskade**.

---

## Registries vinculados

| Registry | Arquivo | Conteúdo | Status |
|----------|---------|----------|--------|
| Bugs | `BUG_REGISTRY.csv` | Bugs conhecidos (FND-xx, RT-xx) | ⬜ |
| Fixes | `FIX_REGISTRY.csv` | Correções aplicadas/validadas/refutadas (FMED-xx) | ⬜ |
| Decisões | `DECISION_REGISTRY.csv` | Decisões do Conselho (DEC/VOT) | ⬜ |
| Runtime | `RUNTIME_REGISTRY.csv` | Launchers, code paths, flags, ambientes | ⬜ |

---

## Achados estruturais já documentados (sementes — confirmar e completar no V5.5_FROZEN)

> ⚠️ As entradas abaixo são **referências previamente documentadas** na fase de auditoria,
> trazidas como ponto de partida. **Cada uma deve ser confirmada com evidência `arquivo:linha`
> no `OMEGA_V55_FROZEN`** antes de ser tratada como definitiva.

| ID | Tema | Resumo | Onde detalhar |
|----|------|--------|---------------|
| FND-02 | Estado órfão | Lockfile órfão (`omega_runner.lock`) | BUG_REGISTRY |
| FND-03 | Configuração | `live_flags.json` congelado / data de freeze expirada | BUG_REGISTRY |
| FND-04 | Execução | SL/TP fixos; execução ignora SL/TP do sinal | BUG_REGISTRY |
| FND-06 | Dados | Fallback de dados sintéticos no fluxo de decisão | BUG_REGISTRY |
| FND-08 | Configuração | Precedência `env > arquivo` sem gating | BUG_REGISTRY |
| FND-11 | Indicadores | RSI key mismatch (`rsi` vs `rsi_14`) ⇒ RSI None | BUG_REGISTRY |
| RT-01 | Runtime | Crash `NameError: MT5BulletproofLayer` no motor legacy | RUNTIME_REGISTRY |
| RT-03 | Runtime | Overnight: 13.640 decisões 100% HOLD, confiança 0.0 | RUNTIME_REGISTRY |
| FMED-05B | Fix | Claim "SISTEMA PRONTO" — refutado (FND-11 persistia) | FIX_REGISTRY |

---

## Critério de saída (GATE-1.5)
- [ ] 4 registries preenchidos e versionados.
- [ ] Cada bug crítico com evidência `arquivo:linha` no snapshot congelado.
- [ ] KMI revisado e aprovado no Taskade.
