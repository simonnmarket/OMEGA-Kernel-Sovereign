"""Ponte SIVR: market data → MIG-1 → output com sinal mínimo."""

from __future__ import annotations

import math
from dataclasses import dataclass

from contracts import IndicatorInput
from indicator_engine import MinimalIndicatorEngine

from sivr.data_adapter_mt5 import MarketSnapshot


@dataclass(frozen=True)
class PipelineOutput:
    rsi: float
    ema: float
    signal: str


def _validate_metric(value: float, name: str) -> None:
    if value is None or math.isnan(value) or math.isinf(value):
        raise ValueError(f"invalid {name}: {value!r}")


def derive_signal(rsi: float, buy_below: float, sell_above: float) -> str:
    if rsi < buy_below:
        return "BUY"
    if rsi > sell_above:
        return "SELL"
    return "HOLD"


class ExecutionBridge:
    """Integra MIG-1 sem strategy/execution engine."""

    def __init__(
        self,
        rsi_period: int = 14,
        ema_period: int = 10,
        buy_below: float = 30.0,
        sell_above: float = 70.0,
    ) -> None:
        self._engine = MinimalIndicatorEngine(rsi_period=rsi_period, ema_period=ema_period)
        self._buy_below = buy_below
        self._sell_above = sell_above

    def run(self, snapshot: MarketSnapshot) -> PipelineOutput:
        result = self._engine.calculate(IndicatorInput(closes=snapshot.closes))
        _validate_metric(result.rsi, "rsi")
        _validate_metric(result.ema, "ema")
        signal = derive_signal(result.rsi, self._buy_below, self._sell_above)
        return PipelineOutput(rsi=result.rsi, ema=result.ema, signal=signal)
