codigo = '''import sys
import os
sys.path.append(os.getcwd())
import MetaTrader5 as mt5
import pandas as pd
import requests
import time
from datetime import datetime
from engines.confluence_engine import ConfluenceEngine

TELEGRAM_TOKEN = "8597898994:AAH-XXDqUSLj6r8srUUR1X1aQYOurWeAq1Y"
TELEGRAM_CHAT_ID = "5205197349"
TF_HTF = mt5.TIMEFRAME_H4
TF_LTF = mt5.TIMEFRAME_M15
MINUTOS_ESPERA = 15

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": mensaje})
    except: pass

def get_mt5_data(symbol, timeframe, count=300):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
    if rates is None or len(rates) == 0: return None
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df

def calcular_lotaje(symbol, entry, sl):
    info = mt5.symbol_info(symbol)
    account = mt5.account_info()
    if info is None or account is None: return 0.01
    distancia = abs(entry - sl)
    tick_value = info.trade_tick_value
    tick_size = info.trade_tick_size
    if tick_size == 0 or tick_value == 0: return 0.01
    riesgo_dinero = account.balance * (1.66 / 100)
    ticks = distancia / tick_size
    lote = riesgo_dinero / (ticks * tick_value)
    return round(max(info.volume_min, lote), 2)

def ejecutar_orden(signal):
    lotaje = calcular_lotaje(signal.symbol, signal.entry_price, signal.stop_loss)
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
    if result.retcode != mt5.RETCODE_DONE:
        print(f"❌ Error en {signal.symbol}: {result.comment}")
        return False
    print(f"✅ ORDEN ABIERTA: {signal.direction} {signal.symbol} | Lotes: {lotaje}")
    return True
'''
with open("app/main.py", "w", encoding="utf-8") as f:
    f.write(codigo)
print("✅ Parte 1 guardada.")