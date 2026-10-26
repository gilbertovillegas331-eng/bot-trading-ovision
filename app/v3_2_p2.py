codigo = '''
def gestionar_trailing_y_parciales():
    posiciones = mt5.positions_get()
    if posiciones is None or len(posiciones) == 0: return
    for pos in posiciones:
        distancia_tp = abs(pos.tp - pos.price_open)
        distancia_actual = abs(pos.price_current - pos.price_open)
        if distancia_tp == 0: continue
        porcentaje_avance = distancia_actual / distancia_tp
        
        if porcentaje_avance >= 0.5 and pos.comment != "Parcial":
            lote_parcial = round(pos.volume / 2, 2)
            if lote_parcial >= mt5.symbol_info(pos.symbol).volume_min:
                tipo = mt5.ORDER_TYPE_SELL if pos.type == mt5.POSITION_TYPE_BUY else mt5.ORDER_TYPE_BUY
                precio = mt5.symbol_info_tick(pos.symbol).bid if pos.type == mt5.POSITION_TYPE_BUY else mt5.symbol_info_tick(pos.symbol).ask
                req = {"action": mt5.TRADE_ACTION_DEAL, "position": pos.ticket, "symbol": pos.symbol,
                       "volume": lote_parcial, "type": tipo, "price": precio, "deviation": 20,
                       "magic": 123456, "comment": "Parcial", "type_time": mt5.ORDER_TIME_GTC,
                       "type_filling": mt5.ORDER_FILLING_IOC}
                mt5.order_send(req)
                enviar_telegram(f"✂️ COBRO PARCIAL: {pos.symbol} (50% asegurado)")
        
        if porcentaje_avance >= 0.5:
            if pos.type == mt5.POSITION_TYPE_BUY:
                nuevo_sl = pos.price_open + (distancia_tp * (porcentaje_avance - 0.1))
                if pos.sl < nuevo_sl:
                    mt5.order_send({"action": mt5.TRADE_ACTION_SLTP, "position": pos.ticket, "symbol": pos.symbol, "sl": nuevo_sl, "tp": pos.tp})
            elif pos.type == mt5.POSITION_TYPE_SELL:
                nuevo_sl = pos.price_open - (distancia_tp * (porcentaje_avance - 0.1))
                if pos.sl > nuevo_sl or pos.sl == 0:
                    mt5.order_send({"action": mt5.TRADE_ACTION_SLTP, "position": pos.ticket, "symbol": pos.symbol, "sl": nuevo_sl, "tp": pos.tp})
'''
with open("app/main.py", "a", encoding="utf-8") as f:
    f.write(codigo)
print("✅ Parte 2A guardada.")
codigo = '''
def ejecutar_orden(signal, balance_dia):
    lotaje = calcular_lotaje(signal.symbol, signal.entry_price, signal.stop_loss, balance_dia)
    tick = mt5.symbol_info_tick(signal.symbol)
    if tick is None: return False
    precio = tick.ask if signal.direction == "LONG" else tick.bid
    request = {
        "action": mt5.TRADE_ACTION_DEAL, "symbol": signal.symbol, "volume": lotaje,
        "type": mt5.ORDER_TYPE_BUY if signal.direction == "LONG" else mt5.ORDER_TYPE_SELL,
        "price": precio, "sl": signal.stop_loss, "tp": signal.take_profit,
        "deviation": 20, "magic": 123456, "comment": "Ovision",
        "type_time": mt5.ORDER_TIME_GTC, "type_filling": mt5.ORDER_FILLING_IOC,
    }
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"❌ Error en {signal.symbol}: {result.comment}")
        return False
    print(f"✅ ORDEN ABIERTA: {signal.direction} {signal.symbol} | Lotes: {lotaje}")
    return True

def run_ovision(balance_dia):
    if not mt5.initialize(): return False
    print(f"\\n[{pd.Timestamp.now().strftime('%H:%M:%S')}] 🔎 Escaneando...")
    
    todos_los_simbolos = mt5.symbols_get()
    activos = [s.name for s in todos_los_simbolos if any(x in s.name.upper() for x in ["EURUSD", "XAUUSD", " C ", " B ", "STEP", "BULL", "BEAR"])]
    operaciones_esta_ronda = 0

    for sym in activos:
        pos_mt5 = mt5.positions_get()
        pos_actuales = len(pos_mt5) if pos_mt5 else 0
        if (pos_actuales + operaciones_esta_ronda) >= 3: 
            print("🛑 Límite de 3 operaciones alcanzado.")
            break 
        if mt5.positions_get(symbol=sym) is not None and len(mt5.positions_get(symbol=sym)) > 0: continue 
            
        df_htf = get_mt5_data(sym, TF_HTF)
        df_ltf = get_mt5_data(sym, TF_LTF)
        if df_htf is None or df_ltf is None: continue
            
        engine = ConfluenceEngine(df_htf, df_ltf, sym)
        signal = engine.analyze()
        
        if signal:
            tarjeta = signal.build_explanation()
            print(tarjeta)
            if (pos_actuales + operaciones_esta_ronda) < 3:
                enviar_telegram(tarjeta)
                if ejecutar_orden(signal, balance_dia):
                    enviar_telegram(f"🚀 ¡Orden Ejecutada! {signal.direction} {sym}")
                    operaciones_esta_ronda += 1
                    time.sleep(2)
            else:
                enviar_telegram(tarjeta + "\\n\\n⚠️ SEÑAL NO EJECUTADA: Límite alcanzado.")

if name == "main":
    print("🚀 Ovision V3.2 (Francotirador) encendido...")
    mt5.initialize()
    acc = mt5.account_info()
    balance_inicio_dia = acc.balance if acc else 1000
    ultimo_escaneo = 0
    
    while True:
        try:
            if time.time() - ultimo_escaneo >= (MINUTOS_ESCANEO * 60):
                run_ovision(balance_inicio_dia)
                ultimo_escaneo = time.time()
            gestionar_trailing_y_parciales()
            time.sleep(SEGUNDOS_TRAILING)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}. Reintentando...")
            time.sleep(10)
'''
with open("app/main.py", "a", encoding="utf-8") as f:
    f.write(codigo)
print("✅ Parte 2B guardada. Ovision V3.2 listo.")