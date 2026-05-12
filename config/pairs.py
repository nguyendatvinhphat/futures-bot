"""
Danh sách USDT pairs trên Binance Futures
Tự động cập nhật từ API hoặc dùng danh sách mặc định
"""

# Top pairs theo volume - luôn được scan
TOP_PAIRS = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT",
    "DOGEUSDT", "ADAUSDT", "AVAXUSDT", "DOTUSDT", "LINKUSDT",
    "MATICUSDT", "LTCUSDT", "UNIUSDT", "ATOMUSDT", "ETCUSDT",
    "NEARUSDT", "APTUSDT", "ARBUSDT", "OPUSDT", "FILUSDT",
]

# Blacklist - không scan các pair này
BLACKLIST = [
    "BUSDUSDT", "USDCUSDT", "TUSDUSDT", "FDUSDUSDT",  # Stablecoins
    "EURUSDT", "GBPUSDT", "AUDUSDT", "BRLUSDT",        # Fiat
]

def get_all_usdt_pairs():
    """Lấy tất cả USDT pairs từ Binance API"""
    try:
        import requests
        resp = requests.get("https://fapi.binance.com/fapi/v1/exchangeInfo", timeout=10)
        data = resp.json()
        pairs = []
        for s in data["symbols"]:
            if (s["quoteAsset"] == "USDT" and 
                s["status"] == "TRADING" and
                s["symbol"] not in BLACKLIST):
                pairs.append(s["symbol"])
        return pairs
    except Exception as e:
        print(f"Error fetching pairs: {e}, using TOP_PAIRS")
        return TOP_PAIRS
