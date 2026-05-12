"""
Risk Manager - Tính SL, TP, Position Size, Leverage
"""

from config import settings
from typing import Dict, List


class RiskManager:
    def __init__(self, account_size: float = None):
        self.account_size = account_size or settings.DEFAULT_ACCOUNT_SIZE

    def calculate_sl(self, entry: float, direction: str, atr: float, multiplier: float = None,
                     atr_pct: float = None) -> float:
        """Tính Stop Loss với dynamic distance theo volatility"""
        mult = multiplier or settings.ATR_SL_MULTIPLIER

        # Dynamic SL: rộng hơn khi volatility cao, hẹp hơn khi thấp
        if atr_pct is not None:
            if atr_pct > 3.0:
                mult = max(mult, 3.0)  # Volatility cao -> SL rộng hơn
            elif atr_pct > 2.0:
                mult = max(mult, 2.5)
            elif atr_pct < 0.5:
                mult = min(mult, 2.0)  # Volatility thấp -> SL hẹp hơn

        risk_distance = atr * mult

        # Minimum SL distance: max(1.0% entry, 1 tick)
        min_distance = max(entry * 0.01, self._get_min_tick(entry))
        risk_distance = max(risk_distance, min_distance)

        # Maximum SL distance: 5% entry (tránh SL quá xa)
        max_distance = entry * 0.05
        risk_distance = min(risk_distance, max_distance)

        if direction == "long":
            sl = entry - risk_distance
        else:
            sl = entry + risk_distance

        # Ensure SL != Entry (final safety check)
        if sl == entry:
            if direction == "long":
                sl = entry - min_distance
            else:
                sl = entry + min_distance

        return sl

    def _get_min_tick(self, price: float) -> float:
        """Tính minimum tick size dựa trên price magnitude"""
        if price >= 100:
            return 0.01
        elif price >= 10:
            return 0.001
        elif price >= 1:
            return 0.0001
        elif price >= 0.1:
            return 0.00001
        elif price >= 0.01:
            return 0.000001
        elif price >= 0.001:
            return 0.0000001
        else:
            return 0.00000001

    def calculate_tps(self, entry: float, sl: float, direction: str) -> List[Dict]:
        """Tính Take Profit levels với R:R cao"""
        risk = abs(entry - sl)
        r_ratios = [1.5, 2.5, 3.5, 5.0, 7.0]
        close_pcts = [25, 25, 20, 15, 15]

        # Xác định số thập phân dựa trên price magnitude
        if entry >= 100:
            decimals = 2
        elif entry >= 10:
            decimals = 3
        elif entry >= 1:
            decimals = 4
        elif entry >= 0.1:
            decimals = 5
        elif entry >= 0.01:
            decimals = 6
        elif entry >= 0.001:
            decimals = 7
        else:
            decimals = 8

        tps = []
        for i, (rr, pct) in enumerate(zip(r_ratios, close_pcts)):
            if direction == "long":
                tp_price = entry + (risk * rr)
            else:
                tp_price = entry - (risk * rr)

            tps.append({
                "level": i + 1,
                "price": round(tp_price, decimals),
                "rr_ratio": rr,
                "close_pct": pct,
                "profit": round(risk * rr, decimals),
            })

        return tps

    def calculate_leverage(self, score: int, atr_pct: float) -> int:
        """Tính leverage tự động dựa trên score và volatility (điều chỉnh cho SL rộng hơn)"""
        # Base leverage theo score (giảm bớt vì SL rộng hơn)
        if score >= 80:
            base_lev = settings.LEVERAGE_MAP["strong"]["max"] - 5  # 20 -> 15
        elif score >= 60:
            base_lev = settings.LEVERAGE_MAP["medium"]["max"] - 3  # 10 -> 7
        else:
            base_lev = settings.LEVERAGE_MAP["weak"]["max"] - 1   # 5 -> 4

        # Giảm leverage nếu volatility cao
        if atr_pct > 3.0:
            base_lev = max(3, base_lev // 3)
        elif atr_pct > 2.0:
            base_lev = max(3, base_lev // 2)
        elif atr_pct > 1.0:
            base_lev = max(3, int(base_lev * 0.75))

        return base_lev

    def calculate_position_size(self, entry: float, sl: float, risk_pct: float = None) -> Dict:
        """Tính position size dựa trên risk"""
        risk_pct = risk_pct or settings.DEFAULT_RISK_PERCENT
        risk_amount = self.account_size * (risk_pct / 100)
        risk_distance = abs(entry - sl)

        if risk_distance == 0:
            return {"size": 0, "value": 0, "risk_amount": 0}

        position_size = risk_amount / risk_distance
        position_value = position_size * entry

        return {
            "size": round(position_size, 6),
            "value": round(position_value, 2),
            "risk_amount": round(risk_amount, 2),
            "risk_pct": risk_pct,
        }

    def calculate_liquidation_price(self, entry: float, direction: str, leverage: int) -> float:
        """Tính giá thanh lý"""
        maint_rate = 0.005  # 0.5%

        if direction == "long":
            return entry * (1 - 1 / leverage + maint_rate)
        else:
            return entry * (1 + 1 / leverage - maint_rate)

    def get_risk_reward_info(self, signal: Dict) -> Dict:
        """Tạo thông tin risk/reward đầy đủ cho signal"""
        entry = signal["entry_price"]
        direction = signal["direction"]
        atr = signal["atr"]
        score = signal["score"]

        # ATR percentage
        atr_pct = (atr / entry) * 100

        # SL (dynamic theo volatility)
        sl = self.calculate_sl(entry, direction, atr, atr_pct=atr_pct)

        # TPs
        tps = self.calculate_tps(entry, sl, direction)

        # Leverage
        leverage = self.calculate_leverage(score, atr_pct)

        # Position size
        risk_pct = settings.RISK_MAP.get(
            "strong" if score >= 80 else "medium" if score >= 60 else "weak",
            settings.DEFAULT_RISK_PERCENT
        )
        pos_info = self.calculate_position_size(entry, sl, risk_pct)

        # Liquidation price
        liq_price = self.calculate_liquidation_price(entry, direction, leverage)

        # Ensure SL is farther from liquidation
        if direction == "long" and sl <= liq_price:
            sl = liq_price + (entry - liq_price) * 0.1
        elif direction == "short" and sl >= liq_price:
            sl = liq_price - (liq_price - entry) * 0.1

        # Risk:Reward ratio (based on TP2 = 1:2.5)
        risk = abs(entry - sl)
        reward = abs(tps[1]["price"] - entry) if len(tps) > 1 else abs(tps[0]["price"] - entry)
        rr_ratio = round(reward / risk, 1) if risk > 0 else 0

        # Risk percentage
        sl_pct = (abs(entry - sl) / entry) * 100

        # Xác định số thập phân cho entry/sl
        if entry >= 100:
            price_dec = 2
        elif entry >= 10:
            price_dec = 3
        elif entry >= 1:
            price_dec = 4
        elif entry >= 0.1:
            price_dec = 5
        elif entry >= 0.01:
            price_dec = 6
        elif entry >= 0.001:
            price_dec = 7
        else:
            price_dec = 8

        return {
            "entry": round(entry, price_dec),
            "sl": round(sl, price_dec),
            "sl_pct": round(sl_pct, 2),
            "tps": tps,
            "leverage": leverage,
            "position": pos_info,
            "liquidation_price": round(liq_price, price_dec),
            "rr_ratio": rr_ratio,
            "risk_pct": risk_pct,
            "atr": round(atr, price_dec),
            "atr_pct": round(atr_pct, 2),
        }


# Singleton
risk_manager = RiskManager()
