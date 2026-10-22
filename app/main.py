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
TELEGRAM_TOKEN = "8597898994:AAH-XXDqUSLj6r8srUUR1X1aQYOurWeAq1Y"
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
        return 
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error enviando a Telegram: {e}")

def get_mt5_data(symbol, timeframe, count=300):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
    if rates is None: return None
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df

def run_ovision():
    if not mt5.initialize():
        print("❌ Error conectando a MT5. Asegúrate de tener MetaTrader 5 abierto.")
        return False
        
    print(f"\n[{pd.Timestamp.now().strftime('%H:%M:%S')}] 🔎 Iniciando escaneo del mercado...")
    
    # LISTA BLANCA PERSONALIZADA (BridgeMarkets)
    lista_sinteticos = [
        "EURUSD!", "XAUUSD!",
        
        # Crash (Solo ventas)
        "C 300 IDX.", "C 500 IDX.", "C 600 IDX.", "C 900 IDX.", "C 1000 IDX.",
        
        # Boom (Solo compras)
        "B 300 IDX.", "B 500 IDX.", "B 600 IDX.", "B 900 IDX.", "B 1000 IDX.",
        
        # Step (Rise = Ventas, Drop = Compras)
        "STEPRISE400.", "STEPRISE600.", "STEPRISE800.", "STEPRISE999.", "STEPRISE1200.",
        "STEPDROP400.", "STEPDROP600.", "STEPDROP800.", "STEPDROP900.", "STEPDROP999.", "STEPDROP1200.",
        
        # Fortune, Fomo, Flip, Vortex (Análisis normal)
        "FORTUNE100.", "FORTUNE1000.", "FORTUNEX200.", "FORTUNEX500.",
        "FOMOX333.",
        "FLIPRAND1.", "FLIPRAND2.", "FLIPRAND3.", "FLIPRAND5.",
        "VORTEX20.", "VORTEX40.", "VORTEX80.",
        
        # Bull y Bear (ISD Break)
        "BULL400", "BULL500", "BULL777", "BULL900", "BULL1000",
        "BEAR400", "BEAR500", "BEAR777", "BEAR900", "BEAR1000",
        "BEARX500", "BEARX777", "BEARX1000",
        
        # Syntex
        "SYNTEX200", "SYNTEX300", "SYNTEX400", "SYNTEX500"
    ]

    print(f"🔎 Analizando {len(lista_sinteticos)} activos sintéticos y Forex...\n")

    for sym in lista_sinteticos:
        mt5.symbol_select(sym, True)
        time.sleep(0.5) 
        
        df_htf = get_mt5_data(sym, TF_HTF)
        df_ltf = get_mt5_data(sym, TF_LTF)
        
        if df_htf is None or df_ltf is None:
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
    enviar_telegram("🤖 Ovision ha arrancado en modo 24/7 con la lista personalizada.")
    
    while True:
        try:
            exito = run_ovision()
            
            if exito:
                print(f"⏳ Escaneo terminado. Esperando {MINUTOS_ESPERA} minutos...")
                time.sleep(MINUTOS_ESPERA * 60)
            else:
                print("⚠️ Fallo en el escaneo. Reintentando en 1 minuto...")
                time.sleep(60)
                
        except KeyboardInterrupt:
            print("\n🛑 Ovision apagado manualmente.")
            enviar_telegram("🛑 Ovision ha sido apagado.")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            print("⏳ Reintentando en 1 minuto...")
            time.sleep(60)  