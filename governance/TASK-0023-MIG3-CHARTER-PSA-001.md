# TASK-0023-MIG3-CHARTER-PSA-001

**Position Manager — Charter Consolidado PSA+AIC**

| Campo | Valor |
|-------|-------|
| **ID** | TASK-0023-MIG3-CHARTER-PSA-001 |
| **Data** | 2026-06-25 |
| **Emitido por** | PSA |
| **Base** | TASK-0023-MIG3-CHARTER-AIC-001 · TASK-0023-PARECER-PSA-001 · DEC-GATE-MIG2 · ADR-012 |
| **Status** | CONSOLIDADO — aguardando deliberação Conselho (DEC-MIG3) |
| **Implementação** | **NÃO AUTORIZADA** até DEC-MIG3 |

---

## VEREDITO PSA

# ✅ FAVORÁVEL COM INCORPORAÇÕES

DIV-AIC-M3-01..05 endereçados. CA-01..CA-08 ratificados. Proibição absoluta de `order_send` em MIG-3 explicitada. Charter pronto para deliberação.

---

## 1. Definição Canônica

**MIG-3 Position Manager** é a **fonte soberana de verdade** sobre exposição e estado de posições no V6.

**Responsabilidade única:** registrar, consultar e validar estado de posições com rastreabilidade ticket-level.

**Proibição absoluta:** `order_send()` — abertura/fechamento de posição é exclusividade de MIG-6.

---

## 2. Posição no Fluxo

**Ordem de migração ADR-012:** MIG-1 → MIG-2 → **MIG-3** → MIG-4 → MIG-5 → MIG-6

**Ordem runtime (quando completo):**

```
[MIG-2] Market Data
        ↓
[MIG-1] Indicators
        ↓
[strategy — futuro]
        ↓
[MIG-5] Signal Validation
        ↓
[MIG-4] Risk Engine ──consulta──▶ [MIG-3] Position Manager (exposure)
        ↓
[MIG-6] Execution Engine ──order_send──▶ broker
        ↓ (fill events)
[MIG-3] Position Manager ◀── apply_event(fill)
        ↓
[telemetry] lineage ticket → posição → decisão
```

**Nota DIV-AIC-M3-02 incorporada:** MIG-3 pode ser implementado e validado (ledger + sync read-only) antes de MIG-6 existir — `apply_event()` testável via mock fills em CI.

---

## 3. Componentes

| Componente | Responsabilidade | Fronteira |
|------------|------------------|-----------|
| `PositionManager` | API soberana de estado | Orquestra ledger + sync |
| `PositionLedger` | Estado interno append-only / event-sourced | Fonte lógica de verdade |
| `PositionSyncAdapter` | Read-only broker sync (`positions_get`, deals) | Não envia ordens |
| `PositionValidator` | Invariantes volume, side, ticket uniqueness | Fail-closed |
| `ExposureCalculator` | Agregação net/gross por symbol | Alimenta MIG-4 |

---

## 4. Localização Canônica

```
OMEGA-KERNEL-SOVEREIGN/
├── contracts/
│   └── position_contract.py         ← contratos (pré-implementação obrigatório)
├── position_manager/
│   ├── __init__.py
│   ├── manager.py                   ← SovereignPositionManager
│   ├── ledger.py                    ← PositionLedger
│   ├── validator.py                 ← PositionValidator
│   ├── exposure.py                  ← ExposureCalculator
│   └── sync/
│       ├── __init__.py
│       └── mt5_sync.py              ← read-only positions_get / deals
└── tests/
    └── test_position_manager_*.py   ← mock ledger + mock broker only
```

---

## 5. Contratos Formais (para `contracts/position_contract.py`)

### Enums

- `PositionSide`: `FLAT · LONG · SHORT`
- `PositionStatus`: `OPEN · CLOSED · PENDING_OPEN · PENDING_CLOSE · DESYNC · ERROR`

### Tipos frozen

- `PositionTicket`: ticket, symbol, side, volume, price_open, price_current, sl, tp, profit, magic, opened_at_utc, closed_at_utc, source_id, lineage_id
- `PositionSnapshot`: symbol, positions, net_volume, gross_volume, status, snapshot_at_utc, request_id, source_id
- `ExposureSummary`: symbol, net_side, net_volume, open_ticket_count, total_unrealized_pnl, computed_at_utc
- `PositionEvent`: event_id, event_type, ticket, symbol, payload, timestamp_utc, correlation_id, source

### Protocol `PositionManager`

- `get_snapshot(symbol) → PositionSnapshot`
- `get_exposure(symbol) → ExposureSummary`
- `apply_event(event) → None` — chamado por MIG-6, nunca inferido internamente
- `sync_from_broker(symbol) → PositionSnapshot` — READ-ONLY, nunca `order_send`
- `is_flat(symbol) → bool`

### Hierarquia de erros

`PositionError` → `PositionStateError · PositionSyncError · PositionNotFoundError · PositionDesyncError`

---

## 6. Fronteiras de Responsabilidade

| Dentro MIG-3 | Fora MIG-3 |
|--------------|------------|
| Registrar posição após fill (via `apply_event`) | `order_send()` — MIG-6 |
| Consultar exposição atual | Decisão BUY/SELL — strategy/MIG-5 |
| Rastrear ticket, magic, volume, side | SL/TP policy — MIG-4 |
| Sync read-only com broker | Reconciliation diff engine — SIVR-1 |
| Fail-closed se estado inconsistente | Market data fetch — MIG-2 |
| Telemetria position events | Kill switch — MIG-6 |

---

## 7. Critérios de Aceite Oficiais

| CA | Critério | CI |
|----|----------|----|
| CA-01 | `position_contract.py` merged antes de `position_manager/` | ✔ |
| CA-02 | Zero `order_send` — grep CI falha se presente | ✔ |
| CA-03 | Fail-closed: estado inválido → `PositionStateError` | ✔ |
| CA-04 | Ticket uniqueness: dois OPEN mesmo ticket → erro | ✔ |
| CA-05 | Determinismo: sequência fixa `PositionEvent` → snapshot idêntico | ✔ |
| CA-06 | `MockBrokerSync` sem MT5 em CI | ✔ |
| CA-07 | Telemetria: `event_id`, `correlation_id`, `timestamp_utc` por evento | ✔ |
| CA-08 | MIG-2 mark price → `price_current` / unrealized PnL | ✔ |

---

## 8. Checklist GATE-MIG3

### Pré-implementação

- [x] Charter AIC produzido e entregue
- [x] Parecer PSA emitido — APROVADO
- [ ] Conselho delibera e autoriza (DEC-MIG3)

### Implementação

- [ ] `contracts/position_contract.py` merged
- [ ] `position_manager/` implementado
- [ ] CA-01..CA-08 verdes em CI
- [ ] Zero `order_send` — grep CI
- [ ] `MIGRATION_ALLOWLIST` MIG-3 ✅

### Prova de integração

- [ ] Mock fills → ledger → snapshot determinístico (CA-05)
- [ ] MIG-2 mark → unrealized PnL (CA-08)
- [ ] `ExposureSummary` + `is_flat()` prontos para MIG-4

---

**PSA — 2026-06-25**  
**Encaminhado ao CFO/Conselho para deliberação.**  
**Implementação: NÃO AUTORIZADA até DEC-MIG3.**
