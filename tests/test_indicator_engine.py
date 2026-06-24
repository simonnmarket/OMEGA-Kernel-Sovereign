"""Testes determinísticos — Indicator Engine MIG-1 mínimo."""

import pytest

from contracts import IndicatorError, IndicatorInput, IndicatorOutput
from indicator_engine import MinimalIndicatorEngine, compute_ema, compute_rsi

# Mock fixo — 20 fechamentos (sem integração externa)
MOCK_CLOSES: tuple[float, ...] = (
    44.0,
    44.34,
    44.09,
    43.61,
    44.33,
    44.83,
    45.10,
    45.42,
    45.84,
    46.08,
    45.89,
    46.03,
    45.61,
    46.28,
    46.28,
    46.00,
    46.03,
    46.41,
    46.22,
    45.64,
)

# Valores esperados — snapshot determinístico da implementação V6
EXPECTED_RSI = 60.13716896582762
EXPECTED_EMA = 45.86834915963691


def test_rsi_deterministic() -> None:
    assert compute_rsi(MOCK_CLOSES, period=14) == pytest.approx(EXPECTED_RSI)


def test_ema_deterministic() -> None:
    assert compute_ema(MOCK_CLOSES, period=10) == pytest.approx(EXPECTED_EMA)


def test_engine_output_shape() -> None:
    engine = MinimalIndicatorEngine()
    result = engine.calculate(IndicatorInput(closes=MOCK_CLOSES))

    assert isinstance(result, IndicatorOutput)
    assert result.rsi is not None
    assert result.ema is not None
    assert isinstance(result.rsi, float)
    assert isinstance(result.ema, float)


def test_engine_output_values() -> None:
    engine = MinimalIndicatorEngine()
    result = engine.calculate(IndicatorInput(closes=MOCK_CLOSES))

    assert result.rsi == pytest.approx(EXPECTED_RSI)
    assert result.ema == pytest.approx(EXPECTED_EMA)


def test_engine_same_input_same_output() -> None:
    engine = MinimalIndicatorEngine()
    data = IndicatorInput(closes=MOCK_CLOSES)

    first = engine.calculate(data)
    second = engine.calculate(data)

    assert first == second


def test_rsi_range() -> None:
    rsi = compute_rsi(MOCK_CLOSES)
    assert 0.0 <= rsi <= 100.0


def test_insufficient_data_rsi_raises() -> None:
    with pytest.raises(IndicatorError):
        compute_rsi((1.0, 2.0, 3.0), period=14)


def test_insufficient_data_ema_raises() -> None:
    with pytest.raises(IndicatorError):
        compute_ema((1.0, 2.0), period=10)


def test_engine_insufficient_data_raises() -> None:
    engine = MinimalIndicatorEngine()
    with pytest.raises(IndicatorError):
        engine.calculate(IndicatorInput(closes=(1.0, 2.0, 3.0)))
