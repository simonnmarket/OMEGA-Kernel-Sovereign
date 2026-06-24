"""Testes SIVR-0 — validação de integração pipeline completo (C1-C6)."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from sivr.generate_dataset import generate_fixed_closes
from sivr.sivr_bridge import REQUIRED_CYCLES, run_sivr


@pytest.fixture()
def dataset_path(tmp_path: Path) -> Path:
    import csv
    path = tmp_path / "ohlcv.csv"
    rows = generate_fixed_closes(200)
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["timestamp", "open", "high", "low", "close", "volume"])
        writer.writeheader()
        writer.writerows(rows)
    return path


@pytest.fixture()
def output_path(tmp_path: Path) -> Path:
    return tmp_path / "output" / "sivr_run.json"


def test_sivr_c1_continuous_execution(dataset_path: Path, output_path: Path) -> None:
    """C1: execução contínua sem erro em 100 ciclos."""
    successful = run_sivr(dataset_path, output_path)
    assert successful == REQUIRED_CYCLES


def test_sivr_c2_determinism(dataset_path: Path, tmp_path: Path) -> None:
    """C2: mesmo dataset → mesmo output em execuções distintas."""
    out1 = tmp_path / "run1.json"
    out2 = tmp_path / "run2.json"

    run_sivr(dataset_path, out1)
    run_sivr(dataset_path, out2)

    data1 = json.loads(out1.read_text())
    data2 = json.loads(out2.read_text())

    assert data1["results"] == data2["results"]


def test_sivr_c3_no_none_no_nan(dataset_path: Path, output_path: Path) -> None:
    """C3: RSI e EMA nunca None/NaN em nenhum ciclo."""
    import math
    run_sivr(dataset_path, output_path)
    data = json.loads(output_path.read_text())

    for entry in data["results"]:
        assert entry["rsi"] is not None, f"rsi None no ciclo {entry['cycle']}"
        assert entry["ema"] is not None, f"ema None no ciclo {entry['cycle']}"
        assert not math.isnan(entry["rsi"]), f"rsi NaN no ciclo {entry['cycle']}"
        assert not math.isnan(entry["ema"]), f"ema NaN no ciclo {entry['cycle']}"


def test_sivr_c4_zero_legacy() -> None:
    """C4: zero imports funcionais de módulos V5.5 no código SIVR."""
    sivr_dir = Path("sivr")
    # Padrões de import concreto do legacy — não strings em comentários/docstrings
    legacy_import_patterns = [
        "import shadow_loop",
        "from shadow_loop",
        "import omega_v55",
        "from omega_v55",
        "import MT5BulletproofLayer",
        "from MT5BulletproofLayer",
    ]

    for py_file in sivr_dir.rglob("*.py"):
        content = py_file.read_text()
        for pattern in legacy_import_patterns:
            assert pattern not in content, (
                f"Import legacy '{pattern}' encontrado em {py_file}"
            )


def test_sivr_c5_observability(dataset_path: Path, output_path: Path) -> None:
    """C5: cada ciclo tem timestamp, rsi e ema no output."""
    run_sivr(dataset_path, output_path)
    data = json.loads(output_path.read_text())

    for entry in data["results"]:
        assert "cycle" in entry
        assert "rsi" in entry
        assert "ema" in entry


def test_sivr_c6_full_flow(dataset_path: Path, output_path: Path) -> None:
    """C6: nenhum ciclo interrompido — 0 failures."""
    run_sivr(dataset_path, output_path)
    data = json.loads(output_path.read_text())
    assert data["failures"] == 0
    assert len(data["results"]) == REQUIRED_CYCLES
