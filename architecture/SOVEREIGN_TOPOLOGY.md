# TOPOLOGIA SOBERANA — OMEGA V6

**ID:** ARCH-SOV-V6 · **Status:** ✅ RATIFICADO (GATE-0, GATE-MIG1, GATE-MIG2, GATE-MIG3 fechados)

## Fluxo soberano único

```
dados → indicadores → estratégia → risco → execução → telemetria
```

Falha em qualquer etapa ⇒ `HOLD`. Sem desvios, atalhos ou caminhos concorrentes.

## Diagrama (texto)

```
                +-------------------+
 OMEGA_ENV ---> |  LAUNCHER ÚNICO   |   (deployment/, gating de ambiente)
                +---------+---------+
                          |
                          v
   [1] MarketDataConnector  --falha-->  HOLD (nunca sintético)
                          |
                          v
   [2] IndicatorEngine      (chaves padronizadas; anti-FND-11)
                          |
                          v
   [3] Strategy / Orchestrator  (multi-strategy)
                          |
                          v
   [3.5] PositionManager    (estado soberano transversal; consumido por [4] e [6])
                          ^
                          |   (fill events via MIG-6)
   [4] RiskManager --------+   (SL/TP derivam do sinal; anti-FND-04)
                          |
                          v
   [5] OrderManager         (1 caminho; trade_mode correto; order_send exclusivo)
                          |
                          v
   [6] Telemetry            (eventos com IDs; lineage ponta a ponta)
```

**Nota MIG-3:** `PositionManager` é a camada de estado soberano de posições. Ordem de migração: MIG-3 antes de MIG-4/MIG-6. Ordem runtime: MIG-6 fornece fill events ao MIG-3; MIG-4 consulta exposição (`ExposureSummary`, `is_flat()`).

## Princípios de soberania (mapeados a anti-padrões)

| Princípio | Anti-padrão eliminado |
|-----------|------------------------|
| Um runtime / um launcher | múltiplos motores e `*_final_fix*` |
| Sem fallback sintético | FND-06 |
| SL/TP do sinal | FND-04 |
| Chaves de indicador padronizadas (contrato) | FND-11 |
| Gating de ambiente explícito | FND-08 |
| Telemetria com IDs | falta de rastreabilidade ponta a ponta |

## Pendências

- MIG-4 Risk Engine: SL/TP derivam do sinal; consome `ExposureSummary` do MIG-3.
- MIG-5 Signal Validation Layer: validação desacoplada.
- MIG-6 Execution Engine: único ponto de `order_send()`; emite fill events ao MIG-3.
- SIVR-1: reconciliação global — permanece congelada até GATE-MIG6 mínimo.
