import os
import asyncio
import argparse
from data.tiingo_connector import TiingoConnector
from data.exchange_connectors.binance import BinanceConnector
from strategies.bookrunner import BookrunnerStrategy
from data.research_aggregator import gather_research
from strategies.strategy_generator import generate_from_research
from data.exchange_connectors.coinbase import CoinbaseConnector
from data.exchange_connectors.kraken import KrakenConnector

# Load API keys from env (fallback to placeholder)
TIINGO_API_KEY = os.getenv("TIINGO_API_KEY", "5c30f6c2e27d1f902ace1d777b29691a610df388")

EXCH_MAP = {
    "binance": BinanceConnector,
    "coinbase": CoinbaseConnector,
    "kraken": KrakenConnector,
}


def build_exchange(name: str):
    cls = EXCH_MAP.get(name.lower())
    if not cls:
        raise ValueError(f"Unsupported exchange: {name}")
    return cls()


def cli():
    parser = argparse.ArgumentParser(description="Quant Crypto Bookrunner")
    parser.add_argument("--exchange", default="binance", choices=list(EXCH_MAP.keys()))
    parser.add_argument("--symbol", default="BTC/USDT")
    parser.add_argument("--research", action="store_true", help="Generate params from latest papers")
    return parser.parse_args()


async def live_loop(args):
    tiingo = TiingoConnector(TIINGO_API_KEY)
    exchange = build_exchange(args.exchange)

    # Optionally generate strategy params from research
    params = {"spread_bps": 10, "inventory_clip": 0.2, "hold_time": 60}
    if args.research:
        papers = gather_research("crypto market making", min_results=120)
        params.update(generate_from_research(papers))
        print("[Research] Generated params:", params)

    strategy = BookrunnerStrategy(
        exchange=exchange,
        spread_bps=params["spread_bps"],
        inventory_clip=params["inventory_clip"],
        hold_time=params["hold_time"],
    )

    symbol = args.symbol
    while True:
        try:
            order_book = exchange.get_order_book(symbol)
            strategy.on_tick(symbol, order_book)
            await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("User interrupted, exiting.")
            break
        except Exception as exc:
            print("Live error:", exc)
            await asyncio.sleep(5)


if __name__ == "__main__":
    _args = cli()
    asyncio.run(live_loop(_args))