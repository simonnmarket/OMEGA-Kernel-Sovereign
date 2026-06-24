"""MIG-2 SovereignMarketDataEngine — orquestra fetch + validate + snapshot.

Pipeline:
1. DataProvider.connect()
2. DataProvider.fetch_bars()
3. DataValidator.validate()
4. SnapshotFactory.build() → MarketDataSnapshot (frozen, auditável)
5. DataProvider.disconnect()

Fail-closed: qualquer etapa com erro → MarketDataError propagada.
Nunca dado sintético silencioso (anti BUG-002).
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from contracts.market_data_contract import (
    BarRequest,
    DataProvider,
    FeedSpec,
    MarketDataSnapshot,
    ProviderConfig,
)
from market_data.validator import DataValidator


class SovereignMarketDataEngine:
    """Implementação canônica do MarketDataEngine MIG-2."""

    def __init__(
        self,
        provider: DataProvider,
        config: ProviderConfig | None = None,
        validator: DataValidator | None = None,
    ) -> None:
        self._provider = provider
        self._config = config or ProviderConfig()
        self._validator = validator or DataValidator()

    def fetch(self, spec: FeedSpec) -> MarketDataSnapshot:
        """Busca, valida e retorna snapshot imutável. Fail-closed."""
        self._provider.connect(self._config)
        try:
            request = BarRequest(
                symbol=spec.symbol,
                timeframe=spec.timeframe,
                bar_count=spec.bar_count,
            )
            bars = self._provider.fetch_bars(request)
            self._validator.validate(
                bars,
                min_count=spec.bar_count,
                max_staleness_seconds=spec.max_staleness_seconds,
            )
        finally:
            self._provider.disconnect()

        return MarketDataSnapshot(
            symbol=spec.symbol,
            timeframe=spec.timeframe,
            bars=bars,
            bar_count=len(bars),
            fetched_at_utc=datetime.now(timezone.utc),
            source_id=self._provider.provider_id(),
            request_id=str(uuid.uuid4()),
        )

    def fetch_closes(self, spec: FeedSpec) -> tuple[float, ...]:
        """Extrai closes do snapshot para adapter MIG-1 (oldest → newest)."""
        snapshot = self.fetch(spec)
        return tuple(bar.close for bar in reversed(snapshot.bars))
