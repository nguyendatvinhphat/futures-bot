import sys, os
sys.path.insert(0, 'C:\\Users\\COHOTECH.VN\\OneDrive\\Desktop\\futures_bot')
os.chdir('C:\\Users\\COHOTECH.VN\\OneDrive\\Desktop\\futures_bot')

from data.binance_fetcher import fetcher
from signals.signal_engine_v2 import signal_engine_v2
from signals.risk_manager import risk_manager
from notifications.telegram_bot_v2 import telegram_bot_v2

# Test one signal
print('Testing BTCUSDT signal...')
htf = fetcher.get_klines('BTCUSDT', '4h', 300)
mtf = fetcher.get_klines('BTCUSDT', '1h', 300)
ltf = fetcher.get_klines('BTCUSDT', '15m', 300)

if htf is not None and mtf is not None and ltf is not None:
    signal = signal_engine_v2.generate_signal('BTCUSDT', htf, mtf, ltf, 'day_trading')
    if signal:
        risk = risk_manager.get_risk_reward_info(signal)
        print(f'Signal: {signal["strength"]} {signal["direction"].upper()}')
        print(f'Score: {signal["score"]}/100')
        print(f'Entry: {risk["entry"]}')
        print(f'SL: {risk["sl"]}')
        print(f'Confidence: {signal["confidence"]}%')
        
        # Send to Telegram
        msg = telegram_bot_v2.format_confluence_signal(signal, risk)
        print(f'Telegram message length: {len(msg)} chars')
        
        # Try to send
        result = telegram_bot_v2.send_message(msg)
        print(f'Telegram send: {"Success" if result else "Failed"}')
    else:
        print('No signal (below threshold)')
else:
    print('Failed to get data')
