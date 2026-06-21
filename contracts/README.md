# contracts/ — Contratos primeiro (Emenda CFO-02)

**Regra de ouro (OBRIGATÓRIA):** no V6, a ordem de construção é

```
Contratos → Interfaces → Testes → Implementação
```

Nunca `Código → Código → Mais código → Descobrir depois`.

## O que vive aqui

Definições **antes** de qualquer implementação:

- **Contratos de dados** (schemas de market data, indicadores, sinais).
- **Interfaces** (protocolos/ABCs) de cada componente soberano:
  - `IndicatorEngine` (resolve a raiz do FND-11 — chaves de indicador padronizadas)
  - `MarketDataConnector` (falha ⇒ HOLD; **sem** fallback sintético — anti-FND-06)
  - `PositionManager`
  - `RiskManager` (SL/TP derivam do sinal — anti-FND-04)
  - `OrderManager` (um único caminho de execução; `trade_mode` correto)
- **Contratos de telemetria** (eventos com IDs, lineage decisão→execução).

## Regra de migração (allow-list)

Um componente do `OMEGA_V55_FROZEN` só pode ser portado quando:

1. Seu **contrato** existe aqui e foi revisado.
2. Sua **interface** está definida.
3. Existe **teste** verde cobrindo o contrato.
4. Há **aprovação documental no Taskade** (GATE-3).

Ver `governance/MIGRATION_ALLOWLIST.md`.
