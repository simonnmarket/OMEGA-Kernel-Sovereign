# ADR-012 — Plano Mestre de Execução V6

- **Status:** ✅ Aceito (CFO-DIR-20260623-02 + CFO-RAT-20260623-03)
- **Origem:** DEC-15 · Plano Mestre CFO
- **Supersede:** mapeamento MIG de 5 trilhas (TASK-0018 inicial) → **6 trilhas oficiais**

## Contexto

Após GATE-0 e integração do PSA como autoridade documental, o projeto necessita de um
roadmap sequencial único desde governança até operação real, sem interrupções paralelas
(CFO-03 — Foco Operacional).

## Decisão

Roadmap executivo oficial:

| Etapa | Componente | Gate | Resolve (BUG) |
|-------|-----------|------|---------------|
| ETAPA 0 | Governança | GATE-0 GOVERNANÇA | — |
| MIG-1 | Indicator Engine | GATE-MIG1 | BUG-001, BUG-003 |
| MIG-2 | Market Data Engine | GATE-MIG2 | BUG-002 |
| MIG-3 | Position Manager | GATE-MIG3 | — |
| MIG-4 | Risk Engine | GATE-MIG4 | BUG-006 |
| MIG-5 | Signal Validation Layer | GATE-MIG5 | (arquitetural) |
| MIG-6 | Execution Engine Sovereign | GATE-MIG6 | BUG-004, BUG-009, BUG-010 |
| — | GATE-DEMO | GATE-DEMO | após MIG-1..6 |
| — | SHADOW MODE | SHADOW | 10 dias úteis mín. |
| — | GATE-REAL | GATE-REAL | após DEMO + SHADOW |
| — | Execução controlada | — | capital reduzido |

**NÃO MIGRAR (evidência forense):** BUG-005, BUG-007, BUG-008

## MIG-6 — Execution Engine Sovereign (trilha independente)

Escopo obrigatório:
- Order Manager
- Trade Mode Validation (DEMO/CONTEST/REAL)
- Broker Connector
- Environment Gating (`OMEGA_ENV`)
- Order routing
- Execution guards
- **Kill switch**
- Guard DEMO×REAL (condição sine qua non CFO)

## Consequências

- **(+)** Sequência única; nenhuma atividade fora do roadmap tem prioridade superior.
- **(+)** Novas descobertas → BACKLOG (exceto risco financeiro/jurídico/segurança/dados).
- **(−)** MIG-1 Charter só inicia após GATE-0 Governança = FECHADO.

## Critérios de parada

Parar imediatamente se: divergência PSA↔GitHub; perda de rastreabilidade; múltiplos runtimes/launchers;
indicadores inválidos; execução fora do ambiente autorizado.
