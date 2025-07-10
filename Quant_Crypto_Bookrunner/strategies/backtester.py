from typing import Iterable, Dict, Any

from .base_strategy import BaseStrategy

class Backtester:
    """Naive back-tester that feeds pre-loaded order book snapshots to a strategy."""

    def __init__(self, strategy: BaseStrategy, snapshots: Iterable[Dict[str, Any]], symbol: str):
        self.strategy = strategy
        self.snapshots = snapshots
        self.symbol = symbol

    def run(self):
        for snapshot in self.snapshots:
            self.strategy.on_tick(self.symbol, snapshot)