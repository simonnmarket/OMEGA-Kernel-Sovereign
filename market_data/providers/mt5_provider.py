"""MIG-2 MT5DataProvider — provider soberano para MetaTrader 5.

Substitui sivr/data_adapter_mt5.py (deprecado pós-GATE-MIG2).
Fail-closed: qualquer falha → exceção tipada da hierarquia MarketDataError.
"""

from __future__ import annotations

from datetime import datetime, timezone

import MetaTrader5 as mt5

from contracts.market_data_contract import (
    BarRequest,
    ConnectionError,
    DataIntegrityError,
    OHLCVBar,
    ProviderConfig,
    UnsupportedSymbolError,
    UnsupportedTimeframeError,
)

_TIMEFRAME_MAP: dict[str, int] = {
    "M1": mt5.TIMEFRAME_M1,
    "M5": mt5.TIMEFRAME_M5,
    "M15": mt5.TIMEFRAME_M15,
    "H1": mt5.TIMEFRAME_H1,
    "H4": mt5.TIMEFRAME_H4,
    "D1": mt5.TIMEFRAME_D1,
}

_PROVIDER_ID = "mt5_demo"


class MT5DataProvider:
    """DataProvider soberano para MT5. Sem ordens. Apenas leitura."""

    def __init__(self) -> None:
        self._connected = False

    def connect(self, config: ProviderConfig) -> None:
        kwargs = {"path": config.mt5_path} if config.mt5_path else {}
        if not mt5.initialize(**kwargs):
            raise ConnectionError(f"mt5.initialize falhou: {mt5.last_error()}")
        self._connected = True

    def disconnect(self) -> None:
        mt5.shutdown()
        self._connected = False

    def fetch_bars(self, request: BarRequest) -> tuple[OHLCVBar, ...]:
        if not self._connected:
            raise ConnectionError("Provider não conectado — chame connect() primeiro")

        tf = _TIMEFRAME_MAP.get(request.timeframe)
        if tf is None:
            raise UnsupportedTimeframeError(f"Timeframe não suportado: {request.timeframe}")

        if not mt5.symbol_select(request.symbol, True):
            raise UnsupportedSymbolError(
                f"symbol_select falhou para {request.symbol}: {mt5.last_error()}"
            )

        rates = mt5.copy_rates_from_pos(request.symbol, tf, 0, request.bar_count)
        if rates is None or len(rates) == 0:
            raise DataIntegrityError(
                f"copy_rates_from_pos retornou vazio para {request.symbol}: {mt5.last_error()}"
            )

        bars = tuple(
            OHLCVBar(
                symbol=request.symbol,
                timeframe=request.timeframe,
                open=float(r["open"]),
                high=float(r["high"]),
                low=float(r["low"]),
                close=float(r["close"]),
                volume=float(r["tick_volume"]),
                timestamp_utc=datetime.fromtimestamp(int(r["time"]), tz=timezone.utc),
                bar_index=i,
            )
            for i, r in enumerate(reversed(rates))
        )
        return bars

    def is_connected(self) -> bool:
        return self._connected

    def provider_id(self) -> str:
        return _PROVIDER_ID
