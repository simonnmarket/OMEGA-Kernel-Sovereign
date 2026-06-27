"""MIG-3 ExposureCalculator — agregação para MIG-4."""

from __future__ import annotations

from datetime import datetime, timezone

from contracts.position_contract import ExposureSummary, PositionSide, PositionTicket


class ExposureCalculator:
    def compute(self, symbol: str, open_positions: tuple[PositionTicket, ...]) -> ExposureSummary:
        net = 0.0
        gross = 0.0
        pnl_total = 0.0
        has_pnl = True

        for pos in open_positions:
            signed = pos.volume if pos.side == PositionSide.LONG else -pos.volume
            net += signed
            gross += abs(pos.volume)
            if pos.profit is None:
                has_pnl = False
            else:
                pnl_total += pos.profit

        if net > 0:
            net_side = PositionSide.LONG
        elif net < 0:
            net_side = PositionSide.SHORT
        else:
            net_side = PositionSide.FLAT

        return ExposureSummary(
            symbol=symbol,
            net_side=net_side,
            net_volume=net,
            open_ticket_count=len(open_positions),
            total_unrealized_pnl=pnl_total if has_pnl and open_positions else None,
            computed_at_utc=datetime.now(timezone.utc),
        )
