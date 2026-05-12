"""
Binance Data Fetcher
Lấy dữ liệu OHLCV từ Binance Futures API
"""

import time
import requests
import pandas as pd
from typing import Optional, Dict, List
from config import settings


BASE_URL = "https://fapi.binance.com"


class BinanceFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.cache: Dict[str, Dict[str, pd.DataFrame]] = {}
        self.cache_time: Dict[str, float] = {}
        self.CACHE_TTL = 30  # Cache TTL in seconds

    def get_klines(self, symbol: str, interval: str, limit: int = 500) -> Optional[pd.DataFrame]:
        """Lấy OHLCV data cho 1 symbol"""
        cache_key = f"{symbol}_{interval}_{limit}"

        # Check cache
        if cache_key in self.cache:
            if time.time() - self.cache_time.get(cache_key, 0) < self.CACHE_TTL:
                return self.cache[cache_key]

        try:
            url = f"{BASE_URL}/fapi/v1/klines"
            params = {
                "symbol": symbol,
                "interval": interval,
                "limit": limit
            }

            resp = self.session.get(url, params=params, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            df = pd.DataFrame(data, columns=[
                "timestamp", "open", "high", "low", "close", "volume",
                "close_time", "quote_volume", "trades", "taker_buy_base",
                "taker_buy_quote", "ignore"
            ])

            # Convert types
            for col in ["open", "high", "low", "close", "volume", "quote_volume"]:
                df[col] = df[col].astype(float)
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            df["trades"] = df["trades"].astype(int)

            # Cache
            self.cache[cache_key] = df
            self.cache_time[cache_key] = time.time()

            return df

        except Exception as e:
            print(f"Error fetching {symbol} {interval}: {e}")
            return None

    def get_ticker_price(self, symbol: str) -> Optional[float]:
        """Lấy giá hiện tại"""
        try:
            url = f"{BASE_URL}/fapi/v1/ticker/price"
            resp = self.session.get(url, params={"symbol": symbol}, timeout=5)
            resp.raise_for_status()
            return float(resp.json()["price"])
        except Exception:
            return None

    def get_all_tickers(self) -> Dict[str, float]:
        """Lấy tất cả giá"""
        try:
            url = f"{BASE_URL}/fapi/v1/ticker/price"
            resp = self.session.get(url, timeout=10)
            resp.raise_for_status()
            return {t["symbol"]: float(t["price"]) for t in resp.json()}
        except Exception as e:
            print(f"Error fetching tickers: {e}")
            return {}

    def get_funding_rate(self, symbol: str) -> Optional[float]:
        """Lấy funding rate"""
        try:
            url = f"{BASE_URL}/fapi/v1/fundingRate"
            resp = self.session.get(url, params={"symbol": symbol, "limit": 1}, timeout=5)
            resp.raise_for_status()
            data = resp.json()
            if data:
                return float(data[0]["fundingRate"])
            return None
        except Exception:
            return None

    def get_24h_volume(self, symbol: str) -> Optional[Dict]:
        """Lấy volume 24h"""
        try:
            url = f"{BASE_URL}/fapi/v1/ticker/24hr"
            resp = self.session.get(url, params={"symbol": symbol}, timeout=5)
            resp.raise_for_status()
            data = resp.json()
            return {
                "volume": float(data["volume"]),
                "quote_volume": float(data["quoteVolume"]),
                "price_change_pct": float(data["priceChangePercent"]),
            }
        except Exception:
            return None

    def get_multi_tf_data(self, symbol: str, trade_type: str = "day_trading") -> Dict[str, pd.DataFrame]:
        """Lấy data cho nhiều timeframe"""
        tf_config = settings.TIMEFRAMES.get(trade_type, settings.TIMEFRAMES["day_trading"])

        result = {}
        for key, tf in tf_config.items():
            df = self.get_klines(symbol, tf)
            if df is not None:
                result[key] = df

        return result

    def get_orderbook(self, symbol: str, limit: int = 20) -> Optional[Dict]:
        """Lấy order book"""
        try:
            url = f"{BASE_URL}/fapi/v1/depth"
            resp = self.session.get(url, params={"symbol": symbol, "limit": limit}, timeout=5)
            resp.raise_for_status()
            data = resp.json()
            return {
                "bids": [[float(p), float(q)] for p, q in data["bids"]],
                "asks": [[float(p), float(q)] for p, q in data["asks"]],
            }
        except Exception:
            return None


# Singleton instance
fetcher = BinanceFetcher()
