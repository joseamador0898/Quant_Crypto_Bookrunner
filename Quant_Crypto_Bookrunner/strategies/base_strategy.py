from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseStrategy(ABC):
    """Abstract base class all strategies must inherit from."""

    def __init__(self, exchange):
        self.exchange = exchange
        self.tick_count = 0
        self.inventory: Dict[str, float] = {}

    @abstractmethod
    def on_tick(self, symbol: str, market_data: Dict[str, Any]):
        """Called on each new market data update."""
        ...

    @abstractmethod
    def on_order_fill(self, order: Dict[str, Any]):
        """Called when an order is filled (or partially filled)."""
        ...

    # Utility
    def _update_inventory(self, asset: str, delta: float):
        self.inventory[asset] = self.inventory.get(asset, 0.0) + delta