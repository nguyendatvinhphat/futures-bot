"""
Volatility Indicators: ATR, Bollinger Bands, Nadaraya-Watson
"""

import pandas as pd
import numpy as np
from config import settings


def calculate_atr(df: pd.DataFrame, period: int = None) -> pd.DataFrame:
    """Tính ATR"""
    df = df.copy()
    period = period or settings.ATR_PERIOD

    tr = pd.DataFrame()
    tr["hl"] = df["high"] - df["low"]
    tr["hc"] = abs(df["high"] - df["close"].shift(1))
    tr["lc"] = abs(df["low"] - df["close"].shift(1))
    df["tr"] = tr[["hl", "hc", "lc"]].max(axis=1)
    df["atr"] = df["tr"].rolling(window=period).mean()

    return df


def calculate_bollinger_bands(df: pd.DataFrame, period: int = None, std_dev: float = None) -> pd.DataFrame:
    """Tính Bollinger Bands"""
    df = df.copy()
    period = period or settings.BB_PERIOD
    std_dev = std_dev or settings.BB_STD

    df["bb_middle"] = df["close"].rolling(window=period).mean()
    df["bb_std"] = df["close"].rolling(window=period).std()
    df["bb_upper"] = df["bb_middle"] + (std_dev * df["bb_std"])
    df["bb_lower"] = df["bb_middle"] - (std_dev * df["bb_std"])

    # %B indicator
    df["bb_pct"] = (df["close"] - df["bb_lower"]) / (df["bb_upper"] - df["bb_lower"])

    return df


def calculate_nadaraya_watson(df: pd.DataFrame, bandwidth: float = 8.0, mult: float = 3.0) -> pd.DataFrame:
    """Tính Nadaraya-Watson Envelope (simplified)"""
    df = df.copy()
    src = df["close"].values
    n = len(src)

    # Gaussian kernel
    def gauss(x, h):
        return np.exp(-(x ** 2) / (h ** 2 * 2))

    # Compute NWE (non-repainting mode)
    coefs = np.array([gauss(i, bandwidth) for i in range(min(500, n))])
    den = coefs.sum()

    out = np.zeros(n)
    window = min(500, n)

    for i in range(window, n):
        out[i] = np.sum(src[i - window:i] * coefs) / den

    # MAE for envelope
    mae = pd.Series(np.abs(src - out)).rolling(window=window).mean() * mult

    df["nwe_mid"] = out
    df["nwe_upper"] = out + mae.values
    df["nwe_lower"] = out - mae.values

    return df


def get_volatility_signal(df: pd.DataFrame) -> dict:
    """Lấy tín hiệu Volatility"""
    # ATR
    if "atr" not in df.columns:
        df = calculate_atr(df)

    # Bollinger Bands
    if "bb_upper" not in df.columns:
        df = calculate_bollinger_bands(df)

    last = df.iloc[-1]
    atr_val = last["atr"]
    atr_pct = (atr_val / last["close"]) * 100

    score = 0
    direction = "neutral"
    details = []

    # Bollinger Band signals
    if last["close"] <= last["bb_lower"]:
        score = 5
        direction = "long"
        details.append("Price at BB Lower")
    elif last["close"] >= last["bb_upper"]:
        score = 5
        direction = "short"
        details.append("Price at BB Upper")
    elif last["bb_pct"] < 0.3:
        score = 3
        direction = "long"
        details.append("Near BB Lower")
    elif last["bb_pct"] > 0.7:
        score = 3
        direction = "short"
        details.append("Near BB Upper")

    # Volatility state
    if atr_pct > 2.0:
        details.append(f"High Volatility ATR:{atr_pct:.1f}%")
    elif atr_pct < 0.5:
        details.append(f"Low Volatility ATR:{atr_pct:.1f}%")
    else:
        details.append(f"Normal Volatility ATR:{atr_pct:.1f}%")

    return {
        "score": min(score, 5),
        "direction": direction,
        "detail": " | ".join(details),
        "data": {
            "atr": round(atr_val, 4),
            "atr_pct": round(atr_pct, 2),
            "bb_upper": round(last["bb_upper"], 4),
            "bb_middle": round(last["bb_middle"], 4),
            "bb_lower": round(last["bb_lower"], 4),
            "bb_pct": round(last["bb_pct"], 4),
        }
    }
