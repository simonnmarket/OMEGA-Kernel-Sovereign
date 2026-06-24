"""RSI (Relative Strength Index) — implementação pura Python, sem dependências."""

from __future__ import annotations

from collections.abc import Sequence

from contracts.indicator_contract import IndicatorError

DEFAULT_RSI_PERIOD = 14


def compute_rsi(closes: Sequence[float], period: int = DEFAULT_RSI_PERIOD) -> float:
    if period < 1:
        raise IndicatorError("period must be >= 1")
    if len(closes) < period + 1:
        raise IndicatorError(
            f"need at least {period + 1} closes for RSI({period}), got {len(closes)}"
        )

    gains: list[float] = []
    losses: list[float] = []
    for i in range(1, len(closes)):
        delta = closes[i] - closes[i - 1]
        gains.append(delta if delta > 0 else 0.0)
        losses.append(-delta if delta < 0 else 0.0)

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period

    if avg_loss == 0:
        return 100.0

    rs = avg_gain / avg_loss
    return 100.0 - (100.0 / (1.0 + rs))
