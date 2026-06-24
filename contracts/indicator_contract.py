"""Contrato do Indicator Engine — MIG-1 Execution Pack v1.0."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class IndicatorError(ValueError):
    """Dados insuficientes ou inválidos para cálculo de indicadores."""


@dataclass(frozen=True, slots=True)
class IndicatorInput:
    """Série de preços de fechamento (mock/teste — sem integração externa)."""

    closes: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class IndicatorOutput:
    """Saída mínima do engine isolado."""

    rsi: float
    ema: float


class IndicatorEngine(Protocol):
    def calculate(self, data: IndicatorInput) -> IndicatorOutput: ...
