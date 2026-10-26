import re

# Ruta del archivo principal
ruta_archivo = "app/main.py" 

print("Leyendo el archivo principal...")
with open(ruta_archivo, "r", encoding="utf-8") as f:
    codigo_actual = f.read()

# La nueva función con la lógica del Kevin, Parciales y Trailing
nueva_funcion = """def gestionar_trailing_y_parciales():
    posiciones = mt5.positions_get()
    if posiciones is None or len(posiciones) == 0: return
    
    for pos in posiciones:
        distancia_tp = abs(pos.tp - pos.price_open)
        if distancia_tp == 0: continue
        
        distancia_actual = abs(pos.price_current - pos.price_open)
        porcentaje_avance = distancia_actual / distancia_tp
        
        # 1. EL "KEVIN" (Breakeven al 50% del camino)
        if porcentaje_avance >= 0.5:
            if pos.type == mt5.POSITION_TYPE_BUY and (pos.sl < pos.price_open or pos.sl == 0):
                mt5.order_send({"action": mt5.TRADE_ACTION_SLTP, "position": pos.ticket, "symbol": pos.symbol, "sl": pos.price_open, "tp": pos.tp})
                enviar_telegram(f"🛡️ Breakeven activado en {pos.symbol}: Operación libre de riesgo.")
                
            elif pos.type == mt5.POSITION_TYPE_SELL and (pos.sl > pos.price_open or pos.sl == 0):
                mt5.order_send({"action": mt5.TRADE_ACTION_SLTP, "position": pos.ticket, "symbol": pos.symbol, "sl": pos.price_open, "tp": pos.tp})
                enviar_telegram(f"🛡️ Breakeven activado en {pos.symbol}: Operación libre de riesgo.")

        # 2. COBRO PARCIAL AL 70% (Tu idea del pellizco)
        if porcentaje_avance >= 0.7 and pos.comment != "Parcial":
            lote_parcial = round(pos.volume / 2, 2)
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
                enviar_telegram(f"✂️ COBRO PARCIAL: {pos.symbol} (70% del camino asegurado)")

        # 3. TRAILING STOP POR ESTRUCTURA (Price Action)
        if porcentaje_avance >= 0.7:
            df_m5 = get_mt5_data(pos.symbol, mt5.TIMEFRAME_M5, 3)
            if df_m5 is not None and len(df_m5) >= 3:
                vela_cerrada = df_m5.iloc[-2] 
                
                if pos.type == mt5.POSITION_TYPE_BUY:
                    nuevo_sl = vela_cerrada['low']
                    if nuevo_sl > pos.sl:
                        mt5.order_send({"action": mt5.TRADE_ACTION_SLTP, "position": pos.ticket, "symbol": pos.symbol, "sl": nuevo_sl, "tp": pos.tp})
                        
                elif pos.type == mt5.POSITION_TYPE_SELL:
                    nuevo_sl = vela_cerrada['high']
                    if nuevo_sl < pos.sl or pos.sl == 0:
                        mt5.order_send({"action": mt5.TRADE_ACTION_SLTP, "position": pos.ticket, "symbol": pos.symbol, "sl": nuevo_sl, "tp": pos.tp})
"""

print("Aplicando la actualización...")
# Usamos Regex para encontrar la función vieja y reemplazarla por la nueva
patron = r"def gestionar_trailing_y_parciales\(\):.*?(?=def|\bwhile\b)"
codigo_nuevo = re.sub(patron, nueva_funcion + "\n\n", codigo_actual, flags=re.DOTALL)

print("Guardando los cambios...")
with open(ruta_archivo, "w", encoding="utf-8") as f:
    f.write(codigo_nuevo)

print("✅ ¡Listo! Código inyectado correctamente sin errores de copiado.")