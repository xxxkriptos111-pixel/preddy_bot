# -*- coding: utf-8 -*-
import time
import requests
import json
import threading
from flask import Flask

# =====================================================================
# МИНИ-СЕРВЕР ДЛЯ ОБМАНА ПРОВЕРКИ ПОРТОВ RENDER (БЕСПЛАТНЫЙ ТАРИФ)
# =====================================================================
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive"

def run_web_server():
    import os
    # Render автоматически выдает порт в переменную окружения, слушаем его
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# Запускаем веб-сервер в параллельном потоке, чтобы он не мешал боту
threading.Thread(target=run_web_server, daemon=True).start()

# =====================================================================
# НАСТРОЙКИ СТРАТЕГИИ И ПОДКЛЮЧЕНИЯ К API
# =====================================================================
CLOB_API_URL = "https://polymarket.com"

CONFIG_MATRIX = {
    "BTC":  {"mode": "50/30", "entry_price": 0.50, "trigger_price": 0.30},
    "ETH":  {"mode": "DYNAMIC", "entry_price": 0.50, "trigger_price": 0.30},
    "SOL":  {"mode": "DYNAMIC", "entry_price": 0.50, "trigger_price": 0.30},
    "XRP":  {"mode": "30/30", "entry_price": 0.30, "trigger_price": 0.30}
}

TEST_POOL_LIMIT = 5          
LOT_SIZE_USD = 1.08          
active_positions = {}

def get_market_volume_and_price(market_slug):
    try:
        url = f"{CLOB_API_URL}/markets/{market_slug}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10).json()
        
        if "outcomePrices" in response:
            prices_list = response["outcomePrices"]
            yes_price = float(prices_list)
            no_price = float(prices_list)
            return yes_price, no_price, True
        return None, None, False
    except Exception:
        return None, None, False

print("=== Универсальный БУМАЖНЫЙ бот запущен напрямую в ЕВРОПЕ ===")

REAL_MARKETS = {
    "BTC": "will-bitcoin-hit-100k-in-2026",
    "ETH": "will-ethereum-hit-4k-in-2026",
    "SOL": "will-solana-hit-250-in-2026",
    "XRP": "will-xrp-hit-1-in-2026"
}

while True:
    for ticker, market_id in REAL_MARKETS.items():
        yes_p, no_p, vol_fade = get_market_volume_and_price(market_id)
        if yes_p and no_p:
            print(f"[ЖИВОЙ РАДАР] {ticker} | Цена ДА: {yes_p}$ | Цена НЕТ: {no_p}$")
            # Принудительно выталкиваем принты в консоль Render каждую секунду
            import sys
            sys.stdout.flush()
    time.sleep(5)
