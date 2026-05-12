"""
Crypto Finder Bot v2 - Main Entry Point
=========================================

CÁCH SỬ DỤNG:

1. Cài đặt dependencies:
   pip install -r requirements.txt

2. Cấu hình API trong config/settings.py:
   - TELEGRAM_BOT_TOKEN
   - TELEGRAM_CHAT_ID
   - (Optional) BINANCE_API_KEY, BINANCE_API_SECRET

3. Chạy bot:
   python main.py              # Chạy scanner + Telegram commands
   python main.py --once       # Chạy 1 lần rồi dừng
   python main.py --dashboard  # Chạy web dashboard
   python main.py --all        # Chạy cả scanner + dashboard
   python main.py --online     # Chạy scanner + dashboard + ngrok (public URL)
   python main.py --test       # Chạy test

4. Telegram Commands:
   /help       - Hiển thị menu
   /check SYMBOL [TF]  - Check 1 coin
   /scan [N]   - Quét top N coins
   /regime SYMBOL  - Xem chế độ thị trường
   /indicators SYMBOL  - Xem indicators
   /pnl        - Xem PnL paper trading
   /status     - Trạng thái bot
   /pause      - Tạm dừng
   /resume     - Tiếp tục
"""

import sys
import os
import threading

# Fix Unicode encoding for Windows console
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import settings


def run_scanner():
    """Chạy signal scanner v2"""
    from scanner_v2 import ScannerV2
    scanner = ScannerV2()
    scanner.run()


def run_scanner_once():
    """Chạy scanner 1 lần"""
    from scanner_v2 import ScannerV2
    scanner = ScannerV2()
    return scanner.run_once()


def run_dashboard():
    """Chạy web dashboard"""
    from dashboard.app import run_dashboard
    run_dashboard()


def run_all():
    """Chạy cả scanner + dashboard"""
    dashboard_thread = threading.Thread(target=run_dashboard, daemon=True)
    dashboard_thread.start()
    run_scanner()


def run_online():
    """Chạy scanner + dashboard + ngrok (public URL)"""
    import subprocess
    import time

    # Start dashboard in background thread
    dashboard_thread = threading.Thread(target=run_dashboard, daemon=True)
    dashboard_thread.start()

    # Wait for dashboard to start
    print("Waiting for dashboard to start...")
    time.sleep(3)

    # Start ngrok
    print("=" * 50)
    print("  NGROK PUBLIC URL:")
    print("  (Link will appear below)")
    print("=" * 50)

    try:
        subprocess.run(["ngrok", "http", str(settings.WEB_PORT)])
    except KeyboardInterrupt:
        print("\nngrok stopped.")
    except FileNotFoundError:
        print("\nngrok not found! Install: winget install ngrok.ngrok")
        print("Or run manually: ngrok http 5000")


def run_test():
    """Chạy test"""
    os.system("python test_bot.py")


def main():
    print("=" * 50)
    print("  CRYPTO FINDER BOT v2.1.0")
    print("  Confluence Multi-Timeframe Scanner")
    print("=" * 50)

    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()

        if arg == "--once":
            print("Running scanner once...")
            signals = run_scanner_once()
            print(f"\nDone! Found {len(signals)} signals.")

        elif arg == "--dashboard":
            print("Starting dashboard only...")
            run_dashboard()

        elif arg == "--all":
            print("Starting scanner + dashboard...")
            run_all()

        elif arg == "--online":
            print("Starting scanner + dashboard + ngrok...")
            run_online()

        elif arg == "--test":
            run_test()

        elif arg == "--help":
            print(__doc__)

        else:
            print(f"Unknown argument: {arg}")
            print("Use --help for usage instructions")
    else:
        print("Starting scanner with Telegram commands...")
        print("Use /help in Telegram for commands")
        run_scanner()


if __name__ == "__main__":
    main()
