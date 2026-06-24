"""Gera dataset OHLCV fixo e determinístico para SIVR-0.

Sem MT5. Sem dados reais. Série sintética fixa — apenas para validar
integração do pipeline. NÃO usar em produção.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

OUTPUT = Path("sivr/data/ohlcv_dataset.csv")


def generate_fixed_closes(n: int = 200, base: float = 44.0) -> list[dict]:
    """Série determinística baseada em função senoidal — reproduzível sem seed."""
    rows = []
    price = base
    for i in range(n):
        close = base + 5.0 * math.sin(i * 0.3) + 0.5 * math.cos(i * 0.7)
        close = round(close, 4)
        rows.append({
            "timestamp": f"2026-01-{(i % 28) + 1:02d}T{(i % 24):02d}:00:00",
            "open": round(close - 0.05, 4),
            "high": round(close + 0.10, 4),
            "low": round(close - 0.10, 4),
            "close": close,
            "volume": 1000 + (i * 7) % 500,
        })
    return rows


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    rows = generate_fixed_closes()
    with OUTPUT.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["timestamp", "open", "high", "low", "close", "volume"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"[SIVR-0] Dataset gerado: {OUTPUT} ({len(rows)} linhas)")


if __name__ == "__main__":
    main()
