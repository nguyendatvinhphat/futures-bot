"""
CRYPTO FINDER BOT - CONFIGURATION
==================================
Lưu trữ API keys và cấu hình bot.

HƯỚNG DẪN:
1. Điền Telegram Bot Token: Tạo bot qua @BotFather trên Telegram
2. Điền Telegram Chat ID: Lấy từ @userinfobot hoặc @getmyid_bot
3. Điền Binance API Key/Secret: Tạo tại https://www.binance.com/en/my/settings/api-management
"""

# =============================================================
# TELEGRAM CONFIGURATION
# =============================================================
TELEGRAM_BOT_TOKEN = "8617534956:AAFM7OtWwy0YiBa3gZ9GGgYqEQCyWHKzRwc"
TELEGRAM_CHAT_ID = "1873677505"

# =============================================================
# BINANCE API CONFIGURATION
# =============================================================
# CHỈ CẦN API KEY/SECRET NẾU MUỐN XEM ACCOUNT INFO
# Nếu chỉ lấy data giá (public) thì KHÔNG cần API key
BINANCE_API_KEY = "t2jiyXZdguOHu6v2VB0DSkZVd6s2fvLpN0mK6EVv9gT4Qyb0TWpRi3V9vxTLnsuO"
BINANCE_API_SECRET = "5WOZPEJ3K7lijQxmiKVEfAwLcGuJ9Egc0zQlEW1LFnVeSfi8fPLZb8ZqfuJ8SS5L"

# =============================================================
# BOT SETTINGS
# =============================================================

# Scan interval (giây) - thời gian giữa các lần quét
SCAN_INTERVAL = 60  # 60 giây

# Số lượng coins tối đa quét cùng lúc
MAX_CONCURRENT_SCANS = 50

# Timeframes quét
TIMEFRAMES = {
    "scalping": {"htf": "15m", "mtf": "5m", "ltf": "1m"},
    "day_trading": {"htf": "4h", "mtf": "1h", "ltf": "15m"},
    "swing_trading": {"htf": "1d", "mtf": "4h", "ltf": "1h"},
}

# Minimum score để tạo signal (0-100)
MIN_SIGNAL_SCORE = 60

# =============================================================
# SIGNAL QUALITY FILTERS (bộ lọc chất lượng gửi Telegram)
# =============================================================

# Minimum score để GỬI TELEGRAM
MIN_SEND_SCORE = 65

# Yêu cầu multi-timeframe aligned (3 TF cùng hướng)
REQUIRE_MULTI_TF = False

# Minimum R:R ratio để gửi
MIN_RR_RATIO = 2.0

# Chỉ gửi nếu có ít nhất 1 confirmation mạnh
REQUIRE_STRONG_CONFIRMATION = False

# Minimum consensus % để gửi
MIN_CONSENSUS_PCT = 55

# Cooldown giữa 2 lần gửi cùng 1 signal (giây)
SIGNAL_COOLDOWN = 300  # 5 phút

# =============================================================
# RISK MANAGEMENT SETTINGS
# =============================================================
DEFAULT_ACCOUNT_SIZE = 10000  # Account size mặc định (USDT)
DEFAULT_RISK_PERCENT = 1.0    # Risk % mỗi trade (giảm từ 2.0 vì SL rộng hơn)

# Leverage tự động theo score (giảm bớt vì SL rộng hơn)
LEVERAGE_MAP = {
    "strong": {"min": 7, "max": 15},   # Score 80-100 (giảm từ 20)
    "medium": {"min": 5, "max": 10},   # Score 60-79
    "weak": {"min": 3, "max": 5},      # Score 40-59
}

# Risk % theo score (giảm bớt vì SL rộng hơn)
RISK_MAP = {
    "strong": 1.5,  # Score 80-100 (giảm từ 2.0)
    "medium": 1.0,  # Score 60-79 (giảm từ 1.5)
    "weak": 0.8,    # Score 40-59 (giảm từ 1.0)
}

# =============================================================
# INDICATOR SETTINGS
# =============================================================

# EMA
EMA_FAST = 9
EMA_MED = 21
EMA_SLOW = 50
EMA_TREND = 200

# RSI
RSI_PERIOD = 14
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30

# MACD
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

# Supertrend
ST_ATR_PERIOD = 10
ST_MULTIPLIER = 3.0

# ATR
ATR_PERIOD = 14
ATR_SL_MULTIPLIER = 2.5  # Tăng từ 1.5 -> 2.5 (SL rộng hơn, tránh bị hit ngay)

# ADX
ADX_PERIOD = 14
ADX_STRONG_THRESHOLD = 25

# Volume
VOL_SMA_PERIOD = 20
VOL_SPIKE_MULTIPLIER = 1.5

# Bollinger Bands
BB_PERIOD = 20
BB_STD = 2.0

# Pivot Points
PIVOT_LEFT = 10
PIVOT_RIGHT = 10

# =============================================================
# SIGNAL SCORING WEIGHTS (tổng = 100)
# =============================================================
SCORING_WEIGHTS = {
    "ema_cross": 15,          # EMA 9/21 crossover
    "rsi": 10,                # RSI condition
    "macd": 10,               # MACD histogram
    "volume": 10,             # Volume confirmation
    "supertrend": 10,         # Supertrend direction
    "adx": 10,                # ADX strength
    "vwap": 5,                # Price vs VWAP
    "structure": 10,          # BOS/CHoCH
    "order_block": 10,        # Order Block zone
    "fvg": 5,                 # Fair Value Gap
    "multi_tf": 5,            # Multi-timeframe confluence
}

# =============================================================
# WEB DASHBOARD SETTINGS
# =============================================================
WEB_HOST = "0.0.0.0"
WEB_PORT = 5000
WEB_DEBUG = False

# =============================================================
# DATABASE
# =============================================================
DB_PATH = "data/signals.db"

# =============================================================
# LOGGING
# =============================================================
LOG_LEVEL = "INFO"
LOG_FILE = "data/bot.log"
