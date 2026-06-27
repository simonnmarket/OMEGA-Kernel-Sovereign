"""MIG-3 SovereignPositionManager — API soberana de estado de posições."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from contracts.market_data_contract import MarketDataSnapshot
from contracts.position_contract import (
    ExposureSummary,
    PositionEvent,
    PositionSide,
    PositionSnapshot,
    PositionStateError,
    PositionStatus,
    PositionSyncAdapter,
)
from position_manager.exposure import ExposureCalculator
from position_manager.ledger import PositionLedger
from position_manager.validator import PositionValidator


class SovereignPositionManager:
    """Implementação canônica MIG-3 — nunca order_send."""

    def __init__(
        self,
        sync_adapter: PositionSyncAdapter,
        ledger: PositionLedger | None = None,
        exposure: ExposureCalculator | None = None,
    ) -> None:
        self._sync = sync_adapter
        self._ledger = ledger or PositionLedger(PositionValidator())
        self._exposure = exposure or ExposureCalculator()

    def get_snapshot(self, symbol: str) -> PositionSnapshot:
        open_positions = self._ledger.open_positions(symbol)
        net = 0.0
        gross = 0.0
        for pos in open_positions:
            signed = pos.volume if pos.side == PositionSide.LONG else -pos.volume
            net += signed
            gross += abs(pos.volume)
        status = PositionStatus.OPEN if open_positions else PositionStatus.CLOSED
        return PositionSnapshot(
            symbol=symbol,
            positions=open_positions,
            net_volume=net,
            gross_volume=gross,
            status=status,
            snapshot_at_utc=datetime.now(timezone.utc),
            request_id=str(uuid.uuid4()),
            source_id="internal_ledger",
        )

    def get_exposure(self, symbol: str) -> ExposureSummary:
        return self._exposure.compute(symbol, self._ledger.open_positions(symbol))

    def apply_event(self, event: PositionEvent) -> None:
        if not event.event_id or not event.correlation_id or not event.timestamp_utc:
            raise PositionStateError("event missing telemetry fields (CA-07)")
        self._ledger.apply(event)

    def sync_from_broker(self, symbol: str) -> PositionSnapshot:
        positions = self._sync.fetch_open_positions(symbol)
        event = PositionEvent(
            event_id=str(uuid.uuid4()),
            event_type="SYNC",
            ticket=None,
            symbol=symbol,
            payload={
                "positions": [
                    {
                        "ticket": p.ticket,
                        "side": p.side.value,
                        "volume": p.volume,
                        "price_open": p.price_open,
                        "price_current": p.price_current,
                        "sl": p.sl,
                        "tp": p.tp,
                        "profit": p.profit,
                        "magic": p.magic,
                        "source_id": p.source_id,
                        "lineage_id": p.lineage_id,
                    }
                    for p in positions
                ]
            },
            timestamp_utc=datetime.now(timezone.utc),
            correlation_id=str(uuid.uuid4()),
            source=self._sync.adapter_id(),
        )
        self._ledger.apply(event)
        snap = self.get_snapshot(symbol)
        return PositionSnapshot(
            symbol=snap.symbol,
            positions=snap.positions,
            net_volume=snap.net_volume,
            gross_volume=snap.gross_volume,
            status=snap.status,
            snapshot_at_utc=snap.snapshot_at_utc,
            request_id=str(uuid.uuid4()),
            source_id=self._sync.adapter_id(),
        )

    def is_flat(self, symbol: str) -> bool:
        return len(self._ledger.open_positions(symbol)) == 0

    def apply_mark_price(self, symbol: str, mark_price: float) -> None:
        """CA-08: atualiza price_current / unrealized PnL a partir de mark MIG-2."""
        for pos in self._ledger.open_positions(symbol):
            if pos.side == PositionSide.LONG:
                profit = (mark_price - pos.price_open) * pos.volume
            else:
                profit = (pos.price_open - mark_price) * pos.volume
            event = PositionEvent(
                event_id=str(uuid.uuid4()),
                event_type="MODIFIED",
                ticket=pos.ticket,
                symbol=symbol,
                payload={"price_current": mark_price, "profit": profit},
                timestamp_utc=datetime.now(timezone.utc),
                correlation_id=str(uuid.uuid4()),
                source="mig2_mark",
            )
            self._ledger.apply(event)

    def apply_market_snapshot(self, snapshot: MarketDataSnapshot) -> None:
        """CA-08: usa close mais recente do MIG-2 como mark."""
        if not snapshot.bars:
            raise PositionStateError("empty market snapshot for mark")
        mark = snapshot.bars[0].close
        self.apply_mark_price(snapshot.symbol, mark)
