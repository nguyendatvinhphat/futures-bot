"""
Run Dashboard + Scanner together for Railway deployment
Dashboard runs in main thread, Scanner runs in background thread
"""

import os
import sys
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Fix Unicode encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass


def run_scanner_thread():
    """Run scanner in background thread"""
    print("[Scanner] Starting scanner in background...")
    try:
        from scanner_v2 import ScannerV2
        scanner = ScannerV2()
        scanner.run()
    except Exception as e:
        print(f"[Scanner] Error: {e}")
        import traceback
        traceback.print_exc()


def main():
    print("=" * 50)
    print("  CONFLUENCE BOT 2.1.0 - Railway Edition")
    print("  Dashboard + Scanner")
    print("=" * 50)

    # Start scanner in background thread
    scanner_thread = threading.Thread(target=run_scanner_thread, daemon=True)
    scanner_thread.start()
    print("[Main] Scanner started in background")

    # Run dashboard in main thread
    print("[Main] Starting dashboard...")
    from dashboard.app import run_dashboard
    run_dashboard()


if __name__ == "__main__":
    main()
