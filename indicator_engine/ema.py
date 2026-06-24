"""EMA (Exponential Moving Average) — implementação pura Python, sem dependências."""

from __future__ import annotations

from collections.abc import Sequence

from contracts.indicator_contract import IndicatorError

DEFAULT_EMA_PERIOD = 10


def compute_ema(closes: Sequence[float], period: int = DEFAULT_EMA_PERIOD) -> float:
    if period < 1:
        raise IndicatorError("period must be >= 1")
    if len(closes) < period:
        raise IndicatorError(
            f"need at least {period} closes for EMA({period}), got {len(closes)}"
        )

    multiplier = 2.0 / (period + 1)
    ema = sum(closes[:period]) / period

    for price in closes[period:]:
        ema = (price - ema) * multiplier + ema

    return ema
