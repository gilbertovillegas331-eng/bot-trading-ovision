codigo = '''
def gestionar_posiciones():
    posiciones = mt5.positions_get()
    if posiciones is None or len(posiciones) == 0: return
    for pos in posiciones:
        distancia_tp = abs(pos.tp - pos.price_open)
        distancia_actual = abs(pos.price_current - pos.price_open)
        
        if distancia_tp == 0: continue
        porcentaje_avance = distancia_actual / distancia_tp
        
        # Si va ganando más del 50% (1:1) y el SL está por debajo de la entrada
        if porcentaje_avance >= 0.5:
            if pos.type == mt5.POSITION_TYPE_BUY:
                nuevo_sl = pos.price_open
                if porcentaje_avance >= 0.75: nuevo_sl = pos.price_open + (distancia_tp * 0.5)
                if pos.sl < nuevo_sl:
                    mt5.order_send({"action": mt5.TRADE_ACTION_SLTP, "position": pos.ticket, "symbol": pos.symbol, "sl": nuevo_sl, "tp": pos.tp})
            elif pos.type == mt5.POSITION_TYPE_SELL:
                nuevo_sl = pos.price_open
                if porcentaje_avance >= 0.75: nuevo_sl = pos.price_open - (distancia_tp * 0.5)
                if pos.sl > nuevo_sl or pos.sl == 0:
                    mt5.order_send({"action": mt5.TRADE_ACTION_SLTP, "position": pos.ticket, "symbol": pos.symbol, "sl": nuevo_sl, "tp": pos.tp})

def run_ovision():
    if not mt5.initialize(): return False
    print(f"\\n[{pd.Timestamp.now().strftime('%H:%M:%S')}] 🔎 Escaneando...")
    
    todos_los_simbolos = mt5.symbols_get()
    activos = []
    for s in todos_los_simbolos:
        nombre = s.name.upper()
        if ("EURUSD" in nombre or "XAUUSD" in nombre or " C " in nombre or " B " in nombre or "STEP" in nombre or "BULL" in nombre or "BEAR" in nombre):
            if mt5.copy_rates_from_pos(s.name, mt5.TIMEFRAME_M15, 0, 5) is not None:
                activos.append(s.name)

    operaciones_esta_ronda = 0

    for sym in activos:
        posiciones_mt5 = mt5.positions_get()
        posiciones_actuales = len(posiciones_mt5) if posiciones_mt5 else 0
        
        if (posiciones_actuales + operaciones_esta_ronda) >= 3:
            print("🛑 Límite de 3 operaciones alcanzado.")
            break 
            
        if mt5.positions_get(symbol=sym) is not None and len(mt5.positions_get(symbol=sym)) > 0:
            continue 
            
        df_htf = get_mt5_data(sym, TF_HTF)
        df_ltf = get_mt5_data(sym, TF_LTF)
        if df_htf is None or df_ltf is None: continue
            
        engine = ConfluenceEngine(df_htf, df_ltf, sym)
        signal = engine.analyze()
        
        if signal:
            tarjeta = signal.build_explanation()
            print(tarjeta)
            
            if (posiciones_actuales + operaciones_esta_ronda) < 3:
                enviar_telegram(tarjeta)
                if ejecutar_orden(signal):
                    enviar_telegram(f"🚀 ¡Orden Ejecutada! {signal.direction} {sym}")
                    operaciones_esta_ronda += 1
                    time.sleep(2)
            else:
                enviar_telegram(tarjeta + "\\n\\n⚠️ SEÑAL NO EJECUTADA: Límite de 3 operaciones alcanzado.")
    return True

if name == "main":
    print("🚀 Ovision V3 (Trailing + Límite 3) encendido...")
    while True:
        try:
            gestionar_posiciones() 
            run_ovision()
            time.sleep(MINUTOS_ESPERA * 60)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(60)
'''
with open("app/main.py", "a", encoding="utf-8") as f:
    f.write(codigo)
print("✅ Parte 2 guardada. Archivo V3 completo.")