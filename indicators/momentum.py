"""
Momentum Indicators: RSI, MACD, Stochastic
"""

import pandas as pd
import numpy as np
from config import settings


def calculate_rsi(df: pd.DataFrame, period: int = None) -> pd.DataFrame:
    """Tính RSI"""
    df = df.copy()
    period = period or settings.RSI_PERIOD

    delta = df["close"].diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    df["rsi"] = 100 - (100 / (1 + rs))

    return df


def get_rsi_signal(df: pd.DataFrame) -> dict:
    """Lấy tín hiệu RSI"""
    if "rsi" not in df.columns:
        df = calculate_rsi(df)

    last = df.iloc[-1]
    prev = df.iloc[-2]
    rsi_val = last["rsi"]

    score = 0
    direction = "neutral"
    details = []

    # Oversold → Long opportunity
    if rsi_val < settings.RSI_OVERSOLD:
        score = 10
        direction = "long"
        details.append(f"RSI:{rsi_val:.1f} Oversold")
    # Overbought → Short opportunity
    elif rsi_val > settings.RSI_OVERBOUGHT:
        score = 10
        direction = "short"
        details.append(f"RSI:{rsi_val:.1f} Overbought")
    # Bullish zone (50-70)
    elif 50 < rsi_val < 70:
        score = 6
        direction = "long"
        details.append(f"RSI:{rsi_val:.1f} Bullish")
    # Bearish zone (30-50)
    elif 30 < rsi_val < 50:
        score = 6
        direction = "short"
        details.append(f"RSI:{rsi_val:.1f} Bearish")
    else:
        score = 3
        details.append(f"RSI:{rsi_val:.1f}")

    # Divergence detection (simple)
    if len(df) > 14:
        # Bullish divergence: price lower low, RSI higher low
        if (df.iloc[-5:]["close"].min() < df.iloc[-10:-5]["close"].min() and
                df.iloc[-5:]["rsi"].min() > df.iloc[-10:-5]["rsi"].min()):
            score += 3
            direction = "long"
            details.append("RSI Bullish Divergence")
        # Bearish divergence: price higher high, RSI lower high
        elif (df.iloc[-5:]["close"].max() > df.iloc[-10:-5]["close"].max() and
              df.iloc[-5:]["rsi"].max() < df.iloc[-10:-5]["rsi"].max()):
            score += 3
            direction = "short"
            details.append("RSI Bearish Divergence")

    return {
        "score": min(score, 10),
        "direction": direction,
        "detail": " | ".join(details),
        "data": {"rsi": round(rsi_val, 2)}
    }


def calculate_macd(df: pd.DataFrame) -> pd.DataFrame:
    """Tính MACD"""
    df = df.copy()

    ema_fast = df["close"].ewm(span=settings.MACD_FAST, adjust=False).mean()
    ema_slow = df["close"].ewm(span=settings.MACD_SLOW, adjust=False).mean()

    df["macd_line"] = ema_fast - ema_slow
    df["macd_signal"] = df["macd_line"].ewm(span=settings.MACD_SIGNAL, adjust=False).mean()
    df["macd_histogram"] = df["macd_line"] - df["macd_signal"]

    return df


def get_macd_signal(df: pd.DataFrame) -> dict:
    """Lấy tín hiệu MACD"""
    if "macd_line" not in df.columns:
        df = calculate_macd(df)

    last = df.iloc[-1]
    prev = df.iloc[-2]

    score = 0
    direction = "neutral"
    details = []

    # MACD cross
    cross_up = prev["macd_line"] <= prev["macd_signal"] and last["macd_line"] > last["macd_signal"]
    cross_down = prev["macd_line"] >= prev["macd_signal"] and last["macd_line"] < last["macd_signal"]

    if cross_up:
        score = 10
        direction = "long"
        details.append("MACD Cross UP")
    elif cross_down:
        score = 10
        direction = "short"
        details.append("MACD Cross DOWN")
    elif last["macd_histogram"] > 0 and last["macd_histogram"] > prev["macd_histogram"]:
        score = 7
        direction = "long"
        details.append("MACD Histogram Increasing")
    elif last["macd_histogram"] < 0 and last["macd_histogram"] < prev["macd_histogram"]:
        score = 7
        direction = "short"
        details.append("MACD Histogram Decreasing")
    elif last["macd_histogram"] > 0:
        score = 4
        direction = "long"
        details.append("MACD Positive")
    else:
        score = 4
        direction = "short"
        details.append("MACD Negative")

    return {
        "score": score,
        "direction": direction,
        "detail": " | ".join(details),
        "data": {
            "macd": round(last["macd_line"], 4),
            "signal": round(last["macd_signal"], 4),
            "histogram": round(last["macd_histogram"], 4),
        }
    }
