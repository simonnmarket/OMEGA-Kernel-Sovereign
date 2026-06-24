"""SIVR-0 Bridge — conecta OHLCV local ao Indicator Engine (MIG-1).

Sem MT5. Sem broker. Sem estratégia. Sem ordens.
Apenas: OHLCV → MIG-1 → output estruturado → log.
"""

from __future__ import annotations

import csv
import json
import logging
import sys
from pathlib import Path

from contracts.indicator_contract import IndicatorError, IndicatorInput
from indicator_engine import MinimalIndicatorEngine

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("sivr")

REQUIRED_CYCLES = 100


def load_ohlcv(path: Path) -> list[float]:
    """Carrega coluna 'close' de CSV local. Sem dependência externa."""
    closes: list[float] = []
    with path.open(newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            closes.append(float(row["close"]))
    if len(closes) < 20:
        raise ValueError(f"Dataset insuficiente: {len(closes)} closes (mínimo 20)")
    return closes


def run_sivr(dataset_path: Path, output_path: Path) -> int:
    """Executa pipeline SIVR-0. Retorna número de ciclos com sucesso."""
    closes = load_ohlcv(dataset_path)
    engine = MinimalIndicatorEngine()
    results: list[dict] = []
    failures = 0

    for cycle_idx in range(REQUIRED_CYCLES):
        window_size = min(20 + cycle_idx, len(closes))
        window: tuple[float, ...] = tuple(closes[:window_size])

        try:
            output = engine.calculate(IndicatorInput(closes=window))

            if output.rsi is None or output.ema is None:
                raise IndicatorError("output contains None")

            entry = {
                "cycle": cycle_idx + 1,
                "window_size": window_size,
                "rsi": round(output.rsi, 8),
                "ema": round(output.ema, 8),
            }
            results.append(entry)
            logger.info(json.dumps(entry))

        except IndicatorError as exc:
            failures += 1
            logger.error(json.dumps({"cycle": cycle_idx + 1, "error": str(exc)}))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w") as fh:
        json.dump({"total_cycles": REQUIRED_CYCLES, "failures": failures, "results": results}, fh, indent=2)

    return len(results)
