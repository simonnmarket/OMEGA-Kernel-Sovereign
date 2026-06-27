"""MIG-3 — Position Manager contracts.

Fail-closed: estado inválido → exceção. MIG-3 nunca envia ordens (MIG-6 only).

Autorização: DEC-MIG3-001 · TASK-0023 · ADR-012
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Protocol, runtime_checkable


class PositionError(Exception):
    """Raiz da hierarquia de erros MIG-3."""


class PositionStateError(PositionError):
    """Invariante violada, ticket duplicado, ou transição inválida."""


class PositionSyncError(PositionError):
    """Falha na sincronização read-only com broker."""


class PositionNotFoundError(PositionError):
    """Ticket ou símbolo inexistente no ledger."""


class PositionDesyncError(PositionError):
    """Divergência interno vs broker além de tolerância."""


class PositionSide(str, Enum):
    FLAT = "FLAT"
    LONG = "LONG"
    SHORT = "SHORT"


class PositionStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    PENDING_OPEN = "PENDING_OPEN"
    PENDING_CLOSE = "PENDING_CLOSE"
    DESYNC = "DESYNC"
    ERROR = "ERROR"


@dataclass(frozen=True)
class PositionTicket:
    ticket: int
    symbol: str
    side: PositionSide
    volume: float
    price_open: float
    price_current: float | None
    sl: float | None
    tp: float | None
    profit: float | None
    magic: int
    opened_at_utc: datetime
    closed_at_utc: datetime | None
    source_id: str
    lineage_id: str


@dataclass(frozen=True)
class PositionSnapshot:
    symbol: str
    positions: tuple[PositionTicket, ...]
    net_volume: float
    gross_volume: float
    status: PositionStatus
    snapshot_at_utc: datetime
    request_id: str
    source_id: str


@dataclass(frozen=True)
class ExposureSummary:
    symbol: str
    net_side: PositionSide
    net_volume: float
    open_ticket_count: int
    total_unrealized_pnl: float | None
    computed_at_utc: datetime


@dataclass(frozen=True)
class PositionEvent:
    event_id: str
    event_type: str
    ticket: int | None
    symbol: str
    payload: dict[str, object]
    timestamp_utc: datetime
    correlation_id: str
    source: str


@runtime_checkable
class PositionSyncAdapter(Protocol):
    """Sync read-only com broker — nunca order_send."""

    def fetch_open_positions(self, symbol: str) -> tuple[PositionTicket, ...]: ...
    def adapter_id(self) -> str: ...


@runtime_checkable
class PositionManager(Protocol):
    def get_snapshot(self, symbol: str) -> PositionSnapshot: ...
    def get_exposure(self, symbol: str) -> ExposureSummary: ...
    def apply_event(self, event: PositionEvent) -> None: ...
    def sync_from_broker(self, symbol: str) -> PositionSnapshot: ...
    def is_flat(self, symbol: str) -> bool: ...
