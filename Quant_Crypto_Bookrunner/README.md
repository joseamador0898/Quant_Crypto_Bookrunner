# Quant Crypto Bookrunner

A modular research-driven trading framework for building, testing, and running book-running / market-making strategies in cryptocurrency markets.

## Features

* Real-time market data & execution through multiple exchange APIs (Binance, Coinbase, Kraken, …)
* Tiingo data integration for spot & alternative datasets
* Automated research ingestion from academic papers and news (100+ sources)
* Strategy engine with back-testing and live trading
* Risk management & post-trade analytics modules

## Quick Start

```bash
# Clone repo & cd
pip install -r requirements.txt

# (Optional) set your credentials
export TIINGO_API_KEY="YOUR_KEY"
# Exchange keys can be placed in .env or exported as environment variables as per ccxt naming convention.

# Run the example strategy
python main.py
```

## Directory Layout

```
data/                  # External data connectors & scrapers
|__ exchange_connectors/
|   |__ binance.py
|   └── …
|__ tiingo_connector.py
|__ research_scraper.py

strategies/            # Strategy engine & back-tester
|__ base_strategy.py
|__ bookrunner.py
|__ backtester.py

analytics/             # Risk & performance analytics
|__ post_trade.py
|__ risk.py

main.py                # Entry-point orchestrator
```

## Extending

* **New exchange** – add a class in `data/exchange_connectors/` that wraps the ccxt instance and exposes `get_order_book`, `place_order`, etc.
* **New strategy** – inherit from `BaseStrategy` and implement `on_tick` & `on_order_fill`.

## Disclaimer

This software is provided **for educational purposes only**. Trading cryptocurrencies involves significant risk. Use at your own discretion.