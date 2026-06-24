"""MIG-2 DataValidator — valida integridade de barras OHLCV.

Regras:
- Invariante OHLC: low <= min(open,close) <= max(open,close) <= high
- Todos os floats finitos (não NaN, não Inf)
- Sequência temporal: barras ordenadas sem duplicatas
- Staleness: barra mais recente dentro de max_staleness_seconds (opcional)
- bar_count mínimo respeitado
"""

from __future__ import annotations

import math
from datetime import datetime, timezone

from contracts.market_data_contract import DataIntegrityError, OHLCVBar


class DataValidator:
    """Valida uma sequência de OHLCVBar. Fail-closed: erro → DataIntegrityError."""

    def validate(
        self,
        bars: tuple[OHLCVBar, ...],
        min_count: int = 1,
        max_staleness_seconds: float | None = None,
    ) -> None:
        if len(bars) < min_count:
            raise DataIntegrityError(
                f"bar_count insuficiente: {len(bars)} < {min_count}"
            )

        for bar in bars:
            self._validate_bar(bar)

        self._validate_sequence(bars)

        if max_staleness_seconds is not None:
            self._validate_staleness(bars[0], max_staleness_seconds)

    def _validate_bar(self, bar: OHLCVBar) -> None:
        for field, value in [
            ("open", bar.open), ("high", bar.high),
            ("low", bar.low), ("close", bar.close), ("volume", bar.volume),
        ]:
            if not math.isfinite(value):
                raise DataIntegrityError(
                    f"{bar.symbol} bar_index={bar.bar_index}: {field}={value!r} não é finito"
                )

        if not (bar.low <= min(bar.open, bar.close) <= max(bar.open, bar.close) <= bar.high):
            raise DataIntegrityError(
                f"{bar.symbol} bar_index={bar.bar_index}: invariante OHLC violada "
                f"(O={bar.open} H={bar.high} L={bar.low} C={bar.close})"
            )

        if bar.timestamp_utc.tzinfo is None:
            raise DataIntegrityError(
                f"{bar.symbol} bar_index={bar.bar_index}: timestamp_utc sem timezone"
            )

    def _validate_sequence(self, bars: tuple[OHLCVBar, ...]) -> None:
        for i in range(len(bars) - 1):
            if bars[i].timestamp_utc <= bars[i + 1].timestamp_utc:
                raise DataIntegrityError(
                    f"Sequência temporal inválida: bar[{i}].timestamp "
                    f"{bars[i].timestamp_utc} <= bar[{i+1}].timestamp "
                    f"{bars[i+1].timestamp_utc} (esperado decrescente: 0=mais recente)"
                )

    def _validate_staleness(self, newest_bar: OHLCVBar, max_seconds: float) -> None:
        now_utc = datetime.now(timezone.utc)
        age = (now_utc - newest_bar.timestamp_utc).total_seconds()
        if age > max_seconds:
            raise DataIntegrityError(
                f"Barra mais recente com {age:.0f}s de idade "
                f"(máximo={max_seconds}s): {newest_bar.timestamp_utc}"
            )
