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
TF_ENTRY = mt5.TIMEFRAME_M5
MINUTOS_ESCANEO = 15
SEGUNDOS_TRAILING = 30

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

def calcular_lotaje(symbol, entry, sl, balance_dia):
    info = mt5.symbol_info(symbol)
    if info is None: return 0.01
    distancia = abs(entry - sl)
    tick_value = info.trade_tick_value
    tick_size = info.trade_tick_size
    if tick_size == 0 or tick_value == 0: return 0.01
    riesgo_dinero = balance_dia * (1.66 / 100)
    ticks = distancia / tick_size
    lote = riesgo_dinero / (ticks * tick_value)
    return round(max(info.volume_min, lote), 2)
'''
with open("app/main.py", "w", encoding="utf-8") as f:
    f.write(codigo)
print("✅ Parte 1 guardada.")