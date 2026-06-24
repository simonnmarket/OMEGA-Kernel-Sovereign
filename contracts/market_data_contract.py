"""MIG-2 — Market Data Engine contracts.

Contratos formais para o Market Data Engine soberano.
Fail-closed: ausência ou invalidade de dado → exceção, nunca dado sintético.

Autorização: DEC-MIG2-001 · TASK-0022 · CEO-DIRECTIVE-021
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, runtime_checkable


# ---------------------------------------------------------------------------
# Exceções
# ---------------------------------------------------------------------------

class MarketDataError(Exception):
    """Raiz da hierarquia de erros MIG-2."""


class ConnectionError(MarketDataError):
    """MT5 offline, initialize falhou, ou conexão perdida."""


class DataIntegrityError(MarketDataError):
    """Dados inválidos: gaps, barras stale, invariante OHLC violada, count insuficiente."""


class UnsupportedSymbolError(MarketDataError):
    """symbol_select falhou ou símbolo não disponível no provider."""


class UnsupportedTimeframeError(MarketDataError):
    """Timeframe não suportado pelo provider."""


# ---------------------------------------------------------------------------
# Tipos de dados
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class OHLCVBar:
    """Barra OHLCV imutável e auditável.

    Invariantes:
    - low <= min(open, close) <= max(open, close) <= high
    - Todos os floats finitos (não NaN, não Inf)
    - timestamp_utc timezone-aware UTC
    - bar_index: 0 = barra mais recente (alinhado com MT5 copy_rates_from_pos)
    """

    symbol: str
    timeframe: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    timestamp_utc: datetime
    bar_index: int


@dataclass(frozen=True)
class MarketDataSnapshot:
    """Snapshot imutável e auditável de N barras OHLCV.

    bars: tuple ordenado — index 0 = barra mais recente.
    source_id: audit trail obrigatório (ex.: "mt5_demo", "mock_test").
    request_id: UUID para lineage e telemetria futura.
    """

    symbol: str
    timeframe: str
    bars: tuple[OHLCVBar, ...]
    bar_count: int
    fetched_at_utc: datetime
    source_id: str
    request_id: str


@dataclass(frozen=True)
class FeedSpec:
    """Especificação de feed — o que buscar e de onde."""

    symbol: str
    timeframe: str
    bar_count: int
    environment: str
    max_staleness_seconds: float | None = None


@dataclass(frozen=True)
class ProviderConfig:
    """Configuração do provider externo."""

    mt5_path: str | None = None
    timeout_seconds: float = 10.0
    retry_count: int = 0


@dataclass(frozen=True)
class BarRequest:
    """Pedido de barras ao provider."""

    symbol: str
    timeframe: str
    bar_count: int


@dataclass(frozen=True)
class FetchResult:
    """Resultado de fetch — para telemetria; alternativa a exceção."""

    status: str  # "SUCCESS" | "FAILURE"
    snapshot: MarketDataSnapshot | None
    error: MarketDataError | None
    latency_ms: float


# ---------------------------------------------------------------------------
# Protocolos
# ---------------------------------------------------------------------------

@runtime_checkable
class DataProvider(Protocol):
    """Interface de provider externo — MT5 é uma implementação."""

    def connect(self, config: ProviderConfig) -> None: ...
    def disconnect(self) -> None: ...
    def fetch_bars(self, request: BarRequest) -> tuple[OHLCVBar, ...]: ...
    def is_connected(self) -> bool: ...
    def provider_id(self) -> str: ...


@runtime_checkable
class MarketDataFeed(Protocol):
    """Interface de feed configurável."""

    def configure(self, spec: FeedSpec) -> None: ...
    def fetch_snapshot(self) -> MarketDataSnapshot: ...
    def feed_id(self) -> str: ...


@runtime_checkable
class MarketDataEngine(Protocol):
    """Interface pública do MIG-2."""

    def fetch(self, spec: FeedSpec) -> MarketDataSnapshot: ...
    def fetch_closes(self, spec: FeedSpec) -> tuple[float, ...]: ...
