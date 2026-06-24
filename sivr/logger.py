"""Logger estruturado SIVR-0 — um registro JSON por ciclo."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class CycleRecord:
    cycle: int
    timestamp: str
    rsi: float
    ema: float
    signal: str
    symbol: str
    bars_used: int


class SivrLogger:
    def __init__(self, log_dir: str | Path, run_id: str) -> None:
        self._dir = Path(log_dir)
        self._dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        self._path = self._dir / f"{run_id}_{stamp}.jsonl"
        self._records: list[CycleRecord] = []

    @property
    def path(self) -> Path:
        return self._path

    def log_cycle(self, record: CycleRecord) -> None:
        self._records.append(record)
        line = json.dumps(asdict(record), ensure_ascii=False)
        with self._path.open("a", encoding="utf-8") as fh:
            fh.write(line + "\n")

    def records(self) -> list[CycleRecord]:
        return list(self._records)
