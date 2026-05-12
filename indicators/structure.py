"""
Structure Indicators: Pivot Points, Support/Resistance, BOS/CHoCH
"""

import pandas as pd
import numpy as np
from config import settings


def find_pivots(df: pd.DataFrame, left: int = None, right: int = None) -> pd.DataFrame:
    """Tìm Pivot High và Pivot Low (vectorized)"""
    df = df.copy()
    left = left or settings.PIVOT_LEFT
    right = right or settings.PIVOT_RIGHT

    highs = df["high"].values
    lows = df["low"].values
    n = len(df)

    pivot_high = np.full(n, np.nan)
    pivot_low = np.full(n, np.nan)

    for i in range(left, n - right):
        # Pivot High: high[i] is max in window [i-left, i+right]
        if highs[i] == np.max(highs[i - left:i + right + 1]):
            pivot_high[i] = highs[i]

        # Pivot Low: low[i] is min in window [i-left, i+right]
        if lows[i] == np.min(lows[i - left:i + right + 1]):
            pivot_low[i] = lows[i]

    df["pivot_high"] = pivot_high
    df["pivot_low"] = pivot_low

    return df


def detect_structure(df: pd.DataFrame) -> dict:
    """Phát hiện market structure: BOS, CHoCH"""
    df = find_pivots(df)

    # Get recent pivot highs and lows
    ph_values = df["pivot_high"].dropna().tail(5).values
    pl_values = df["pivot_low"].dropna().tail(5).values

    last_close = df.iloc[-1]["close"]
    prev_close = df.iloc[-2]["close"]

    result = {
        "bos_bullish": False,
        "bos_bearish": False,
        "choch_bullish": False,
        "choch_bearish": False,
        "trend": "neutral",
        "last_ph": ph_values[-1] if len(ph_values) > 0 else None,
        "last_pl": pl_values[-1] if len(pl_values) > 0 else None,
    }

    if len(ph_values) >= 2 and len(pl_values) >= 2:
        # Higher Highs and Higher Lows = Uptrend
        hh = ph_values[-1] > ph_values[-2]
        hl = pl_values[-1] > pl_values[-2]
        # Lower Highs and Lower Lows = Downtrend
        lh = ph_values[-1] < ph_values[-2]
        ll = pl_values[-1] < pl_values[-2]

        if hh and hl:
            result["trend"] = "uptrend"
        elif lh and ll:
            result["trend"] = "downtrend"

        # BOS (Break of Structure): Price breaks last pivot in trend direction
        if last_close > ph_values[-1] and result["trend"] == "uptrend":
            result["bos_bullish"] = True
        elif last_close < pl_values[-1] and result["trend"] == "downtrend":
            result["bos_bearish"] = True

        # CHoCH (Change of Character): Price breaks last pivot against trend
        if last_close > ph_values[-1] and result["trend"] == "downtrend":
            result["choch_bullish"] = True
        elif last_close < pl_values[-1] and result["trend"] == "uptrend":
            result["choch_bearish"] = True

    return result


def get_structure_signal(df: pd.DataFrame) -> dict:
    """Lấy tín hiệu Structure"""
    structure = detect_structure(df)

    score = 0
    direction = "neutral"
    details = []

    if structure["choch_bullish"]:
        score = 10
        direction = "long"
        details.append("CHoCH Bullish (Change of Character)")
    elif structure["choch_bearish"]:
        score = 10
        direction = "short"
        details.append("CHoCH Bearish (Change of Character)")
    elif structure["bos_bullish"]:
        score = 8
        direction = "long"
        details.append("BOS Bullish (Break of Structure)")
    elif structure["bos_bearish"]:
        score = 8
        direction = "short"
        details.append("BOS Bearish (Break of Structure)")
    elif structure["trend"] == "uptrend":
        score = 5
        direction = "long"
        details.append("Uptrend (HH + HL)")
    elif structure["trend"] == "downtrend":
        score = 5
        direction = "short"
        details.append("Downtrend (LH + LL)")

    # Support/Resistance proximity
    if structure["last_pl"] and structure["last_ph"]:
        last_close = df.iloc[-1]["close"]
        dist_to_support = abs(last_close - structure["last_pl"]) / last_close * 100
        dist_to_resistance = abs(last_close - structure["last_ph"]) / last_close * 100

        if dist_to_support < 1.0:
            details.append(f"Near Support ({structure['last_pl']:.2f})")
            if direction != "short":
                score += 2
        if dist_to_resistance < 1.0:
            details.append(f"Near Resistance ({structure['last_ph']:.2f})")
            if direction != "long":
                score += 2

    return {
        "score": min(score, 10),
        "direction": direction,
        "detail": " | ".join(details) if details else "No structure signal",
        "data": structure
    }
