# app/main.py
import sys
import os
sys.path.append(os.getcwd())

import MetaTrader5 as mt5
import pandas as pd
import requests
import time
from engines.confluence_engine import ConfluenceEngine

# ==========================================
# CONFIGURACIÓN DE TELEGRAM
# ==========================================
TELEGRAM_TOKEN = "8597898994:AAH-XXDqUSLj6r8srUURlXlaQYOurWeAqlY"
TELEGRAM_CHAT_ID = "5205197349"

# ==========================================
# CONFIGURACIÓN DEL BOT
# ==========================================
TF_HTF = mt5.TIMEFRAME_H4
TF_LTF = mt5.TIMEFRAME_M15
DRY_RUN = True 
MINUTOS_ESPERA = 15
def enviar_telegram(mensaje):
    if "PEGA_AQUI" in TELEGRAM_TOKEN or "PEGA_AQUI" in TELEGRAM_CHAT_ID:
        print("⚠️ ATENCIÓN: Aún tienes el texto 'PEGA_AQUI' en tu Token o Chat ID.")
        return 
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje}
    try:
        respuesta = requests.post(url, json=payload)
        print(f"📡 Estado de Telegram: {respuesta.text}")
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

def get_mt5_data(symbol, timeframe, count=300):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
    if rates is None: return None
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df

def run_ovision():
    if not mt5.initialize():
        print("❌ Error conectando a MT5. Asegúrate de tener MetaTrader 5 abierto.")
        return
        
    print("✅ Ovision Alpha 0.1 iniciado. Buscando oportunidades...\n")
    # enviar_telegram("✅ Ovision iniciado. Buscando oportunidades en Sintéticos...")
    
    todos_los_simbolos = mt5.symbols_get()
    lista_sinteticos = [s.name for s in todos_los_simbolos if "idx" in s.name.lower() or "stp" in s.name.lower()]
    
    lista_sinteticos.append("EURUSD!") 
    lista_sinteticos = list(set(lista_sinteticos))
    
    print(f"🔎 Analizando {len(lista_sinteticos)} activos sintéticos y Forex...\n")

    for sym in lista_sinteticos:
        mt5.symbol_select(sym, True)
        time.sleep(0.5) # Pausa de medio segundo para que MT5 cargue el activo
        df_htf = get_mt5_data(sym, TF_HTF)
        df_ltf = get_mt5_data(sym, TF_LTF)
        
        if df_htf is None or df_ltf is None:
           print(f"⚠️ Saltando {sym}: MT5 aún no tiene los datos descargados.")
           continue
            
        engine = ConfluenceEngine(df_htf, df_ltf, sym)
        signal = engine.analyze()
        
        if signal:
            tarjeta = signal.build_explanation()
            print(tarjeta)
            print("-" * 60)
            enviar_telegram(tarjeta)
        else:
            print(f"🔍 {sym}: Analizado. Sin confluencias.")
    return True
if __name__ == "__main__":
    print("🚀 Ovision encendido. Buscando oportunidades 24/7...")
    enviar_telegram("🤖 Ovision ha arrancado en modo 24/7.")
    
    while True:
        try:
            exito = run_ovision()
            
            if exito:
                print(f"⏳ Escaneo terminado. Esperando {MINUTOS_ESPERA} minutos...")
                time.sleep(MINUTOS_ESPERA * 60)
            else:
                time.sleep(60)
                
        except KeyboardInterrupt:
            print("\n🛑 Ovision apagado manualmente.")
            enviar_telegram("🛑 Ovision ha sido apagado.")
            break