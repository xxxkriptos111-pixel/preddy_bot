settings = CONFIG_MATRIX.get(ticker, {"mode": "30/30", "entry_price": 0.30, "trigger_price": 0.30})
        yes_p, no_p, vol_fade = get_market_volume_and_price(market_id)
        
        if yes_p and no_p:
            print(f"[ЖИВОЙ РАДАР] {ticker} | Цена ДА: {yes_p}$ | Цена НЕТ: {no_p}$ | Прошло раунда: {round(passed_pct, 1)}% | Баланс: {round(current_balance, 2)} USDT | Текущий лот: {dynamic_lot_size}$")
            
            if settings["mode"] == "30/30" and market_id not in active_positions:
                # ВНЕДРЯЕМ УТВЕРЖДЕННЫЙ ФИЛЬТР ВРЕМЕНИ: Если прошло больше 65% раунда, вход ЗАПРЕЩЕН!
                if passed_pct >= 65.0:
                    continue
                    
                if yes_p <= settings["entry_price"] and vol_fade:
                    print(f"\n⚡ [СИГНАЛ 30/30] {ticker} коснулся реального дна! Цена: {yes_p}$")
                    if execute_blockchain_order(market_id, "yes", dynamic_lot_size):
                        active_positions[market_id] = {"stage": "FIRST_LEG_BOUGHT", "entry": yes_p, "lot_size": dynamic_lot_size}
            
            elif market_id in active_positions and active_positions[market_id]["stage"] == "FIRST_LEG_BOUGHT":
                if no_p <= settings["trigger_price"]:
                    print(f"\n🔒 [ЗАМОК] Вторая нога по {ticker} упала до {no_p}$. Хеджируем прибыль!")
                    if execute_blockchain_order(market_id, "no", active_positions[market_id]["lot_size"]):
                        active_positions[market_id]["stage"] = "LOCKED_PROFIT"
                        print(f"[УСПЕХ] Рост баланса зафиксирован в симуляторе сложного процента.\n")

        sys.stdout.flush()
    time.sleep(5)
