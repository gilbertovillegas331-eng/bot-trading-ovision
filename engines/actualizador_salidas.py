import re

ruta = "app/main.py"

print("Leyendo main.py...")
with open(ruta, "r", encoding="utf-8") as f:
    codigo = f.read()

# Buscamos la función entera desde su inicio hasta la siguiente 'def'
patron = r"def gestionar_trailing_y_parciales\(\):.*?(?=def |\Z)"

nuevo_bloque = """def gestionar_trailing_y_parciales():
    posiciones = mt5.positions_get()
    if posiciones is None or len(posiciones) == 0: return
    
    for pos in posiciones:
        distancia_tp = abs(pos.tp - pos.price_open)
        if distancia_tp == 0: continue
        
        distancia_actual = abs(pos.price_current - pos.price_open)
        porcentaje_avance = distancia_actual / distancia_tp
        
        # 1. SALVAVIDAS (Breakeven al 40%)
        if porcentaje_avance >= 0.40:
            if pos.type == mt5.POSITION_TYPE_BUY and (pos.sl < pos.price_open or pos.sl == 0):
                mt5.order_send({"action": mt5.TRADE_ACTION_SLTP, "position": pos.ticket, "symbol": pos.symbol, "sl": pos.price_open, "tp": pos.tp})
                enviar_telegram(f"🛡️ Salvavidas (40%): Breakeven en {pos.symbol}")
            elif pos.type == mt5.POSITION_TYPE_SELL and (pos.sl > pos.price_open or pos.sl == 0):
                mt5.order_send({"action": mt5.TRADE_ACTION_SLTP, "position": pos.ticket, "symbol": pos.symbol, "sl": pos.price_open, "tp": pos.tp})
                enviar_telegram(f"🛡️ Salvavidas (40%): Breakeven en {pos.symbol}")

        # 2. PELLIZCO (Cobrar 70% al llegar al 50%)
        if porcentaje_avance >= 0.50 and pos.comment != "Parcial":
            lote_parcial = round(pos.volume * 0.70, 2)
            if lote_parcial >= mt5.symbol_info(pos.symbol).volume_min:
                tipo = mt5.ORDER_TYPE_SELL if pos.type == mt5.POSITION_TYPE_BUY else mt5.ORDER_TYPE_BUY
                precio = mt5.symbol_info_tick(pos.symbol).bid if pos.type == mt5.POSITION_TYPE_BUY else mt5.symbol_info_tick(pos.symbol).ask
                
                req = {
                    "action": mt5.TRADE_ACTION_DEAL, "position": pos.ticket, "symbol": pos.symbol,
                    "volume": lote_parcial, "type": tipo, "price": precio,
                    "deviation": 20, "magic": 123456, "comment": "Parcial", 
                    "type_time": mt5.ORDER_TIME_GTC, "type_filling": mt5.ORDER_FILLING_IOC
                }
                mt5.order_send(req)
                enviar_telegram(f"✂️ COBRO PARCIAL (50%): {pos.symbol} (70% asegurado)")

        # 3. RASTRO (M1, maximo 10 velas) - Se activa después del 50%
        if porcentaje_avance >= 0.50:
            df_m1 = get_mt5_data(pos.symbol, mt5.TIMEFRAME_M1, 12)
            if df_m1 is not None and len(df_m1) >= 12:
                ultimas_10 = df_m1.iloc[-11:-1] 
                
                if pos.type == mt5.POSITION_TYPE_BUY:
                    nuevo_sl = ultimas_10['low'].min()
                    if nuevo_sl > pos.sl:
                        mt5.order_send({"action": mt5.TRADE_ACTION_SLTP, "position": pos.ticket, "symbol": pos.symbol, "sl": nuevo_sl, "tp": pos.tp})
                elif pos.type == mt5.POSITION_TYPE_SELL:
                    nuevo_sl = ultimas_10['high'].max()
                    if nuevo_sl < pos.sl or pos.sl == 0:
                        mt5.order_send({"action": mt5.TRADE_ACTION_SLTP, "position": pos.ticket, "symbol": pos.symbol, "sl": nuevo_sl, "tp": pos.tp})

"""

codigo_nuevo = re.sub(patron, nuevo_bloque, codigo, flags=re.DOTALL)

if codigo_nuevo != codigo:
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(codigo_nuevo)
    print("✅ ¡Listo! La nueva Gestion de Salidas (40%, 70% y 10 velas) ha sido inyectada.")
else:
    print("❌ ERROR: No se pudo encontrar la funcion de gestion.")