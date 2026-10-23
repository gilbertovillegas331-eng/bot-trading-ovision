import sys
import os
sys.path.append(os.getcwd())

import MetaTrader5 as mt5
import pandas as pd
import requests
import time
from datetime import datetime  # <-- AÑADE ESTA LÍNEA AQUÍ
from engines.confluence_engine import ConfluenceEngine
# ==========================================
# CONFIGURACIÓN
# ==========================================
TELEGRAM_TOKEN = "8597898994:AAFsT2LqmBtw1b2YWHvYruoUMHUsNSfbhSc"
TELEGRAM_CHAT_ID = "5205197349"

TF_HTF = mt5.TIMEFRAME_H4
TF_LTF = mt5.TIMEFRAME_M15
MINUTOS_ESPERA = 15
# ==========================================
# CONTROL DE RIESGO DIARIO DINÁMICO
# ==========================================
DRY_RUN = False  # ¡Ojo! Lo ponemos en False para que ejecute de verdad en MT5
RIESGO_MAXIMO_DIA = 5.0  # Porcentaje máximo de pérdida diaria
RIESGO_POR_OPERACION = 1.66 # Porcentaje de riesgo por cada trade

# Variables globales de control
balance_inicio_dia = 0.0
fecha_ultimo_trade = None

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje}
    try:
        respuesta = requests.post(url, json=payload)
        print(f"📡 Estado de Telegram: {respuesta.text}")
    except Exception as e:
        print(f"❌ Error enviando a Telegram: {e}")

def get_mt5_data(symbol, timeframe, count=300):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
    if rates is None or len(rates) == 0:
        return None
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df
def calcular_lotaje(symbol, entry, sl):
    info = mt5.symbol_info(symbol)
    account = mt5.account_info()
    
    if info is None or account is None:
        return 0.01 # Lote mínimo de seguridad si falla algo

    distancia = abs(entry - sl)
    tick_value = info.trade_tick_value
    tick_size = info.trade_tick_size
    
    if tick_size == 0 or tick_value == 0:
        return 0.01

    # Calculamos cuánto dinero vamos a arriesgar (1.66% del balance)
    riesgo_dinero = account.balance * (RIESGO_POR_OPERACION / 100)
    
    # Calculamos el lote basado en la distancia del Stop Loss
    ticks = distancia / tick_size
    lote = riesgo_dinero / (ticks * tick_value)
    
    # Ajustamos a los límites del bróker (ej. 0.01 mínimo)
    lote = max(info.volume_min, min(info.volume_max, lote))
    
    # Redondeamos a 2 decimales (como lo pide MT5)
    return round(lote, 2)
def ejecutar_orden(signal):
    symbol = signal.symbol
    lotaje = calcular_lotaje(symbol, signal.entry_price, signal.stop_loss)
    
    tick = mt5.symbol_info_tick(symbol)
    if tick is None: return False

    # Si es LONG compramos al Ask, si es SHORT vendemos al Bid
    precio = tick.ask if signal.direction == "LONG" else tick.bid
    
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lotaje,
        "type": mt5.ORDER_TYPE_BUY if signal.direction == "LONG" else mt5.ORDER_TYPE_SELL,
        "price": precio,
        "sl": signal.stop_loss,
        "tp": signal.take_profit,
        "deviation": 20,
        "magic": 123456,
        "comment": "Ovision",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"❌ Error al abrir orden en {symbol}: {result.comment}")
        return False
    
    print(f"✅ ORDEN ABIERTA: {signal.direction} {symbol} | Lotes: {lotaje} | Precio: {precio}")
    return True

def run_ovision():
    global balance_inicio_dia, fecha_ultimo_trade

    if not mt5.initialize():
        print("❌ Error conectando a MT5.")
        return False

    account = mt5.account_info()
    if account is None: return False

    hoy = datetime.now().date()
    if fecha_ultimo_trade != hoy:
        fecha_ultimo_trade = hoy
        balance_inicio_dia = account.balance
        print(f"\n🌅 NUEVO DÍA DETECTADO. Balance inicial: ${balance_inicio_dia:.2f}")

    limite_perdida = balance_inicio_dia * (1 - (RIESGO_MAXIMO_DIA / 100))
    if account.balance <= limite_perdida:
        print(f"🛑 LÍMITE DE PÉRDIDA DIARIO ALCANZADO. Balance actual: ${account.balance:.2f}")
        return True 

    print(f"\n[{pd.Timestamp.now().strftime('%H:%M:%S')}] 🔎 Iniciando escaneo...")
    
    # --- FILTRO DINÁMICO (Solo activos que MT5 reconoce) ---
    todos_los_simbolos = mt5.symbols_get()
    activos_validos = []
    
    for s in todos_los_simbolos:
        nombre = s.name.upper()
        if ("EURUSD" in nombre or "XAUUSD" in nombre or 
            " C " in nombre or " B " in nombre or 
            "STEP" in nombre or "BULL" in nombre or "BEAR" in nombre):
            
            if mt5.copy_rates_from_pos(s.name, mt5.TIMEFRAME_M15, 0, 5) is not None:
                activos_validos.append(s.name)

    print(f"🔎 Analizando {len(activos_validos)} activos...\n")

    for sym in activos_validos:
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
            
            exito_orden = ejecutar_orden(signal)
            if exito_orden:
                enviar_telegram(f"🚀 ¡Orden Ejecutada! {signal.direction} {sym} | Revisa MT5.")
        else:
            print(f"🔍 {sym}: Analizado. Sin confluencias.")
            
    return True
# ==========================================
# ARRANQUE
# ==========================================
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