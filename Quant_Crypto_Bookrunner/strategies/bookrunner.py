from typing import Any, Dict
import statistics

from .base_strategy import BaseStrategy

SPREAD_BPS = 10  # 0.10% quoted spread

class BookrunnerStrategy(BaseStrategy):
    """Illustrative book-running strategy quoting inside the spread."""

    def on_tick(self, symbol: str, market_data: Dict[str, Any]):
        self.tick_count += 1
        bid = market_data["bids"][0][0]
        ask = market_data["asks"][0][0]
        mid = statistics.mean([bid, ask])
        spread = mid * SPREAD_BPS / 10_000

        bid_quote = round(mid - spread, 2)
        ask_quote = round(mid + spread, 2)

        # For demo purposes we only print quotes every 10 ticks
        if self.tick_count % 10 == 0:
            print(f"[Bookrunner] {symbol} bid_quote={bid_quote} ask_quote={ask_quote} mid={mid}")

    def on_order_fill(self, order: Dict[str, Any]):
        # Update inventory and PnL tracking
        side = order["side"]
        filled = float(order["filled"])
        price = float(order["price"])
        base_asset = order["symbol"].split("/")[0]

        delta = filled if side == "buy" else -filled
        self._update_inventory(base_asset, delta)
        print(f"[Fill] {side} {filled} {base_asset} @ {price}")