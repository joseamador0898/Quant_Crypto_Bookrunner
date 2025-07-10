from typing import Any, Dict
import statistics

from .base_strategy import BaseStrategy

SPREAD_BPS = 10  # 0.10% quoted spread

class BookrunnerStrategy(BaseStrategy):
    """Simple passive maker/Bookrunner strategy.

    Parameters
    ----------
    spread_bps : int
        Half-spread in basis points (bps) around mid.
    inventory_clip : float
        Maximum inventory (in base asset units) we allow before skewing quotes.
    hold_time : int
        Placeholder for how long we keep orders alive (seconds).
    """

    def __init__(self, exchange, *, spread_bps: int = 10, inventory_clip: float = 0.2, hold_time: int = 60):
        super().__init__(exchange)
        self.spread_bps = spread_bps
        self.inventory_clip = inventory_clip
        self.hold_time = hold_time

    # -------- Strategy Core -------- #
    def on_tick(self, symbol: str, market_data: Dict[str, Any]):
        self.tick_count += 1

        bid_price = market_data["bids"][0][0]
        ask_price = market_data["asks"][0][0]
        mid = statistics.mean([bid_price, ask_price])

        # Adjust spread for inventory: widen if over clip
        inventory = self.inventory.get(symbol.split("/")[0], 0.0)
        inv_factor = min(abs(inventory) / self.inventory_clip, 1.0)
        spread_bps_eff = self.spread_bps * (1 + inv_factor)

        half_spread = mid * spread_bps_eff / 10_000
        bid_quote = round(mid - half_spread, 2)
        ask_quote = round(mid + half_spread, 2)

        # Here we could place/modify orders; for demo just print occasionally
        if self.tick_count % 10 == 0:
            print(
                f"[Bookrunner] {symbol} mid={mid:.2f} bid_quote={bid_quote:.2f} "
                f"ask_quote={ask_quote:.2f} inv={inventory:.4f}"
            )

    def on_order_fill(self, order: Dict[str, Any]):
        side = order["side"].lower()
        filled = float(order["filled"])
        price = float(order["price"])
        base_asset = order["symbol"].split("/")[0]

        delta = filled if side == "buy" else -filled
        self._update_inventory(base_asset, delta)
        print(f"[Fill] {side.upper()} {filled} {base_asset} @ {price}")