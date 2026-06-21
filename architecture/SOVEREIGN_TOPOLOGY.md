# TOPOLOGIA SOBERANA — OMEGA V6

**ID:** ARCH-SOV-V6 · **Status:** ⬜ A RATIFICAR (depende de GATE-0)

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
   [4] RiskManager          (SL/TP derivam do sinal; anti-FND-04)
                          |
                          v
   [5] OrderManager         (1 caminho; trade_mode correto)
                          |
                          v
   [6] Telemetry            (eventos com IDs; lineage ponta a ponta)
```

## Princípios de soberania (mapeados a anti-padrões)

| Princípio | Anti-padrão eliminado |
|-----------|------------------------|
| Um runtime / um launcher | múltiplos motores e `*_final_fix*` |
| Sem fallback sintético | FND-06 |
| SL/TP do sinal | FND-04 |
| Chaves de indicador padronizadas (contrato) | FND-11 |
| Gating de ambiente explícito | FND-08 |
| Telemetria com IDs | falta de rastreabilidade ponta a ponta |

## Pendências (GATE-0)
As definições canônicas de runtime/launcher/fluxo/ambiente são ratificadas em
`governance/DECLARACAO_SOBERANIA_GATE0.md` antes da implementação.
