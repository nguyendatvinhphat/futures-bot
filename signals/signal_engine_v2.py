"""
Enhanced Signal Engine v2 - Kết hợp tất cả indicators nâng cao
"""

import pandas as pd
from typing import Dict, Optional, List
from config import settings
from indicators import (
    get_ema_signal, get_supertrend_signal, get_adx_signal,
    get_rsi_signal, get_macd_signal, get_volume_signal,
    get_structure_signal, get_smc_signal, get_volatility_signal,
    calculate_ema, calculate_supertrend, calculate_adx,
    calculate_rsi, calculate_macd, calculate_vwap, calculate_obv,
    calculate_volume_sma, calculate_atr, calculate_bollinger_bands
)
from indicators.advanced import (
    calculate_stochastic, get_stochastic_signal,
    get_fibonacci_signal, detect_candlestick_patterns,
    detect_market_regime
)
from signals.rating import signal_rating


class SignalEngineV2:
    def __init__(self):
        self.weights = settings.SCORING_WEIGHTS

    def prepare_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Tính tất cả indicators cho dataframe"""
        df = calculate_ema(df)
        df = calculate_supertrend(df)
        df = calculate_adx(df)
        df = calculate_rsi(df)
        df = calculate_macd(df)
        df = calculate_vwap(df)
        df = calculate_obv(df)
        df = calculate_volume_sma(df)
        df = calculate_atr(df)
        df = calculate_bollinger_bands(df)
        df = calculate_stochastic(df)
        return df

    def analyze_single_tf(self, df: pd.DataFrame) -> Dict:
        """Phân tích 1 timeframe với tất cả indicators"""
        df = self.prepare_data(df)

        signals = {
            "ema": get_ema_signal(df),
            "supertrend": get_supertrend_signal(df),
            "adx": get_adx_signal(df),
            "rsi": get_rsi_signal(df),
            "macd": get_macd_signal(df),
            "volume": get_volume_signal(df),
            "structure": get_structure_signal(df),
            "smc": get_smc_signal(df),
            "volatility": get_volatility_signal(df),
            "stochastic": get_stochastic_signal(df),
            "fibonacci": get_fibonacci_signal(df),
            "candlestick": detect_candlestick_patterns(df),
            "regime": detect_market_regime(df),
        }

        return {"signals": signals, "df": df}

    def calculate_score(self, signals: Dict) -> Dict:
        """Tính tổng điểm - yêu cầu consensus mạnh"""
        total_score = 0
        long_count = 0
        short_count = 0
        neutral_count = 0
        details = []

        # Danh sách tất cả indicators
        indicator_keys = [
            "ema", "supertrend", "adx", "rsi", "macd",
            "volume", "structure", "smc", "volatility",
            "stochastic", "fibonacci", "candlestick"
        ]

        # Đếm hướng của từng indicator
        for key in indicator_keys:
            sig = signals.get(key, {})
            direction = sig.get("direction", "neutral")
            if direction == "long":
                long_count += 1
            elif direction == "short":
                short_count += 1
            else:
                neutral_count += 1

        # Xác định hướng chính (majority vote)
        total_directional = long_count + short_count
        if total_directional == 0:
            # Tất cả neutral -> không có signal
            return {
                "score": 0,
                "direction": "neutral",
                "strength": "WEAK",
                "rating": {"rank": "WEAK", "emoji": "⚠️"},
                "long_count": 0,
                "short_count": 0,
                "details": ["All indicators neutral"],
                "raw_signals": signals,
            }

        # Tính % đồng thuận
        if long_count > short_count:
            direction = "long"
            consensus_pct = long_count / total_directional * 100
        elif short_count > long_count:
            direction = "short"
            consensus_pct = short_count / total_directional * 100
        else:
            direction = "neutral"
            consensus_pct = 50

        # ===== RULE 1: Yêu cầu ít nhất 4/11 indicators đồng thuận =====
        max_votes = max(long_count, short_count)
        if max_votes < 4:
            return {
                "score": 0,
                "direction": "neutral",
                "strength": "WEAK",
                "rating": {"rank": "WEAK", "emoji": "⚠️"},
                "long_count": long_count,
                "short_count": short_count,
                "details": [f"Too few aligned: {max_votes}/11 (need 4+)"],
                "raw_signals": signals,
            }

        # ===== RULE 2: Yêu cầu consensus >= 50% (chỉ cần nhiều hơn 1 phiếu) =====
        if consensus_pct < 50:
            return {
                "score": 0,
                "direction": "neutral",
                "strength": "WEAK",
                "rating": {"rank": "WEAK", "emoji": "⚠️"},
                "long_count": long_count,
                "short_count": short_count,
                "details": [f"Low consensus: {consensus_pct:.0f}% (need 50%+)"],
                "raw_signals": signals,
            }

        # ===== Tính điểm cho các indicators ĐỒNG THUẬN =====
        aligned_score = 0
        aligned_details = []

        for key in indicator_keys:
            sig = signals.get(key, {})
            sig_direction = sig.get("direction", "neutral")
            sig_score = sig.get("score", 0)
            sig_detail = sig.get("detail", "")

            # Chỉ cộng điểm nếu ĐỒNG THUẬN với hướng chính
            if sig_direction == direction:
                aligned_score += sig_score
                aligned_details.append(f"[+] {key}: {sig_detail}")
            elif sig_direction == "neutral":
                # Neutral cộng 80% điểm
                aligned_score += sig_score * 0.8
                aligned_details.append(f"[=] {key}: {sig_detail}")
            else:
                # Đối nghịch -> cộng 30% điểm (không trừ)
                aligned_score += sig_score * 0.3
                aligned_details.append(f"[-] {key}: {sig_detail}")

        # ===== Bonus cho consensus cao =====
        consensus_bonus = 0
        if consensus_pct >= 90:
            consensus_bonus = 15  # Gần như tất cả đồng thuận
        elif consensus_pct >= 80:
            consensus_bonus = 10
        elif consensus_pct >= 70:
            consensus_bonus = 5

        # ===== Bonus cho multi-TF alignment =====
        multi_tf_bonus = 0
        if signals.get("multi_tf_aligned", False):
            multi_tf_bonus = 10

        # ===== Tổng điểm =====
        total_score = aligned_score + consensus_bonus + multi_tf_bonus

        # Giới hạn 0-100
        total_score = max(0, min(100, total_score))

        # ===== Rating =====
        if total_score >= 90:
            rank = "PLATINUM"
            emoji = "💎"
        elif total_score >= 75:
            rank = "GOLD"
            emoji = "🥇"
        elif total_score >= 60:
            rank = "SILVER"
            emoji = "🥈"
        elif total_score >= 45:
            rank = "BRONZE"
            emoji = "🥉"
        else:
            rank = "WEAK"
            emoji = "⚠️"

        details = [
            f"Consensus: {consensus_pct:.0f}% ({long_count}L/{short_count}S/{neutral_count}N)",
            f"Aligned score: {aligned_score:.0f}",
            f"Consensus bonus: +{consensus_bonus}",
            f"Multi-TF bonus: +{multi_tf_bonus}",
        ] + aligned_details[:5]  # Chỉ hiện 5 indicators đầu

        return {
            "score": round(total_score),
            "direction": direction,
            "strength": rank,
            "rating": {"rank": rank, "emoji": emoji},
            "long_count": long_count,
            "short_count": short_count,
            "consensus_pct": round(consensus_pct),
            "details": details,
            "raw_signals": signals,
        }

    def generate_signal(self, symbol: str, htf_df: pd.DataFrame, mtf_df: pd.DataFrame,
                        ltf_df: pd.DataFrame, trade_type: str,
                        funding_rate: float = None, open_interest: float = None) -> Optional[Dict]:
        """Tạo tín hiệu từ multi-timeframe analysis"""
        try:
            # Analyze each timeframe
            htf_result = self.analyze_single_tf(htf_df)
            mtf_result = self.analyze_single_tf(mtf_df)
            ltf_result = self.analyze_single_tf(ltf_df)

            htf_signals = htf_result["signals"]
            mtf_signals = mtf_result["signals"]
            ltf_signals = ltf_result["signals"]

            # Calculate scores
            htf_score = self.calculate_score(htf_signals)
            mtf_score = self.calculate_score(mtf_signals)
            ltf_score = self.calculate_score(ltf_signals)

            # Multi-timeframe confluence
            confluence_score = 0
            multi_tf_aligned = False
            if htf_score["direction"] == mtf_score["direction"] == ltf_score["direction"]:
                confluence_score = 15  # 3 TF aligned
                multi_tf_aligned = True
            elif htf_score["direction"] == mtf_score["direction"] and htf_score["direction"] != "neutral":
                confluence_score = 10  # 2 TF aligned (HTF + MTF)
                multi_tf_aligned = True
            elif htf_score["direction"] == ltf_score["direction"] and htf_score["direction"] != "neutral":
                confluence_score = 8  # 2 TF aligned (HTF + LTF)
                multi_tf_aligned = True
            elif mtf_score["direction"] == ltf_score["direction"] and mtf_score["direction"] != "neutral":
                confluence_score = 5  # 2 TF aligned (MTF + LTF)

            # Weighted score: HTF 35%, MTF 35%, LTF 30% (cân bằng hơn)
            final_score = (
                htf_score["score"] * 0.35 +
                mtf_score["score"] * 0.35 +
                ltf_score["score"] * 0.30 +
                confluence_score
            )

            # Determine final direction (HTF has priority)
            if htf_score["direction"] != "neutral":
                final_direction = htf_score["direction"]
            elif mtf_score["direction"] != "neutral":
                final_direction = mtf_score["direction"]
            else:
                final_direction = ltf_score["direction"]

            # ===== SHORT ACCURACY BOOST =====
            if final_direction == "short":
                if htf_score["direction"] != "short":
                    final_score *= 0.7
                    confluence_score = max(0, confluence_score - 5)

                if (htf_score["direction"] == "short" and 
                    mtf_score["direction"] == "short" and 
                    ltf_score["direction"] == "short"):
                    final_score *= 1.1

                ltf_rsi = ltf_signals.get("rsi", {}).get("data", {}).get("rsi", 50)
                if ltf_rsi < 30:
                    final_score *= 0.8

                regime = ltf_signals.get("regime", {}).get("regime", "")
                if regime == "trending_up":
                    final_score *= 0.75

            # ===== LONG ACCURACY BOOST =====
            if final_direction == "long":
                if htf_score["direction"] != "long":
                    final_score *= 0.8

                ltf_rsi = ltf_signals.get("rsi", {}).get("data", {}).get("rsi", 50)
                if ltf_rsi > 75:
                    final_score *= 0.85

                regime = ltf_signals.get("regime", {}).get("regime", "")
                if regime == "trending_down":
                    final_score *= 0.8

            # Check minimum score
            if final_score < settings.MIN_SIGNAL_SCORE:
                return None

            # Get entry price from LTF
            entry_price = ltf_df.iloc[-1]["close"]

            # Validate entry price - reject if 0 or too small
            if entry_price is None or entry_price <= 0:
                return None

            # Get ATR for SL calculation
            atr_val = ltf_df.iloc[-1].get("atr", entry_price * 0.01)

            # Validate ATR - ensure it's positive
            if atr_val is None or atr_val <= 0:
                atr_val = entry_price * 0.01  # Fallback: 1% of entry

            # ATR percentage
            atr_pct = (atr_val / entry_price) * 100

            # Rating
            rating = signal_rating.get_rating(int(final_score))
            confidence = signal_rating.get_confidence(int(final_score), multi_tf_aligned)
            tf_label = signal_rating.get_timeframe_label(trade_type)
            leverage_info = signal_rating.get_leverage_suggestion(int(final_score), atr_pct)

            # Market regime
            regime = ltf_signals["regime"]

            # Stochastic
            stoch = ltf_signals["stochastic"]

            # Fibonacci
            fib = ltf_signals["fibonacci"]

            # Candlestick patterns
            cs = ltf_signals["candlestick"]

            # Support/Resistance
            structure = ltf_signals["structure"]

            return {
                "symbol": symbol,
                "trade_type": trade_type,
                "strength": rating["rank"],
                "rating": rating,
                "confidence": confidence,
                "tf_label": tf_label,
                "score": round(final_score),
                "direction": final_direction,
                "entry_price": entry_price,
                "atr": atr_val,
                "atr_pct": atr_pct,
                "leverage_info": leverage_info,
                "regime": regime,
                "multi_tf_aligned": multi_tf_aligned,
                "funding_rate": funding_rate,
                "open_interest": open_interest,
                "htf": {
                    "score": htf_score["score"],
                    "direction": htf_score["direction"],
                    "details": htf_score["details"],
                    "regime": htf_signals["regime"],
                },
                "mtf": {
                    "score": mtf_score["score"],
                    "direction": mtf_score["direction"],
                    "details": mtf_score["details"],
                    "regime": mtf_signals["regime"],
                },
                "ltf": {
                    "score": ltf_score["score"],
                    "direction": ltf_score["direction"],
                    "details": ltf_score["details"],
                    "regime": ltf_signals["regime"],
                    "rsi": ltf_signals["rsi"]["data"]["rsi"],
                    "adx": ltf_signals["adx"]["data"]["adx"],
                    "stoch": stoch["data"],
                    "fib": fib["data"],
                    "candlestick": cs["patterns"],
                    "bb": ltf_signals["volatility"]["data"],
                    "ema": ltf_signals["ema"]["data"],
                    "structure": structure["data"],
                    "smc": ltf_signals["smc"]["data"],
                },
                "confluence_score": confluence_score,
                "consensus_pct": ltf_score.get("consensus_pct", 0),
                "long_count": ltf_score.get("long_count", 0),
                "short_count": ltf_score.get("short_count", 0),
            }

        except Exception as e:
            print(f"Error generating signal for {symbol}: {e}")
            import traceback
            traceback.print_exc()
            return None


# Singleton
signal_engine_v2 = SignalEngineV2()
