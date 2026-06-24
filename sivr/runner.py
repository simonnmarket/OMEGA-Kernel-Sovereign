"""SIVR-0 runner — 100 ciclos MT5 demo → MIG-1 → log estruturado."""

from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sivr.data_adapter_mt5 import fetch_closes, initialize, shutdown
from sivr.execution_bridge import ExecutionBridge
from sivr.logger import CycleRecord, SivrLogger


def load_config() -> dict:
    config_path = Path(__file__).parent / "config_sivr.json"
    with config_path.open(encoding="utf-8") as fh:
        return json.load(fh)


def evaluate_criteria(
    records: list[CycleRecord],
    expected_cycles: int,
    failures: int,
    determinism_check: bool,
) -> dict[str, bool]:
    c1 = len(records) == expected_cycles and failures == 0
    c2 = all(
        isinstance(r.rsi, float)
        and isinstance(r.ema, float)
        and r.rsi == r.rsi
        and r.ema == r.ema
        for r in records
    )
    c3 = len(records) == expected_cycles
    c4 = all(
        r.timestamp and r.signal in {"BUY", "SELL", "HOLD"} for r in records
    )
    c5 = c1 and c2
    c6 = determinism_check
    return {
        "C1_100_cycles_no_failure": c1,
        "C2_rsi_ema_valid": c2,
        "C3_pipeline_complete": c3,
        "C4_structured_logs": c4,
        "C5_stability": c5,
        "C6_repeatable": c6,
    }


def main() -> int:
    cfg = load_config()
    run_id = cfg["run_id"]
    cycles = int(cfg["cycles"])
    interval = float(cfg["cycle_interval_seconds"])

    logger = SivrLogger(cfg["log_dir"], run_id)
    bridge = ExecutionBridge(
        rsi_period=int(cfg["rsi_period"]),
        ema_period=int(cfg["ema_period"]),
        buy_below=float(cfg["signal_rsi_buy_below"]),
        sell_above=float(cfg["signal_rsi_sell_above"]),
    )

    print(f"[SIVR-0] starting run_id={run_id} cycles={cycles} symbol={cfg['symbol']}")
    initialize(cfg.get("mt5_path"))

    failures = 0
    last_snapshot = None
    try:
        for cycle in range(1, cycles + 1):
            try:
                snapshot = fetch_closes(
                    symbol=cfg["symbol"],
                    timeframe=cfg["timeframe"],
                    bars=int(cfg["bars_required"]),
                )
                last_snapshot = snapshot
                output = bridge.run(snapshot)
                ts = datetime.now(timezone.utc).isoformat()
                record = CycleRecord(
                    cycle=cycle,
                    timestamp=ts,
                    rsi=output.rsi,
                    ema=output.ema,
                    signal=output.signal,
                    symbol=snapshot.symbol,
                    bars_used=snapshot.bar_count,
                )
                logger.log_cycle(record)
                print(
                    f"[{cycle}/{cycles}] rsi={output.rsi:.4f} ema={output.ema:.4f} "
                    f"signal={output.signal}"
                )
            except Exception as exc:  # noqa: BLE001 — SIVR must capture cycle failures
                failures += 1
                print(f"[{cycle}/{cycles}] FAIL: {exc}")
                if failures > 3:
                    raise
            if cycle < cycles and interval > 0:
                time.sleep(interval)
    finally:
        shutdown()

    determinism_check = False
    if last_snapshot is not None:
        a = bridge.run(last_snapshot)
        b = bridge.run(last_snapshot)
        determinism_check = a == b

    criteria = evaluate_criteria(logger.records(), cycles, failures, determinism_check)
    summary = {
        "run_id": run_id,
        "cycles_requested": cycles,
        "cycles_logged": len(logger.records()),
        "failures": failures,
        "log_file": str(logger.path),
        "criteria": criteria,
        "pass": all(criteria.values()) and failures == 0,
    }

    summary_path = logger.path.with_suffix(".summary.json")
    with summary_path.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2)

    print(f"[SIVR-0] log: {logger.path}")
    print(f"[SIVR-0] summary: {summary_path}")
    print(f"[SIVR-0] criteria: {criteria}")
    print(f"[SIVR-0] PASS={summary['pass']}")
    return 0 if summary["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
