"""Testes MIG-2 — CA-01 a CA-08 (DEC-MIG2-001 · TASK-0022).

CA-01: contrato importável antes de qualquer código market_data/
CA-02: zero fallback sintético no caminho soberano
CA-03: fail-closed — falha propaga DataIntegrityError, nunca snapshot parcial
CA-04: OHLCVBar e MarketDataSnapshot imutáveis; invariantes OHLC validadas
CA-05: determinismo — mock com barras fixas → snapshot idêntico em N runs
CA-06: CI sem dependência MT5 (MockDataProvider only)
CA-07: log estruturado por fetch (request_id, source_id, bar_count)
CA-08: adapter MIG-1 (snapshot → closes → IndicatorInput) testado isoladamente
"""

from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timedelta, timezone

import pytest

from contracts.market_data_contract import (
    BarRequest,
    DataIntegrityError,
    FeedSpec,
    MarketDataSnapshot,
    OHLCVBar,
    ProviderConfig,
)
from market_data.engine import SovereignMarketDataEngine
from market_data.providers.mock_provider import MockDataProvider, _generate_fixed_bars
from market_data.validator import DataValidator


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _make_bar(
    index: int = 0,
    close: float = 3990.0,
    offset_minutes: int = 0,
) -> OHLCVBar:
    ts = datetime(2026, 6, 25, 12, 0, 0, tzinfo=timezone.utc) - timedelta(minutes=offset_minutes)
    return OHLCVBar(
        symbol="XAUUSD",
        timeframe="M1",
        open=close - 0.05,
        high=close + 0.10,
        low=close - 0.10,
        close=close,
        volume=1000.0,
        timestamp_utc=ts,
        bar_index=index,
    )


def _make_snapshot(bar_count: int = 20) -> MarketDataSnapshot:
    bars = _generate_fixed_bars("XAUUSD", "M1", bar_count)
    return MarketDataSnapshot(
        symbol="XAUUSD",
        timeframe="M1",
        bars=bars,
        bar_count=len(bars),
        fetched_at_utc=datetime(2026, 6, 25, 12, 0, 0, tzinfo=timezone.utc),
        source_id="mock_test",
        request_id="fixed-request-id",
    )


def _engine(bars: tuple[OHLCVBar, ...] | None = None) -> SovereignMarketDataEngine:
    return SovereignMarketDataEngine(provider=MockDataProvider(bars=bars))


def _spec(bar_count: int = 20) -> FeedSpec:
    return FeedSpec(symbol="XAUUSD", timeframe="M1", bar_count=bar_count, environment="test")


# ---------------------------------------------------------------------------
# CA-01: contrato importável (import check)
# ---------------------------------------------------------------------------

def test_ca01_contract_importable() -> None:
    """CA-01: market_data_contract importável e tipos instanciáveis."""
    from contracts import market_data_contract  # noqa: F401
    assert hasattr(market_data_contract, "OHLCVBar")
    assert hasattr(market_data_contract, "MarketDataSnapshot")
    assert hasattr(market_data_contract, "DataProvider")
    assert hasattr(market_data_contract, "MarketDataEngine")
    assert hasattr(market_data_contract, "DataIntegrityError")


# ---------------------------------------------------------------------------
# CA-02: zero fallback sintético
# ---------------------------------------------------------------------------

def test_ca02_no_synthetic_fallback_on_provider_error() -> None:
    """CA-02: provider que falha → DataIntegrityError, nunca snapshot com dados inventados."""

    class FailingProvider:
        def connect(self, config: ProviderConfig) -> None: pass
        def disconnect(self) -> None: pass
        def fetch_bars(self, request: BarRequest) -> tuple[OHLCVBar, ...]:
            raise DataIntegrityError("provider falhou — sem dados")
        def is_connected(self) -> bool: return True
        def provider_id(self) -> str: return "mock_fail"

    engine = SovereignMarketDataEngine(provider=FailingProvider())
    with pytest.raises(DataIntegrityError):
        engine.fetch(_spec())


def test_ca02_no_hardcoded_prices_in_sovereign_path() -> None:
    """CA-02: engine.py não contém preços fixos hardcoded."""
    import inspect
    import market_data.engine as engine_mod
    source = inspect.getsource(engine_mod)
    assert "3990" not in source, "Preço fixo hardcoded encontrado em engine.py"
    assert "sample_data" not in source
    assert "_get_sample" not in source


# ---------------------------------------------------------------------------
# CA-03: fail-closed
# ---------------------------------------------------------------------------

def test_ca03_fail_closed_insufficient_bars() -> None:
    """CA-03: bar_count insuficiente → DataIntegrityError."""
    bars = _generate_fixed_bars("XAUUSD", "M1", 5)
    engine = _engine(bars=bars)
    spec = FeedSpec(symbol="XAUUSD", timeframe="M1", bar_count=20, environment="test")
    with pytest.raises(DataIntegrityError, match="bar_count insuficiente"):
        engine.fetch(spec)


def test_ca03_fail_closed_ohlc_invariant() -> None:
    """CA-03: barra com high < close → DataIntegrityError."""
    bad_bar = OHLCVBar(
        symbol="XAUUSD", timeframe="M1",
        open=3990.0, high=3988.0, low=3989.0, close=3991.0,
        volume=1000.0,
        timestamp_utc=datetime(2026, 6, 25, 12, 0, 0, tzinfo=timezone.utc),
        bar_index=0,
    )
    validator = DataValidator()
    with pytest.raises(DataIntegrityError, match="invariante OHLC"):
        validator.validate((bad_bar,), min_count=1)


def test_ca03_fail_closed_nan_value() -> None:
    """CA-03: barra com NaN → DataIntegrityError."""
    bad_bar = OHLCVBar(
        symbol="XAUUSD", timeframe="M1",
        open=float("nan"), high=3991.0, low=3989.0, close=3990.0,
        volume=1000.0,
        timestamp_utc=datetime(2026, 6, 25, 12, 0, 0, tzinfo=timezone.utc),
        bar_index=0,
    )
    validator = DataValidator()
    with pytest.raises(DataIntegrityError, match="não é finito"):
        validator.validate((bad_bar,), min_count=1)


# ---------------------------------------------------------------------------
# CA-04: imutabilidade e invariantes
# ---------------------------------------------------------------------------

def test_ca04_ohlcvbar_immutable() -> None:
    """CA-04: OHLCVBar é frozen dataclass — atribuição deve falhar."""
    bar = _make_bar()
    with pytest.raises((AttributeError, TypeError)):
        bar.close = 9999.0  # type: ignore[misc]


def test_ca04_snapshot_immutable() -> None:
    """CA-04: MarketDataSnapshot é frozen dataclass."""
    snap = _make_snapshot()
    with pytest.raises((AttributeError, TypeError)):
        snap.bar_count = 0  # type: ignore[misc]


def test_ca04_validator_ohlc_valid_passes() -> None:
    """CA-04: barra OHLC válida passa sem exceção."""
    bar = _make_bar(close=3990.0, offset_minutes=0)
    DataValidator().validate((bar,), min_count=1)


# ---------------------------------------------------------------------------
# CA-05: determinismo
# ---------------------------------------------------------------------------

def test_ca05_determinism_same_closes() -> None:
    """CA-05: duas execuções com mock fixo → closes idênticos."""
    closes_1 = _engine().fetch_closes(_spec(20))
    closes_2 = _engine().fetch_closes(_spec(20))
    assert closes_1 == closes_2


def test_ca05_determinism_snapshot_hash() -> None:
    """CA-05: closes serialized → hash idêntico em N runs."""
    def _hash(closes: tuple[float, ...]) -> str:
        return hashlib.sha256(json.dumps(closes).encode()).hexdigest()

    results = {_hash(_engine().fetch_closes(_spec(20))) for _ in range(5)}
    assert len(results) == 1, "Hash diferente entre runs — não determinístico"


# ---------------------------------------------------------------------------
# CA-06: CI sem MT5
# ---------------------------------------------------------------------------

def test_ca06_ci_no_mt5_dependency() -> None:
    """CA-06: engine e validator não importam MT5 directamente."""
    import inspect
    import market_data.engine as engine_mod
    import market_data.validator as validator_mod

    for mod in (engine_mod, validator_mod):
        source = inspect.getsource(mod)
        assert "import MetaTrader5" not in source, (
            f"Import MT5 encontrado em {mod.__name__} — viola CA-06"
        )


# ---------------------------------------------------------------------------
# CA-07: log estruturado por fetch (request_id, source_id, bar_count)
# ---------------------------------------------------------------------------

def test_ca07_snapshot_has_audit_fields() -> None:
    """CA-07: snapshot contém request_id, source_id e bar_count após fetch."""
    snap = _engine().fetch(_spec(20))
    assert snap.request_id, "request_id vazio"
    assert snap.source_id == "mock_test"
    assert snap.bar_count == 20
    assert snap.fetched_at_utc.tzinfo is not None


def test_ca07_request_id_unique_per_fetch() -> None:
    """CA-07: request_id distinto a cada fetch (UUID)."""
    engine = _engine()
    ids = {engine.fetch(_spec(20)).request_id for _ in range(5)}
    assert len(ids) == 5, "request_id repetido — não é UUID único por fetch"


# ---------------------------------------------------------------------------
# CA-08: adapter MIG-1 — snapshot → closes → IndicatorInput
# ---------------------------------------------------------------------------

def test_ca08_mig1_adapter_closes_extraction() -> None:
    """CA-08: fetch_closes retorna closes oldest→newest para IndicatorInput."""
    closes = _engine().fetch_closes(_spec(20))
    assert len(closes) == 20
    assert all(isinstance(c, float) for c in closes)
    assert all(math.isfinite(c) for c in closes)


def test_ca08_mig1_adapter_integration() -> None:
    """CA-08: closes do MIG-2 alimentam MinimalIndicatorEngine sem erro."""
    from contracts.indicator_contract import IndicatorInput
    from indicator_engine import MinimalIndicatorEngine

    closes = _engine().fetch_closes(_spec(20))
    engine_mig1 = MinimalIndicatorEngine()
    output = engine_mig1.calculate(IndicatorInput(closes=closes))

    assert output.rsi is not None
    assert output.ema is not None
    assert math.isfinite(output.rsi)
    assert math.isfinite(output.ema)
