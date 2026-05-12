"""
Smart Money Concepts: Order Blocks, Fair Value Gaps
"""

import pandas as pd
import numpy as np


def find_order_blocks(df: pd.DataFrame, lookback: int = 50) -> list:
    """Tìm Order Blocks"""
    obs = []

    for i in range(max(2, len(df) - lookback), len(df) - 1):
        # Bullish OB: Last bearish candle before big bullish move
        if (df.iloc[i]["close"] < df.iloc[i]["open"] and  # Bearish candle
                df.iloc[i + 1]["close"] > df.iloc[i + 1]["open"] and  # Next is bullish
                df.iloc[i + 1]["close"] - df.iloc[i + 1]["open"] >  # Big move
                (df.iloc[i]["high"] - df.iloc[i]["low"]) * 1.5):
            obs.append({
                "type": "bullish",
                "high": df.iloc[i]["high"],
                "low": df.iloc[i]["low"],
                "index": i,
            })

        # Bearish OB: Last bullish candle before big bearish move
        if (df.iloc[i]["close"] > df.iloc[i]["open"] and  # Bullish candle
                df.iloc[i + 1]["close"] < df.iloc[i + 1]["open"] and  # Next is bearish
                df.iloc[i + 1]["open"] - df.iloc[i + 1]["close"] >  # Big move
                (df.iloc[i]["high"] - df.iloc[i]["low"]) * 1.5):
            obs.append({
                "type": "bearish",
                "high": df.iloc[i]["high"],
                "low": df.iloc[i]["low"],
                "index": i,
            })

    return obs


def find_fair_value_gaps(df: pd.DataFrame, lookback: int = 50) -> list:
    """Tìm Fair Value Gaps"""
    fvgs = []

    for i in range(max(2, len(df) - lookback), len(df) - 1):
        # Bullish FVG: Gap up (low[i] > high[i-2])
        if df.iloc[i]["low"] > df.iloc[i - 2]["high"]:
            fvgs.append({
                "type": "bullish",
                "top": df.iloc[i]["low"],
                "bottom": df.iloc[i - 2]["high"],
                "index": i,
            })

        # Bearish FVG: Gap down (high[i] < low[i-2])
        if df.iloc[i]["high"] < df.iloc[i - 2]["low"]:
            fvgs.append({
                "type": "bearish",
                "top": df.iloc[i - 2]["low"],
                "bottom": df.iloc[i]["high"],
                "index": i,
            })

    return fvgs


def get_smc_signal(df: pd.DataFrame) -> dict:
    """Lấy tín hiệu Smart Money Concepts"""
    obs = find_order_blocks(df)
    fvgs = find_fair_value_gaps(df)

    last_close = df.iloc[-1]["close"]
    score = 0
    direction = "neutral"
    details = []

    # Check if price is near a bullish OB (support)
    for ob in reversed(obs):
        if ob["type"] == "bullish":
            if ob["low"] <= last_close <= ob["high"]:
                score += 5
                direction = "long"
                details.append("At Bullish Order Block")
                break

    # Check if price is near a bearish OB (resistance)
    for ob in reversed(obs):
        if ob["type"] == "bearish":
            if ob["low"] <= last_close <= ob["high"]:
                score += 5
                direction = "short"
                details.append("At Bearish Order Block")
                break

    # Check if price is filling a FVG
    for fvg in reversed(fvgs):
        if fvg["type"] == "bullish" and fvg["bottom"] <= last_close <= fvg["top"]:
            score += 3
            if direction != "short":
                direction = "long"
            details.append("In Bullish FVG")
            break
        elif fvg["type"] == "bearish" and fvg["bottom"] <= last_close <= fvg["top"]:
            score += 3
            if direction != "long":
                direction = "short"
            details.append("In Bearish FVG")
            break

    return {
        "score": min(score, 10),
        "direction": direction,
        "detail": " | ".join(details) if details else "No SMC signal",
        "data": {
            "order_blocks": obs[-5:] if obs else [],
            "fvgs": fvgs[-5:] if fvgs else [],
        }
    }
