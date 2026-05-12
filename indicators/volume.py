"""
Volume Indicators: OBV, VWAP, Volume Analysis
"""

import pandas as pd
import numpy as np
from config import settings


def calculate_obv(df: pd.DataFrame) -> pd.DataFrame:
    """Tính On Balance Volume (vectorized)"""
    df = df.copy()

    close = df["close"].values
    volume = df["volume"].values
    n = len(df)

    # Vectorized: sign of close change
    sign = np.zeros(n)
    sign[1:] = np.where(close[1:] > close[:-1], 1, np.where(close[1:] < close[:-1], -1, 0))

    # Cumulative sum of signed volume
    obv = np.cumsum(sign * volume)

    df["obv"] = obv
    df["obv_sma"] = pd.Series(obv).rolling(window=20).mean().values
    return df


def calculate_vwap(df: pd.DataFrame) -> pd.DataFrame:
    """Tính VWAP"""
    df = df.copy()

    typical_price = (df["high"] + df["low"] + df["close"]) / 3
    df["vwap"] = (typical_price * df["volume"]).cumsum() / df["volume"].cumsum()

    return df


def calculate_volume_sma(df: pd.DataFrame) -> pd.DataFrame:
    """Tính Volume SMA"""
    df = df.copy()
    df["vol_sma"] = df["volume"].rolling(window=settings.VOL_SMA_PERIOD).mean()
    df["vol_ratio"] = df["volume"] / df["vol_sma"]
    return df


def get_volume_signal(df: pd.DataFrame) -> dict:
    """Lấy tín hiệu Volume"""
    df = calculate_volume_sma(df)

    if "vwap" not in df.columns:
        df = calculate_vwap(df)
    if "obv" not in df.columns:
        df = calculate_obv(df)

    last = df.iloc[-1]
    prev = df.iloc[-2]

    score = 0
    direction = "neutral"
    details = []

    vol_ratio = last["vol_ratio"]

    # Volume spike
    if vol_ratio > settings.VOL_SPIKE_MULTIPLIER:
        score += 5
        details.append(f"Vol Spike {vol_ratio:.1f}x")

        # Bullish: price up + volume spike
        if last["close"] > prev["close"]:
            direction = "long"
            details.append("Bullish Volume")
        else:
            direction = "short"
            details.append("Bearish Volume")
    elif vol_ratio > 1.0:
        score += 3
        details.append(f"Vol Above Avg {vol_ratio:.1f}x")
    else:
        score += 1
        details.append(f"Vol Below Avg {vol_ratio:.1f}x")

    # OBV trend
    if last["obv"] > last["obv_sma"]:
        score += 3
        if direction == "neutral":
            direction = "long"
        details.append("OBV Above SMA")
    elif last["obv"] < last["obv_sma"]:
        score += 3
        if direction == "neutral":
            direction = "short"
        details.append("OBV Below SMA")

    # Price vs VWAP
    if last["close"] > last["vwap"]:
        score += 2
        details.append("Price > VWAP")
    else:
        score += 2
        details.append("Price < VWAP")

    return {
        "score": min(score, 10),
        "direction": direction,
        "detail": " | ".join(details),
        "data": {
            "volume": last["volume"],
            "vol_sma": last["vol_sma"],
            "vol_ratio": round(vol_ratio, 2),
            "vwap": round(last["vwap"], 4),
            "obv": last["obv"],
        }
    }
