"""Core engine — compõe RSI e EMA a partir de dados mock."""

from __future__ import annotations

from contracts.indicator_contract import IndicatorInput, IndicatorOutput
from indicator_engine.ema import DEFAULT_EMA_PERIOD, compute_ema
from indicator_engine.rsi import DEFAULT_RSI_PERIOD, compute_rsi


class MinimalIndicatorEngine:
    """Indicator Engine mínimo isolado — MIG-1 Execution Pack v1.0."""

    def __init__(
        self,
        rsi_period: int = DEFAULT_RSI_PERIOD,
        ema_period: int = DEFAULT_EMA_PERIOD,
    ) -> None:
        self._rsi_period = rsi_period
        self._ema_period = ema_period

    def calculate(self, data: IndicatorInput) -> IndicatorOutput:
        rsi = compute_rsi(data.closes, self._rsi_period)
        ema = compute_ema(data.closes, self._ema_period)
        return IndicatorOutput(rsi=rsi, ema=ema)
