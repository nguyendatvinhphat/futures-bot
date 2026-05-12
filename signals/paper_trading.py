"""
Paper Trading System - Theo dõi PnL giả lập
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class PaperTrader:
    """Hệ thống paper trading"""

    def __init__(self, initial_capital: float = 10.0):
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.positions: List[Dict] = []
        self.history: List[Dict] = []
        self.total_trades = 0
        self.winning_trades = 0
        self.losing_trades = 0
        self.total_pnl = 0.0
        self.max_drawdown = 0.0
        self.peak_capital = initial_capital
        self.data_file = "data/paper_trading.json"
        self.load()

    def open_position(self, signal: Dict, risk_info: Dict) -> Dict:
        """Mở vị thế mới"""
        position = {
            "id": len(self.positions) + len(self.history) + 1,
            "symbol": signal["symbol"],
            "direction": signal["direction"],
            "entry_price": risk_info["entry"],
            "sl": risk_info["sl"],
            "tps": [tp["price"] for tp in risk_info["tps"]],
            "leverage": risk_info["leverage"],
            "size": risk_info["position"]["size"],
            "value": risk_info["position"]["value"],
            "risk_amount": risk_info["position"]["risk_amount"],
            "trade_type": signal["trade_type"],
            "score": signal["score"],
            "opened_at": datetime.utcnow().isoformat(),
            "status": "open",
            "pnl": 0.0,
            "tp_hits": [],
        }

        self.positions.append(position)
        self.save()
        return position

    def check_positions(self, current_prices: Dict[str, float]) -> List[Dict]:
        """Kiểm tra và cập nhật positions"""
        closed = []

        for pos in self.positions[:]:
            symbol = pos["symbol"]
            if symbol not in current_prices:
                continue

            price = current_prices[symbol]
            direction = pos["direction"]

            # Calculate unrealized PnL
            if direction == "long":
                pnl = (price - pos["entry_price"]) * pos["size"]
            else:
                pnl = (pos["entry_price"] - price) * pos["size"]

            pos["pnl"] = pnl
            pos["current_price"] = price

            # Check SL
            if direction == "long" and price <= pos["sl"]:
                self._close_position(pos, price, "SL hit")
                closed.append(pos)
            elif direction == "short" and price >= pos["sl"]:
                self._close_position(pos, price, "SL hit")
                closed.append(pos)

            # Check TPs
            for i, tp in enumerate(pos["tps"]):
                if i not in pos["tp_hits"]:
                    if direction == "long" and price >= tp:
                        pos["tp_hits"].append(i)
                    elif direction == "short" and price <= tp:
                        pos["tp_hits"].append(i)

            # Close if all TPs hit
            if len(pos["tp_hits"]) >= 5:
                self._close_position(pos, price, "All TPs hit")
                closed.append(pos)

        if closed:
            self.save()

        return closed

    def _close_position(self, pos: Dict, exit_price: float, reason: str):
        """Đóng vị thế"""
        direction = pos["direction"]
        if direction == "long":
            final_pnl = (exit_price - pos["entry_price"]) * pos["size"]
        else:
            final_pnl = (pos["entry_price"] - exit_price) * pos["size"]

        # Apply leverage
        leveraged_pnl = final_pnl * pos["leverage"]

        pos["exit_price"] = exit_price
        pos["final_pnl"] = leveraged_pnl
        pos["close_reason"] = reason
        pos["closed_at"] = datetime.utcnow().isoformat()
        pos["status"] = "closed"

        self.capital += leveraged_pnl
        self.total_pnl += leveraged_pnl
        self.total_trades += 1

        if leveraged_pnl > 0:
            self.winning_trades += 1
        else:
            self.losing_trades += 1

        # Update peak and drawdown
        if self.capital > self.peak_capital:
            self.peak_capital = self.capital
        drawdown = (self.peak_capital - self.capital) / self.peak_capital * 100
        if drawdown > self.max_drawdown:
            self.max_drawdown = drawdown

        # Move to history
        self.positions.remove(pos)
        self.history.append(pos)
        self.save()

    def get_stats(self) -> Dict:
        """Lấy thống kê"""
        win_rate = (self.winning_trades / self.total_trades * 100) if self.total_trades > 0 else 0
        avg_win = 0
        avg_loss = 0

        wins = [t["final_pnl"] for t in self.history if t.get("final_pnl", 0) > 0]
        losses = [t["final_pnl"] for t in self.history if t.get("final_pnl", 0) < 0]

        if wins:
            avg_win = sum(wins) / len(wins)
        if losses:
            avg_loss = sum(losses) / len(losses)

        return {
            "initial_capital": self.initial_capital,
            "current_capital": round(self.capital, 4),
            "total_pnl": round(self.total_pnl, 4),
            "pnl_pct": round(self.total_pnl / self.initial_capital * 100, 2),
            "total_trades": self.total_trades,
            "winning_trades": self.winning_trades,
            "losing_trades": self.losing_trades,
            "win_rate": round(win_rate, 1),
            "avg_win": round(avg_win, 4),
            "avg_loss": round(avg_loss, 4),
            "max_drawdown": round(self.max_drawdown, 2),
            "open_positions": len(self.positions),
            "profit_factor": round(abs(avg_win / avg_loss), 2) if avg_loss != 0 else 0,
        }

    def save(self):
        """Lưu data"""
        os.makedirs("data", exist_ok=True)
        data = {
            "capital": self.capital,
            "initial_capital": self.initial_capital,
            "positions": self.positions,
            "history": self.history[-200:],
            "total_trades": self.total_trades,
            "winning_trades": self.winning_trades,
            "losing_trades": self.losing_trades,
            "total_pnl": self.total_pnl,
            "max_drawdown": self.max_drawdown,
            "peak_capital": self.peak_capital,
        }
        with open(self.data_file, "w") as f:
            json.dump(data, f, indent=2, default=str)

    def load(self):
        """Load data"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    data = json.load(f)
                self.capital = data.get("capital", self.initial_capital)
                self.initial_capital = data.get("initial_capital", self.initial_capital)
                self.positions = data.get("positions", [])
                self.history = data.get("history", [])
                self.total_trades = data.get("total_trades", 0)
                self.winning_trades = data.get("winning_trades", 0)
                self.losing_trades = data.get("losing_trades", 0)
                self.total_pnl = data.get("total_pnl", 0)
                self.max_drawdown = data.get("max_drawdown", 0)
                self.peak_capital = data.get("peak_capital", self.initial_capital)
            except Exception:
                pass


# Singleton
paper_trader = PaperTrader()
