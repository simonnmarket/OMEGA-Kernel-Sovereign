"""MIG-2 MockDataProvider — provider determinístico para CI.

Zero dependência MT5. Nunca dados sintéticos implícitos — cada mock
declara explicitamente source_id="mock_test".
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from contracts.market_data_contract import (
    BarRequest,
    OHLCVBar,
    ProviderConfig,
)


class MockDataProvider:
    """Provider de teste com barras fixas e determinísticas."""

    _PROVIDER_ID = "mock_test"

    def __init__(self, bars: tuple[OHLCVBar, ...] | None = None) -> None:
        self._bars = bars
        self._connected = False

    def connect(self, config: ProviderConfig) -> None:
        self._connected = True

    def disconnect(self) -> None:
        self._connected = False

    def fetch_bars(self, request: BarRequest) -> tuple[OHLCVBar, ...]:
        if self._bars is not None:
            return self._bars[: request.bar_count]
        return _generate_fixed_bars(
            request.symbol, request.timeframe, request.bar_count
        )

    def is_connected(self) -> bool:
        return self._connected

    def provider_id(self) -> str:
        return self._PROVIDER_ID


def _generate_fixed_bars(
    symbol: str, timeframe: str, count: int
) -> tuple[OHLCVBar, ...]:
    """Série OHLCV determinística baseada em índice — sem random, sem seed."""
    import math

    base_price = 3990.0
    base_time = datetime(2026, 6, 25, 12, 0, 0, tzinfo=timezone.utc)
    bars = []
    for i in range(count):
        close = base_price + 5.0 * math.sin(i * 0.3)
        close = round(close, 4)
        bar = OHLCVBar(
            symbol=symbol,
            timeframe=timeframe,
            open=round(close - 0.05, 4),
            high=round(close + 0.10, 4),
            low=round(close - 0.10, 4),
            close=close,
            volume=1000.0 + (i * 7) % 500,
            timestamp_utc=base_time - timedelta(minutes=i),
            bar_index=i,
        )
        bars.append(bar)
    return tuple(bars)
