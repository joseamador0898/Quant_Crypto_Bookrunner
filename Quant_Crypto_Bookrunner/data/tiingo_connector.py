import os
import requests
from typing import List, Dict, Any

TIINGO_BASE_URL = "https://api.tiingo.com/tiingo"

class TiingoConnector:
    """Lightweight Tiingo REST wrapper for crypto endpoints."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("TIINGO_API_KEY")
        if not self.api_key:
            raise ValueError("Tiingo API key not provided.")

    def _get(self, endpoint: str, params: Dict[str, Any] | None = None):
        url = f"{TIINGO_BASE_URL}/{endpoint}"
        headers = {"Content-Type": "application/json"}
        params = params or {}
        params["token"] = self.api_key
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()

    # ------------- Crypto Endpoints ------------- #
    def get_crypto_price(self, ticker: str) -> Dict[str, Any]:
        """Return the latest price data for a given crypto ticker (e.g. 'btcusd')."""
        return self._get("crypto/prices", {"tickers": ticker})

    def get_historical_prices(self, ticker: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        """Fetch historical OHLCV data between two dates (YYYY-MM-DD)."""
        endpoint = f"crypto/prices/{ticker}/historical"
        return self._get(endpoint, {"startDate": start_date, "endDate": end_date})