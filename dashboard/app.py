"""
Web Dashboard - Hien thi tin hieu truc quan + Learning Stats
"""

import os
import sys
import json
import threading
import time

# Fix Unicode encoding for Windows console
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from datetime import datetime
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Default settings (fallback if config import fails)
WEB_HOST = "0.0.0.0"
WEB_PORT = 5000

try:
    from config import settings
    WEB_HOST = settings.WEB_HOST
    WEB_PORT = settings.WEB_PORT
except Exception as e:
    print(f"[Dashboard] Cannot import config: {e}")

app = Flask(__name__,
            template_folder="templates",
            static_folder="static")
app.config["SECRET_KEY"] = "crypto-finder-bot-secret"
socketio = SocketIO(app, cors_allowed_origins="*")

# Store signals in memory
signals_store = []

# Path to signals history file
HISTORY_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "signals_history.json")


def load_signals_from_file():
    """Load signals tu file JSON"""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                data = json.load(f)

            # Clear old data
            signals_store.clear()

            for item in data[-500:]:
                # Giu nguyen cau truc {signal: {...}, risk: {...}, ...}
                sig = item.get("signal", item)
                risk = item.get("risk", {})

                # Tao entry cho dashboard voi day du fields
                entry = {
                    "signal": {
                        "symbol": sig.get("symbol", ""),
                        "direction": sig.get("direction", ""),
                        "strength": sig.get("strength", "WEAK"),
                        "score": sig.get("score", 0),
                        "trade_type": sig.get("trade_type", ""),
                        "entry_price": sig.get("entry_price", risk.get("entry", 0)),
                        "confidence": sig.get("confidence", 0),
                        "rating": sig.get("rating", {"rank": sig.get("strength", "WEAK")}),
                        "regime": sig.get("regime", {}),
                        "leverage_info": sig.get("leverage_info", {}),
                        "multi_tf_aligned": sig.get("multi_tf_aligned", False),
                        "confluence_score": sig.get("confluence_score", 0),
                        "htf": sig.get("htf", {}),
                        "mtf": sig.get("mtf", {}),
                        "ltf": sig.get("ltf", {}),
                        "funding_rate": sig.get("funding_rate"),
                        "open_interest": sig.get("open_interest"),
                        "consensus_pct": sig.get("consensus_pct", 0),
                        "long_count": sig.get("long_count", 0),
                        "short_count": sig.get("short_count", 0),
                    },
                    "risk": {
                        "entry": risk.get("entry", sig.get("entry_price", 0)),
                        "sl": risk.get("sl", 0),
                        "sl_pct": risk.get("sl_pct", 0),
                        "tps": risk.get("tps", []),
                        "rr_ratio": risk.get("rr_ratio", 0),
                        "leverage": risk.get("leverage", 1),
                        "risk_pct": risk.get("risk_pct", 0),
                        "position": risk.get("position", {}),
                        "liquidation_price": risk.get("liquidation_price", 0),
                        "atr": risk.get("atr", 0),
                        "atr_pct": risk.get("atr_pct", 0),
                    },
                    "timestamp": item.get("timestamp", ""),
                    "status": item.get("status", "active"),
                    "tp_hits": item.get("tp_hits", []),
                }
                signals_store.append(entry)

            print(f"[Dashboard] Loaded {len(signals_store)} signals from history")
        else:
            print(f"[Dashboard] History file not found: {HISTORY_FILE}")
    except Exception as e:
        print(f"[Dashboard] Cannot load signals history: {e}")


def check_outcomes_in_store():
    """Kiem tra TP/SL hits cho cac signal active trong signals_store"""
    try:
        import requests as req
        resp = req.get("https://fapi.binance.com/fapi/v1/ticker/price", timeout=10)
        if resp.status_code != 200:
            return
        tickers = {t["symbol"]: float(t["price"]) for t in resp.json()}
    except Exception:
        return

    updated = False
    for entry in signals_store:
        status = entry.get("status", "active")
        if status not in ("active", None, "", "N/A"):
            continue

        sig = entry.get("signal", {})
        risk = entry.get("risk", {})
        symbol = sig.get("symbol", "")
        if symbol not in tickers:
            continue

        price = tickers[symbol]
        direction = sig.get("direction", "")
        sl = risk.get("sl", 0)
        tps = risk.get("tps", [])
        tp_prices = [tp.get("price", 0) if isinstance(tp, dict) else tp for tp in tps]

        # Check SL
        if sl > 0:
            if direction == "long" and price <= sl:
                entry["status"] = "sl_hit"
                updated = True
                continue
            elif direction == "short" and price >= sl:
                entry["status"] = "sl_hit"
                updated = True
                continue

        # Check TPs
        tp_hits = entry.get("tp_hits", [])
        for i, tp in enumerate(tp_prices):
            if tp > 0 and i not in tp_hits:
                if direction == "long" and price >= tp:
                    tp_hits.append(i)
                    updated = True
                elif direction == "short" and price <= tp:
                    tp_hits.append(i)
                    updated = True

        entry["tp_hits"] = tp_hits

        # Update status based on TP hits
        if entry.get("status") != "sl_hit":
            if len(tp_hits) >= 3:
                entry["status"] = "tp3_hit"
                updated = True
            elif len(tp_hits) >= 2:
                entry["status"] = "tp2_hit"
                updated = True
            elif len(tp_hits) >= 1:
                entry["status"] = "tp1_hit"
                updated = True
            else:
                entry["status"] = "active"

    # Save back to file if updated
    if updated:
        try:
            with open(HISTORY_FILE, "w") as f:
                json.dump(signals_store, f, indent=2, default=str)
            print(f"[Dashboard] Updated signal outcomes")
        except Exception:
            pass


def auto_refresh_loop():
    """Tu dong refresh signals tu file moi 30 giay + check outcomes"""
    while True:
        try:
            time.sleep(30)
            if os.path.exists(HISTORY_FILE):
                load_signals_from_file()
                check_outcomes_in_store()
        except Exception:
            pass


# Load signals on startup
load_signals_from_file()
check_outcomes_in_store()

# Start auto-refresh thread
refresh_thread = threading.Thread(target=auto_refresh_loop, daemon=True)
refresh_thread.start()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/stats")
def get_stats():
    """API lay thong ke tong hop"""
    if not signals_store:
        return jsonify({
            "total": 0, "strong": 0, "medium": 0, "weak": 0,
            "long_count": 0, "short_count": 0,
            "tp1_hits": 0, "tp2_hits": 0, "tp3_hits": 0, "sl_hits": 0,
            "tp_sl_ratio": 0, "win_rate": 0,
            "platinum": 0, "gold": 0, "silver": 0, "bronze": 0,
        })

    total = len(signals_store)
    long_count = len([s for s in signals_store if s.get("signal", {}).get("direction") == "long"])
    short_count = len([s for s in signals_store if s.get("signal", {}).get("direction") == "short"])

    # Rating counts
    platinum = len([s for s in signals_store if s.get("signal", {}).get("strength") == "PLATINUM"])
    gold = len([s for s in signals_store if s.get("signal", {}).get("strength") == "GOLD"])
    silver = len([s for s in signals_store if s.get("signal", {}).get("strength") == "SILVER"])
    bronze = len([s for s in signals_store if s.get("signal", {}).get("strength") == "BRONZE"])

    # TP/SL hits
    tp1_hits = 0
    tp2_hits = 0
    tp3_hits = 0
    sl_hits = 0

    for s in signals_store:
        status = s.get("status", "")
        tp_hits = s.get("tp_hits", [])

        if status == "sl_hit":
            sl_hits += 1
        if 0 in tp_hits or status == "tp1_hit":
            tp1_hits += 1
        if 1 in tp_hits or status == "tp2_hit":
            tp2_hits += 1
        if 2 in tp_hits or status == "tp3_hit":
            tp3_hits += 1

    # TP/SL ratio
    total_tp = tp1_hits + tp2_hits + tp3_hits
    tp_sl_ratio = round(total_tp / sl_hits, 2) if sl_hits > 0 else total_tp

    # Win rate
    resolved = sl_hits + tp1_hits
    win_rate = round(tp1_hits / resolved * 100, 1) if resolved > 0 else 0

    return jsonify({
        "total": total,
        "strong": platinum + gold,
        "medium": silver,
        "weak": bronze,
        "long_count": long_count,
        "short_count": short_count,
        "platinum": platinum,
        "gold": gold,
        "silver": silver,
        "bronze": bronze,
        "tp1_hits": tp1_hits,
        "tp2_hits": tp2_hits,
        "tp3_hits": tp3_hits,
        "sl_hits": sl_hits,
        "tp_sl_ratio": tp_sl_ratio,
        "win_rate": win_rate,
    })


@app.route("/api/signals")
def get_signals():
    """API lay tat ca signals"""
    limit = request.args.get("limit", 200, type=int)
    trade_type = request.args.get("type", "all")
    status_filter = request.args.get("status", "all")

    filtered = signals_store
    if trade_type != "all":
        filtered = [s for s in filtered if s.get("signal", {}).get("trade_type") == trade_type]
    if status_filter != "all":
        filtered = [s for s in filtered if s.get("status") == status_filter]

    return jsonify({
        "signals": filtered[-limit:],
        "total": len(filtered),
        "timestamp": datetime.utcnow().isoformat(),
    })


@app.route("/api/add_signal", methods=["POST"])
def add_signal():
    """API them signal moi (tu scanner)"""
    data = request.json
    if data:
        signals_store.append(data)
        # Keep only last 500 signals
        if len(signals_store) > 500:
            signals_store.pop(0)
        socketio.emit("new_signal", data)
    return jsonify({"status": "ok"})


def run_dashboard():
    """Chay dashboard server"""
    port = int(os.environ.get("PORT", WEB_PORT))
    print(f"Dashboard running at http://{WEB_HOST}:{port}")
    socketio.run(app, host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    run_dashboard()
