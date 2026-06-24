# TASK-0022-MIG2-CHARTER-AIC-001

**Market Data Engine — Charter Técnico Consolidado (AIC)**

| Campo | Valor |
|-------|-------|
| **ID** | TASK-0022-MIG2-CHARTER-AIC-001 |
| **Data** | 2026-06-25 |
| **Emitido por** | AIC (Architecture & Integration Council) |
| **Destinatários** | PSA · CFO · Conselho |
| **Responde a** | TASK-0022-INITIATION-001 · CEO-DIRECTIVE-021 |
| **Documento PSA revisado** | TASK-0022 — MIG-2 Charter (PSA workspace) |
| **Base factual** | SABM-001 · SIVR-0-CLOSURE-001 · ADR-010 · ADR-012 · BUG-002 |
| **Repositório referência** | `OMEGA-Kernel-Sovereign` @ `sivr-0-run` / `main` |
| **Status** | ENTREGUE — aguardando validação PSA + deliberação Conselho |
| **Implementação** | **NÃO AUTORIZADA** por este documento |

---

## VEREDITO AIC (SUMÁRIO)

# FAVORÁVEL COM RESSALVAS ESTRUTURAIS

O charter PSA para MIG-2 está **direcionalmente correto** e **mandatório** na sequência canônica pós-GATE-MIG1. A arquitetura proposta neste documento consolida a versão técnica AIC, corrige lacunas identificadas em SABM-001 e estabelece fronteiras explícitas com MIG-1, SIVR-0 e futuro SIVR-1.

**Nenhuma linha de código executável** está incluída ou autorizada por este charter.

---

## 1. REVISÃO TÉCNICA DO CHARTER PSA

### 1.1 Alinhamentos confirmados (AIC concorda)

| Item PSA (escopo TASK-0022-INITIATION-001) | Posição AIC | Base |
|--------------------------------------------|-------------|------|
| MIG-2 = Market Data Engine soberano | ✔ Concorda | ADR-010 posição [1] no fluxo; ADR-012 sequência |
| Resolve BUG-002 (fallback sintético) | ✔ Concorda | `BUG_REGISTRY.csv` — FND-06 |
| Contratos antes de implementação (CFO-02) | ✔ Concorda | `contracts/README.md` |
| Fail-closed: ausência de dado ⇒ erro explícito, nunca sintético | ✔ Concorda | ADR-010 regra 2 |
| CA-01..CA-06 como gate de aceite | ✔ Concorda — com revisões §4 | Initiation-001 §3.3 |
| OHLCVBar, MarketDataFeed, DataProvider, DataIntegrityError | ✔ Concorda — especificação §3 | Initiation-001 §3.2 |
| Mapeamento deps MIG-3..6 e SIVR-1 | ✔ Concorda — §5 | Initiation-001 §3.4 |

### 1.2 Divergências registradas formalmente (AIC → PSA)

| ID | Divergência | Severidade | Recomendação AIC |
|----|-------------|------------|------------------|
| **DIV-AIC-01** | `IndicatorInput` (MIG-1) aceita apenas `closes: tuple[float]` — charter PSA pressupõe OHLCV completo | Alta | MIG-2 expõe `MarketDataSnapshot`; **adapter MIG-1** extrai `closes` — não alterar MIG-1 retroactivamente |
| **DIV-AIC-02** | `sivr/data_adapter_mt5.py` funciona como proto-MIG-2 não soberano (53 linhas, `MarketSnapshot` ad-hoc) | Alta | Charter declara **deprecação futura** do adapter SIVR em favor de `market_data/` soberano pós-implementação |
| **DIV-AIC-03** | SIVR CSV path (`sivr/sivr_bridge.py`) usa dataset sintético — viola espírito ADR-010 se confundido com MIG-2 | Média | Manter CSV **restrito a testes offline**; proibir no caminho soberano de decisão |
| **DIV-AIC-04** | `MIGRATION_ALLOWLIST.md` marca MIG-2 PENDENTE — correto; MIG-1 também desatualizado | Baixa | PSA sync allowlist na consolidação GATE-MIG1/MIG-2 |
| **DIV-AIC-05** | ADR-010 checklist CQO ainda `[ ]` aberto — MIG-2 deve contribuir item "sem sintético" | Média | GATE-MIG2 exige teste automatizado anti-BUG-002 |

### 1.3 Estado atual vs charter (SABM-001 cruzado)

| Elemento | Existe hoje | Pós-charter (implementação futura) |
|----------|-------------|-------------------------------------|
| `contracts/market_data_contract.py` | ❌ | Obrigatório antes de código |
| `market_data/` package | ❌ | Local canônico proposto |
| `MarketDataConnector` (nome ADR-010) | ❌ | Alias conceitual de `DataProvider` |
| MT5 integration soberana | ⚠ ad-hoc em `sivr/` | Migrar para provider plugável |
| Testes MIG-2 | ❌ | Mock provider only in tests |

---

## 2. ARQUITETURA PROPOSTA DO MIG-2

### 2.1 Definição

**MIG-2 Market Data Engine** é o primeiro estágio executável do fluxo soberano ADR-010. Responsabilidade única: **adquirir, validar e entregar snapshots de mercado OHLCV auditáveis** a consumidores downstream (MIG-1, futuramente MIG-3..6).

**Não é:** estratégia, risco, execução, indicador, ou harness SIVR.

### 2.2 Posição no fluxo soberano

```
┌─────────────────────────────────────────────────────────────────┐
│ FLUXO ADR-010 — MIG-2 destacado                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [MIG-2] Market Data Engine  ──falha──▶ DataIntegrityError       │
│              │                              (fail-closed)        │
│              ▼                                                   │
│  [MIG-1] Indicator Engine    ◀── adapter: closes extraction    │
│              │                                                   │
│              ▼                                                   │
│  [MIG-5] Signal Validation     (futuro)                          │
│              ▼                                                   │
│  [MIG-3] Position Manager      (futuro)                          │
│              ▼                                                   │
│  [MIG-4] Risk Engine           (futuro)                          │
│              ▼                                                   │
│  [MIG-6] Execution Engine      (futuro)                          │
│              ▼                                                   │
│  [telemetry]                   (futuro)                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.3 Componentes lógicos (definição — não implementados)

| Componente | Responsabilidade | Fronteira |
|------------|------------------|-----------|
| **MarketDataEngine** | Orquestra fetch + validate + snapshot | API pública do MIG-2 |
| **DataProvider** | Interface para fonte externa (MT5, futuro: outros) | Abstrai broker/API |
| **MarketDataFeed** | Configura símbolo, timeframe, depth, polling | Não calcula indicadores |
| **DataValidator** | Integridade: gaps, stale bars, OHLC consistency | Emite `DataIntegrityError` |
| **SnapshotFactory** | Monta `MarketDataSnapshot` imutável | Único output canônico |

### 2.4 Localização canônica proposta (implementação futura)

```
OMEGA-KERNEL-SOVEREIGN/
├── contracts/
│   └── market_data_contract.py      ← contratos (GATE-MIG2 pré-req)
├── market_data/                      ← implementação MIG-2 (futuro)
│   ├── __init__.py
│   ├── engine.py                     ← MarketDataEngine
│   ├── validator.py                  ← DataValidator
│   └── providers/
│       ├── __init__.py
│       └── mt5_provider.py           ← MT5DataProvider
└── tests/
    └── test_market_data_*.py         ← mock provider only
```

**Regra:** `sivr/data_adapter_mt5.py` permanece harness SIVR-0 até migração explícita pós-GATE-MIG2 — não duplicar lógica permanentemente.

### 2.5 Fluxo de aquisição de dados

```
1. MarketDataFeed.configure(symbol, timeframe, bar_count, source_id)
2. DataProvider.connect()           → falha: ConnectionError
3. DataProvider.fetch_bars(params)  → raw bars
4. DataValidator.validate(bars)     → falha: DataIntegrityError
5. SnapshotFactory.build(...)       → MarketDataSnapshot (frozen)
6. DataProvider.disconnect()        → opcional; lifecycle explícito
```

**Regras invioláveis:**
- Passo 4 falhou ⇒ **nunca** substituir por dado sintético (anti BUG-002).
- Passo 4 falhou ⇒ consumidor recebe exceção ou `FetchResult.FAILURE` — nunca `IndicatorInput` parcial silencioso.
- Timestamps UTC obrigatórios por barra.
- `source_id` obrigatório para audit trail (ex.: `"mt5_demo"`, `"mock_test"`).

### 2.6 Fronteiras de responsabilidade

| Dentro MIG-2 | Fora MIG-2 |
|--------------|------------|
| Fetch OHLCV | Cálculo RSI/EMA (MIG-1) |
| Validação integridade | Decisão BUY/SELL (strategy/MIG-5) |
| Normalização para contrato | Envio ordens (MIG-6) |
| Fail-closed em dado inválido | Gestão posição (MIG-3) |
| Provider lifecycle (connect/disconnect) | Reconciliação financeira (SIVR-1/futuro) |

### 2.7 Dependência com MIG-1

MIG-1 **permanece encerrado** (GATE-MIG1). Integração futura:

```
MarketDataSnapshot.bars → extract closes → IndicatorInput(closes=...)
```

**Não alterar** assinatura `MinimalIndicatorEngine.calculate(IndicatorInput)` na MIG-2. Adapter fino entre camadas — princípio de isolamento sequencial ADR-012.

---

## 3. CONTRATOS FORMAIS (ESPECIFICAÇÃO)

> Especificação para `contracts/market_data_contract.py` — **documento only**, sem código no repo nesta fase.

### 3.1 OHLCVBar

```text
OHLCVBar (frozen dataclass)
├── symbol: str              # ex. "XAUUSD"
├── timeframe: str           # ex. "M1" — enum futuro: Timeframe
├── open: float
├── high: float
├── low: float
├── close: float
├── volume: float            # tick volume ou real — documentar por provider
├── timestamp_utc: datetime  # abertura ou fechamento — FIXAR: bar open UTC
└── bar_index: int           # 0 = mais recente (align MT5 copy_rates_from_pos)
```

**Invariantes:**
- `low <= min(open, close) <= max(open, close) <= high`
- Todos floats finitos (não NaN, não Inf)
- `timestamp_utc` timezone-aware UTC

### 3.2 MarketDataSnapshot

```text
MarketDataSnapshot (frozen dataclass)
├── symbol: str
├── timeframe: str
├── bars: tuple[OHLCVBar, ...]   # ordenado: index 0 = barra mais recente
├── bar_count: int               # == len(bars)
├── fetched_at_utc: datetime
├── source_id: str               # audit: "mt5_demo" | "mock_test"
└── request_id: str              # UUID para lineage telemetria futura
```

### 3.3 DataProvider (Protocol)

```text
DataProvider (Protocol)
├── connect(config: ProviderConfig) -> None
│     raises: ConnectionError
├── disconnect() -> None
├── fetch_bars(request: BarRequest) -> tuple[OHLCVBar, ...]
│     raises: ConnectionError | DataIntegrityError
├── is_connected() -> bool
└── provider_id() -> str
```

### 3.4 MarketDataFeed (Protocol)

```text
MarketDataFeed (Protocol)
├── configure(spec: FeedSpec) -> None
├── fetch_snapshot() -> MarketDataSnapshot
│     raises: DataIntegrityError | ConnectionError
└── feed_id() -> str
```

### 3.5 MarketDataEngine (Protocol)

```text
MarketDataEngine (Protocol)
├── fetch(spec: FeedSpec) -> MarketDataSnapshot
└── fetch_closes(spec: FeedSpec) -> tuple[float, ...]
      # convenience — ordem temporal: oldest → newest para MIG-1
      # DEPRECAR se MIG-1 evoluir a consumir snapshot completo
```

### 3.6 Hierarquia de erros

```text
MarketDataError (Exception)
├── ConnectionError          # MT5 offline, init failed
├── DataIntegrityError       # gaps, stale, OHLC inválido, bar count insuficiente
├── UnsupportedSymbolError   # symbol_select failed
└── UnsupportedTimeframeError
```

**Semântica fail-closed:** qualquer `MarketDataError` propagado ao pipeline soberano ⇒ etapas downstream **não executam** (equivalente HOLD no fluxo completo futuro).

### 3.7 Tipos auxiliares

```text
FeedSpec (frozen)
├── symbol: str
├── timeframe: str
├── bar_count: int           # mínimo: max(MIG-1 rsi_period+1, ema_period)
├── max_staleness_seconds: float | None   # opcional — barra mais recente
└── environment: str       # "demo" | "test" | "dev" — align OMEGA_ENV futuro

ProviderConfig (frozen)
├── mt5_path: str | None
├── timeout_seconds: float
└── retry_count: int         # default 0 na v1 — retry explícito charter futuro

FetchResult (frozen) — alternativa a exceção para telemetria
├── status: "SUCCESS" | "FAILURE"
├── snapshot: MarketDataSnapshot | None
├── error: MarketDataError | None
└── latency_ms: float
```

---

## 4. CRITÉRIOS DE ACEITE REVISADOS (CA-01 a CA-06)

### 4.1 Tabela consolidada AIC

| ID | Critério (versão AIC revisada) | Testável | Auditável | Determinístico | CI |
|----|--------------------------------|:--------:|:---------:|:--------------:|:--:|
| **CA-01** | Contrato `market_data_contract.py` existe e é importável antes de qualquer código em `market_data/` | ✔ | ✔ | N/A | ✔ lint/import |
| **CA-02** | **Zero fallback sintético** no caminho de produção: nenhum método retorna preço fixo ou CSV embutido quando provider falha (anti BUG-002) | ✔ | ✔ | ✔ | ✔ test must fail if synthetic |
| **CA-03** | Fail-closed: falha de fetch/validate propaga `DataIntegrityError` ou `ConnectionError` — nunca snapshot parcial silencioso | ✔ | ✔ | ✔ | ✔ |
| **CA-04** | `OHLCVBar` e `MarketDataSnapshot` imutáveis; invariantes OHLC validadas em `DataValidator` | ✔ | ✔ | ✔ | ✔ |
| **CA-05** | **Determinismo:** mock provider com bars fixos produz snapshot idêntico byte-a-byte (hash) em N runs | ✔ | ✔ | ✔ | ✔ |
| **CA-06** | **CI compatível:** suite usa apenas `MockDataProvider` — zero dependência MT5 terminal em CI | ✔ | ✔ | ✔ | ✔ |

### 4.2 Revisões AIC vs charter PSA (propostas)

| CA | Revisão AIC | Motivo |
|----|-------------|--------|
| CA-02 | Reforçar: incluir grep CI `assert no _get_sample_data` pattern / no hardcoded price | BUG-002 root cause V5.5 |
| CA-05 | Adicionar hash snapshot determinístico | SIVR-0 C6 lesson — partial determinism |
| CA-06 | Explicitar mock-only in CI | SABM-001 — MT5 não disponível em GitHub Actions |
| *(novo sugerido)* **CA-07** | Log estruturado mínimo por fetch: `{request_id, source_id, bar_count, latency_ms, status}` | Prepara telemetria; alinha SIVR observability |
| *(novo sugerido)* **CA-08** | Adapter MIG-1: `snapshot → IndicatorInput` testado isoladamente | DIV-AIC-01 mitigation |

**PSA deve ratificar** CA-07/CA-08 ou rejeitar formalmente.

### 4.3 Critérios de aceite explícitos — o que NÃO é CA

- Latência <100ms p99 — **fora escopo MIG-2 v1** (meta institucional futura)
- Failover multi-broker — **fora escopo v1**
- Streaming tick-by-tick — **fora escopo v1** (bar polling suficiente para SIVR-0/1)

---

## 5. DEPENDÊNCIAS EXPLÍCITAS

### 5.1 Upstream (MIG-2 depende de)

| Dependência | Tipo | Status |
|-------------|------|--------|
| GATE-MIG1 encerrado | Gate | ✅ |
| MIG-1 `IndicatorInput` estável | Contrato | ✅ |
| ADR-010 fail-closed ratificado | Governança | ✅ |
| `contracts/` package structure | Infra | ✅ |
| MetaTrader5 package (provider MT5 only) | Runtime externo | ⚠ branch `sivr-0-run` |

### 5.2 Downstream (dependem de MIG-2)

| Consumidor | O que precisa do MIG-2 | Criticidade |
|------------|------------------------|-------------|
| **MIG-1** (integrado) | `closes` ou snapshot validado | Alta — já parcial via SIVR adapter |
| **MIG-3** Position Manager | Preço mark-to-market, posição sync timestamps | Alta |
| **MIG-4** Risk Engine | Bid/ask spread, staleness guard | Alta |
| **MIG-5** Signal Validation | Snapshot freshness antes de sinal | Média |
| **MIG-6** Execution | Preço referência, mercado aberto, symbol info | **Crítica** |
| **SIVR-1** (futuro) | Stream confiável + reconnect + state events | **Crítica** |
| **telemetry/** (futuro) | `request_id`, `source_id`, latency | Média |

### 5.3 Mapa SIVR-1 ← MIG-2 (referência futura — SIVR-1 congelado)

| Requisito SIVR-1-DESIGN-001 | Componente MIG-2 necessário |
|-----------------------------|----------------------------|
| OHLCV stream live demo | `MT5DataProvider` + `MarketDataFeed` |
| Disconnect recovery (F1) | `DataProvider.connect()` idempotente + state event |
| Latency measurement (F2) | `FetchResult.latency_ms` |
| Reconciliation input | Snapshot timestamps + `request_id` |
| 16h continuous run | Connection health check + stale bar detection (CA extended) |

**Conclusão:** SIVR-1 **permanece bloqueado** até GATE-MIG2 + MIG-3..6 conforme Opção A. MIG-2 é **pré-requisito necessário mas não suficiente** para SIVR-1.

### 5.4 Matriz de sequência

```
GATE-MIG1 ✅ → TASK-0022 Charter 🟢 → GATE-MIG2 (futuro) → MIG-3 Charter → ... → SIVR-1
```

---

## 6. RISCOS ARQUITETURAIS

| ID | Risco | Prob. | Impacto | Mitigação charter |
|----|-------|:-----:|:-------:|-------------------|
| R-01 | MT5 API acoplamento monolítico | Alta | Alta | `DataProvider` protocol — MT5 uma implementação |
| R-02 | Duplicação `sivr/data_adapter_mt5` vs `market_data/` | Alta | Média | Plano deprecação pós-GATE-MIG2 |
| R-03 | CSV sintético confundido com market data real | Média | **Crítica** | CA-02 + segregação `tests/fixtures/` only |
| R-04 | `IndicatorInput` só closes — descarte OHLCV | Média | Média | Snapshot completo preservado; adapter extrai closes |
| R-05 | Stale bars silenciosos (mercado pausado) | Média | Alta | CA extended: `max_staleness_seconds` |
| R-06 | CI verde com mock mas falha MT5 real | Alta | Alta | SIVR-2 read-only pós-GATE-MIG2 (proposta) |
| R-07 | Scope creep → implementar execution no MIG-2 | Baixa | **Crítica** | Fronteiras §2.6 + CEO-DIRECTIVE-021 |
| R-08 | Allowlist não atualizada → merge prematuro | Média | Alta | GATE-MIG2 checklist §7 |

---

## 7. CRITÉRIOS DE ELEGIBILIDADE PARA GATE-MIG2

GATE-MIG2 **só pode ser declarado elegível** quando **todas** as condições abaixo forem verdadeiras:

### 7.1 Pré-implementação (gate de entrada)

- [ ] TASK-0022-MIG2-CHARTER-AIC-001 validado pelo PSA
- [ ] Conselho delibera versão consolidada PSA+AIC
- [ ] DEC-MIG2 registrado em `DECISION_REGISTRY.csv`
- [ ] Autorização explícita de implementação (análogo TASK-0022-INITIATION para código)

### 7.2 Implementação (CFO-02)

- [ ] `contracts/market_data_contract.py` merged
- [ ] Interfaces `DataProvider`, `MarketDataFeed`, `MarketDataEngine` definidas
- [ ] `market_data/` implementado com `MockDataProvider`
- [ ] `MT5DataProvider` implementado (opcional no merge — pode ser fase 2 com waiver)
- [ ] Testes CA-01..CA-06 (CA-07/08 se ratificados) verdes em CI
- [ ] Zero imports de `OMEGA_V55_FROZEN` ou paths legacy

### 7.3 Allowlist (`MIGRATION_ALLOWLIST.md`)

Todas colunas MIG-2 marcadas ✅:
Contrato | Interface | Teste | Aprovado PSA

### 7.4 Prova de integração (read-only)

- [ ] Pipeline: `MarketDataEngine.fetch()` → adapter → `MIG-1.calculate()` — determinístico
- [ ] **SIVR-2 proposto:** re-run MT5 read-only usando MIG-2 soberano (substitui adapter SIVR-0)
- [ ] Logs com `request_id`, `source_id`, `latency_ms`

### 7.5 Explicitamente NÃO requerido para GATE-MIG2

- order_send / execução financeira
- SIVR-1 stress framework
- MIG-3..6 implementados
- `deployment/omega_run.py`

---

## 8. CONCLUSÃO TÉCNICA DO AIC

### 8.1 Síntese

MIG-2 é o **próximo elo obrigatório** da sequência canônica. Sem Market Data Engine soberano, o V6 permanece dependente de adapters ad-hoc (`sivr/data_adapter_mt5.py`) que **não satisfazem** ADR-010 posição [1] nem eliminam formalmente BUG-002.

O charter consolidado AIC:
- Define contratos formais OHLCV + provider + fail-closed
- Preserva MIG-1 encerrado via adapter pattern
- Mapeia dependências SIVR-1 sem autorizar SIVR-1
- Estabelece GATE-MIG2 com critérios verificáveis

### 8.2 Recomendação ao Conselho

| # | Recomendação | Prioridade |
|---|--------------|------------|
| 1 | **Aprovar** TASK-0022-MIG2-CHARTER-AIC-001 como base técnica | Alta |
| 2 | PSA consolidar com charter PSA — resolver DIV-AIC-01..05 | Alta |
| 3 | Ratificar CA-07/CA-08 ou rejeitar formalmente | Média |
| 4 | Merge `sivr-0-run` → `main` como housekeeping (separado de MIG-2) | Média |
| 5 | **Não autorizar** implementação até deliberação pós-validação PSA | **Obrigatório** |
| 6 | Planejar SIVR-2 (read-only MIG-2 proof) como sucessor natural de SIVR-0 | Média |

### 8.3 Veredito final

# FAVORÁVEL COM RESSALVAS ESTRUTURAIS

MIG-2 Charter está **pronto para revisão PSA** e **deliberação Conselho**. Implementação permanece **bloqueada** até nova autorização formal.

---

## ANEXO A — Comparativo SIVR-0 adapter vs MIG-2 alvo

| Aspecto | `sivr/data_adapter_mt5.py` (hoje) | MIG-2 soberano (alvo) |
|---------|-----------------------------------|------------------------|
| Localização | `sivr/` harness | `market_data/` |
| Output | `MarketSnapshot(closes only)` | `MarketDataSnapshot(OHLCV full)` |
| Validação | bar count > 0 | OHLC invariants + staleness |
| Erros | `Mt5AdapterError` | Hierarquia `MarketDataError` |
| Fail-closed | ✔ raise | ✔ raise — nunca sintético |
| Audit trail | ❌ | `request_id`, `source_id` |
| Contrato formal | ❌ | ✔ `contracts/` |
| CI testável | ❌ precisa MT5 | ✔ MockDataProvider |

---

## ANEXO B — Referências

- CEO-DIRECTIVE-021
- TASK-0022-INITIATION-001
- SABM-001
- SIVR-0-CLOSURE-001
- AIC-CONCLUSION-SIVR1-GATE-MIG1-001
- ADR-010, ADR-012
- BUG-002 / FND-06
- `governance/MIGRATION_ALLOWLIST.md`
- `architecture/SOVEREIGN_TOPOLOGY.md`

---

**AIC — Architecture & Integration Council**  
**TASK-0022-MIG2-CHARTER-AIC-001 — Entregue**  
**Implementação: NÃO AUTORIZADA**
