# -*- coding: utf-8 -*-
import time
import requests
import json

# =====================================================================
# ИНФРАСТРУКТУРНЫЕ НАСТРОЕКИ (ДЛЯ СЕРВЕРА В ЕВРОПЕ ПРОКСИ НЕ НУЖНЫ)
# =====================================================================
CLOB_API_URL = "https://polymarket.com"

# МАТРИЦА УТВЕРЖДЕННЫХ НАСТРОЕК СТРАТЕГИЙ ПО МОНЕТАМ
CONFIG_MATRIX = {
    "BTC":  {"mode": "50/30", "entry_price": 0.50, "trigger_price": 0.30},
    "ETH":  {"mode": "DYNAMIC", "entry_price": 0.50, "trigger_price": 0.30},
    "SOL":  {"mode": "DYNAMIC", "entry_price": 0.50, "trigger_price": 0.30},
    "XRP":  {"mode": "30/30", "entry_price": 0.30, "trigger_price": 0.30},
    "SUI":  {"mode": "30/30", "entry_price": 0.30, "trigger_price": 0.30},
    "NEAR": {"mode": "30/30", "entry_price": 0.30, "trigger_price": 0.30}
}

# МАНI-МЕНЕДЖМЕНТ И РИСК-ФИЛЬТРЫ ИЗ ВАШЕГО ТЗ
TEST_POOL_LIMIT = 5          # Максимум 5 одновременных событий
LOT_SIZE_USD = 1.08          # Жесткий лот 1.08 USDT на одну сделку

active_positions = {}

def get_market_volume_and_price(market_slug):
    """Прямой высокоскоростной запрос цен из Polymarket Gamma API"""
    try:
        # Ссылка со слэшем и правильным техническим доменом из документации
        url = f"{CLOB_API_URL}/markets/{market_slug}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(url, headers=headers, timeout=10).json()
        
        # Безопасно вытаскиваем массив актуальных цен в центах
        if "outcomePrices" in response:
            prices_list = response["outcomePrices"]
            
            yes_price = float(prices_list[0])  # Акция ДА
            no_price = float(prices_list[1])   # Акция НЕТ
            return yes_price, no_price, True
        else:
            return None, None, False
            
    except Exception as e:
        print(f"[ЖИВОЙ РАДАР СБОЙ] Ошибка получения данных: {e}")
        return None, None, False

def execute_blockchain_order(market_slug, outcome, amount):
    """Бумажная симуляция отправки ордера в сеть Polygon"""
    print(f"🔥  [БЛОКЧЕЙН] Симуляция ордера: {outcome.upper()} на сумму {amount}$")
    return True

print("=== Универсальный БУМАЖНЫЙ бот запущен напрямую в ЕВРОПЕ ===")
print(f"Режим: Тест без денег. Мониторинг живых стаканов. Лимит: {TEST_POOL_LIMIT} рынков.")

# Список активных живых контрактов Polymarket на сегодня
REAL_MARKETS = {
    "BTC": "bitcoin-above-85000-september-23",
    "ETH": "ethereum-above-26000-september-23",
    "SOL": "solana-above-14000-september-23",
    "XRP": "xrp-above-150-september-23"
}

while True:
    for ticker, market_id in REAL_MARKETS.items():
        if len(active_positions) >= TEST_POOL_LIMIT:
            break
            
        settings = CONFIG_MATRIX.get(ticker, {"mode": "30/30", "entry_price": 0.30, "trigger_price": 0.30})
        yes_p, no_p, vol_fade = get_market_volume_and_price(market_id)
        
        if yes_p and no_p:
            print(f"[ЖИВОЙ РАДАР] {ticker} | Цена ДА: {yes_p}$ | Цена НЕТ: {no_p}$")
            
            # Логика дельта-нейтральной стратегии 30/30
            if settings["mode"] == "30/30" and market_id not in active_positions:
                if yes_p <= settings["entry_price"] and vol_fade:
                    print(f"\n⚡ [СИГНАЛ 30/30] {ticker} коснулся дна! Цена: {yes_p}$")
                    if execute_blockchain_order(market_id, "yes", LOT_SIZE_USD):
                        active_positions[market_id] = {"stage": "FIRST_LEG_BOUGHT", "entry": yes_p}
            
            elif market_id in active_positions and active_positions[market_id]["stage"] == "FIRST_LEG_BOUGHT":
                if no_p <= settings["trigger_price"]:
                    print(f"\n🔒 [ЗАМОК] Вторая нога по {ticker} упала до {no_p}$. Хеджируем прибыль!")
                    if execute_blockchain_order(market_id, "no", LOT_SIZE_USD):
                        active_positions[market_id]["stage"] = "LOCKED_PROFIT"
                        print(f"[УСПЕХ] +66.6% успешно заперты в симуляторе.\n")

    time.sleep(5)  # Интервал опроса стаканов
