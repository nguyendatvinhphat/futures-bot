"""
Signal Quality Rating System
PLATINUM > GOLD > SILVER > BRONZE
"""

from typing import Dict


class SignalRating:
    """Đánh giá chất lượng tín hiệu"""

    # Thresholds
    PLATINUM = 90
    GOLD = 75
    SILVER = 60
    BRONZE = 45

    @staticmethod
    def get_rating(score: int) -> Dict:
        """Lấy rating từ score"""
        if score >= SignalRating.PLATINUM:
            return {
                "rank": "PLATINUM",
                "emoji": "💎",
                "color": "#E5E4E2",
                "priority": 1,
            }
        elif score >= SignalRating.GOLD:
            return {
                "rank": "GOLD",
                "emoji": "🥇",
                "color": "#FFD700",
                "priority": 2,
            }
        elif score >= SignalRating.SILVER:
            return {
                "rank": "SILVER",
                "emoji": "🥈",
                "color": "#C0C0C0",
                "priority": 3,
            }
        elif score >= SignalRating.BRONZE:
            return {
                "rank": "BRONZE",
                "emoji": "🥉",
                "color": "#CD7F32",
                "priority": 4,
            }
        else:
            return {
                "rank": "WEAK",
                "emoji": "⚠️",
                "color": "#808080",
                "priority": 5,
            }

    @staticmethod
    def get_confidence(score: int, multi_tf_aligned: bool = False) -> float:
        """Tính confidence %"""
        base = score

        # Bonus nếu multi-TF aligned
        if multi_tf_aligned:
            base = min(100, base + 5)

        # Confidence formula
        if base >= 95:
            return 99.0
        elif base >= 90:
            return 95.0
        elif base >= 85:
            return 92.0
        elif base >= 80:
            return 88.0
        elif base >= 75:
            return 85.0
        elif base >= 70:
            return 80.0
        elif base >= 65:
            return 75.0
        elif base >= 60:
            return 70.0
        else:
            return 60.0

    @staticmethod
    def get_timeframe_label(trade_type: str) -> str:
        """Lấy nhãn thời hạn"""
        labels = {
            "scalping": "NGẮN HẠN 🎯",
            "day_trading": "TRUNG HẠN ⏳",
            "swing_trading": "DÀI HẠN 📅",
        }
        return labels.get(trade_type, "KHÁC")

    @staticmethod
    def get_leverage_suggestion(score: int, atr_pct: float) -> Dict:
        """Gợi ý đòn bẩy"""
        if score >= 90 and atr_pct < 1.5:
            leverage = 20
            risk = "CỰC CAO"
        elif score >= 80 and atr_pct < 2.0:
            leverage = 15
            risk = "CAO"
        elif score >= 70 and atr_pct < 2.5:
            leverage = 10
            risk = "TRUNG BÌNH"
        elif score >= 60:
            leverage = 5
            risk = "THẤP"
        else:
            leverage = 3
            risk = "RẤT THẤP"

        return {
            "leverage": leverage,
            "risk_label": risk,
            "detail": f"{leverage}x ({risk})",
        }


# Singleton
signal_rating = SignalRating()
