"""
Quick Test - Kiểm tra bot hoạt động
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_binance_connection():
    """Test kết nối Binance API"""
    print("1. Testing Binance API connection...")
    from data.binance_fetcher import fetcher

    # Test get price
    price = fetcher.get_ticker_price("BTCUSDT")
    if price:
        print(f"   ✅ BTC Price: ${price:,.2f}")
    else:
        print("   ❌ Failed to get BTC price")
        return False

    # Test get klines
    df = fetcher.get_klines("BTCUSDT", "1h", limit=100)
    if df is not None and len(df) > 0:
        print(f"   ✅ Got {len(df)} candles for BTCUSDT 1H")
    else:
        print("   ❌ Failed to get klines")
        return False

    return True


def test_indicators():
    """Test indicators"""
    print("\n2. Testing Indicators...")
    from data.binance_fetcher import fetcher
    from indicators import (
        calculate_ema, calculate_rsi, calculate_macd,
        calculate_supertrend, calculate_adx, calculate_vwap,
        calculate_atr, calculate_bollinger_bands
    )

    df = fetcher.get_klines("BTCUSDT", "1h", limit=300)
    if df is None:
        print("   ❌ No data to test")
        return False

    # Test each indicator
    try:
        df = calculate_ema(df)
        print(f"   ✅ EMA: 9={df.iloc[-1]['ema_9']:.2f}, 21={df.iloc[-1]['ema_21']:.2f}")

        df = calculate_rsi(df)
        print(f"   ✅ RSI: {df.iloc[-1]['rsi']:.2f}")

        df = calculate_macd(df)
        print(f"   ✅ MACD: {df.iloc[-1]['macd_line']:.4f}")

        df = calculate_supertrend(df)
        print(f"   ✅ Supertrend: direction={df.iloc[-1]['st_direction']}")

        df = calculate_adx(df)
        print(f"   ✅ ADX: {df.iloc[-1]['adx']:.2f}")

        df = calculate_vwap(df)
        print(f"   ✅ VWAP: {df.iloc[-1]['vwap']:.2f}")

        df = calculate_atr(df)
        print(f"   ✅ ATR: {df.iloc[-1]['atr']:.2f}")

        df = calculate_bollinger_bands(df)
        print(f"   ✅ BB: upper={df.iloc[-1]['bb_upper']:.2f}, lower={df.iloc[-1]['bb_lower']:.2f}")

    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

    return True


def test_signal_engine():
    """Test signal engine"""
    print("\n3. Testing Signal Engine...")
    from data.binance_fetcher import fetcher
    from signals.signal_engine import signal_engine

    # Get multi-timeframe data
    htf_df = fetcher.get_klines("BTCUSDT", "4h", limit=300)
    mtf_df = fetcher.get_klines("BTCUSDT", "1h", limit=300)
    ltf_df = fetcher.get_klines("BTCUSDT", "15m", limit=300)

    if htf_df is None or mtf_df is None or ltf_df is None:
        print("   ❌ Failed to get multi-tf data")
        return False

    signal = signal_engine.generate_signal("BTCUSDT", htf_df, mtf_df, ltf_df, "day_trading")

    if signal:
        print(f"   ✅ Signal generated: {signal['strength']} {signal['direction'].upper()}")
        print(f"      Score: {signal['score']}/100")
        print(f"      Entry: ${signal['entry_price']:,.2f}")
    else:
        print("   ⚠️ No signal (score below threshold - normal)")

    return True


def test_risk_manager():
    """Test risk manager"""
    print("\n4. Testing Risk Manager...")
    from signals.risk_manager import risk_manager

    # Test with sample data
    test_signal = {
        "entry_price": 50000,
        "direction": "long",
        "atr": 500,
        "score": 75,
    }

    risk_info = risk_manager.get_risk_reward_info(test_signal)

    print(f"   ✅ Entry: ${risk_info['entry']:,.2f}")
    print(f"   ✅ SL: ${risk_info['sl']:,.2f} ({risk_info['sl_pct']}%)")
    print(f"   ✅ Leverage: {risk_info['leverage']}x")
    print(f"   ✅ Liquidation: ${risk_info['liquidation_price']:,.2f}")
    print(f"   ✅ R:R Ratio: 1:{risk_info['rr_ratio']}")
    for tp in risk_info["tps"]:
        print(f"      TP{tp['level']}: ${tp['price']:,.2f} (1:{tp['rr_ratio']})")

    return True


def test_pairs():
    """Test getting pairs"""
    print("\n5. Testing Pairs...")
    from config.pairs import get_all_usdt_pairs

    pairs = get_all_usdt_pairs()
    print(f"   ✅ Found {len(pairs)} USDT pairs")
    print(f"   First 10: {pairs[:10]}")

    return True


if __name__ == "__main__":
    print("=" * 50)
    print("🤖 CRYPTO FINDER BOT - QUICK TEST")
    print("=" * 50)

    results = []
    results.append(("Binance API", test_binance_connection()))
    results.append(("Indicators", test_indicators()))
    results.append(("Signal Engine", test_signal_engine()))
    results.append(("Risk Manager", test_risk_manager()))
    results.append(("Pairs", test_pairs()))

    print("\n" + "=" * 50)
    print("RESULTS:")
    print("=" * 50)
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} | {name}")

    all_pass = all(r for _, r in results)
    print(f"\n{'✅ ALL TESTS PASSED!' if all_pass else '❌ SOME TESTS FAILED'}")
