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
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        
        response = requests.get(url, headers=headers, timeout=10, verify=False).json()
        
        # Если API вернуло ошибку или рынок не найден
        if "error" in response or "detail" in response:
            print(f"[РАДАР ПРЕДУПРЕЖДЕНИЕ] API вернуло ошибку для {market_slug}: {response}")
            return None, None, False
            
        if "outcomePrices" in response:
            prices_list = response["outcomePrices"]  # Получаем массив строк типа ["0.52", "0.48"]
            
            # Извлекаем первый элемент как цену ДА, второй — как цену НЕТ
            yes_price = float(prices_list[0]) if len(prices_list) > 0 else 0.5
            no_price = float(prices_list[1]) if len(prices_list) > 1 else 0.5
            return yes_price, no_price, True
        else:
            print(f"[РАДАР ПРЕДУПРЕЖДЕНИЕ] В ответе API нет поля outcomePrices для {market_slug}")
            return None, None, False
            
    except Exception as e:
        # Теперь бот обязан громко доложить в консоль, если что-то пойдет не так
        print(f"[ЖИВОЙ РАДАР КРИТ] Внутренний сбой парсинга для {market_slug}: {e}")
            
        if "outcomePrices" in response:
            prices_list = response["outcomePrices"]  # Получаем массив строк типа ["0.52", "0.48"]
            
            # Извлекаем первый элемент как цену ДА, второй — как цену НЕТ
            yes_price = float(prices_list[0]) if len(prices_list) > 0 else 0.5
            no_price = float(prices_list[1]) if len(prices_list) > 1 else 0.5
            return yes_price, no_price, True
        else:
            print(f"[РАДАР ПРЕДУПРЕЖДЕНИЕ] В ответе API нет поля outcomePrices для {market_slug}")
            return None, None, False
            
    except Exception as e:
        # Теперь бот обязан громко доложить в консоль, если что-то пойдет не так
        print(f"[ЖИВОЙ РАДАР КРИТ] Внутренний сбой парсинга для {market_slug}: {e}")
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
