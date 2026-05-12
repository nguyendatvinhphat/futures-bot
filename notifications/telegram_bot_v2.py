"""
Enhanced Telegram Bot v2 - Full Commands + Confluence Format
"""

import requests
import time
from typing import Dict, List, Optional
from datetime import datetime
from config import settings


class TelegramBotV2:
    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.chat_id = settings.TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.token}"
        self.paused = False
        self.auto_trade = False
        self.last_update_id = 0

    def send_message(self, text: str, parse_mode: str = None) -> bool:
        """Gửi message qua Telegram"""
        if not self.token or not self.chat_id:
            print("[Telegram] Not configured")
            return False

        try:
            url = f"{self.base_url}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": text,
                "disable_web_page_preview": True,
            }
            if parse_mode:
                payload["parse_mode"] = parse_mode

            resp = requests.post(url, json=payload, timeout=10)

            if resp.status_code != 200:
                error_data = resp.json()
                print(f"[Telegram] Error {resp.status_code}: {error_data.get('description', 'Unknown')}")

                # Retry without parse_mode if Markdown fails
                if parse_mode and "can't parse" in error_data.get("description", "").lower():
                    print("[Telegram] Retrying without parse_mode...")
                    payload.pop("parse_mode", None)
                    resp = requests.post(url, json=payload, timeout=10)

            return resp.status_code == 200
        except Exception as e:
            print(f"Telegram error: {e}")
            return False

    def get_updates(self, offset: int = None, timeout: int = 1) -> List[Dict]:
        """Lấy updates từ Telegram"""
        try:
            url = f"{self.base_url}/getUpdates"
            params = {"timeout": timeout, "allowed_updates": ["message"]}
            if offset:
                params["offset"] = offset
            resp = requests.get(url, params=params, timeout=timeout + 5)
            if resp.status_code == 200:
                return resp.json().get("result", [])
        except Exception:
            pass
        return []

    def format_confluence_signal(self, signal: Dict, risk_info: Dict) -> str:
        """Format signal theo phong cách Confluence Bot"""
        direction = signal["direction"].upper()
        strength = signal["strength"]
        symbol = signal["symbol"]
        score = signal["score"]
        confidence = signal.get("confidence", 70)

        # Direction emoji
        dir_emoji = "🟢" if direction == "LONG" else "🔴"
        dir_text = "LONG" if direction == "LONG" else "SHORT"

        # Rating
        rating = signal.get("rating", {})
        rank = rating.get("rank", "WEAK")
        rank_emoji = rating.get("emoji", "⚠️")

        # Timeframe label
        tf_label = signal.get("tf_label", "KHÁC")

        # Market regime
        regime = signal.get("regime", {})
        regime_emoji = regime.get("emoji", "➡️")
        regime_label = regime.get("label", "Unknown")

        # LTF data
        ltf = signal.get("ltf", {})
        rsi = ltf.get("rsi", 0)
        adx = ltf.get("adx", 0)
        stoch = ltf.get("stoch", {})
        fib = ltf.get("fib", {})
        bb = ltf.get("bb", {})
        candlestick = ltf.get("candlestick", [])
        structure = ltf.get("structure", {})
        smc = ltf.get("smc", {})

        # Volume ratio
        vol_ratio = signal.get("ltf", {}).get("ema", {})

        # Leverage
        lev_info = signal.get("leverage_info", {})
        leverage = lev_info.get("leverage", 5)
        risk_label = lev_info.get("risk_label", "TRUNG BÌNH")

        # Funding rate
        funding = signal.get("funding_rate")
        oi = signal.get("open_interest")

        # TPs
        tps = risk_info.get("tps", [])

        # Support/Resistance
        support = structure.get("last_pl")
        resistance = structure.get("last_ph")
        support_str = f"${support:.4f}" if support is not None else "N/A"
        resistance_str = f"${resistance:.4f}" if resistance is not None else "N/A"

        # FVG/OB counts from SMC
        fvgs = smc.get("fvgs", [])
        obs = smc.get("order_blocks", [])
        fvg_bull = len([f for f in fvgs if f.get("type") == "bullish"])
        fvg_bear = len([f for f in fvgs if f.get("type") == "bearish"])
        ob_bull = len([o for o in obs if o.get("type") == "bullish"])
        ob_bear = len([o for o in obs if o.get("type") == "bearish"])

        # Candlestick label
        cs_label = " ".join(candlestick) if candlestick else "None"

        # Fibonacci level
        fib_nearest = fib.get("nearest_level", "N/A")
        fib_price = fib.get("levels", {}).get(fib_nearest, 0)

        # BB values
        bb_upper = bb.get("bb_upper", 0)
        bb_lower = bb.get("bb_lower", 0)

        # Build message
        message = f"""
🎯 {rank_emoji} CONFLUENCE 2.1.0 {rank} {dir_text} {dir_emoji}
  {symbol} | 💰 {risk_info['entry']:.4f}
 ⏱️ Thời hạn: {tf_label}
 🎯 TP1: {tps[0]['price']:.4f} | TP2: {tps[1]['price']:.4f} | TP3: {tps[2]['price']:.4f}
 🛑 SL: {risk_info['sl']:.4f}
 📊 Tin cậy: {confidence}% | Hạng: {rank} {rank_emoji}
 🔍 Xu hướng: {regime_label} | ADX: {adx:.1f} | RSI: {rsi:.1f} | KL: {signal.get('volume_ratio', 'N/A')}x
 🏷️ Chế độ: {regime_emoji} {regime_label} {'🕯️ ' + cs_label if cs_label != 'None' else ''} 📐 Fib {fib_nearest} @ ${fib_price:.4f}
 🟠 Bollinger: BB: ${bb_upper:.4f}/${bb_lower:.4f}
 🟢 Stochastic: %K={stoch.get('k', 0):.1f}% | %D={stoch.get('d', 0):.1f}%
 🏷️ FVG: {fvg_bull}B/{fvg_bear}S | OB: {ob_bull}B/{ob_bear}S
 📊 Hỗ trợ: {support_str} | Kháng cự: {resistance_str}
 💰 Funding: {f'{funding:+.3f}%' if funding is not None else 'N/A'} | OI: {f'{oi:,.0f}' if oi is not None else 'N/A'}
 💪 Đòn bẩy gợi ý: {leverage}x ({risk_label})
 🔥 Bot 2.1.0"""

        return message.strip()

    def format_check_result(self, symbol: str, signal: Dict, risk_info: Dict) -> str:
        """Format kết quả /check command"""
        if signal is None:
            return f"❌ {symbol} - Không tìm thấy tín hiệu đủ mạnh"

        return self.format_confluence_signal(signal, risk_info)

    def format_regime(self, symbol: str, regime: Dict) -> str:
        """Format market regime"""
        return f"""
📊 Market Regime - {symbol}
━━━━━━━━━━━━━━━━━━━━
{regime.get('emoji', '➡️')} Chế độ: {regime.get('label', 'Unknown')}
📈 ADX: {regime.get('adx', 0)}
🌊 Volatility: {regime.get('volatility', 0)}%
📐 Trend Slope: {regime.get('trend_slope', 0)}%
━━━━━━━━━━━━━━━━━━━━
"""

    def format_indicators(self, symbol: str, data: Dict) -> str:
        """Format chi tiết indicators"""
        return f"""
📊 Indicators - {symbol}
━━━━━━━━━━━━━━━━━━━━
RSI: {data.get('rsi', 0):.1f}
MACD: {data.get('macd', 0):.4f}
EMA 9: ${data.get('ema_9', 0):,.2f}
EMA 21: ${data.get('ema_21', 0):,.2f}
Supertrend: {'UP' if data.get('st_direction', 1) == 1 else 'DOWN'}
ADX: {data.get('adx', 0):.1f}
VWAP: ${data.get('vwap', 0):,.2f}
ATR: ${data.get('atr', 0):,.2f}
Stoch %K: {data.get('stoch_k', 0):.1f}%
Stoch %D: {data.get('stoch_d', 0):.1f}%
BB Upper: ${data.get('bb_upper', 0):,.2f}
BB Lower: ${data.get('bb_lower', 0):,.2f}
━━━━━━━━━━━━━━━━━━━━
"""

    def format_scan_results(self, signals: List[Dict]) -> str:
        """Format kết quả /scan"""
        if not signals:
            return "❌ Không tìm thấy tín hiệu nào"

        header = f"🔍 Scan Results - {len(signals)} signals found\n━━━━━━━━━━━━━━━━━━━━\n"

        lines = []
        for s in signals[:10]:
            sig = s.get("signal", s)
            risk = s.get("risk", {})
            dir_emoji = "🟢" if sig["direction"] == "long" else "🔴"
            rank_emoji = sig.get("rating", {}).get("emoji", "⚠️")
            lines.append(
                f"{dir_emoji} {sig['symbol']} | {sig['strength']} {rank_emoji} | "
                f"Score: {sig['score']} | Entry: ${risk.get('entry', sig.get('entry_price', 0)):.4f} | "
                f"R:R 1:{risk.get('rr_ratio', 0)}"
            )

        return header + "\n".join(lines)

    def format_pnl(self, stats: Dict) -> str:
        """Format PnL stats"""
        pnl_emoji = "📈" if stats["total_pnl"] >= 0 else "📉"
        pnl_sign = "+" if stats["total_pnl"] >= 0 else ""

        return f"""
💰 Paper Trading PnL
━━━━━━━━━━━━━━━━━━━━
💵 Vốn ban đầu: ${stats['initial_capital']:.2f}
💵 Vốn hiện tại: ${stats['current_capital']:.2f}
{pnl_emoji} PnL: {pnl_sign}${stats['total_pnl']:.2f} ({pnl_sign}{stats['pnl_pct']:.1f}%)
━━━━━━━━━━━━━━━━━━━━
📊 Tổng lệnh: {stats['total_trades']}
✅ Thắng: {stats['winning_trades']}
❌ Thua: {stats['losing_trades']}
🎯 Win Rate: {stats['win_rate']}%
📉 Max Drawdown: {stats['max_drawdown']}%
💎 Profit Factor: {stats['profit_factor']}
📈 Positions đang mở: {stats['open_positions']}
━━━━━━━━━━━━━━━━━━━━
"""

    def format_help(self) -> str:
        """Format help menu"""
        return """
🤖 Confluence Bot 2.1.0 - Commands

🔍 Check Coin:
/check SYMBOL [TF]
Ví dụ:
/check BTCUSDT 1h
/check SOLUSDT 4h

📊 Quick Scan:
/scan [NUMBER]
Ví dụ: /scan 10

📈 Market Regime:
/regime SYMBOL - Xem chế độ thị trường

📊 Indicators:
/indicators SYMBOL - Xem chi tiết indicators

⚙️ System:
/status → Xem trạng thái bot
/presets → Xem các chiến lược
/learn → Xem thống kê học tập từ lịch sử
/help → Hiện menu này

🌐 Web Dashboard:
http://127.0.0.1:5000

🔥 Bot 2.1.0
"""

    def format_status(self, scanner_status: Dict) -> str:
        """Format bot status"""
        return f"""
🤖 Bot Status
━━━━━━━━━━━━━━━━━━━━
🔄 Scanner: {'🟢 Running' if scanner_status.get('running', False) else '🔴 Stopped'}
📊 Pairs: {scanner_status.get('pairs_count', 0)}
⏰ Last Scan: {scanner_status.get('last_scan', 'N/A')}
📢 Signals Sent: {scanner_status.get('signals_sent', 0)}
━━━━━━━━━━━━━━━━━━━━
"""

    def format_presets(self) -> str:
        """Format presets"""
        return """
📋 Chiến lược (Presets)
━━━━━━━━━━━━━━━━━━━━
1. Conservative (An toàn)
- Min Score: 75
- R:R tối thiểu: 1:3
- Leverage max: 5x
- Risk/trade: 1%

2. Standard (Tiêu chuẩn)
- Min Score: 65
- R:R tối thiểu: 1:2
- Leverage max: 10x
- Risk/trade: 2%

3. Aggressive (Tấn công)
- Min Score: 55
- R:R tối thiểu: 1:1.5
- Leverage max: 20x
- Risk/trade: 3%

━━━━━━━━━━━━━━━━━━━━
"""

    def send_signal(self, signal: Dict, risk_info: Dict) -> bool:
        """Gửi signal qua Telegram"""
        message = self.format_confluence_signal(signal, risk_info)
        return self.send_message(message)


# Singleton
telegram_bot_v2 = TelegramBotV2()
