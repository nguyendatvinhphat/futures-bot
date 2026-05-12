"""
Advanced Indicators: Stochastic, Fibonacci, Candlestick Patterns, Market Regime
"""

import pandas as pd
import numpy as np


def calculate_stochastic(df: pd.DataFrame, k_period: int = 14, d_period: int = 3) -> pd.DataFrame:
    """Tính Stochastic Oscillator"""
    df = df.copy()

    low_min = df["low"].rolling(window=k_period).min()
    high_max = df["high"].rolling(window=k_period).max()

    df["stoch_k"] = ((df["close"] - low_min) / (high_max - low_min)) * 100
    df["stoch_d"] = df["stoch_k"].rolling(window=d_period).mean()

    return df


def get_stochastic_signal(df: pd.DataFrame) -> dict:
    """Lấy tín hiệu Stochastic"""
    if "stoch_k" not in df.columns:
        df = calculate_stochastic(df)

    last = df.iloc[-1]
    k = last["stoch_k"]
    d = last["stoch_d"]

    score = 0
    direction = "neutral"
    details = []

    # Oversold
    if k < 20 and d < 20:
        score = 5
        direction = "long"
        details.append(f"Stoch Oversold %K={k:.1f}% %D={d:.1f}%")
    # Overbought
    elif k > 80 and d > 80:
        score = 5
        direction = "short"
        details.append(f"Stoch Overbought %K={k:.1f}% %D={d:.1f}%")
    # Bullish cross
    elif k > d and df.iloc[-2]["stoch_k"] <= df.iloc[-2]["stoch_d"]:
        score = 4
        direction = "long"
        details.append(f"Stoch Bullish Cross %K={k:.1f}% %D={d:.1f}%")
    # Bearish cross
    elif k < d and df.iloc[-2]["stoch_k"] >= df.iloc[-2]["stoch_d"]:
        score = 4
        direction = "short"
        details.append(f"Stoch Bearish Cross %K={k:.1f}% %D={d:.1f}%")
    else:
        details.append(f"Stoch %K={k:.1f}% %D={d:.1f}%")

    return {
        "score": score,
        "direction": direction,
        "detail": " | ".join(details),
        "data": {"k": round(k, 1), "d": round(d, 1)}
    }


def find_fibonacci_levels(df: pd.DataFrame, lookback: int = 100) -> dict:
    """Tìm Fibonacci levels"""
    recent = df.tail(lookback)

    swing_high = recent["high"].max()
    swing_low = recent["low"].min()
    swing_range = swing_high - swing_low

    # Fibonacci retracement levels (từ đáy lên đỉnh)
    fib_levels = {
        "0.0": swing_low,
        "0.236": swing_low + swing_range * 0.236,
        "0.382": swing_low + swing_range * 0.382,
        "0.5": swing_low + swing_range * 0.5,
        "0.618": swing_low + swing_range * 0.618,
        "0.786": swing_low + swing_range * 0.786,
        "1.0": swing_high,
    }

    # Fibonacci extension levels
    fib_extensions = {
        "1.272": swing_high + swing_range * 0.272,
        "1.618": swing_high + swing_range * 0.618,
        "2.618": swing_high + swing_range * 1.618,
    }

    return {
        "swing_high": swing_high,
        "swing_low": swing_low,
        "range": swing_range,
        "levels": fib_levels,
        "extensions": fib_extensions,
    }


def get_fibonacci_signal(df: pd.DataFrame) -> dict:
    """Lấy tín hiệu Fibonacci"""
    fib = find_fibonacci_levels(df)
    last_close = df.iloc[-1]["close"]

    score = 0
    direction = "neutral"
    details = []
    nearest_level = None
    min_dist = float("inf")

    for level_name, level_price in fib["levels"].items():
        dist = abs(last_close - level_price) / last_close * 100
        if dist < min_dist:
            min_dist = dist
            nearest_level = level_name

    # Near support levels (0.236, 0.382) → potential bounce
    if nearest_level in ["0.236", "0.382"] and min_dist < 1.0:
        score = 4
        direction = "long"
        details.append(f"Fib {nearest_level} @ ${fib['levels'][nearest_level]:.2f}")
    # Near resistance levels (0.618, 0.786) → potential rejection
    elif nearest_level in ["0.618", "0.786"] and min_dist < 1.0:
        score = 4
        direction = "short"
        details.append(f"Fib {nearest_level} @ ${fib['levels'][nearest_level]:.2f}")
    else:
        details.append(f"Fib nearest: {nearest_level} @ ${fib['levels'][nearest_level]:.2f}")

    return {
        "score": score,
        "direction": direction,
        "detail": " | ".join(details),
        "data": {
            "levels": fib["levels"],
            "extensions": fib["extensions"],
            "nearest_level": nearest_level,
        }
    }


def detect_candlestick_patterns(df: pd.DataFrame) -> dict:
    """Phát hiện candlestick patterns"""
    if len(df) < 5:
        return {"patterns": [], "score": 0, "direction": "neutral", "detail": "Insufficient data"}

    patterns = []
    last = df.iloc[-1]
    prev = df.iloc[-2]
    prev2 = df.iloc[-3]

    body = last["close"] - last["open"]
    body_abs = abs(body)
    upper_wick = last["high"] - max(last["close"], last["open"])
    lower_wick = min(last["close"], last["open"]) - last["low"]
    candle_range = last["high"] - last["low"]

    prev_body = prev["close"] - prev["open"]
    prev_body_abs = abs(prev_body)

    # Bullish Engulfing
    if (prev_body < 0 and body > 0 and
            last["close"] > prev["open"] and last["open"] < prev["close"] and
            body_abs > prev_body_abs):
        patterns.append("BULL_ENGULF")

    # Bearish Engulfing
    if (prev_body > 0 and body < 0 and
            last["close"] < prev["open"] and last["open"] > prev["close"] and
            body_abs > prev_body_abs):
        patterns.append("BEAR_ENGULF")

    # Hammer (bullish reversal)
    if (lower_wick > body_abs * 2 and upper_wick < body_abs * 0.5 and
            candle_range > 0):
        patterns.append("HAMMER")

    # Shooting Star (bearish reversal)
    if (upper_wick > body_abs * 2 and lower_wick < body_abs * 0.5 and
            candle_range > 0):
        patterns.append("SHOOTING_STAR")

    # Doji
    if body_abs < candle_range * 0.1 and candle_range > 0:
        patterns.append("DOJI")

    # Morning Star (bullish)
    if (prev2["close"] < prev2["open"] and  # Bearish
            abs(prev["close"] - prev["open"]) < (prev2["high"] - prev2["low"]) * 0.3 and  # Small body
            last["close"] > last["open"] and  # Bullish
            last["close"] > (prev2["open"] + prev2["close"]) / 2):  # Close above midpoint
        patterns.append("MORNING_STAR")

    # Evening Star (bearish)
    if (prev2["close"] > prev2["open"] and  # Bullish
            abs(prev["close"] - prev["open"]) < (prev2["high"] - prev2["low"]) * 0.3 and  # Small body
            last["close"] < last["open"] and  # Bearish
            last["close"] < (prev2["open"] + prev2["close"]) / 2):  # Close below midpoint
        patterns.append("EVENING_STAR")

    # Three White Soldiers
    if (df.iloc[-3]["close"] > df.iloc[-3]["open"] and
            df.iloc[-2]["close"] > df.iloc[-2]["open"] and
            last["close"] > last["open"] and
            df.iloc[-2]["close"] > df.iloc[-3]["close"] and
            last["close"] > df.iloc[-2]["close"]):
        patterns.append("THREE_WHITE_SOLDIERS")

    # Three Black Crows
    if (df.iloc[-3]["close"] < df.iloc[-3]["open"] and
            df.iloc[-2]["close"] < df.iloc[-2]["open"] and
            last["close"] < last["open"] and
            df.iloc[-2]["close"] < df.iloc[-3]["close"] and
            last["close"] < df.iloc[-2]["close"]):
        patterns.append("THREE_BLACK_CROWS")

    # Determine direction
    bullish_patterns = ["BULL_ENGULF", "HAMMER", "MORNING_STAR", "THREE_WHITE_SOLDIERS"]
    bearish_patterns = ["BEAR_ENGULF", "SHOOTING_STAR", "EVENING_STAR", "THREE_BLACK_CROWS"]

    direction = "neutral"
    score = 0

    for p in patterns:
        if p in bullish_patterns:
            direction = "long"
            score = 5
            break
        elif p in bearish_patterns:
            direction = "short"
            score = 5
            break

    return {
        "patterns": patterns,
        "score": score,
        "direction": direction,
        "detail": " ".join(patterns) if patterns else "No pattern",
    }


def detect_market_regime(df: pd.DataFrame) -> dict:
    """Phát hiện chế độ thị trường"""
    if len(df) < 50:
        return {"regime": "unknown", "detail": "Insufficient data"}

    recent = df.tail(50)

    # Calculate ADX for trend strength
    if "adx" not in df.columns:
        # Simple ADX approximation
        tr = pd.DataFrame()
        tr["hl"] = recent["high"] - recent["low"]
        tr["hc"] = abs(recent["high"] - recent["close"].shift(1))
        tr["lc"] = abs(recent["low"] - recent["close"].shift(1))
        atr = tr[["hl", "hc", "lc"]].max(axis=1).rolling(14).mean()

        # Price direction
        ema20 = recent["close"].ewm(span=20).mean()
        ema50 = recent["close"].ewm(span=50).mean()

        # Trend detection
        price_slope = (recent["close"].iloc[-1] - recent["close"].iloc[-20]) / recent["close"].iloc[-20] * 100
        adx_approx = abs(price_slope) * 5  # Simplified ADX approximation
    else:
        adx_approx = df.iloc[-1]["adx"]
        ema20 = recent["close"].ewm(span=20).mean()
        price_slope = (recent["close"].iloc[-1] - recent["close"].iloc[-20]) / recent["close"].iloc[-20] * 100

    # Volatility
    volatility = recent["close"].pct_change().std() * 100

    # Determine regime
    if adx_approx > 25:
        if price_slope > 0:
            regime = "trending_up"
            emoji = "📈"
            label = "Xu hướng tăng"
        else:
            regime = "trending_down"
            emoji = "📉"
            label = "Xu hướng giảm"
    elif volatility > 3:
        regime = "volatile"
        emoji = "🌊"
        label = "Biến động mạnh"
    elif adx_approx < 15:
        regime = "sideway"
        emoji = "➡️"
        label = "Sideway"
    else:
        regime = "transitioning"
        emoji = "🔄"
        label = "Chuyển đổi"

    return {
        "regime": regime,
        "emoji": emoji,
        "label": label,
        "adx": round(adx_approx, 1),
        "volatility": round(volatility, 2),
        "trend_slope": round(price_slope, 2),
        "detail": f"{emoji} {label}",
    }
