import ccxt
from typing import Any, Dict

class KrakenConnector:
    """Wrapper around ccxt.kraken."""

    def __init__(self, api_key: str | None = None, secret: str | None = None, sandbox: bool = False):
        self.exchange = ccxt.kraken({
            "apiKey": api_key,
            "secret": secret,
            "enableRateLimit": True,
        })
        if sandbox:
            self.exchange.set_sandbox_mode(True)

    # Market Data
    def get_order_book(self, symbol: str, limit: int = 20) -> Dict[str, Any]:
        return self.exchange.fetch_order_book(symbol, limit=limit)

    def get_ticker(self, symbol: str) -> Dict[str, Any]:
        return self.exchange.fetch_ticker(symbol)

    # Trading
    def place_order(self, symbol: str, side: str, amount: float, price: float | None = None, order_type: str = "limit"):
        params = {}
        if order_type == "limit":
            return self.exchange.create_limit_order(symbol, side, amount, price, params)
        elif order_type == "market":
            return self.exchange.create_market_order(symbol, side, amount, params)
        else:
            raise ValueError("Unsupported order_type: " + order_type)

    def cancel_order(self, order_id: str, symbol: str):
        return self.exchange.cancel_order(order_id, symbol)

    def fetch_balance(self):
        return self.exchange.fetch_balance()