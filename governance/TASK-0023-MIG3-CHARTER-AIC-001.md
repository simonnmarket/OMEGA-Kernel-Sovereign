# TASK-0023-MIG3-CHARTER-AIC-001

**Position Manager — Charter Técnico Consolidado (AIC)**

| Campo | Valor |
|-------|-------|
| **ID** | TASK-0023-MIG3-CHARTER-AIC-001 |
| **Data** | 2026-06-25 |
| **Emitido por** | AIC (Architecture & Integration Council) |
| **Destinatários** | PSA · CFO · Conselho |
| **Responde a** | TASK-0023-INITIATION-001 · DEC-GATE-MIG2-001 · ADR-012 |
| **Documento PSA revisado** | TASK-0023 — MIG-3 Charter (PSA workspace) |
| **Base factual** | SABM-001 · DEC-GATE-MIG2-001 · ADR-010 · ADR-012 |
| **Repositório referência** | `OMEGA-Kernel-Sovereign` — MIG-1/MIG-2 validados (branch `sivr-0-run` / `503f5fa`) |
| **Status** | ENTREGUE — aguardando validação PSA + deliberação Conselho |
| **Implementação** | **NÃO AUTORIZADA** por este documento |

---

## VEREDITO AIC (SUMÁRIO)

# FAVORÁVEL COM RESSALVAS DE SEQUÊNCIA

O MIG-3 Position Manager é **mandatório** na sequência canônica ADR-012 e **pré-requisito estrutural** para MIG-4 (Risk), MIG-6 (Execution feedback) e futuro SIVR-1 (reconciliação de estado). O charter consolidado AIC define responsabilidades, contratos, estados, telemetria e critérios de aceite **sem código**.

**Nenhuma linha de código executável** está incluída ou autorizada.

---

## 1. REVISÃO TÉCNICA DO CHARTER PSA

### 1.1 Alinhamentos confirmados (AIC concorda)

| Item | Posição AIC | Base |
|------|-------------|------|
| MIG-3 = Position Manager soberano | ✔ | ADR-012 · `MIGRATION_ALLOWLIST.md` |
| Escopo documental only (TASK-0023-INITIATION-001) | ✔ | Sem order_send / execution |
| Contratos antes de implementação (CFO-02) | ✔ | `contracts/README.md` |
| Rastreabilidade ticket ↔ posição | ✔ | SIVR-1-DESIGN-001 · anti-ghost/orphan |
| Dependências MIG-4..6 e SIVR-1 explícitas | ✔ | Initiation-001 §2 |
| Fail-closed em estado inválido | ✔ | ADR-010 |

### 1.2 Divergências registradas formalmente (AIC → PSA)

| ID | Divergência | Severidade | Recomendação AIC |
|----|-------------|------------|------------------|
| **DIV-AIC-M3-01** | `SOVEREIGN_TOPOLOGY.md` não lista Position Manager explicitamente no diagrama [1]–[6] | Média | Ratificar MIG-3 como **camada de estado transversal** consumida por MIG-4 e atualizada por MIG-6 |
| **DIV-AIC-M3-02** | ADR-012 sequencia MIG-3 **antes** de MIG-6, mas runtime exige MIG-6 para **abrir** posições | Alta | Charter distingue **ordem de migração** (contratos v3) vs **ordem runtime** (eventos de fill pós-MIG-6) |
| **DIV-AIC-M3-03** | MIG-3 charter PSA pode incluir `order_send` implicitamente via "gestão de posição" | **Crítica** | **Proibir explicitamente** — abertura/fechamento de posição = MIG-6; MIG-3 apenas **registra e consulta estado** |
| **DIV-AIC-M3-04** | Reconciliation Engine (SIVR-1) não é MIG-3, mas consome estado MIG-3 | Alta | MIG-3 expõe `PositionSnapshot` read-only; reconciliação = módulo futuro separado |
| **DIV-AIC-M3-05** | Zero código position no V6 hoje — risco de subestimar escopo MT5 `positions_get` / deals | Média | CA-06: sync read-only broker como prova GATE-MIG3 |

### 1.3 Estado atual vs charter (radiografia)

| Elemento | Existe hoje | Pós-charter (implementação futura) |
|----------|-------------|-------------------------------------|
| `contracts/position_contract.py` | ❌ | Obrigatório pré-implementação |
| `position_manager/` package | ❌ | Local canônico proposto |
| Estado de posição em runtime | ❌ | — |
| `order_send` / fills | ❌ | MIG-6 only |
| MIG-2 `MarketDataSnapshot` | ✅ (branch `sivr-0-run`) | Preço mark-to-market |
| SIVR-0/1 position tracking | ❌ | SIVR-1 congelado |

---

## 2. ARQUITETURA PROPOSTA DO MIG-3

### 2.1 Definição

**MIG-3 Position Manager** é a **fonte soberana de verdade** sobre exposição e estado de posições no V6. Responsabilidade única: **registrar, consultar e validar estado de posições** com rastreabilidade ticket-level — **sem enviar ordens**.

### 2.2 Posição no fluxo (runtime vs migração)

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
[MIG-3] Position Manager ◀── registra ticket, volume, PnL
        ↓
[telemetry] lineage ticket → posição → decisão
```

### 2.3 Componentes lógicos (definição — não implementados)

| Componente | Responsabilidade | Fronteira |
|------------|------------------|-----------|
| **PositionManager** | API soberana de estado | Orquestra ledger + sync |
| **PositionLedger** | Estado interno append-only / event-sourced | Fonte lógica de verdade |
| **PositionSyncAdapter** | Read-only broker sync (`positions_get`, deals) | Não envia ordens |
| **PositionValidator** | Invariantes volume, side, ticket uniqueness | Fail-closed |
| **ExposureCalculator** | Agregação net/gross por symbol | Alimenta MIG-4 |

### 2.4 Localização canônica proposta (implementação futura)

```
OMEGA-KERNEL-SOVEREIGN/
├── contracts/
│   └── position_contract.py         ← contratos (GATE-MIG3 pré-req)
├── position_manager/                ← implementação MIG-3 (futuro)
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

### 2.5 Fronteiras de responsabilidade

| Dentro MIG-3 | Fora MIG-3 |
|--------------|------------|
| Registrar posição após evento de fill (input MIG-6) | `order_send()` (MIG-6) |
| Consultar exposição atual | Decisão BUY/SELL (strategy/MIG-5) |
| Rastrear ticket, magic, volume, side | SL/TP policy (MIG-4) |
| Sync read-only com broker | Reconciliation diff engine (SIVR-1/futuro) |
| Fail-closed se estado inconsistente | Market data fetch (MIG-2) |
| Telemetria position events | Kill switch (MIG-6) |

### 2.6 Dependência com MIG-1 e MIG-2

| MIG | Relação com MIG-3 |
|-----|-------------------|
| **MIG-2** | Fornece preço mark (`MarketDataSnapshot`) para PnL unrealized |
| **MIG-1** | Sem dependência direta — desacoplado |

---

## 3. CONTRATOS FORMAIS (ESPECIFICAÇÃO)

> Especificação para `contracts/position_contract.py` — **documento only**.

### 3.1 PositionSide e PositionStatus

```text
PositionSide (Enum)
├── FLAT      # sem exposição
├── LONG
└── SHORT

PositionStatus (Enum)
├── OPEN
├── CLOSED
├── PENDING_OPEN    # ordem enviada, fill não confirmado (evento MIG-6)
├── PENDING_CLOSE
├── DESYNC          # divergência interno vs broker detectada
└── ERROR           # estado inválido — fail-closed
```

### 3.2 PositionTicket

```text
PositionTicket (frozen dataclass)
├── ticket: int                    # ID broker (MT5 position ticket)
├── symbol: str
├── side: PositionSide
├── volume: float                  # lotes — finito, > 0 quando OPEN
├── price_open: float
├── price_current: float | None    # mark — de MIG-2 ou broker sync
├── sl: float | None
├── tp: float | None
├── profit: float | None           # unrealized PnL quando disponível
├── magic: int                     # strategy/run identifier
├── opened_at_utc: datetime
├── closed_at_utc: datetime | None
├── source_id: str                 # "internal_ledger" | "mt5_sync"
└── lineage_id: str                # UUID — liga a decisão/sinal/ordem futura
```

### 3.3 PositionSnapshot

```text
PositionSnapshot (frozen dataclass)
├── symbol: str
├── positions: tuple[PositionTicket, ...]
├── net_volume: float              # signed: + long, - short
├── gross_volume: float
├── status: PositionStatus         # agregado worst-case
├── snapshot_at_utc: datetime
├── request_id: str
└── source_id: str
```

### 3.4 ExposureSummary

```text
ExposureSummary (frozen dataclass)
├── symbol: str
├── net_side: PositionSide
├── net_volume: float
├── open_ticket_count: int
├── total_unrealized_pnl: float | None
└── computed_at_utc: datetime
```

### 3.5 Eventos (telemetria / ledger)

```text
PositionEvent (frozen dataclass)
├── event_id: str                  # UUID
├── event_type: str                # OPENED | CLOSED | MODIFIED | SYNC | DESYNC_DETECTED
├── ticket: int | None
├── symbol: str
├── payload: dict                  # campos mínimos auditáveis
├── timestamp_utc: datetime
├── correlation_id: str            # liga ordem MIG-6 / ciclo SIVR
└── source: str                    # "mig6_fill" | "mt5_sync" | "manual_recovery"
```

### 3.6 PositionManager (Protocol)

```text
PositionManager (Protocol)
├── get_snapshot(symbol: str) -> PositionSnapshot
│     raises: PositionError
├── get_exposure(symbol: str) -> ExposureSummary
├── apply_event(event: PositionEvent) -> None
│     # chamado por MIG-6 após fill — MIG-3 não infere fills sozinho
│     raises: PositionStateError
├── sync_from_broker(symbol: str) -> PositionSnapshot
│     # READ-ONLY — positions_get / deals; nunca order_send
│     raises: PositionSyncError
└── is_flat(symbol: str) -> bool
```

### 3.7 Hierarquia de erros

```text
PositionError (Exception)
├── PositionStateError         # invariante violada, ticket duplicado
├── PositionSyncError          # broker sync falhou
├── PositionNotFoundError      # ticket/symbol inexistente
└── PositionDesyncError        # interno ≠ broker além de tolerância
```

**Semântica fail-closed:** `PositionError` propagado ⇒ MIG-4 deve bloquear nova exposição; MIG-6 não deve enviar ordem adicional até recovery.

---

## 4. CRITÉRIOS DE ACEITE (CA-01 a CA-08)

| ID | Critério (versão AIC) | Testável | Auditável | CI |
|----|------------------------|:--------:|:---------:|:--:|
| **CA-01** | Contrato `position_contract.py` existe antes de `position_manager/` | ✔ | ✔ | ✔ |
| **CA-02** | **Zero `order_send`** em MIG-3 — grep CI falha se presente | ✔ | ✔ | ✔ |
| **CA-03** | Fail-closed: estado inválido ⇒ `PositionStateError`, nunca posição silenciosa | ✔ | ✔ | ✔ |
| **CA-04** | Ticket uniqueness: dois OPEN com mesmo `ticket` ⇒ erro | ✔ | ✔ | ✔ |
| **CA-05** | Determinismo: sequência fixa de `PositionEvent` ⇒ snapshot idêntico | ✔ | ✔ | ✔ |
| **CA-06** | Sync read-only testável via `MockBrokerSync` — sem MT5 em CI | ✔ | ✔ | ✔ |
| **CA-07** | Telemetria: todo evento contém `event_id`, `correlation_id`, `timestamp_utc` | ✔ | ✔ | ✔ |
| **CA-08** | Integração MIG-2: mark price atualiza `price_current` / unrealized PnL | ✔ | ✔ | ✔ |

### 4.1 Critérios explícitos — o que NÃO é CA

- Reconciliation ≥99.5% (SIVR-1) — **fora escopo MIG-3 v1**
- Multi-symbol portfolio aggregation — **v2 charter amendment**
- Persistência durable (DB) — **v1 in-memory ledger + JSONL export suficiente para gate**

---

## 5. DEPENDÊNCIAS EXPLÍCITAS

### 5.1 Upstream (MIG-3 depende de)

| Dependência | Status | Uso |
|-------------|--------|-----|
| GATE-MIG2 fechado | ✅ | Sequência ADR-012 |
| MIG-2 mark price | ✅ | PnL unrealized |
| Contratos base `contracts/` | ✅ | CFO-02 |
| MIG-6 fill events (runtime completo) | ❌ futuro | `apply_event()` |

**Nota:** MIG-3 **pode** implementar ledger + sync read-only **antes** de MIG-6 existir — prova GATE-MIG3 sem ordens reais.

### 5.2 Downstream (dependem de MIG-3)

| Consumidor | Necessidade | Criticidade |
|------------|-------------|-------------|
| **MIG-4** Risk Engine | `ExposureSummary`, `is_flat()`, max position limits | **Crítica** |
| **MIG-5** Signal Validation | Verificar flat vs pyramiding rules | Alta |
| **MIG-6** Execution | `apply_event()` target; pre-trade exposure check | **Crítica** |
| **SIVR-1** (congelado) | Estado interno para reconciliation; ghost/orphan detection | **Crítica** |
| **telemetry/** (futuro) | `PositionEvent` stream | Média |

### 5.3 Mapa SIVR-1 ← MIG-3

| Requisito SIVR-1-DESIGN-001 | Componente MIG-3 |
|-----------------------------|------------------|
| Estado financeiro stateful | `PositionLedger` + `PositionSnapshot` |
| Ghost positions | `sync_from_broker()` vs ledger diff |
| Orphan orders | `lineage_id` + ticket tracking (ordem MIG-6) |
| Reconciliation input | `PositionSnapshot` export JSONL |
| 16h run state continuity | Event log replay (`CA-05`) |

**SIVR-1 permanece bloqueado** até GATE-MIG3 + MIG-4 + MIG-6 mínimo (Opção A ratificada).

---

## 6. RISCOS ARQUITETURAIS

| ID | Risco | Prob. | Impacto | Mitigação |
|----|-------|:-----:|:-------:|-----------|
| R-M3-01 | Confundir MIG-3 com Execution (order_send) | Média | **Crítica** | CA-02 · fronteiras §2.5 |
| R-M3-02 | Implementar MIG-3 antes de contratos | Baixa | Alta | CA-01 · CFO-02 |
| R-M3-03 | Estado in-memory perdido em crash | Alta | Alta | JSONL event log + replay (CA-05) |
| R-M3-04 | Desync interno vs MT5 demo | Alta | Alta | `PositionDesyncError` + CA-06 |
| R-M3-05 | MIG-4 bloqueado sem exposure API clara | Média | Alta | `ExposureSummary` contrato §3.4 |
| R-M3-06 | Scope creep — reconciliation dentro MIG-3 | Média | Alta | DIV-AIC-M3-04 — módulo separado SIVR-1 |
| R-M3-07 | Topology doc desatualizado | Média | Média | PSA update ARCH-SOV-V6 pós-charter |

---

## 7. CRITÉRIOS DE ELEGIBILIDADE PARA GATE-MIG3

### 7.1 Pré-implementação

- [ ] TASK-0023-MIG3-CHARTER-AIC-001 validado PSA
- [ ] Conselho delibera versão consolidada
- [ ] DEC-MIG3 registrado
- [ ] Autorização explícita de implementação

### 7.2 Implementação (CFO-02)

- [ ] `contracts/position_contract.py` merged
- [ ] `position_manager/` com ledger + validator + mock sync
- [ ] CA-01..CA-08 verdes em CI
- [ ] Zero `order_send` no package
- [ ] `MIGRATION_ALLOWLIST` MIG-3 colunas ✅

### 7.3 Prova de integração

- [ ] Mock fill events → ledger → snapshot determinístico
- [ ] MIG-2 mark price → unrealized PnL update (CA-08)
- [ ] Optional: MT5 demo `positions_get` read-only smoke (fora CI)

### 7.4 NÃO requerido para GATE-MIG3

- MIG-6 implementado
- SIVR-1
- Reconciliation engine
- Persistência DB
- order_send

---

## 8. CONCLUSÃO TÉCNICA DO AIC

### 8.1 Síntese

MIG-3 Position Manager é a **camada de estado** que transforma o V6 de pipeline read-only (MIG-1/MIG-2) em sistema **capaz de representar exposição financeira** — pré-requisito para Risk, Execution feedback e SIVR-1 — **sem ainda operar mercado**.

### 8.2 Recomendação ao Conselho

| # | Recomendação | Prioridade |
|---|--------------|------------|
| 1 | Aprovar charter AIC como base técnica TASK-0023 | Alta |
| 2 | Ratificar DIV-AIC-M3-02 (migração vs runtime) no doc PSA | Alta |
| 3 | Proibir explicitamente order_send em MIG-3 (DIV-AIC-M3-03) | **Crítica** |
| 4 | Atualizar `SOVEREIGN_TOPOLOGY.md` com camada Position | Média |
| 5 | **Não autorizar implementação** até deliberação pós-PSA | Obrigatório |

### 8.3 Veredito final

# FAVORÁVEL COM RESSALVAS DE SEQUÊNCIA

MIG-3 Charter pronto para **revisão PSA** e **deliberação Conselho**. Implementação **bloqueada** até nova autorização formal.

---

## ANEXO A — Modelo de estados (máquina simplificada)

```
                    apply_event(OPENED)
         FLAT ──────────────────────────▶ OPEN (LONG/SHORT)
          ▲                                    │
          │         apply_event(CLOSED)        │
          └────────────────────────────────────┘

PENDING_OPEN ──timeout/desync──▶ DESYNC ──recovery──▶ OPEN | FLAT
```

---

## ANEXO B — Referências

- TASK-0023-INITIATION-001
- DEC-GATE-MIG2-001
- ADR-010 · ADR-012
- SABM-001 · SIVR-1-DESIGN-001 (congelado)
- `governance/MIGRATION_ALLOWLIST.md`
- `contracts/README.md`

---

**AIC — Architecture & Integration Council**  
**TASK-0023-MIG3-CHARTER-AIC-001 — Entregue**  
**Implementação: NÃO AUTORIZADA**
