"""
Scanner - Main loop quét tín hiệu toàn bộ USDT pairs
"""

import time
import sys
import os
import json
from datetime import datetime
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import settings
from config.pairs import get_all_usdt_pairs, TOP_PAIRS
from data.binance_fetcher import fetcher
from signals.signal_engine import signal_engine
from signals.risk_manager import risk_manager
from notifications.telegram_bot import telegram_bot


class Scanner:
    def __init__(self):
        self.pairs = []
        self.signals_history = []
        self.running = False
        self.last_signals = {}  # Avoid duplicate signals

    def load_pairs(self):
        """Load danh sách pairs"""
        print("Loading USDT pairs...")
        self.pairs = get_all_usdt_pairs()
        print(f"Loaded {len(self.pairs)} pairs")

    def scan_pair(self, symbol: str, trade_type: str) -> Dict:
        """Quét 1 pair cho 1 loại giao dịch"""
        try:
            # Get multi-timeframe data
            tf_config = settings.TIMEFRAMES[trade_type]

            htf_df = fetcher.get_klines(symbol, tf_config["htf"])
            mtf_df = fetcher.get_klines(symbol, tf_config["mtf"])
            ltf_df = fetcher.get_klines(symbol, tf_config["ltf"])

            if htf_df is None or mtf_df is None or ltf_df is None:
                return None

            # Generate signal
            signal = signal_engine.generate_signal(symbol, htf_df, mtf_df, ltf_df, trade_type)

            if signal is None:
                return None

            # Calculate risk info
            risk_info = risk_manager.get_risk_reward_info(signal)

            return {
                "signal": signal,
                "risk": risk_info,
                "timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            print(f"Error scanning {symbol} ({trade_type}): {e}")
            return None

    def scan_all(self):
        """Quét tất cả pairs cho tất cả trade types"""
        all_signals = []

        trade_types = ["scalping", "day_trading", "swing_trading"]

        print(f"\n{'='*60}")
        print(f"🔍 Scanning {len(self.pairs)} pairs at {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"{'='*60}")

        for trade_type in trade_types:
            print(f"\n📊 Scanning {trade_type.upper()}...")

            with ThreadPoolExecutor(max_workers=settings.MAX_CONCURRENT_SCANS) as executor:
                futures = {
                    executor.submit(self.scan_pair, symbol, trade_type): (symbol, trade_type)
                    for symbol in self.pairs
                }

                for future in as_completed(futures):
                    symbol, tt = futures[future]
                    try:
                        result = future.result(timeout=30)
                        if result:
                            all_signals.append(result)
                            sig = result["signal"]
                            risk = result["risk"]
                            emoji = "🟢" if sig["direction"] == "long" else "🔴"
                            print(f"  {emoji} {sig['symbol']} | {sig['strength']} {sig['direction'].upper()} | Score: {sig['score']} | R:R 1:{risk['rr_ratio']}")
                    except Exception as e:
                        pass

        return all_signals

    def process_signals(self, signals: List[Dict]):
        """Xử lý và gửi tín hiệu"""
        if not signals:
            print("\n⚠️ No signals found in this scan.")
            return

        # Sort by score (highest first)
        signals.sort(key=lambda x: x["signal"]["score"], reverse=True)

        print(f"\n{'='*60}")
        print(f"📢 Found {len(signals)} signals!")
        print(f"{'='*60}")

        for result in signals:
            sig = result["signal"]
            risk = result["risk"]
            symbol = sig["symbol"]
            trade_type = sig["trade_type"]

            # Create unique key to avoid duplicates
            key = f"{symbol}_{trade_type}_{sig['direction']}"

            # Check if already sent recently (within 4 hours)
            if key in self.last_signals:
                last_time = self.last_signals[key]
                if time.time() - last_time < 4 * 3600:
                    continue

            # Send Telegram notification
            telegram_bot.send_signal(sig, risk)
            self.last_signals[key] = time.time()

            # Add to history
            self.signals_history.append(result)

            # Print summary
            print(f"\n{'─'*40}")
            print(f"{'🟢' if sig['direction'] == 'long' else '🔴'} {symbol} | {sig['strength']} {sig['direction'].upper()}")
            print(f"  Score: {sig['score']}/100 | Entry: ${risk['entry']:,.2f}")
            print(f"  SL: ${risk['sl']:,.2f} ({risk['sl_pct']:.1f}%) | Leverage: {risk['leverage']}x")
            print(f"  TP1: ${risk['tps'][0]['price']:,.2f} | TP2: ${risk['tps'][1]['price']:,.2f} | TP3: ${risk['tps'][2]['price']:,.2f}")

    def save_signals(self):
        """Lưu signals history vào file"""
        try:
            os.makedirs("data", exist_ok=True)
            with open("data/signals_history.json", "w") as f:
                json.dump(self.signals_history[-1000:], f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving signals: {e}")

    def run(self):
        """Chạy scanner loop"""
        self.running = True
        self.load_pairs()

        print("\n" + "=" * 60)
        print("🚀 CRYPTO FINDER BOT STARTED")
        print("=" * 60)
        print(f"📊 Pairs: {len(self.pairs)}")
        print(f"⏱️ Scan interval: {settings.SCAN_INTERVAL}s")
        print(f"🎯 Min score: {settings.MIN_SIGNAL_SCORE}")
        print(f"📱 Telegram: {'✅ Configured' if settings.TELEGRAM_BOT_TOKEN else '❌ Not configured'}")
        print("=" * 60)

        scan_count = 0
        while self.running:
            try:
                scan_count += 1
                print(f"\n🔄 Scan #{scan_count}")

                signals = self.scan_all()
                self.process_signals(signals)
                self.save_signals()

                print(f"\n⏳ Next scan in {settings.SCAN_INTERVAL}s...")
                time.sleep(settings.SCAN_INTERVAL)

            except KeyboardInterrupt:
                print("\n\n🛑 Bot stopped by user")
                self.running = False
                break
            except Exception as e:
                print(f"\n❌ Error in scan loop: {e}")
                time.sleep(10)

    def run_once(self):
        """Chạy 1 lần duy nhất (for testing)"""
        self.load_pairs()
        signals = self.scan_all()
        self.process_signals(signals)
        self.save_signals()
        return signals


if __name__ == "__main__":
    scanner = Scanner()

    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        scanner.run_once()
    else:
        scanner.run()
