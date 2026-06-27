"""MT5 read-only position sync — positions_get only, no order execution."""

from __future__ import annotations

from datetime import datetime, timezone

from contracts.position_contract import (
    PositionSide,
    PositionSyncError,
    PositionTicket,
)

try:
    import MetaTrader5 as mt5
except ImportError:  # pragma: no cover — CI uses MockBrokerSync
    mt5 = None  # type: ignore[assignment]


class Mt5PositionSync:
    """Sync read-only via MT5 API."""

    def __init__(self, mt5_path: str | None = None) -> None:
        self._mt5_path = mt5_path

    def fetch_open_positions(self, symbol: str) -> tuple[PositionTicket, ...]:
        if mt5 is None:
            raise PositionSyncError("MetaTrader5 package not available")
        if self._mt5_path:
            if not mt5.initialize(path=self._mt5_path):
                raise PositionSyncError(f"mt5.initialize failed: {mt5.last_error()}")
        elif not mt5.initialize():
            raise PositionSyncError(f"mt5.initialize failed: {mt5.last_error()}")
        try:
            positions = mt5.positions_get(symbol=symbol)
            if positions is None:
                err = mt5.last_error()
                if err[0] != 0:
                    raise PositionSyncError(f"positions_get failed: {err}")
                return ()
            result: list[PositionTicket] = []
            for pos in positions:
                side = PositionSide.LONG if pos.type == mt5.POSITION_TYPE_BUY else PositionSide.SHORT
                opened = datetime.fromtimestamp(pos.time, tz=timezone.utc)
                result.append(
                    PositionTicket(
                        ticket=int(pos.ticket),
                        symbol=pos.symbol,
                        side=side,
                        volume=float(pos.volume),
                        price_open=float(pos.price_open),
                        price_current=float(pos.price_current),
                        sl=float(pos.sl) if pos.sl else None,
                        tp=float(pos.tp) if pos.tp else None,
                        profit=float(pos.profit),
                        magic=int(pos.magic),
                        opened_at_utc=opened,
                        closed_at_utc=None,
                        source_id="mt5_sync",
                        lineage_id=str(pos.identifier),
                    )
                )
            return tuple(result)
        finally:
            mt5.shutdown()

    def adapter_id(self) -> str:
        return "mt5_broker"
