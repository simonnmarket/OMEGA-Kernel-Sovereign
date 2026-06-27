"""TASK-0023-V6-VALIDATION-001 — Validação integrada baseline V6.

Pipeline: MIG-2 → MIG-1 → MIG-3
Critérios: CA-V6-01 .. CA-V6-06

Não altera módulos internos — apenas orquestra integração.
"""

from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import pytest

from contracts.indicator_contract import IndicatorInput
from contracts.market_data_contract import FeedSpec
from contracts.position_contract import PositionEvent, PositionSide
from indicator_engine import MinimalIndicatorEngine
from market_data.engine import SovereignMarketDataEngine
from market_data.providers.mock_provider import MockDataProvider
from position_manager import SovereignPositionManager
from position_manager.sync.mock_sync import MockBrokerSync

ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT_PATH = ROOT / "validation" / "snapshots" / "v6_baseline_deterministic_snapshot.json"

SPEC = FeedSpec(symbol="XAUUSD", timeframe="M1", bar_count=20, environment="validation")
BASE_TS = datetime(2026, 6, 27, 12, 0, 0, tzinfo=timezone.utc)


def _mig2_engine() -> SovereignMarketDataEngine:
    return SovereignMarketDataEngine(provider=MockDataProvider())


def _fill_event(
    ticket: int,
    event_id: str,
    correlation_id: str,
    price: float = 3990.0,
) -> PositionEvent:
    return PositionEvent(
        event_id=event_id,
        event_type="OPENED",
        ticket=ticket,
        symbol="XAUUSD",
        payload={
            "side": PositionSide.LONG.value,
            "volume": 0.1,
            "price_open": price,
            "price_current": price,
            "profit": 0.0,
            "magic": 42,
            "source_id": "mock_fill",
            "lineage_id": correlation_id,
        },
        timestamp_utc=BASE_TS,
        correlation_id=correlation_id,
        source="mock_mig6_fill",
    )


def run_v6_pipeline(*, cycles: int = 3) -> dict:
    """Executa pipeline integrado e retorna estado determinístico (sem UUIDs/timestamps)."""
    mig2 = _mig2_engine()
    snapshot = mig2.fetch(SPEC)
    closes = mig2.fetch_closes(SPEC)

    mig1 = MinimalIndicatorEngine()
    indicators = mig1.calculate(IndicatorInput(closes=closes))

    mgr = SovereignPositionManager(sync_adapter=MockBrokerSync())
    for i in range(cycles):
        mgr.apply_event(
            _fill_event(
                ticket=1000 + i,
                event_id=f"evt-{i}",
                correlation_id=f"corr-{i}",
                price=closes[-1],
            )
        )
        mgr.apply_market_snapshot(snapshot)

    pos_snap = mgr.get_snapshot("XAUUSD")
    exposure = mgr.get_exposure("XAUUSD")

    return {
        "closes_count": len(closes),
        "closes_hash": hashlib.sha256(json.dumps(closes).encode()).hexdigest(),
        "bars_finite": all(
            math.isfinite(b.close) and math.isfinite(b.open)
            for b in snapshot.bars
        ),
        "rsi": indicators.rsi,
        "ema": indicators.ema,
        "net_volume": pos_snap.net_volume,
        "gross_volume": pos_snap.gross_volume,
        "open_tickets": sorted(p.ticket for p in pos_snap.positions),
        "mark_prices": [p.price_current for p in pos_snap.positions],
        "profits": [p.profit for p in pos_snap.positions],
        "ledger_event_count": len(mgr._ledger.events),
        "exposure_net_side": exposure.net_side.value,
        "is_flat": mgr.is_flat("XAUUSD"),
    }


def export_deterministic_snapshot() -> Path:
    """Persiste snapshot determinístico para evidência institucional."""
    state = run_v6_pipeline(cycles=3)
    payload = {
        "task_id": "TASK-0023-V6-VALIDATION-001",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "pipeline": "MIG-2 → MIG-1 → MIG-3",
        "deterministic_state": state,
        "state_fingerprint": hashlib.sha256(
            json.dumps(state, sort_keys=True).encode()
        ).hexdigest(),
    }
    SNAPSHOT_PATH.parent.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return SNAPSHOT_PATH


# ---------------------------------------------------------------------------
# CA-V6-01 — Consistência de dados
# ---------------------------------------------------------------------------


def test_ca_v6_01_valid_ohlcv_no_nan() -> None:
    mig2 = _mig2_engine()
    snapshot = mig2.fetch(SPEC)
    closes = mig2.fetch_closes(SPEC)

    assert len(closes) == SPEC.bar_count
    assert all(math.isfinite(c) for c in closes)
    for bar in snapshot.bars:
        assert math.isfinite(bar.close)
        assert math.isfinite(bar.open)
        assert math.isfinite(bar.high)
        assert math.isfinite(bar.low)
        assert not math.isnan(bar.volume)


# ---------------------------------------------------------------------------
# CA-V6-02 — Determinismo MIG-1
# ---------------------------------------------------------------------------


def test_ca_v6_02_indicator_determinism() -> None:
    closes = _mig2_engine().fetch_closes(SPEC)
    mig1 = MinimalIndicatorEngine()
    first = mig1.calculate(IndicatorInput(closes=closes))
    second = mig1.calculate(IndicatorInput(closes=closes))
    assert first == second
    assert math.isfinite(first.rsi)
    assert math.isfinite(first.ema)


# ---------------------------------------------------------------------------
# CA-V6-03 — Integração MIG-3
# ---------------------------------------------------------------------------


def test_ca_v6_03_position_manager_multi_cycle_ledger() -> None:
    state_a = run_v6_pipeline(cycles=3)
    state_b = run_v6_pipeline(cycles=3)
    assert state_a["ledger_event_count"] == state_b["ledger_event_count"]
    assert state_a["open_tickets"] == state_b["open_tickets"]
    assert state_a["net_volume"] == state_b["net_volume"]
    assert not state_a["is_flat"]


# ---------------------------------------------------------------------------
# CA-V6-04 — Fluxo end-to-end
# ---------------------------------------------------------------------------


def test_ca_v6_04_end_to_end_pipeline() -> None:
    mig2 = _mig2_engine()
    snapshot = mig2.fetch(SPEC)
    closes = mig2.fetch_closes(SPEC)

    output = MinimalIndicatorEngine().calculate(IndicatorInput(closes=closes))
    assert output.rsi is not None

    mgr = SovereignPositionManager(sync_adapter=MockBrokerSync())
    mgr.apply_event(_fill_event(ticket=9001, event_id="e2e-1", correlation_id="c2e-1"))
    mgr.apply_market_snapshot(snapshot)

    snap = mgr.get_snapshot("XAUUSD")
    assert len(snap.positions) == 1
    assert snap.positions[0].price_current == snapshot.bars[0].close
    assert snap.positions[0].profit is not None


# ---------------------------------------------------------------------------
# CA-V6-05 — Isolamento de execução
# ---------------------------------------------------------------------------


def test_ca_v6_05_no_order_send_in_baseline_packages() -> None:
    packages = ("indicator_engine", "market_data", "position_manager")
    for pkg_name in packages:
        pkg = ROOT / pkg_name
        for path in pkg.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            assert "order_send(" not in text, f"order_send() in {path}"


def test_ca_v6_05_no_mig6_execution_imports() -> None:
    import indicator_engine  # noqa: F401
    import market_data.engine  # noqa: F401
    import position_manager.manager  # noqa: F401

    for mod_name in ("execution", "execution_engine", "order_manager"):
        assert mod_name not in dir(indicator_engine)


# ---------------------------------------------------------------------------
# CA-V6-06 — Reprodutibilidade
# ---------------------------------------------------------------------------


def test_ca_v6_06_reproducible_final_state() -> None:
    fingerprints = {
        hashlib.sha256(json.dumps(run_v6_pipeline(cycles=3), sort_keys=True).encode()).hexdigest()
        for _ in range(5)
    }
    assert len(fingerprints) == 1


def test_ca_v6_06_export_deterministic_snapshot() -> None:
    path = export_deterministic_snapshot()
    assert path.exists()
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["task_id"] == "TASK-0023-V6-VALIDATION-001"
    assert "state_fingerprint" in data
