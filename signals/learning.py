"""
Signal Learning System - Học từ lịch sử signal để cải thiện bot
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict


class SignalLearner:
    """Hệ thống học từ lịch sử signal"""

    def __init__(self):
        self.data_file = "data/learning_data.json"
        self.history: List[Dict] = []
        self.indicator_stats = defaultdict(lambda: {"correct": 0, "wrong": 0, "total": 0})
        self.regime_stats = defaultdict(lambda: {"correct": 0, "wrong": 0, "total": 0})
        self.weight_adjustments = {}
        self.accuracy_history = []
        self.load()

    def load(self):
        """Load learning data"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    data = json.load(f)
                self.history = data.get("history", [])
                self.indicator_stats = defaultdict(
                    lambda: {"correct": 0, "wrong": 0, "total": 0},
                    data.get("indicator_stats", {})
                )
                self.regime_stats = defaultdict(
                    lambda: {"correct": 0, "wrong": 0, "total": 0},
                    data.get("regime_stats", {})
                )
                self.weight_adjustments = data.get("weight_adjustments", {})
                self.accuracy_history = data.get("accuracy_history", [])
            except Exception:
                pass

    def save(self):
        """Save learning data"""
        os.makedirs("data", exist_ok=True)
        data = {
            "history": self.history[-2000:],
            "indicator_stats": dict(self.indicator_stats),
            "regime_stats": dict(self.regime_stats),
            "weight_adjustments": self.weight_adjustments,
            "accuracy_history": self.accuracy_history[-500:],
            "last_updated": datetime.utcnow().isoformat(),
        }
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=2, default=str)

    def record_signal(self, signal: Dict, risk_info: Dict):
        """Ghi nhận signal mới để theo dõi"""
        record = {
            "id": len(self.history) + 1,
            "symbol": signal.get("symbol"),
            "direction": signal.get("direction"),
            "trade_type": signal.get("trade_type"),
            "strength": signal.get("strength"),
            "score": signal.get("score"),
            "confidence": signal.get("confidence"),
            "entry_price": risk_info.get("entry"),
            "sl": risk_info.get("sl"),
            "tps": [tp.get("price") for tp in risk_info.get("tps", [])],
            "leverage": risk_info.get("leverage"),
            "regime": signal.get("regime", {}).get("regime"),
            "indicators": self._extract_indicator_states(signal),
            "created_at": datetime.utcnow().isoformat(),
            "status": "active",
            "outcome": None,
            "closed_at": None,
            "close_price": None,
            "pnl_pct": None,
            "tp_hits": [],
        }

        self.history.append(record)
        self.save()
        return record

    def _extract_indicator_states(self, signal: Dict) -> Dict:
        """Trích xuất trạng thái indicators khi signal được tạo"""
        indicators = {}

        # LTF indicators
        ltf = signal.get("ltf", {})

        # RSI
        rsi = ltf.get("rsi", 50)
        if rsi < 30:
            indicators["rsi"] = "oversold"
        elif rsi > 70:
            indicators["rsi"] = "overbought"
        elif rsi < 50:
            indicators["rsi"] = "bearish"
        else:
            indicators["rsi"] = "bullish"

        # ADX
        adx = ltf.get("adx", 0)
        indicators["adx"] = "strong" if adx > 25 else "weak"

        # Stochastic
        stoch = ltf.get("stoch", {})
        k = stoch.get("k", 50)
        if k < 20:
            indicators["stochastic"] = "oversold"
        elif k > 80:
            indicators["stochastic"] = "overbought"
        else:
            indicators["stochastic"] = "neutral"

        # Candlestick
        candle = ltf.get("candlestick", [])
        indicators["candlestick"] = candle[0] if candle else "none"

        # Fibonacci
        fib = ltf.get("fib", {})
        indicators["fib_level"] = fib.get("nearest_level", "none")

        # BB position
        bb = ltf.get("bb", {})
        bb_upper = bb.get("bb_upper", 0)
        bb_lower = bb.get("bb_lower", 0)
        entry = signal.get("entry_price", 0)
        if bb_upper > 0 and bb_lower > 0:
            if entry <= bb_lower:
                indicators["bb_position"] = "below_lower"
            elif entry >= bb_upper:
                indicators["bb_position"] = "above_upper"
            else:
                indicators["bb_position"] = "middle"

        # EMA alignment
        ema = ltf.get("ema", {})
        indicators["ema_cross"] = "up" if ema.get("cross_up") else "down" if ema.get("cross_down") else "none"

        # Structure
        structure = ltf.get("structure", {})
        if structure.get("bos_bullish"):
            indicators["structure"] = "bos_bullish"
        elif structure.get("bos_bearish"):
            indicators["structure"] = "bos_bearish"
        elif structure.get("choch_bullish"):
            indicators["structure"] = "choch_bullish"
        elif structure.get("choch_bearish"):
            indicators["structure"] = "choch_bearish"
        else:
            indicators["structure"] = "none"

        # Market regime
        regime = signal.get("regime", {})
        indicators["regime"] = regime.get("regime", "unknown")

        # Multi-TF alignment
        indicators["multi_tf_aligned"] = signal.get("multi_tf_aligned", False)

        # HTF/MTF/LTF direction
        indicators["htf_direction"] = signal.get("htf", {}).get("direction", "neutral")
        indicators["mtf_direction"] = signal.get("mtf", {}).get("direction", "neutral")
        indicators["ltf_direction"] = signal.get("ltf", {}).get("direction", "neutral")

        return indicators

    def check_signal_outcome(self, signal_id: int, current_prices: Dict[str, float]):
        """Kiểm tra kết quả signal"""
        for record in self.history:
            if record["id"] != signal_id or record["status"] != "active":
                continue

            symbol = record["symbol"]
            if symbol not in current_prices:
                continue

            price = current_prices[symbol]
            direction = record["direction"]
            entry = record["entry_price"]
            sl = record["sl"]
            tps = record.get("tps", [])

            # Check SL
            if direction == "long" and price <= sl:
                self._close_signal(record, price, "sl_hit")
                return "sl_hit"
            elif direction == "short" and price >= sl:
                self._close_signal(record, price, "sl_hit")
                return "sl_hit"

            # Check TPs
            for i, tp in enumerate(tps):
                if i not in record.get("tp_hits", []):
                    if direction == "long" and price >= tp:
                        record.setdefault("tp_hits", []).append(i)
                    elif direction == "short" and price <= tp:
                        record.setdefault("tp_hits", []).append(i)

            # Update status based on TP hits
            tp_hits = record.get("tp_hits", [])
            if len(tp_hits) >= 3:
                self._close_signal(record, price, "tp3_hit")
                return "tp3_hit"
            elif len(tp_hits) >= 2:
                record["status"] = "tp2_hit"
            elif len(tp_hits) >= 1:
                record["status"] = "tp1_hit"

            # Check timeout (48 hours)
            created = datetime.fromisoformat(record["created_at"])
            if datetime.utcnow() - created > timedelta(hours=48):
                if not tp_hits:
                    self._close_signal(record, price, "timeout_loss")
                    return "timeout_loss"
                else:
                    self._close_signal(record, price, "timeout_win")
                    return "timeout_win"

            self.save()
            return record["status"]

        return None

    def _close_signal(self, record: Dict, close_price: float, outcome: str):
        """Đóng signal và ghi nhận kết quả"""
        direction = record["direction"]
        entry = record["entry_price"]

        if direction == "long":
            pnl_pct = (close_price - entry) / entry * 100
        else:
            pnl_pct = (entry - close_price) / entry * 100

        record["status"] = outcome
        record["outcome"] = outcome
        record["closed_at"] = datetime.utcnow().isoformat()
        record["close_price"] = close_price
        record["pnl_pct"] = round(pnl_pct, 2)

        # Update indicator stats
        is_win = outcome.startswith("tp") or outcome == "timeout_win"
        indicators = record.get("indicators", {})

        for ind_name, ind_value in indicators.items():
            key = f"{ind_name}:{ind_value}"
            self.indicator_stats[key]["total"] += 1
            if is_win:
                self.indicator_stats[key]["correct"] += 1
            else:
                self.indicator_stats[key]["wrong"] += 1

        # Update regime stats
        regime = indicators.get("regime", "unknown")
        self.regime_stats[regime]["total"] += 1
        if is_win:
            self.regime_stats[regime]["correct"] += 1
        else:
            self.regime_stats[regime]["wrong"] += 1

        # Update accuracy history
        self.accuracy_history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "outcome": outcome,
            "is_win": is_win,
            "pnl_pct": pnl_pct,
            "score": record.get("score"),
            "strength": record.get("strength"),
            "regime": regime,
        })

        self.save()

    def get_indicator_performance(self) -> Dict:
        """Phân tích hiệu suất từng indicator"""
        results = {}

        for key, stats in self.indicator_stats.items():
            if stats["total"] < 5:  # Cần ít nhất 5 mẫu
                continue

            parts = key.split(":")
            indicator = parts[0]
            value = parts[1] if len(parts) > 1 else "default"

            win_rate = stats["correct"] / stats["total"] * 100

            if indicator not in results:
                results[indicator] = {}

            results[indicator][value] = {
                "win_rate": round(win_rate, 1),
                "correct": stats["correct"],
                "wrong": stats["wrong"],
                "total": stats["total"],
                "reliability": "high" if win_rate > 65 else "medium" if win_rate > 50 else "low",
            }

        return results

    def get_regime_performance(self) -> Dict:
        """Phân tích hiệu suất theo market regime"""
        results = {}

        for regime, stats in self.regime_stats.items():
            if stats["total"] < 3:
                continue

            win_rate = stats["correct"] / stats["total"] * 100

            results[regime] = {
                "win_rate": round(win_rate, 1),
                "correct": stats["correct"],
                "wrong": stats["wrong"],
                "total": stats["total"],
            }

        return results

    def calculate_weight_adjustments(self) -> Dict:
        """Tính toán điều chỉnh weights dựa trên hiệu suất"""
        perf = self.get_indicator_performance()
        adjustments = {}

        # Base weights
        base_weights = {
            "ema": 15,
            "rsi": 10,
            "macd": 10,
            "volume": 10,
            "supertrend": 10,
            "adx": 10,
            "structure": 10,
            "smc": 10,
            "stochastic": 5,
            "fibonacci": 5,
            "candlestick": 5,
        }

        for indicator, values in perf.items():
            if indicator not in base_weights:
                continue

            # Calculate average win rate for this indicator
            total_correct = sum(v["correct"] for v in values.values())
            total_trades = sum(v["total"] for v in values.values())

            if total_trades < 10:
                continue

            avg_win_rate = total_correct / total_trades * 100

            # Adjust weight based on performance
            base = base_weights.get(indicator, 10)

            if avg_win_rate > 65:
                # Increase weight for high-performing indicators
                adjustment = min(1.5, base * 1.2)
                adjustments[indicator] = {
                    "original": base,
                    "adjusted": round(adjustment, 1),
                    "reason": f"High win rate: {avg_win_rate:.1f}%",
                    "win_rate": round(avg_win_rate, 1),
                }
            elif avg_win_rate < 40:
                # Decrease weight for low-performing indicators
                adjustment = max(3, base * 0.7)
                adjustments[indicator] = {
                    "original": base,
                    "adjusted": round(adjustment, 1),
                    "reason": f"Low win rate: {avg_win_rate:.1f}%",
                    "win_rate": round(avg_win_rate, 1),
                }

        self.weight_adjustments = adjustments
        self.save()
        return adjustments

    def get_optimal_conditions(self) -> Dict:
        """Tìm điều kiện tối ưu cho signal thành công"""
        winning_signals = [h for h in self.history if h.get("outcome", "").startswith("tp")]
        losing_signals = [h for h in self.history if h.get("outcome") == "sl_hit"]

        if len(winning_signals) < 5 or len(losing_signals) < 5:
            return {"status": "insufficient_data", "min_signals_needed": 10}

        # Analyze winning conditions
        win_conditions = defaultdict(int)
        lose_conditions = defaultdict(int)

        for sig in winning_signals:
            for key, value in sig.get("indicators", {}).items():
                win_conditions[f"{key}:{value}"] += 1

        for sig in losing_signals:
            for key, value in sig.get("indicators", {}).items():
                lose_conditions[f"{key}:{value}"] += 1

        # Find conditions with highest win ratio
        optimal = {}
        for condition in set(list(win_conditions.keys()) + list(lose_conditions.keys())):
            wins = win_conditions.get(condition, 0)
            losses = lose_conditions.get(condition, 0)
            total = wins + losses

            if total < 3:
                continue

            win_rate = wins / total * 100
            optimal[condition] = {
                "win_rate": round(win_rate, 1),
                "wins": wins,
                "losses": losses,
                "total": total,
            }

        # Sort by win rate
        sorted_optimal = dict(sorted(optimal.items(), key=lambda x: x[1]["win_rate"], reverse=True))

        return {
            "status": "ok",
            "best_conditions": dict(list(sorted_optimal.items())[:10]),
            "worst_conditions": dict(list(sorted_optimal.items())[-10:]),
            "total_wins": len(winning_signals),
            "total_losses": len(losing_signals),
        }

    def get_overall_stats(self) -> Dict:
        """Lấy thống kê tổng quan"""
        total = len(self.history)
        active = len([h for h in self.history if h["status"] == "active"])
        wins = len([h for h in self.history if h.get("outcome", "").startswith("tp")])
        losses = len([h for h in self.history if h.get("outcome") == "sl_hit"])
        timeouts = len([h for h in self.history if h.get("outcome", "").startswith("timeout")])
        closed = wins + losses + timeouts

        win_rate = (wins / closed * 100) if closed > 0 else 0

        # Average PnL
        pnls = [h.get("pnl_pct", 0) for h in self.history if h.get("pnl_pct") is not None]
        avg_pnl = sum(pnls) / len(pnls) if pnls else 0

        # Best/Worst
        best_pnl = max(pnls) if pnls else 0
        worst_pnl = min(pnls) if pnls else 0

        # By strength
        by_strength = {}
        for strength in ["PLATINUM", "GOLD", "SILVER", "BRONZE"]:
            sigs = [h for h in self.history if h.get("strength") == strength and h.get("outcome")]
            if sigs:
                str_wins = len([s for s in sigs if s.get("outcome", "").startswith("tp")])
                by_strength[strength] = {
                    "total": len(sigs),
                    "wins": str_wins,
                    "win_rate": round(str_wins / len(sigs) * 100, 1),
                }

        # By trade type
        by_type = {}
        for tt in ["scalping", "day_trading", "swing_trading"]:
            sigs = [h for h in self.history if h.get("trade_type") == tt and h.get("outcome")]
            if sigs:
                tt_wins = len([s for s in sigs if s.get("outcome", "").startswith("tp")])
                by_type[tt] = {
                    "total": len(sigs),
                    "wins": tt_wins,
                    "win_rate": round(tt_wins / len(sigs) * 100, 1),
                }

        # Recent trend (last 50 signals)
        recent = [h for h in self.history if h.get("outcome")][-50:]
        recent_wins = len([s for s in recent if s.get("outcome", "").startswith("tp")])
        recent_win_rate = (recent_wins / len(recent) * 100) if recent else 0

        return {
            "total_signals": total,
            "active_signals": active,
            "closed_signals": closed,
            "wins": wins,
            "losses": losses,
            "timeouts": timeouts,
            "win_rate": round(win_rate, 1),
            "avg_pnl": round(avg_pnl, 2),
            "best_pnl": round(best_pnl, 2),
            "worst_pnl": round(worst_pnl, 2),
            "by_strength": by_strength,
            "by_type": by_type,
            "recent_win_rate": round(recent_win_rate, 1),
            "recent_sample_size": len(recent),
        }

    def format_learning_report(self) -> str:
        """Format báo cáo học tập cho Telegram"""
        stats = self.get_overall_stats()
        indicator_perf = self.get_indicator_performance()
        regime_perf = self.get_regime_performance()
        adjustments = self.calculate_weight_adjustments()
        optimal = self.get_optimal_conditions()

        report = f"""
📚 *BÁO CÁO HỌC TẬP - Bot 2.1.0*
━━━━━━━━━━━━━━━━━━━━

📊 *Tổng quan:*
• Tổng signals: {stats['total_signals']}
• Đang active: {stats['active_signals']}
• Đã đóng: {stats['closed_signals']}
• Thắng: {stats['wins']} | Thua: {stats['losses']} | Timeout: {stats['timeouts']}
• Win Rate: {stats['win_rate']}%
• Avg PnL: {stats['avg_pnl']}%
• Best: +{stats['best_pnl']}% | Worst: {stats['worst_pnl']}%
• Recent WR (50 lệnh): {stats['recent_win_rate']}%

📈 *Theo Rating:*
"""
        for strength, data in stats.get("by_strength", {}).items():
            emoji = {"PLATINUM": "💎", "GOLD": "🥇", "SILVER": "🥈", "BRONZE": "🥉"}.get(strength, "")
            report += f"• {emoji} {strength}: {data['win_rate']}% ({data['wins']}/{data['total']})\n"

        report += "\n⏱️ *Theo Timeframe:*\n"
        for tt, data in stats.get("by_type", {}).items():
            label = {"scalping": "Scalping", "day_trading": "Day Trading", "swing_trading": "Swing"}.get(tt, tt)
            report += f"• {label}: {data['win_rate']}% ({data['wins']}/{data['total']})\n"

        # Best indicators
        report += "\n🏆 *Indicators tốt nhất:*\n"
        best_indicators = []
        for ind, values in indicator_perf.items():
            for val, data in values.items():
                if data["total"] >= 5 and data["win_rate"] > 60:
                    best_indicators.append((ind, val, data))

        best_indicators.sort(key=lambda x: x[2]["win_rate"], reverse=True)
        for ind, val, data in best_indicators[:5]:
            report += f"• {ind}={val}: {data['win_rate']}% ({data['total']} samples)\n"

        # Worst indicators
        report += "\n⚠️ *Indicators kém nhất:*\n"
        worst_indicators = []
        for ind, values in indicator_perf.items():
            for val, data in values.items():
                if data["total"] >= 5 and data["win_rate"] < 45:
                    worst_indicators.append((ind, val, data))

        worst_indicators.sort(key=lambda x: x[2]["win_rate"])
        for ind, val, data in worst_indicators[:5]:
            report += f"• {ind}={val}: {data['win_rate']}% ({data['total']} samples)\n"

        # Regime performance
        report += "\n🌍 *Market Regime:*\n"
        for regime, data in regime_perf.items():
            report += f"• {regime}: {data['win_rate']}% ({data['wins']}/{data['total']})\n"

        # Weight adjustments
        if adjustments:
            report += "\n⚙️ *Đề xuất điều chỉnh weights:*\n"
            for ind, adj in adjustments.items():
                direction = "⬆️" if adj["adjusted"] > adj["original"] else "⬇️"
                report += f"• {ind}: {adj['original']} → {adj['adjusted']} {direction} ({adj['reason']})\n"

        report += "\n━━━━━━━━━━━━━━━━━━━━"

        return report


# Singleton
signal_learner = SignalLearner()
