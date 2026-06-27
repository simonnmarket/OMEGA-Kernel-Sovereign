"""Mock broker sync — CA-06 CI sem MT5."""

from __future__ import annotations

from contracts.position_contract import PositionSyncAdapter, PositionTicket


class MockBrokerSync:
    """Read-only mock — retorna posições fixas configuráveis."""

    def __init__(self, positions: tuple[PositionTicket, ...] | None = None) -> None:
        self._positions = positions or ()

    def fetch_open_positions(self, symbol: str) -> tuple[PositionTicket, ...]:
        return tuple(p for p in self._positions if p.symbol == symbol)

    def adapter_id(self) -> str:
        return "mock_broker"
