"""Testes MIG-3 — CA-01 a CA-08 (DEC-MIG3-001 · TASK-0023)."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from contracts.market_data_contract import MarketDataSnapshot, OHLCVBar
from contracts.position_contract import (
    PositionEvent,
    PositionSide,
    PositionStateError,
    PositionTicket,
)
from market_data.providers.mock_provider import _generate_fixed_bars
from position_manager import SovereignPositionManager
from position_manager.ledger import PositionLedger
from position_manager.sync.mock_sync import MockBrokerSync


ROOT = Path(__file__).resolve().parent.parent


def _ts() -> datetime:
    return datetime(2026, 6, 27, 12, 0, 0, tzinfo=timezone.utc)


def _opened_event(
    ticket: int = 1001,
    symbol: str = "XAUUSD",
    side: PositionSide = PositionSide.LONG,
    volume: float = 0.1,
    price: float = 3990.0,
    event_id: str = "evt-1",
    correlation_id: str = "corr-1",
) -> PositionEvent:
    return PositionEvent(
        event_id=event_id,
        event_type="OPENED",
        ticket=ticket,
        symbol=symbol,
        payload={
            "side": side.value,
            "volume": volume,
            "price_open": price,
            "price_current": price,
            "profit": 0.0,
            "magic": 42,
            "source_id": "mock_fill",
            "lineage_id": correlation_id,
        },
        timestamp_utc=_ts(),
        correlation_id=correlation_id,
        source="mock_mig6_fill",
    )


def _manager() -> SovereignPositionManager:
    return SovereignPositionManager(sync_adapter=MockBrokerSync())


# CA-01
def test_ca01_position_contract_importable() -> None:
    from contracts import position_contract  # noqa: F401

    assert hasattr(position_contract, "PositionTicket")
    assert hasattr(position_contract, "PositionManager")
    assert hasattr(position_contract, "PositionStateError")


# CA-02
def test_ca02_no_order_send_in_position_manager() -> None:
    pkg = ROOT / "position_manager"
    for path in pkg.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "order_send(" not in text, f"order_send() call found in {path}"


# CA-03
def test_ca03_fail_closed_invalid_volume() -> None:
    mgr = _manager()
    event = _opened_event(volume=0.0)
    with pytest.raises(PositionStateError):
        mgr.apply_event(event)


# CA-04
def test_ca04_duplicate_open_ticket_raises() -> None:
    mgr = _manager()
    mgr.apply_event(_opened_event(ticket=1001, event_id="e1", correlation_id="c1"))
    with pytest.raises(PositionStateError):
        mgr.apply_event(_opened_event(ticket=1001, event_id="e2", correlation_id="c2"))


# CA-05
def test_ca05_deterministic_snapshot_from_events() -> None:
    def run() -> str:
        ledger = PositionLedger()
        mgr = SovereignPositionManager(sync_adapter=MockBrokerSync(), ledger=ledger)
        mgr.apply_event(_opened_event(ticket=1001, event_id="e1", correlation_id="c1"))
        mgr.apply_event(_opened_event(ticket=1002, side=PositionSide.SHORT, event_id="e2", correlation_id="c2"))
        snap = mgr.get_snapshot("XAUUSD")
        payload = {
            "net": snap.net_volume,
            "gross": snap.gross_volume,
            "tickets": [p.ticket for p in snap.positions],
        }
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

    assert run() == run()


# CA-06
def test_ca06_no_mt5_import_in_core_modules() -> None:
    import position_manager.manager as mgr_mod
    import position_manager.ledger as ledger_mod

    for mod in (mgr_mod, ledger_mod):
        src = Path(mod.__file__).read_text(encoding="utf-8")
        assert "MetaTrader5" not in src
        assert "import mt5" not in src


# CA-07
def test_ca07_event_telemetry_fields() -> None:
    mgr = _manager()
    event = _opened_event()
    mgr.apply_event(event)
    stored = mgr._ledger.events[0]
    assert stored.event_id == "evt-1"
    assert stored.correlation_id == "corr-1"
    assert stored.timestamp_utc.tzinfo is not None


# CA-08
def test_ca08_mig2_mark_updates_unrealized_pnl() -> None:
    mgr = _manager()
    mgr.apply_event(_opened_event(price=3990.0))
    bars = _generate_fixed_bars("XAUUSD", "M1", 5)
    snapshot = MarketDataSnapshot(
        symbol="XAUUSD",
        timeframe="M1",
        bars=bars,
        bar_count=len(bars),
        fetched_at_utc=_ts(),
        source_id="mock_test",
        request_id="req-1",
    )
    mgr.apply_market_snapshot(snapshot)
    snap = mgr.get_snapshot("XAUUSD")
    assert snap.positions[0].price_current == bars[0].close
    assert snap.positions[0].profit is not None


def test_is_flat_and_exposure() -> None:
    mgr = _manager()
    assert mgr.is_flat("XAUUSD")
    mgr.apply_event(_opened_event())
    assert not mgr.is_flat("XAUUSD")
    exp = mgr.get_exposure("XAUUSD")
    assert exp.net_side == PositionSide.LONG
    assert exp.open_ticket_count == 1


def test_sync_from_broker_mock() -> None:
    ticket = PositionTicket(
        ticket=2001,
        symbol="XAUUSD",
        side=PositionSide.LONG,
        volume=0.2,
        price_open=4000.0,
        price_current=4001.0,
        sl=None,
        tp=None,
        profit=1.0,
        magic=0,
        opened_at_utc=_ts(),
        closed_at_utc=None,
        source_id="mock_broker",
        lineage_id="ln-1",
    )
    mgr = SovereignPositionManager(sync_adapter=MockBrokerSync(positions=(ticket,)))
    snap = mgr.sync_from_broker("XAUUSD")
    assert len(snap.positions) == 1
    assert snap.source_id == "mock_broker"
