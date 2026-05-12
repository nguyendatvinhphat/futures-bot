"""
Trend Indicators: EMA, Supertrend, ADX
"""

import pandas as pd
import numpy as np
from config import settings


def calculate_ema(df: pd.DataFrame) -> pd.DataFrame:
    """Tính EMA 9, 21, 50, 200"""
    df = df.copy()
    df["ema_9"] = df["close"].ewm(span=settings.EMA_FAST, adjust=False).mean()
    df["ema_21"] = df["close"].ewm(span=settings.EMA_MED, adjust=False).mean()
    df["ema_50"] = df["close"].ewm(span=settings.EMA_SLOW, adjust=False).mean()
    df["ema_200"] = df["close"].ewm(span=settings.EMA_TREND, adjust=False).mean()
    return df


def get_ema_signal(df: pd.DataFrame) -> dict:
    """Lấy tín hiệu EMA"""
    if len(df) < 200:
        return {"score": 0, "direction": "neutral", "detail": "Insufficient data"}

    last = df.iloc[-1]
    prev = df.iloc[-2]

    # EMA Cross detection
    cross_up = prev["ema_9"] <= prev["ema_21"] and last["ema_9"] > last["ema_21"]
    cross_down = prev["ema_9"] >= prev["ema_21"] and last["ema_9"] < last["ema_21"]

    # EMA alignment (bullish: 9 > 21 > 50 > 200)
    bullish_align = (last["ema_9"] > last["ema_21"] > last["ema_50"] > last["ema_200"])
    bearish_align = (last["ema_9"] < last["ema_21"] < last["ema_50"] < last["ema_200"])

    # Price vs EMA
    price_above_ema21 = last["close"] > last["ema_21"]
    price_above_ema200 = last["close"] > last["ema_200"]

    # Score
    score = 0
    direction = "neutral"
    details = []

    if cross_up:
        score += 15
        direction = "long"
        details.append("EMA 9/21 Cross UP")
    elif cross_down:
        score += 15
        direction = "short"
        details.append("EMA 9/21 Cross DOWN")
    elif bullish_align:
        score += 10
        direction = "long"
        details.append("EMA Bullish Alignment")
    elif bearish_align:
        score += 10
        direction = "short"
        details.append("EMA Bearish Alignment")

    if price_above_ema21 and price_above_ema200:
        score += 3
        details.append("Price > EMA21 & EMA200")
    elif not price_above_ema21 and not price_above_ema200:
        score += 3
        details.append("Price < EMA21 & EMA200")

    return {
        "score": min(score, 15),
        "direction": direction,
        "detail": " | ".join(details) if details else "No EMA signal",
        "data": {
            "ema_9": round(last["ema_9"], 4),
            "ema_21": round(last["ema_21"], 4),
            "ema_50": round(last["ema_50"], 4),
            "ema_200": round(last["ema_200"], 4),
            "cross_up": cross_up,
            "cross_down": cross_down,
        }
    }


def calculate_supertrend(df: pd.DataFrame, period: int = None, multiplier: float = None) -> pd.DataFrame:
    """Tính Supertrend (vectorized)"""
    df = df.copy()
    period = period or settings.ST_ATR_PERIOD
    multiplier = multiplier or settings.ST_MULTIPLIER

    # ATR
    hl = df["high"] - df["low"]
    hc = abs(df["high"] - df["close"].shift(1))
    lc = abs(df["low"] - df["close"].shift(1))
    tr = pd.concat([hl, hc, lc], axis=1).max(axis=1)
    df["atr"] = tr.rolling(window=period).mean()

    # Basic bands
    hl2 = (df["high"] + df["low"]) / 2
    df["st_upper"] = hl2 + (multiplier * df["atr"])
    df["st_lower"] = hl2 - (multiplier * df["atr"])

    # Supertrend using numpy
    close = df["close"].values
    st_upper = df["st_upper"].values
    st_lower = df["st_lower"].values
    n = len(df)

    direction = np.ones(n, dtype=int)
    supertrend = np.zeros(n)

    for i in range(1, n):
        if close[i] > st_upper[i - 1]:
            direction[i] = 1
        elif close[i] < st_lower[i - 1]:
            direction[i] = -1
        else:
            direction[i] = direction[i - 1]

        if direction[i] == 1:
            supertrend[i] = st_lower[i]
        else:
            supertrend[i] = st_upper[i]

    df["st_direction"] = direction
    df["supertrend"] = supertrend

    return df


def get_supertrend_signal(df: pd.DataFrame) -> dict:
    """Lấy tín hiệu Supertrend"""
    if "supertrend" not in df.columns:
        df = calculate_supertrend(df)

    last = df.iloc[-1]
    prev = df.iloc[-2]

    direction = "long" if last["st_direction"] == 1 else "short"
    flip_up = prev["st_direction"] == -1 and last["st_direction"] == 1
    flip_down = prev["st_direction"] == 1 and last["st_direction"] == -1

    score = 0
    details = []

    if flip_up:
        score = 10
        details.append("Supertrend Flip UP")
    elif flip_down:
        score = 10
        details.append("Supertrend Flip DOWN")
    elif last["st_direction"] == 1:
        score = 7
        details.append("Supertrend UP")
    else:
        score = 7
        details.append("Supertrend DOWN")

    return {
        "score": score,
        "direction": direction,
        "detail": " | ".join(details),
        "data": {
            "direction": last["st_direction"],
            "supertrend": round(last["supertrend"], 4),
            "flip_up": flip_up,
            "flip_down": flip_down,
        }
    }


def calculate_adx(df: pd.DataFrame, period: int = None) -> pd.DataFrame:
    """Tính ADX (vectorized)"""
    df = df.copy()
    period = period or settings.ADX_PERIOD

    # True Range
    hl = df["high"] - df["low"]
    hc = abs(df["high"] - df["close"].shift(1))
    lc = abs(df["low"] - df["close"].shift(1))
    df["tr"] = pd.concat([hl, hc, lc], axis=1).max(axis=1)

    # Directional Movement (vectorized)
    high_diff = df["high"].diff()
    low_diff = -df["low"].diff()

    dm_plus = np.where((high_diff > low_diff) & (high_diff > 0), high_diff, 0.0)
    dm_minus = np.where((low_diff > high_diff) & (low_diff > 0), low_diff, 0.0)

    df["dm_plus"] = dm_plus
    df["dm_minus"] = dm_minus

    # Smooth
    df["atr_adx"] = df["tr"].rolling(window=period).mean()
    df["di_plus"] = (df["dm_plus"].rolling(window=period).mean() / df["atr_adx"]) * 100
    df["di_minus"] = (df["dm_minus"].rolling(window=period).mean() / df["atr_adx"]) * 100

    # ADX
    dx = abs(df["di_plus"] - df["di_minus"]) / (df["di_plus"] + df["di_minus"]) * 100
    df["adx"] = dx.rolling(window=period).mean()

    return df


def get_adx_signal(df: pd.DataFrame) -> dict:
    """Lấy tín hiệu ADX"""
    if "adx" not in df.columns:
        df = calculate_adx(df)

    last = df.iloc[-1]
    adx_val = last["adx"]
    di_plus = last["di_plus"]
    di_minus = last["di_minus"]

    score = 0
    direction = "neutral"
    details = []

    if adx_val > settings.ADX_STRONG_THRESHOLD:
        score = 10
        if di_plus > di_minus:
            direction = "long"
            details.append(f"ADX:{adx_val:.1f} Strong Bullish")
        else:
            direction = "short"
            details.append(f"ADX:{adx_val:.1f} Strong Bearish")
    elif adx_val > 20:
        score = 5
        details.append(f"ADX:{adx_val:.1f} Moderate")
    else:
        score = 2
        details.append(f"ADX:{adx_val:.1f} Weak/Sideways")

    return {
        "score": score,
        "direction": direction,
        "detail": " | ".join(details),
        "data": {
            "adx": round(adx_val, 2),
            "di_plus": round(di_plus, 2),
            "di_minus": round(di_minus, 2),
        }
    }
