"""MIG-3 PositionValidator — invariantes fail-closed."""

from __future__ import annotations

import math

from contracts.position_contract import (
    PositionSide,
    PositionStateError,
    PositionTicket,
)


class PositionValidator:
    def validate_ticket(self, ticket: PositionTicket) -> None:
        if ticket.volume <= 0 or not math.isfinite(ticket.volume):
            raise PositionStateError(f"invalid volume for ticket {ticket.ticket}")
        if not math.isfinite(ticket.price_open):
            raise PositionStateError(f"invalid price_open for ticket {ticket.ticket}")
        if ticket.side not in {PositionSide.LONG, PositionSide.SHORT}:
            raise PositionStateError(f"invalid side for open ticket {ticket.ticket}")

    def validate_no_duplicate_open(
        self,
        ticket_id: int,
        open_tickets: dict[int, PositionTicket],
    ) -> None:
        if ticket_id in open_tickets:
            raise PositionStateError(f"duplicate OPEN ticket: {ticket_id}")
