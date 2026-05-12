# Confluence Bot 2.1.0 - Crypto Futures Trading Dashboard

Real-time crypto futures signal scanner with multi-timeframe analysis and web dashboard.

## Features

- Multi-timeframe confluence analysis (HTF + MTF + LTF)
- 12+ technical indicators (EMA, RSI, MACD, Supertrend, ADX, SMC, etc.)
- Real-time signal scanning every 60 seconds
- Web dashboard with live updates
- Telegram notifications
- Paper trading simulation
- Risk management with dynamic SL/TP

## Quick Start

### Local
```bash
pip install -r requirements.txt
python main.py
```

### Online (Railway)
1. Fork this repo
2. Go to [railway.app](https://railway.app)
3. Deploy from GitHub repo
4. Get your permanent URL

## Commands

```bash
python main.py              # Scanner + Telegram
python main.py --dashboard  # Dashboard only
python main.py --all        # Scanner + Dashboard
python main.py --online     # Scanner + Dashboard + ngrok
```

## Telegram Commands

- `/help` - Show menu
- `/check SYMBOL [TF]` - Check a coin
- `/scan [N]` - Scan top N coins
- `/regime SYMBOL` - Market regime
- `/indicators SYMBOL` - View indicators
- `/status` - Bot status

## Dashboard

Access at: `http://localhost:5000` or your Railway URL

## Tech Stack

- Python 3.11+
- Flask + SocketIO
- Binance Futures API
- Pandas + NumPy
- Telegram Bot API
