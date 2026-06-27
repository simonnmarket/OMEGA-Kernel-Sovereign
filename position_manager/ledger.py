"""MIG-3 PositionLedger — estado append-only event-sourced."""

from __future__ import annotations

from contracts.position_contract import (
    PositionEvent,
    PositionNotFoundError,
    PositionSide,
    PositionStateError,
    PositionTicket,
)
from position_manager.validator import PositionValidator


class PositionLedger:
    def __init__(self, validator: PositionValidator | None = None) -> None:
        self._validator = validator or PositionValidator()
        self._open: dict[int, PositionTicket] = {}
        self._closed: dict[int, PositionTicket] = {}
        self._events: list[PositionEvent] = []

    @property
    def events(self) -> tuple[PositionEvent, ...]:
        return tuple(self._events)

    def open_positions(self, symbol: str | None = None) -> tuple[PositionTicket, ...]:
        items = self._open.values()
        if symbol is not None:
            items = [p for p in items if p.symbol == symbol]
        return tuple(sorted(items, key=lambda p: p.ticket))

    def apply(self, event: PositionEvent) -> None:
        self._events.append(event)
        if event.event_type == "OPENED":
            self._apply_opened(event)
        elif event.event_type == "CLOSED":
            self._apply_closed(event)
        elif event.event_type == "MODIFIED":
            self._apply_modified(event)
        elif event.event_type == "SYNC":
            self._apply_sync(event)
        else:
            raise PositionStateError(f"unknown event_type: {event.event_type}")

    def _apply_opened(self, event: PositionEvent) -> None:
        ticket = event.ticket
        if ticket is None:
            raise PositionStateError("OPENED event requires ticket")
        self._validator.validate_no_duplicate_open(ticket, self._open)
        payload = event.payload
        pos = PositionTicket(
            ticket=ticket,
            symbol=event.symbol,
            side=PositionSide(str(payload["side"])),
            volume=float(payload["volume"]),
            price_open=float(payload["price_open"]),
            price_current=float(payload["price_current"]) if payload.get("price_current") is not None else None,
            sl=float(payload["sl"]) if payload.get("sl") is not None else None,
            tp=float(payload["tp"]) if payload.get("tp") is not None else None,
            profit=float(payload["profit"]) if payload.get("profit") is not None else None,
            magic=int(payload.get("magic", 0)),
            opened_at_utc=event.timestamp_utc,
            closed_at_utc=None,
            source_id=str(payload.get("source_id", event.source)),
            lineage_id=str(payload.get("lineage_id", event.correlation_id)),
        )
        self._validator.validate_ticket(pos)
        self._open[ticket] = pos

    def _apply_closed(self, event: PositionEvent) -> None:
        ticket = event.ticket
        if ticket is None:
            raise PositionStateError("CLOSED event requires ticket")
        if ticket not in self._open:
            raise PositionNotFoundError(f"cannot close unknown ticket: {ticket}")
        existing = self._open.pop(ticket)
        closed = PositionTicket(
            ticket=existing.ticket,
            symbol=existing.symbol,
            side=existing.side,
            volume=existing.volume,
            price_open=existing.price_open,
            price_current=existing.price_current,
            sl=existing.sl,
            tp=existing.tp,
            profit=float(event.payload["profit"]) if event.payload.get("profit") is not None else existing.profit,
            magic=existing.magic,
            opened_at_utc=existing.opened_at_utc,
            closed_at_utc=event.timestamp_utc,
            source_id=existing.source_id,
            lineage_id=existing.lineage_id,
        )
        self._closed[ticket] = closed

    def _apply_modified(self, event: PositionEvent) -> None:
        ticket = event.ticket
        if ticket is None or ticket not in self._open:
            raise PositionNotFoundError(f"cannot modify unknown ticket: {ticket}")
        existing = self._open[ticket]
        price_current = event.payload.get("price_current", existing.price_current)
        profit = event.payload.get("profit", existing.profit)
        updated = PositionTicket(
            ticket=existing.ticket,
            symbol=existing.symbol,
            side=existing.side,
            volume=existing.volume,
            price_open=existing.price_open,
            price_current=float(price_current) if price_current is not None else None,
            sl=existing.sl,
            tp=existing.tp,
            profit=float(profit) if profit is not None else None,
            magic=existing.magic,
            opened_at_utc=existing.opened_at_utc,
            closed_at_utc=None,
            source_id=existing.source_id,
            lineage_id=existing.lineage_id,
        )
        self._validator.validate_ticket(updated)
        self._open[ticket] = updated

    def _apply_sync(self, event: PositionEvent) -> None:
        """Replace open set for symbol from broker snapshot in payload."""
        symbol = event.symbol
        for ticket_id in list(self._open):
            if self._open[ticket_id].symbol == symbol:
                del self._open[ticket_id]
        for raw in event.payload.get("positions", []):
            fake_event = PositionEvent(
                event_id=f"{event.event_id}-sync-{raw['ticket']}",
                event_type="OPENED",
                ticket=int(raw["ticket"]),
                symbol=symbol,
                payload=raw,
                timestamp_utc=event.timestamp_utc,
                correlation_id=event.correlation_id,
                source=event.source,
            )
            self._apply_opened(fake_event)
