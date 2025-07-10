import os
import asyncio
from data.tiingo_connector import TiingoConnector
from data.exchange_connectors.binance import BinanceConnector
from strategies.bookrunner import BookrunnerStrategy

# Load API keys from env (fallback to placeholder)
TIINGO_API_KEY = os.getenv("TIINGO_API_KEY", "5c30f6c2e27d1f902ace1d777b29691a610df388")

async def live_loop():
    """Continuously fetch market data and feed the strategy."""
    tiingo = TiingoConnector(TIINGO_API_KEY)
    binance = BinanceConnector()
    strategy = BookrunnerStrategy(exchange=binance)

    symbol = "BTC/USDT"
    while True:
        try:
            # Fetch level-2 order book from Binance
            order_book = binance.get_order_book(symbol)
            # Forward to strategy
            strategy.on_tick(symbol, order_book)

            # Example: each 60 ticks print a heartbeat
            if strategy.tick_count % 60 == 0:
                price = tiingo.get_crypto_price("btcusd")
                print(f"[Heartbeat] Tiingo mid-price: {price}\nStrategy inventory: {strategy.inventory}")

            await asyncio.sleep(1)  # 1-second granularity
        except KeyboardInterrupt:
            print("Interrupted by user. Exiting…")
            break
        except Exception as exc:
            print(f"⚠️  Error in live loop: {exc}")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(live_loop())