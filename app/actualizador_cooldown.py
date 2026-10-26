import re

ruta_archivo = "app/main.py" 

print("Leyendo el archivo principal...")
with open(ruta_archivo, "r", encoding="utf-8") as f:
    codigo_actual = f.read()

# Texto exacto que estamos buscando para anclar la inyección
ancla = 'if mt5.positions_get(symbol=sym) is not None and len(mt5.positions_get(symbol=sym)) > 0: continue'

# El nuevo bloque de código (Cooldown)
nuevo_bloque = ancla + '''

            # --- FILTRO ANTIRREENTRADA (COOLDOWN 15 MIN) ---
            import datetime
            ahora = datetime.datetime.now()
            desde = ahora - datetime.timedelta(minutes=15)
            deals = mt5.history_deals_get(desde, ahora)
            bloqueado = False
            if deals is not None:
                for d in deals:
                    # Revisa si hubo un cierre en este mismo símbolo
                    if d.symbol == sym and d.entry == mt5.DEAL_ENTRY_OUT:
                        bloqueado = True
                        break
            
            if bloqueado:
                print(f"⏳ {sym} en Cooldown (cerró hace <15 min). Buscando otro activo...")
                continue
            # -----------------------------------------------'''

print("Inyectando el filtro Antirreentrada...")
# Reemplazamos el ancla por el ancla + el nuevo bloque
if ancla in codigo_actual:
    codigo_nuevo = codigo_actual.replace(ancla, nuevo_bloque)
else:
    print("❌ ERROR: No se encontró la línea exacta en el código.")
    exit()

print("Guardando los cambios...")
with open(ruta_archivo, "w", encoding="utf-8") as f:
    f.write(codigo_nuevo)

print("✅ ¡Listo! Filtro Antirreentrada (Cooldown) inyectado correctamente.")