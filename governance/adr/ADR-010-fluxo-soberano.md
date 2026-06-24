# ADR-010 — Fluxo Soberano

- **Status:** ✅ Aceito (ratificado no GATE-0, Ata do Conselho 2026-06-22)
- **Origem:** GATE-0-DECL-V6 · TASK-0013
- **Supersede:** —
- **Resolve:** BUG-001 (FND-11, RSI key), BUG-002 (FND-06, fallback sintético), BUG-003 (FND-10, 8 filtros PASS), BUG-006 (FND-04, SL/TP), BUG-008 (RT-02/RT-03, logs sintéticos + 100% HOLD)

## Contexto
No V5.5, o caminho de decisão era frágil e enganoso: chave de RSI divergente derrubava a confiança
a 0.0 (HOLD eterno — BUG-001/BUG-008), dados sintéticos podiam alimentar decisões reais
(BUG-002), 8 filtros eram marcados "PASS" sem avaliação (BUG-003) e o SL/TP não derivava do sinal
(BUG-006).

## Decisão
O **fluxo soberano** é único e linear:

```
data → indicators → strategy → risk → execution → telemetry
```

Regras invioláveis:
1. **Fail-closed:** falha em qualquer etapa ⇒ `HOLD` (nunca prosseguir com dado parcial).
2. **Sem dados sintéticos** no caminho de decisão (anti BUG-002).
3. **SL/TP derivam do sinal/risco** (anti BUG-006); aplicação no Execution Engine (MIG-5).
4. **Execution guards + kill switch** obrigatórios antes de qualquer `order_send` (MIG-5).
5. **Chaves de indicador padronizadas por contrato** (anti BUG-001); filtros avaliados
   individualmente, sem "PASS" hardcoded (anti BUG-003).

## Checklist de validação (requisito CQO)
- [ ] Cada indicador tem chave única definida em `contracts/` e teste que falha se a chave divergir.
- [ ] Nenhum caminho retorna dado sintético; ausência de dado ⇒ `HOLD` registrado em telemetria.
- [ ] SL/TP no log de execução == SL/TP do sinal/risco (asserção automatizada).
- [ ] Cada filtro emite resultado individual (PASS/FAIL + razão) na trilha de auditoria.
- [ ] Kill switch testado: aciona e bloqueia `order_send`.

## Consequências
- **(+)** Decisões reproduzíveis e auditáveis ponta a ponta.
- **(+)** Impossível "HOLD eterno silencioso" ou ordem sobre dado falso.
- **(−)** Mais rigor exigido na camada de contratos/testes antes de habilitar execução.
