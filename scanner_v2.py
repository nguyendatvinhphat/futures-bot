"""
Enhanced Scanner v2 - Full featured scanner with commands
"""

import sys
import os

# Fix Unicode encoding for Windows console
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

import time
import json
import threading
from datetime import datetime, timezone
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import settings
from config.pairs import get_all_usdt_pairs, TOP_PAIRS
from data.binance_fetcher import fetcher
from signals.signal_engine_v2 import signal_engine_v2
from signals.risk_manager import risk_manager
from signals.paper_trading import paper_trader
from signals.learning import signal_learner
from notifications.telegram_bot_v2 import telegram_bot_v2


class ScannerV2:
    def __init__(self):
        self.pairs = []
        self.signals_history = []
        self.running = False
        self.paused = False
        self.last_signals = {}
        self.signals_sent = 0
        self.last_scan_time = None
        self.scan_count = 0
        self.prev_signal_keys = set()  # Track signal keys tu scan truoc
        self.sent_signal_keys = set()  # Track ALL sent signal keys (dedup)

    def load_pairs(self):
        """Load danh sach pairs"""
        print("Loading USDT pairs...")
        self.pairs = get_all_usdt_pairs()
        # Gioi han chi scan top 20 pairs de nhanh hon
        if len(self.pairs) > 20:
            self.pairs = self.pairs[:20]
        print(f"Loaded {len(self.pairs)} pairs")

    def get_funding_rate(self, symbol: str) -> Optional[float]:
        """Lay funding rate"""
        return fetcher.get_funding_rate(symbol)

    def get_open_interest(self, symbol: str) -> Optional[float]:
        """Lay open interest"""
        try:
            url = "https://fapi.binance.com/fapi/v1/openInterest"
            import requests
            resp = requests.get(url, params={"symbol": symbol}, timeout=5)
            if resp.status_code == 200:
                return float(resp.json().get("openInterest", 0))
        except Exception:
            pass
        return None

    def scan_pair(self, symbol: str, trade_type: str) -> Optional[Dict]:
        """Quet 1 pair cho 1 loai giao dich"""
        try:
            tf_config = settings.TIMEFRAMES[trade_type]

            htf_df = fetcher.get_klines(symbol, tf_config["htf"])
            mtf_df = fetcher.get_klines(symbol, tf_config["mtf"])
            ltf_df = fetcher.get_klines(symbol, tf_config["ltf"])

            if htf_df is None or mtf_df is None or ltf_df is None:
                return None

            # Get funding rate and OI
            funding = self.get_funding_rate(symbol)
            oi = self.get_open_interest(symbol)

            # Generate signal
            signal = signal_engine_v2.generate_signal(
                symbol, htf_df, mtf_df, ltf_df, trade_type,
                funding_rate=funding, open_interest=oi
            )

            if signal is None:
                return None

            # Calculate risk info
            risk_info = risk_manager.get_risk_reward_info(signal)

            # Validate risk - reject if SL == Entry or Entry == 0
            if risk_info["entry"] == 0 or risk_info["sl"] == risk_info["entry"]:
                return None

            return {
                "signal": signal,
                "risk": risk_info,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        except Exception as e:
            print(f"Error scanning {symbol} ({trade_type}): {e}")
            return None

    def scan_specific(self, symbol: str, trade_type: str = "day_trading") -> Optional[Dict]:
        """Quet 1 symbol cu the"""
        return self.scan_pair(symbol.upper(), trade_type)

    def scan_top(self, count: int = 10) -> List[Dict]:
        """Quet top N pairs"""
        all_signals = []
        trade_types = ["scalping", "day_trading", "swing_trading"]

        for trade_type in trade_types:
            pairs_to_scan = self.pairs[:count]
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = {
                    executor.submit(self.scan_pair, symbol, trade_type): symbol
                    for symbol in pairs_to_scan
                }
                for future in as_completed(futures):
                    try:
                        result = future.result(timeout=30)
                        if result:
                            all_signals.append(result)
                    except Exception:
                        pass

        return all_signals

    def scan_all(self):
        """Quet tat ca pairs"""
        all_signals = []
        trade_types = ["scalping", "day_trading", "swing_trading"]

        print(f"\n{'='*60}")
        print(f"Scanning {len(self.pairs)} pairs at {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"{'='*60}")

        for trade_type in trade_types:
            if self.paused:
                print("Scanner paused")
                break

            print(f"\nScanning {trade_type.upper()}...")

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
                            emoji = "+" if sig["direction"] == "long" else "-"
                            rating = sig.get("rating", {})
                            print(f"  {emoji} {sig['symbol']} | {sig['strength']} | Score: {sig['score']} | R:R 1:{risk['rr_ratio']}")
                    except Exception:
                        pass

        self.last_scan_time = datetime.now(timezone.utc).isoformat()
        return all_signals

    def process_signals(self, signals: List[Dict]):
        """Xu ly va gui tin hieu (chi gui signal chat luong cao)"""
        if not signals:
            print("\nNo signals found in this scan.")
            return

        signals.sort(key=lambda x: x["signal"]["score"], reverse=True)

        print(f"\n{'='*60}")
        print(f"Found {len(signals)} raw signals, filtering for quality...")
        print(f"{'='*60}")

        sent_count = 0
        skipped_count = 0
        filtered_count = 0
        dup_count = 0

        # Tao set signal keys tu scan hien tai
        current_signal_keys = set()

        # Tao set dedup tu history hien tai (chi active)
        existing_active_keys = set()
        for result in self.signals_history:
            if result.get("status", "active") in ("active", "tp1_hit"):
                sig = result.get("signal", {})
                dedup_key = f"{sig.get('symbol', '')}_{sig.get('direction', '')}_{sig.get('trade_type', '')}"
                existing_active_keys.add(dedup_key)

        # Luu TAT CA signals vao history (cho dashboard) - nhung KHONG luu duplicate
        for result in signals:
            sig = result["signal"]
            dedup_key = f"{sig['symbol']}_{sig['direction']}_{sig['trade_type']}"

            # Skip neu da co signal active cung symbol+direction+trade_type
            if dedup_key in existing_active_keys:
                dup_count += 1
                continue

            # Them status va tp_hits neu chua co
            if "status" not in result:
                result["status"] = "active"
            if "tp_hits" not in result:
                result["tp_hits"] = []
            self.signals_history.append(result)
            existing_active_keys.add(dedup_key)

        # Gioi han history
        if len(self.signals_history) > 1000:
            self.signals_history = self.signals_history[-1000:]

        # Luu ra file ngay
        self.save_signals()

        for result in signals:
            sig = result["signal"]
            risk = result["risk"]
            symbol = sig["symbol"]
            trade_type = sig["trade_type"]

            key = f"{symbol}_{trade_type}_{sig['direction']}"
            current_signal_keys.add(key)

            # ===== QUALITY FILTERS =====
            quality_pass, reason = self._check_quality(sig, risk)
            if not quality_pass:
                filtered_count += 1
                continue

            # Dedup check - da gui signal nay trong session chua
            if key in self.sent_signal_keys:
                skipped_count += 1
                continue

            # Cooldown check - chi gui signal MOI hoac da het cooldown
            is_new = key not in self.prev_signal_keys

            if key in self.last_signals:
                last_time = self.last_signals[key]
                elapsed = time.time() - last_time
                if elapsed < settings.SIGNAL_COOLDOWN and not is_new:
                    skipped_count += 1
                    continue

            # Send Telegram notification
            ok = telegram_bot_v2.send_signal(sig, risk)
            if ok:
                print(f"  [OK] Sent {symbol} {sig['direction']} Score:{sig['score']} R:R 1:{risk['rr_ratio']}")
                sent_count += 1
            else:
                print(f"  [FAIL] to send {symbol} to Telegram!")

            self.last_signals[key] = time.time()
            self.sent_signal_keys.add(key)
            self.signals_sent += 1

            # Push to dashboard
            self._push_to_dashboard(result)

            # Record to learning system
            signal_learner.record_signal(sig, risk)

            # Open paper trade
            if sig["score"] >= 70:
                paper_trader.open_position(sig, risk)

        # Cap nhat prev_signal_keys cho scan tiep theo
        self.prev_signal_keys = current_signal_keys

        # Gui summary moi 5 scans
        self.scan_count += 1
        if self.scan_count % 5 == 0:
            self._send_summary(signals)

        print(f"\nSummary: {sent_count} sent, {skipped_count} skipped (cooldown), {filtered_count} filtered (low quality), {dup_count} deduped")

    def _check_quality(self, sig: Dict, risk: Dict) -> tuple:
        """Kiem tra chat luong signal. Tra ve (pass, reason)"""

        # 1. Check minimum score
        if sig["score"] < settings.MIN_SEND_SCORE:
            return False, f"Score {sig['score']} < {settings.MIN_SEND_SCORE}"

        # 2. Check R:R ratio
        rr = risk.get("rr_ratio", 0)
        if rr < settings.MIN_RR_RATIO:
            return False, f"R:R {rr} < {settings.MIN_RR_RATIO}"

        # 3. Check multi-TF alignment
        if settings.REQUIRE_MULTI_TF:
            multi_tf = sig.get("multi_tf_aligned", False)
            if not multi_tf:
                return False, "Multi-TF not aligned"

        # 4. Check consensus percentage
        consensus_pct = sig.get("consensus_pct", 0)
        if consensus_pct < settings.MIN_CONSENSUS_PCT:
            return False, f"Consensus {consensus_pct}% < {settings.MIN_CONSENSUS_PCT}%"

        # 5. Check strong confirmation
        if settings.REQUIRE_STRONG_CONFIRMATION:
            has_strong = self._has_strong_confirmation(sig)
            if not has_strong:
                return False, "No strong confirmation"

        # 6. Check RSI extremes (chi reject extreme)
        direction = sig.get("direction", "")
        ltf = sig.get("ltf", {})
        rsi = ltf.get("rsi", 50)
        if direction == "long" and rsi > 85:
            return False, f"LONG nhung RSI {rsi:.0f} > 85 (qua overbought)"
        if direction == "short" and rsi < 15:
            return False, f"SHORT nhung RSI {rsi:.0f} < 15 (qua oversold)"

        # 7. Check ADX (tranh signal trong thi truong qua sideway)
        adx = ltf.get("adx", 0)
        if adx < 10:
            return False, f"ADX {adx:.0f} < 10 (thi truong qua sideway)"

        return True, "OK"

    def _has_strong_confirmation(self, sig: Dict) -> bool:
        """Kiem tra co confirmation manh khong"""
        # Check cac tin hieu manh
        ltf = sig.get("ltf", {})
        raw_signals = sig.get("raw_signals", ltf.get("raw_signals", {}))

        # EMA cross
        ema_data = ltf.get("ema", {})
        if ema_data.get("cross_up") or ema_data.get("cross_down"):
            return True

        # BOS/CHoCH (structure)
        structure = ltf.get("structure", {})
        if structure.get("bos_bullish") or structure.get("bos_bearish"):
            return True
        if structure.get("choch_bullish") or structure.get("choch_bearish"):
            return True

        # Volume spike
        vol_ratio = ltf.get("vol_ratio", 0)
        if isinstance(vol_ratio, (int, float)) and vol_ratio > settings.VOL_SPIKE_MULTIPLIER:
            return True

        # RSI extreme
        rsi = ltf.get("rsi", 50)
        if isinstance(rsi, (int, float)) and (rsi < 25 or rsi > 75):
            return True

        # Stochastic extreme
        stoch = ltf.get("stoch", {})
        stoch_k = stoch.get("k", 50)
        if isinstance(stoch_k, (int, float)) and (stoch_k < 20 or stoch_k > 80):
            return True

        # Score rat cao (>= 80) thi coi nhu strong
        if sig["score"] >= 80:
            return True

        return False

    def _send_summary(self, signals: List[Dict]):
        """Gui tong hop signal hien tai qua Telegram"""
        try:
            if not signals:
                return

            lines = [f"TONG HOP - {len(signals)} signals dang hoat dong"]
            lines.append("-" * 30)

            for s in signals[:15]:
                sig = s["signal"]
                risk = s["risk"]
                dir_emoji = "+" if sig["direction"] == "long" else "-"
                rank_emoji = sig.get("rating", {}).get("emoji", "")
                lines.append(
                    f"{dir_emoji} {sig['symbol']} | {sig['strength']} {rank_emoji} | "
                    f"Score:{sig['score']} | Entry:{risk.get('entry', 0):.4f}"
                )

            if len(signals) > 15:
                lines.append(f"... va {len(signals) - 15} signal khac")

            lines.append("-" * 30)
            lines.append(f"Cap nhat moi {settings.SCAN_INTERVAL}s")

            telegram_bot_v2.send_message("\n".join(lines))
            print(f"  Sent summary to Telegram")
        except Exception as e:
            print(f"  Summary error: {e}")

    def get_status(self) -> Dict:
        """Lay trang thai scanner"""
        return {
            "running": self.running,
            "paused": self.paused,
            "pairs_count": len(self.pairs),
            "last_scan": self.last_scan_time,
            "signals_sent": self.signals_sent,
        }

    def check_signal_outcomes(self):
        """Kiem tra ket qua cac signal dang active"""
        try:
            # Get current prices for all symbols with active signals
            active_symbols = set()

            # Check learning system
            for record in signal_learner.history:
                if record["status"] == "active":
                    active_symbols.add(record["symbol"])

            # Check signals_history (dashboard)
            for result in self.signals_history:
                sig = result.get("signal", {})
                status = result.get("status", "active")

                # Chi xu ly signals active (hoac khong co status)
                if status not in ("active", None, "", "N/A"):
                    continue

                active_symbols.add(sig.get("symbol", ""))

            if not active_symbols:
                return

            # Get current prices (fetch all at once)
            tickers = fetcher.get_all_tickers()
            if not tickers:
                return

            # Update learning system
            for record in signal_learner.history:
                if record["status"] == "active":
                    result = signal_learner.check_signal_outcome(record["id"], tickers)
                    if result and result != "active":
                        print(f"  Signal {record['symbol']} outcome: {result}")

            # Update signals_history (dashboard)
            updated = False
            for result in self.signals_history:
                sig = result.get("signal", {})
                status = result.get("status", "active")

                # Chi xu ly signals active (hoac khong co status)
                if status not in ("active", None, "", "N/A"):
                    continue

                symbol = sig.get("symbol", "")
                if symbol not in tickers:
                    continue

                price = tickers[symbol]
                direction = sig.get("direction", "")
                risk = result.get("risk", {})
                entry = risk.get("entry", 0)
                sl = risk.get("sl", 0)
                tps = risk.get("tps", [])
                tp_prices = [tp.get("price", 0) if isinstance(tp, dict) else tp for tp in tps]

                # Check SL
                if direction == "long" and price <= sl:
                    result["status"] = "sl_hit"
                    updated = True
                elif direction == "short" and price >= sl:
                    result["status"] = "sl_hit"
                    updated = True

                # Check TPs
                tp_hits = result.get("tp_hits", [])
                for i, tp in enumerate(tp_prices):
                    if i not in tp_hits:
                        if direction == "long" and price >= tp:
                            tp_hits.append(i)
                            updated = True
                        elif direction == "short" and price <= tp:
                            tp_hits.append(i)
                            updated = True

                result["tp_hits"] = tp_hits

                # Update status based on TP hits (chi neu chua SL)
                if result.get("status") != "sl_hit":
                    if len(tp_hits) >= 3:
                        result["status"] = "tp3_hit"
                        updated = True
                    elif len(tp_hits) >= 2:
                        result["status"] = "tp2_hit"
                        updated = True
                    elif len(tp_hits) >= 1:
                        result["status"] = "tp1_hit"
                        updated = True
                    else:
                        result["status"] = "active"

            # Save if updated
            if updated:
                self.save_signals()
                print(f"  Updated signal statuses in dashboard")

        except Exception as e:
            print(f"Error checking outcomes: {e}")

    def run(self):
        """Chay scanner loop"""
        self.running = True
        self.load_pairs()

        print("\n" + "=" * 60)
        print("CRYPTO FINDER BOT v2.1.0 STARTED")
        print("=" * 60)
        print(f"Pairs: {len(self.pairs)}")
        print(f"Scan interval: {settings.SCAN_INTERVAL}s")
        print(f"Min score: {settings.MIN_SIGNAL_SCORE}")
        print(f"Telegram: {'Configured' if settings.TELEGRAM_BOT_TOKEN else 'Not configured'}")
        print("=" * 60)

        # Start Telegram command listener
        if settings.TELEGRAM_BOT_TOKEN:
            cmd_thread = threading.Thread(target=self._listen_commands, daemon=True)
            cmd_thread.start()

        scan_count = 0
        while self.running:
            try:
                if not self.paused:
                    scan_count += 1
                    print(f"\nScan #{scan_count}")

                    signals = self.scan_all()
                    print(f"scan_all() returned {len(signals)} signals")

                    try:
                        self.process_signals(signals)
                    except Exception as proc_err:
                        print(f"process_signals ERROR: {proc_err}")
                        import traceback
                        traceback.print_exc()

                    self.save_signals()

                    # Check outcomes of active signals
                    self.check_signal_outcomes()

                    # Reset sent_signal_keys every 10 scans to avoid memory leak
                    if scan_count % 10 == 0:
                        self.sent_signal_keys.clear()

                print(f"\nNext scan in {settings.SCAN_INTERVAL}s...")
                time.sleep(settings.SCAN_INTERVAL)

            except KeyboardInterrupt:
                print("\n\nBot stopped by user")
                self.running = False
                break
            except Exception as e:
                print(f"\nError in scan loop: {e}")
                import traceback
                traceback.print_exc()
                time.sleep(10)

    def _listen_commands(self):
        """Lang nghe Telegram commands"""
        print("Listening for Telegram commands...")

        while self.running:
            try:
                updates = telegram_bot_v2.get_updates(
                    offset=telegram_bot_v2.last_update_id + 1,
                    timeout=1
                )

                for update in updates:
                    telegram_bot_v2.last_update_id = update["update_id"]
                    message = update.get("message", {})
                    text = message.get("text", "")
                    chat_id = str(message.get("chat", {}).get("id", ""))

                    print(f"[TELE] Received from {chat_id}: '{text}'")
                    print(f"[TELE] Expected chat_id: '{settings.TELEGRAM_CHAT_ID}'")
                    print(f"[TELE] Match: {chat_id == settings.TELEGRAM_CHAT_ID}")

                    if chat_id != settings.TELEGRAM_CHAT_ID:
                        print(f"[TELE] Ignoring - wrong chat_id")
                        continue

                    self._handle_command(text)

            except Exception as e:
                print(f"[TELE] Error: {e}")
                time.sleep(1)

    def _handle_command(self, text: str):
        """Xu ly Telegram commands"""
        text = text.strip()
        print(f"[CMD] Received: '{text}'")

        if text == "/help":
            telegram_bot_v2.send_message(telegram_bot_v2.format_help())

        elif text == "/status":
            status = self.get_status()
            telegram_bot_v2.send_message(telegram_bot_v2.format_status(status))

        elif text == "/presets":
            telegram_bot_v2.send_message(telegram_bot_v2.format_presets())

        elif text == "/learn":
            telegram_bot_v2.send_message("Dang tao bao cao hoc tap...")
            report = signal_learner.format_learning_report()
            telegram_bot_v2.send_message(report)

        elif text.startswith("/check"):
            parts = text.split()
            if len(parts) >= 2:
                symbol = parts[1].upper()
                trade_type = "day_trading"
                if len(parts) >= 3:
                    tf = parts[2].lower()
                    if tf in ["1m", "5m", "15m"]:
                        trade_type = "scalping"
                    elif tf in ["1h", "4h"]:
                        trade_type = "day_trading"
                    elif tf in ["1d", "1w"]:
                        trade_type = "swing_trading"

                telegram_bot_v2.send_message(f"Checking {symbol}...")
                threading.Thread(
                    target=self._run_check,
                    args=(symbol, trade_type),
                    daemon=True
                ).start()
            else:
                telegram_bot_v2.send_message("Usage: /check SYMBOL [TF]\nExample: /check BTCUSDT 1h")

        elif text.startswith("/scan"):
            parts = text.split()
            count = 10
            if len(parts) >= 2:
                try:
                    count = int(parts[1])
                except ValueError:
                    pass

            telegram_bot_v2.send_message(f"Scanning top {count} pairs...")
            threading.Thread(
                target=self._run_scan_top,
                args=(count,),
                daemon=True
            ).start()

        elif text.startswith("/regime"):
            parts = text.split()
            if len(parts) >= 2:
                symbol = parts[1].upper()
                telegram_bot_v2.send_message(f"Checking regime for {symbol}...")
                threading.Thread(
                    target=self._run_regime,
                    args=(symbol,),
                    daemon=True
                ).start()

        elif text.startswith("/indicators"):
            parts = text.split()
            if len(parts) >= 2:
                symbol = parts[1].upper()
                telegram_bot_v2.send_message(f"Loading indicators for {symbol}...")
                threading.Thread(
                    target=self._run_indicators,
                    args=(symbol,),
                    daemon=True
                ).start()

        else:
            telegram_bot_v2.send_message("Unknown command. Use /help")

    def _run_scan_top(self, count: int):
        """Chay scan_top trong thread rieng de khong block command listener"""
        try:
            import time as _time
            start = _time.time()

            all_signals = []
            trade_types = ["scalping", "day_trading", "swing_trading"]

            for idx, trade_type in enumerate(trade_types):
                telegram_bot_v2.send_message(f"({idx+1}/3) Scanning {trade_type}...")
                pairs_to_scan = self.pairs[:count]

                with ThreadPoolExecutor(max_workers=10) as executor:
                    futures = {
                        executor.submit(self.scan_pair, symbol, trade_type): symbol
                        for symbol in pairs_to_scan
                    }
                    for future in as_completed(futures):
                        try:
                            result = future.result(timeout=30)
                            if result:
                                all_signals.append(result)
                        except Exception:
                            pass

            elapsed = _time.time() - start

            if all_signals:
                msg = telegram_bot_v2.format_scan_results(all_signals)
                telegram_bot_v2.send_message(msg)
            else:
                telegram_bot_v2.send_message(f"No signals found (scanned {count} pairs, {elapsed:.0f}s)")
        except Exception as e:
            telegram_bot_v2.send_message(f"Scan error: {e}")

    def _run_check(self, symbol: str, trade_type: str):
        """Chay check trong thread rieng"""
        try:
            result = self.scan_specific(symbol, trade_type)
            if result:
                msg = telegram_bot_v2.format_check_result(symbol, result["signal"], result["risk"])
                telegram_bot_v2.send_message(msg)
            else:
                # Get raw score for debugging
                tf_config = settings.TIMEFRAMES[trade_type]
                htf = fetcher.get_klines(symbol, tf_config["htf"])
                mtf = fetcher.get_klines(symbol, tf_config["mtf"])
                ltf = fetcher.get_klines(symbol, tf_config["ltf"])

                if htf is None or mtf is None or ltf is None:
                    telegram_bot_v2.send_message(f"{symbol} - Cannot fetch data")
                else:
                    from signals.signal_engine_v2 import signal_engine_v2
                    htf_r = signal_engine_v2.analyze_single_tf(htf)
                    mtf_r = signal_engine_v2.analyze_single_tf(mtf)
                    ltf_r = signal_engine_v2.analyze_single_tf(ltf)
                    htf_s = signal_engine_v2.calculate_score(htf_r["signals"])
                    mtf_s = signal_engine_v2.calculate_score(mtf_r["signals"])
                    ltf_s = signal_engine_v2.calculate_score(ltf_r["signals"])
                    weighted = htf_s['score'] * 0.4 + mtf_s['score'] * 0.35 + ltf_s['score'] * 0.25
                    telegram_bot_v2.send_message(
                        f"{symbol} - Score {weighted:.0f} < {settings.MIN_SIGNAL_SCORE}\n"
                        f"HTF: {htf_s['score']} {htf_s['direction']} | "
                        f"MTF: {mtf_s['score']} {mtf_s['direction']} | "
                        f"LTF: {ltf_s['score']} {ltf_s['direction']}"
                    )
        except Exception as e:
            telegram_bot_v2.send_message(f"Check error: {e}")

    def _run_regime(self, symbol: str):
        """Chay regime check trong thread rieng"""
        try:
            df = fetcher.get_klines(symbol, "1h", limit=100)
            if df is not None:
                from indicators.advanced import detect_market_regime
                regime = detect_market_regime(df)
                msg = telegram_bot_v2.format_regime(symbol, regime)
                telegram_bot_v2.send_message(msg)
        except Exception as e:
            telegram_bot_v2.send_message(f"Regime error: {e}")

    def _run_indicators(self, symbol: str):
        """Chay indicators check trong thread rieng"""
        try:
            df = fetcher.get_klines(symbol, "1h", limit=300)
            if df is not None:
                from indicators import (
                    calculate_ema, calculate_rsi, calculate_macd,
                    calculate_supertrend, calculate_adx, calculate_vwap,
                    calculate_atr, calculate_bollinger_bands
                )
                from indicators.advanced import calculate_stochastic

                df = calculate_ema(df)
                df = calculate_rsi(df)
                df = calculate_macd(df)
                df = calculate_supertrend(df)
                df = calculate_adx(df)
                df = calculate_vwap(df)
                df = calculate_atr(df)
                df = calculate_bollinger_bands(df)
                df = calculate_stochastic(df)

                last = df.iloc[-1]
                data = {
                    "rsi": last.get("rsi", 0),
                    "macd": last.get("macd_line", 0),
                    "ema_9": last.get("ema_9", 0),
                    "ema_21": last.get("ema_21", 0),
                    "st_direction": last.get("st_direction", 1),
                    "adx": last.get("adx", 0),
                    "vwap": last.get("vwap", 0),
                    "atr": last.get("atr", 0),
                    "stoch_k": last.get("stoch_k", 0),
                    "stoch_d": last.get("stoch_d", 0),
                    "bb_upper": last.get("bb_upper", 0),
                    "bb_lower": last.get("bb_lower", 0),
                }
                msg = telegram_bot_v2.format_indicators(symbol, data)
                telegram_bot_v2.send_message(msg)
        except Exception as e:
            telegram_bot_v2.send_message(f"Indicators error: {e}")

    def save_signals(self):
        """Luu signals history"""
        try:
            os.makedirs("data", exist_ok=True)
            with open("data/signals_history.json", "w") as f:
                json.dump(self.signals_history[-1000:], f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving signals: {e}")

    def _push_to_dashboard(self, result: Dict):
        """Push signal toi dashboard qua HTTP API"""
        try:
            import requests
            # Gui nguyen cau truc {signal: {...}, risk: {...}, ...}
            data = {
                "signal": result["signal"],
                "risk": result["risk"],
                "timestamp": result.get("timestamp", ""),
                "status": "active",
                "tp_hits": [],
            }
            requests.post(
                f"http://127.0.0.1:{settings.WEB_PORT}/api/add_signal",
                json=data, timeout=2
            )
        except Exception:
            pass

    def run_once(self):
        """Chay 1 lan"""
        self.load_pairs()
        signals = self.scan_all()
        self.process_signals(signals)
        self.save_signals()
        return signals


if __name__ == "__main__":
    scanner = ScannerV2()

    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        scanner.run_once()
    else:
        scanner.run()
