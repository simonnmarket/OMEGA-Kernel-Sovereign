"""MIG-2 — Market Data Engine soberano.

Autorização: DEC-MIG2-001 · TASK-0022 · CEO-DIRECTIVE-021
Fail-closed: dado inválido → DataIntegrityError, nunca sintético.
"""

from market_data.engine import SovereignMarketDataEngine
from market_data.validator import DataValidator

__all__ = ["SovereignMarketDataEngine", "DataValidator"]
