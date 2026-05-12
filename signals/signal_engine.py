"""
Signal Engine - Tổng hợp tất cả indicators và chấm điểm tín hiệu
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


class SignalEngine:
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
        return df

    def analyze_single_tf(self, df: pd.DataFrame) -> Dict:
        """Phân tích 1 timeframe"""
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
        }

        return signals

    def calculate_score(self, signals: Dict) -> Dict:
        """Tính tổng điểm từ tất cả signals"""
        total_score = 0
        long_count = 0
        short_count = 0
        details = []

        # EMA
        ema_score = signals["ema"]["score"]
        total_score += ema_score
        if signals["ema"]["direction"] == "long":
            long_count += 1
        elif signals["ema"]["direction"] == "short":
            short_count += 1
        if ema_score > 0:
            details.append(f"{'✅' if signals['ema']['direction'] != 'neutral' else '⚠️'} EMA: {signals['ema']['detail']}")

        # Supertrend
        st_score = signals["supertrend"]["score"]
        total_score += st_score
        if signals["supertrend"]["direction"] == "long":
            long_count += 1
        elif signals["supertrend"]["direction"] == "short":
            short_count += 1
        details.append(f"{'✅' if signals['supertrend']['direction'] != 'neutral' else '⚠️'} SuperT: {signals['supertrend']['detail']}")

        # ADX
        adx_score = signals["adx"]["score"]
        total_score += adx_score
        if signals["adx"]["direction"] == "long":
            long_count += 1
        elif signals["adx"]["direction"] == "short":
            short_count += 1
        details.append(f"{'✅' if signals['adx']['direction'] != 'neutral' else '⚠️'} ADX: {signals['adx']['detail']}")

        # RSI
        rsi_score = signals["rsi"]["score"]
        total_score += rsi_score
        if signals["rsi"]["direction"] == "long":
            long_count += 1
        elif signals["rsi"]["direction"] == "short":
            short_count += 1
        details.append(f"{'✅' if signals['rsi']['direction'] != 'neutral' else '⚠️'} RSI: {signals['rsi']['detail']}")

        # MACD
        macd_score = signals["macd"]["score"]
        total_score += macd_score
        if signals["macd"]["direction"] == "long":
            long_count += 1
        elif signals["macd"]["direction"] == "short":
            short_count += 1
        details.append(f"{'✅' if signals['macd']['direction'] != 'neutral' else '⚠️'} MACD: {signals['macd']['detail']}")

        # Volume
        vol_score = signals["volume"]["score"]
        total_score += vol_score
        if signals["volume"]["direction"] == "long":
            long_count += 1
        elif signals["volume"]["direction"] == "short":
            short_count += 1
        details.append(f"{'✅' if signals['volume']['direction'] != 'neutral' else '⚠️'} Vol: {signals['volume']['detail']}")

        # Structure
        struct_score = signals["structure"]["score"]
        total_score += struct_score
        if signals["structure"]["direction"] == "long":
            long_count += 1
        elif signals["structure"]["direction"] == "short":
            short_count += 1
        if struct_score > 0:
            details.append(f"{'✅' if signals['structure']['direction'] != 'neutral' else '⚠️'} Structure: {signals['structure']['detail']}")

        # SMC
        smc_score = signals["smc"]["score"]
        total_score += smc_score
        if signals["smc"]["direction"] == "long":
            long_count += 1
        elif signals["smc"]["direction"] == "short":
            short_count += 1
        if smc_score > 0:
            details.append(f"{'✅' if signals['smc']['direction'] != 'neutral' else '⚠️'} SMC: {signals['smc']['detail']}")

        # Volatility
        vol_score2 = signals["volatility"]["score"]
        total_score += vol_score2
        if signals["volatility"]["direction"] == "long":
            long_count += 1
        elif signals["volatility"]["direction"] == "short":
            short_count += 1
        details.append(f"{'✅' if signals['volatility']['direction'] != 'neutral' else '⚠️'} Volat: {signals['volatility']['detail']}")

        # Determine overall direction
        if long_count > short_count:
            direction = "long"
        elif short_count > long_count:
            direction = "short"
        else:
            direction = "neutral"

        # Signal strength
        if total_score >= 80:
            strength = "STRONG"
        elif total_score >= 60:
            strength = "MEDIUM"
        elif total_score >= 40:
            strength = "WEAK"
        else:
            strength = "NO_SIGNAL"

        return {
            "score": min(total_score, 100),
            "direction": direction,
            "strength": strength,
            "long_count": long_count,
            "short_count": short_count,
            "details": details,
            "raw_signals": signals,
        }

    def generate_signal(self, symbol: str, htf_df: pd.DataFrame, mtf_df: pd.DataFrame,
                        ltf_df: pd.DataFrame, trade_type: str) -> Optional[Dict]:
        """Tạo tín hiệu từ multi-timeframe analysis"""
        try:
            # Analyze each timeframe
            htf_signals = self.analyze_single_tf(htf_df)
            mtf_signals = self.analyze_single_tf(mtf_df)
            ltf_signals = self.analyze_single_tf(ltf_df)

            # Calculate scores
            htf_result = self.calculate_score(htf_signals)
            mtf_result = self.calculate_score(mtf_signals)
            ltf_result = self.calculate_score(ltf_signals)

            # Multi-timeframe confluence
            confluence_score = 0
            if htf_result["direction"] == mtf_result["direction"] == ltf_result["direction"]:
                confluence_score = 5  # All 3 TFs aligned
            elif htf_result["direction"] == mtf_result["direction"]:
                confluence_score = 3  # HTF and MTF aligned

            # Weighted score: HTF 40%, MTF 35%, LTF 25%
            final_score = (
                htf_result["score"] * 0.4 +
                mtf_result["score"] * 0.35 +
                ltf_result["score"] * 0.25 +
                confluence_score
            )

            # Determine final direction (HTF has priority)
            if htf_result["direction"] != "neutral":
                final_direction = htf_result["direction"]
            elif mtf_result["direction"] != "neutral":
                final_direction = mtf_result["direction"]
            else:
                final_direction = ltf_result["direction"]

            # Check minimum score
            if final_score < settings.MIN_SIGNAL_SCORE:
                return None

            # Get entry price from LTF
            entry_price = ltf_df.iloc[-1]["close"]

            # Get ATR for SL calculation
            atr_val = ltf_df.iloc[-1].get("atr", entry_price * 0.01)

            # Signal strength
            if final_score >= 80:
                strength = "STRONG"
            elif final_score >= 60:
                strength = "MEDIUM"
            else:
                strength = "WEAK"

            return {
                "symbol": symbol,
                "trade_type": trade_type,
                "strength": strength,
                "score": round(final_score),
                "direction": final_direction,
                "entry_price": entry_price,
                "atr": atr_val,
                "htf": {
                    "score": htf_result["score"],
                    "direction": htf_result["direction"],
                    "details": htf_result["details"],
                },
                "mtf": {
                    "score": mtf_result["score"],
                    "direction": mtf_result["direction"],
                    "details": mtf_result["details"],
                },
                "ltf": {
                    "score": ltf_result["score"],
                    "direction": ltf_result["direction"],
                    "details": ltf_result["details"],
                },
                "confluence_score": confluence_score,
            }

        except Exception as e:
            print(f"Error generating signal for {symbol}: {e}")
            return None


# Singleton
signal_engine = SignalEngine()
