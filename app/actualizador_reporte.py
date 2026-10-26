ruta_archivo = "app/main.py" 

print("Leyendo el archivo principal...")
with open(ruta_archivo, "r", encoding="utf-8") as f:
    codigo = f.read()

# 1. Asegurar la importación de datetime global
if "import datetime" not in codigo:
    codigo = "import datetime\n" + codigo

# 2. Inyectar la función de reporte antes de run_ovision
funcion_reporte = '''
def enviar_reporte_diario():
    ahora = datetime.datetime.now()
    inicio_dia = ahora.replace(hour=0, minute=0, second=0, microsecond=0)
    deals = mt5.history_deals_get(inicio_dia, ahora)
    
    if deals is None or len(deals) == 0:
        enviar_telegram("📊 REPORTE DIARIO: No hubo operaciones cerradas hoy.")
        return

    ganadas = 0
    perdidas = 0
    pnl_total = 0.0
    activos = {}

    for d in deals:
        if d.entry == mt5.DEAL_ENTRY_OUT:
            if d.profit > 0:
                ganadas += 1
            elif d.profit < 0:
                perdidas += 1
            pnl_total += d.profit
            
            if d.symbol not in activos:
                activos[d.symbol] = 0.0
            activos[d.symbol] += d.profit

    total_ops = ganadas + perdidas
    win_rate = (ganadas / total_ops * 100) if total_ops > 0 else 0.0
    mejor_activo = max(activos, key=activos.get) if activos else "Ninguno"

    mensaje = f"📊 REPORTE DIARIO OVISION V3.2\\n"
    mensaje += f"━━━━━━━━━━━━━━━━━━\\n"
    mensaje += f"✅ Ganadas: {ganadas}\\n"
    mensaje += f"❌ Perdidas: {perdidas}\\n"
    mensaje += f"🎯 Win Rate: {win_rate:.2f}%\\n"
    mensaje += f"💰 PnL Total: ${pnl_total:.2f}\\n"
    mensaje += f"🏆 Mejor Activo: {mejor_activo}\\n"
    mensaje += f"━━━━━━━━━━━━━━━━━━"

    enviar_telegram(mensaje)
    print("✅ Reporte diario enviado a Telegram.")

'''
codigo = codigo.replace("def run_ovision(balance_dia):", funcion_reporte + "\ndef run_ovision(balance_dia):")

# 3. Inyectar el disparador en el bucle principal (a las 23:55)
ancla_loop = "time.sleep(SEGUNDOS_TRAILING)"
trigger = """        # --- TRIGGER REPORTE DIARIO (23:55) ---
        global ultimo_reporte_dia
        hoy_str = datetime.datetime.now().strftime("%Y-%m-%d")
        if datetime.datetime.now().hour == 23 and datetime.datetime.now().minute == 55 and ultimo_reporte_dia != hoy_str:
            enviar_reporte_diario()
            ultimo_reporte_dia = hoy_str
        # --------------------------------------
        
""" + ancla_loop
codigo = codigo.replace(ancla_loop, trigger)

# 4. Inicializar la variable global
codigo = codigo.replace("ultimo_escaneo = 0", "ultimo_reporte_dia = None\nultimo_escaneo = 0")

print("Guardando los cambios...")
with open(ruta_archivo, "w", encoding="utf-8") as f:
    f.write(codigo)

print("✅ ¡Listo! Reporte Diario inyectado correctamente.")