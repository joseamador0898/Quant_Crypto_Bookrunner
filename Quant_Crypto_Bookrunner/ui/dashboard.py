import os
import sys
import time
import asyncio
from datetime import datetime

import streamlit as st

# Add project root to path to allow absolute imports when running via Streamlit
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from data.tiingo_connector import TiingoConnector  # noqa: E402
from data.exchange_connectors import BinanceConnector, CoinbaseConnector, KrakenConnector  # noqa: E402
from strategies.bookrunner import BookrunnerStrategy  # noqa: E402
from data.research_aggregator import gather_research  # noqa: E402
from strategies.strategy_generator import generate_from_research  # noqa: E402

# ---------------- Config ---------------- #
TIINGO_API_KEY = os.getenv("TIINGO_API_KEY", "5c30f6c2e27d1f902ace1d777b29691a610df388")

EXCH_MAP = {
    "Binance": BinanceConnector,
    "Coinbase": CoinbaseConnector,
    "Kraken": KrakenConnector,
}

REFRESH_SEC = 1


# ---------------- UI ---------------- #
st.set_page_config(page_title="Quant Crypto Bookrunner", layout="wide")
st.title("📈 Quant Crypto Bookrunner Dashboard")

with st.sidebar:
    st.header("Settings")
    exchange_name = st.selectbox("Exchange", list(EXCH_MAP.keys()), index=0)
    symbol = st.text_input("Symbol", "BTC/USDT")
    use_research = st.checkbox("Generate params from research (100+ papers)")
    run_btn = st.button("▶️ Run / Refresh")

placeholder_header = st.empty()
placeholder_quotes = st.empty()
placeholder_metrics = st.empty()


@st.cache_data(show_spinner=False)
def _get_research_params() -> dict:
    papers = gather_research("crypto market making", min_results=120)
    params = generate_from_research(papers)
    return params


def main():
    if not run_btn:
        st.info("Configure settings and press Run to start streaming.")
        return

    # Build exchange + strategy
    exchange_cls = EXCH_MAP[exchange_name]
    exchange = exchange_cls()

    params = {"spread_bps": 10, "inventory_clip": 0.2, "hold_time": 60}
    if use_research:
        params.update(_get_research_params())
        st.sidebar.success(f"Research-powered params: {params}")

    strategy = BookrunnerStrategy(
        exchange=exchange,
        spread_bps=params["spread_bps"],
        inventory_clip=params["inventory_clip"],
        hold_time=params["hold_time"],
    )

    tiingo = TiingoConnector(TIINGO_API_KEY)

    st.success("Streaming started – updates every second.")
    while True:
        try:
            order_book = exchange.get_order_book(symbol)
            strategy.on_tick(symbol, order_book)

            bid = order_book["bids"][0][0]
            ask = order_book["asks"][0][0]
            mid = (bid + ask) / 2

            placeholder_header.markdown(
                f"### {symbol}  |  Time: {datetime.utcnow().strftime('%H:%M:%S')}  |  Mid: **{mid:.2f}**"
            )

            placeholder_quotes.table({
                "Side": ["Bid", "Ask"],
                "Price": [bid, ask],
                "Quote": [strategy.inventory.get(symbol.split("/")[0], 0.0), "-"]
            })

            placeholder_metrics.json({
                "tick": strategy.tick_count,
                "inventory": strategy.inventory,
            })

            time.sleep(REFRESH_SEC)
        except Exception as e:
            st.error(f"Error: {e}")
            time.sleep(REFRESH_SEC)


if __name__ == "__main__":
    main()