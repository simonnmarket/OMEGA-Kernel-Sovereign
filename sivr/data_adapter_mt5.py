"""Adaptador MT5 demo — OHLCV reais para SIVR-0."""

from __future__ import annotations

from dataclasses import dataclass

import MetaTrader5 as mt5

TIMEFRAME_MAP = {
    "M1": mt5.TIMEFRAME_M1,
    "M5": mt5.TIMEFRAME_M5,
    "M15": mt5.TIMEFRAME_M15,
    "H1": mt5.TIMEFRAME_H1,
}


class Mt5AdapterError(RuntimeError):
    """Falha de conexão ou dados MT5."""


@dataclass(frozen=True)
class MarketSnapshot:
    symbol: str
    closes: tuple[float, ...]
    bar_count: int


def initialize(mt5_path: str | None = None) -> None:
    if mt5_path:
        if not mt5.initialize(path=mt5_path):
            raise Mt5AdapterError(f"mt5.initialize failed: {mt5.last_error()}")
    elif not mt5.initialize():
        raise Mt5AdapterError(f"mt5.initialize failed: {mt5.last_error()}")


def shutdown() -> None:
    mt5.shutdown()


def fetch_closes(symbol: str, timeframe: str, bars: int) -> MarketSnapshot:
    tf = TIMEFRAME_MAP.get(timeframe)
    if tf is None:
        raise Mt5AdapterError(f"unsupported timeframe: {timeframe}")

    if not mt5.symbol_select(symbol, True):
        raise Mt5AdapterError(f"symbol_select failed for {symbol}: {mt5.last_error()}")

    rates = mt5.copy_rates_from_pos(symbol, tf, 0, bars)
    if rates is None or len(rates) == 0:
        raise Mt5AdapterError(f"copy_rates_from_pos returned no data: {mt5.last_error()}")

    closes = tuple(float(bar["close"]) for bar in rates)
    return MarketSnapshot(symbol=symbol, closes=closes, bar_count=len(closes))
