# ALLOW-LIST DE MIGRAÇÃO (FASE 3) — DEC-3

**ID:** MIG-ALLOWLIST-V6 · **Regra:** contrato → interface → teste → implementação (CFO-02)

> Migrar **apenas** os componentes abaixo, **um a um**, cada um passando por GATE-3
> (contrato + interface + teste verde + aprovação Taskade). **Proibido copiar em massa.**

| ID | Componente | Pré-condição obrigatória | Contrato | Interface | Teste | Aprovado Taskade | Status |
|----|-----------|--------------------------|:--------:|:---------:|:-----:|:----------------:|--------|
| MIG-1 | EMA/Indicator Engine | Chaves de indicador padronizadas (resolve FND-11) | ⬜ | ⬜ | ⬜ | ⬜ | PENDENTE |
| MIG-2 | MT5 Connector | Falha ⇒ HOLD; sem fallback sintético (resolve FND-06) | ⬜ | ⬜ | ⬜ | ⬜ | PENDENTE |
| MIG-3 | Position Manager | — | ⬜ | ⬜ | ⬜ | ⬜ | PENDENTE |
| MIG-4 | Risk Manager (Adaptive) | SL/TP derivam do sinal (resolve FND-04) | ⬜ | ⬜ | ⬜ | ⬜ | PENDENTE |
| MIG-5 | Order Manager | trade_mode correto + 1 caminho de execução | ⬜ | ⬜ | ⬜ | ⬜ | PENDENTE |

## Regra de bloqueio
Nenhum componente entra no `main` sem **todas** as 4 colunas marcadas.
GATE-DEMO (execução em conta DEMO) só após MIG-1..5 completos.
