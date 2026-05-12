"""
Quick Test v2 - Kiểm tra bot nâng cao
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ["PYTHONIOENCODING"] = "utf-8"

def test_advanced_indicators():
    """Test advanced indicators"""
    print("1. Testing Advanced Indicators...")
    from data.binance_fetcher import fetcher
    from indicators.advanced import (
        calculate_stochastic, get_stochastic_signal,
        get_fibonacci_signal, detect_candlestick_patterns,
        detect_market_regime
    )

    df = fetcher.get_klines("BTCUSDT", "1h", limit=300)
    if df is None:
        print("   ❌ No data")
        return False

    try:
        df = calculate_stochastic(df)
        stoch = get_stochastic_signal(df)
        print(f"   ✅ Stochastic: K={stoch['data']['k']:.1f}% D={stoch['data']['d']:.1f}%")

        fib = get_fibonacci_signal(df)
        print(f"   ✅ Fibonacci: nearest={fib['data']['nearest_level']}")

        cs = detect_candlestick_patterns(df)
        print(f"   ✅ Candlestick: {cs['detail']}")

        regime = detect_market_regime(df)
        print(f"   ✅ Market Regime: {regime['detail']}")

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

    return True


def test_signal_engine_v2():
    """Test signal engine v2"""
    print("\n2. Testing Signal Engine v2...")
    from data.binance_fetcher import fetcher
    from signals.signal_engine_v2 import signal_engine_v2

    htf_df = fetcher.get_klines("BTCUSDT", "4h", limit=300)
    mtf_df = fetcher.get_klines("BTCUSDT", "1h", limit=300)
    ltf_df = fetcher.get_klines("BTCUSDT", "15m", limit=300)

    if htf_df is None or mtf_df is None or ltf_df is None:
        print("   ❌ No data")
        return False

    signal = signal_engine_v2.generate_signal("BTCUSDT", htf_df, mtf_df, ltf_df, "day_trading")

    if signal:
        print(f"   ✅ Signal: {signal['strength']} {signal['direction'].upper()}")
        print(f"      Score: {signal['score']}/100")
        print(f"      Confidence: {signal['confidence']}%")
        print(f"      Regime: {signal['regime']['label']}")
        print(f"      Leverage: {signal['leverage_info']['leverage']}x ({signal['leverage_info']['risk_label']})")
        print(f"      RSI: {signal['ltf']['rsi']:.1f}")
        print(f"      ADX: {signal['ltf']['adx']:.1f}")
        print(f"      Stoch: K={signal['ltf']['stoch']['k']:.1f}% D={signal['ltf']['stoch']['d']:.1f}%")
        print(f"      Candle: {signal['ltf']['candlestick']}")
        print(f"      Fib: {signal['ltf']['fib']['nearest_level']}")
    else:
        print("   ⚠️ No signal (score below threshold)")

    return True


def test_rating():
    """Test signal rating"""
    print("\n3. Testing Signal Rating...")
    from signals.rating import signal_rating

    tests = [95, 85, 70, 55, 40]
    for score in tests:
        rating = signal_rating.get_rating(score)
        confidence = signal_rating.get_confidence(score)
        lev = signal_rating.get_leverage_suggestion(score, 1.5)
        print(f"   Score {score}: {rating['rank']} {rating['emoji']} | Conf: {confidence}% | Lev: {lev['leverage']}x ({lev['risk_label']})")

    return True


def test_paper_trading():
    """Test paper trading"""
    print("\n4. Testing Paper Trading...")
    from signals.paper_trading import paper_trader

    stats = paper_trader.get_stats()
    print(f"   ✅ Capital: ${stats['current_capital']:.2f}")
    print(f"   ✅ Total PnL: ${stats['total_pnl']:.2f} ({stats['pnl_pct']:.1f}%)")
    print(f"   ✅ Trades: {stats['total_trades']} (Win: {stats['winning_trades']}, Loss: {stats['losing_trades']})")
    print(f"   ✅ Win Rate: {stats['win_rate']}%")

    return True


def test_telegram_format():
    """Test telegram format"""
    print("\n5. Testing Telegram Format...")
    from notifications.telegram_bot_v2 import telegram_bot_v2

    # Test help
    help_text = telegram_bot_v2.format_help()
    print(f"   ✅ Help: {len(help_text)} chars")

    # Test presets
    presets = telegram_bot_v2.format_presets()
    print(f"   ✅ Presets: {len(presets)} chars")

    return True


if __name__ == "__main__":
    print("=" * 50)
    print("🤖 CRYPTO FINDER BOT v2.1.0 - QUICK TEST")
    print("=" * 50)

    results = []
    results.append(("Advanced Indicators", test_advanced_indicators()))
    results.append(("Signal Engine v2", test_signal_engine_v2()))
    results.append(("Rating System", test_rating()))
    results.append(("Paper Trading", test_paper_trading()))
    results.append(("Telegram Format", test_telegram_format()))

    print("\n" + "=" * 50)
    print("RESULTS:")
    print("=" * 50)
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} | {name}")

    all_pass = all(r for _, r in results)
    print(f"\n{'✅ ALL TESTS PASSED!' if all_pass else '❌ SOME TESTS FAILED'}")
