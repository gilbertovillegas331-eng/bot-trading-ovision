import sys
import os
sys.path.append(os.getcwd())
import MetaTrader5 as mt5
import pandas as pd
import requests
import time
from datetime import datetime, timedelta
from engines.confluence_engine import ConfluenceEngine

TELEGRAM_TOKEN = "9048473930:AAGMy1UGgkb-Dwix-tfFRYwwI062s3VQDmc"
TELEGRAM_CHAT_ID = "5205197349"
TF_HTF = mt5.TIMEFRAME_H4
TF_LTF = mt5.TIMEFRAME_M15
TF_ENTRY = mt5.TIMEFRAME_M5
MINUTOS_ESCANEO = 0.0333
SEGUNDOS_TRAILING = 30

def enviar_telegram(mensaje):
    mensaje = f"[MODELO 1] {mensaje}"

    # --- GRABADORA PARA AUDITORÍA ---
    with open("historial_señales.csv", "a", encoding="utf-8") as archivo:
        archivo.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, {mensaje}\n")
    # --------------------------------

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": mensaje})
    except: pass

def get_mt5_data(symbol, timeframe, count=100):
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

    
def gestionar_trailing_y_parciales():
    posiciones = mt5.positions_get()
    if posiciones is None or len(posiciones) == 0: return

    for pos in posiciones:
        distancia_tp = abs(pos.tp - pos.price_open)
        if distancia_tp == 0: continue

        # Calculo de distancia a favor (SIN ABS)
        if pos.type == mt5.POSITION_TYPE_BUY:
            distancia_actual = pos.price_current - pos.price_open
        else:
            distancia_actual = pos.price_open - pos.price_current

        porcentaje_avance = distancia_actual / distancia_tp

        # 1. SALVAVIDAS (40% del recorrido al TP)
        if porcentaje_avance >= 0.40:
            if pos.type == mt5.POSITION_TYPE_BUY and (pos.sl < pos.price_open or pos.sl == 0):
                mt5.order_send({"action": mt5.TRADE_ACTION_SLTP, "position": pos.ticket, "symbol": pos.symbol, "sl": pos.price_open, "tp": pos.tp})
                enviar_telegram(f"🛡️ Salvavidas (40%): Breakeven en {pos.symbol}")
            elif pos.type == mt5.POSITION_TYPE_SELL and (pos.sl > pos.price_open or pos.sl == 0):
                mt5.order_send({"action": mt5.TRADE_ACTION_SLTP, "position": pos.ticket, "symbol": pos.symbol, "sl": pos.price_open, "tp": pos.tp})
                enviar_telegram(f"🛡️ Salvavidas (40%): Breakeven en {pos.symbol}")

        # 2. COBRO PARCIAL (50% del recorrido al TP)
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

        # 3. TRAILING STOP (30% restante, velas M1)
        if porcentaje_avance >= 0.50:
            df_m1 = get_mt5_data(pos.symbol, mt5.TIMEFRAME_M1, 12)
            if df_m1 is not None and len(df_m1) >= 10:
                ultimas_10 = df_m1.iloc[-11:-1]
                if pos.type == mt5.POSITION_TYPE_BUY:
                    nuevo_sl = ultimas_10['low'].min()
                    if nuevo_sl > pos.sl:
                        mt5.order_send({"action": mt5.TRADE_ACTION_SLTP, "position": pos.ticket, "symbol": pos.symbol, "sl": nuevo_sl, "tp": pos.tp})
                elif pos.type == mt5.POSITION_TYPE_SELL:
                    nuevo_sl = ultimas_10['high'].max()
                    if nuevo_sl < pos.sl or pos.sl == 0:
                        mt5.order_send({"action": mt5.TRADE_ACTION_SLTP, "position": pos.ticket, "symbol": pos.symbol, "sl": nuevo_sl, "tp": pos.tp})


def ejecutar_orden(signal, balance_dia):
    riesgo_usd = balance_dia * (signal.risk_percent / 100)
    distancia_sl = abs(signal.entry_price - signal.stop_loss)
    lotaje = round(riesgo_usd / (distancia_sl * 10), 2)
    if lotaje < 0.01: lotaje = 0.01

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": signal.symbol,
        "volume": lotaje,
        "type": mt5.ORDER_TYPE_BUY if signal.direction == "LONG" else mt5.ORDER_TYPE_SELL,
        "price": signal.entry_price,
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
        print(f"❌ Error en {signal.symbol}: {result.comment}")
        return False
    
    print(f"✅ ORDEN ABIERTA: {signal.direction} {signal.symbol} | Lotes: {lotaje}")
    return True

def run_ovision(balance_dia):
    if not mt5.initialize(path="C:\\Program Files\\MetaTrader 5 agresivo\\terminal64.exe"): return False
    print(f"\n[{pd.Timestamp.now().strftime('%H:%M:%S')}] 🔍 Escaneando...")
    
    todos_los_simbolos = mt5.symbols_get()
    activos = [s.name for s in todos_los_simbolos if any(x in s.name.upper() for x in ["EURUSD", "XAUUSD", "C ", "B ", "STEP", "BULL", "BEAR"])]
    
    operaciones_esta_ronda = 0

    for sym in activos:
        pos_mt5 = mt5.positions_get(symbol=sym)
        pos_actuales = len(pos_mt5) if pos_mt5 else 0

        if (pos_actuales + operaciones_esta_ronda) >= 3:
            print("🛑 Límite de 3 operaciones alcanzado.")
            break

        if pos_actuales > 0:
            continue

        # --- FILTRO ANTIRREENTRADA (COOLDOWN PROFESIONAL) ---
        pos_abiertas = mt5.positions_get(symbol=sym)
        if pos_abiertas is not None and len(pos_abiertas) > 0:
            continue


        # --- DESPERTAR MT5 (FORZAR DESCARGA DE VELAS) ---
        if not mt5.symbol_select(sym, True):
            print(f"⚠️ No se pudo seleccionar {sym} en MT5. Saltando...")
            continue
        time.sleep(0.1) # Pequeña pausa para que MT5 procese

        # --- ANÁLISIS DE MERCADO ---
        df_htf = get_mt5_data(sym, TF_HTF)
        df_ltf = get_mt5_data(sym, TF_LTF)
        if df_htf is None or df_ltf is None: continue

        engine = ConfluenceEngine(df_htf, df_ltf, sym)
        signal = engine.analyze()

        if signal and signal.total_score() >= 6:
            tarjeta = signal.build_explanation()
            print(tarjeta)
            print("-" * 60)
            
            enviar_telegram(tarjeta)
            
            if ejecutar_orden(signal, balance_dia):
                enviar_telegram(f"🚀 ¡Orden Ejecutada! {signal.direction} {sym}")
                operaciones_esta_ronda += 1
                time.sleep(2)
            else:
                print(f"🔍 {sym}: Error al ejecutar.")

def enviar_reporte_diario():
    ahora = datetime.now()
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
            if d.profit > 0: ganadas += 1
            elif d.profit < 0: perdidas += 1
            pnl_total += d.profit
            
            if d.symbol not in activos: activos[d.symbol] = 0.0
            activos[d.symbol] += d.profit
        
        total_ops = ganadas + perdidas
        win_rate = (ganadas / total_ops * 100) if total_ops > 0 else 0.0
        mejor_activo = max(activos, key=activos.get) if activos else "Ninguno"
        
        mensaje = f"📊 REPORTE DIARIO OVISION V3.2\n"
        mensaje += f"━━━━━━━━━━━━━━━━━━\n"
        mensaje += f"✅ Ganadas: {ganadas}\n"
        mensaje += f"❌ Perdidas: {perdidas}\n"
        mensaje += f"🎯 Win Rate: {win_rate:.2f}%\n"
        mensaje += f"💰 PnL Total: ${pnl_total:.2f}\n"
        mensaje += f"🏆 Mejor Activo: {mejor_activo}\n"
        mensaje += f"━━━━━━━━━━━━━━━━━━"
        
        enviar_telegram(mensaje)
        print("✅ Reporte diario enviado a Telegram.")
        
        
        


if __name__ == "__main__":
    print("🚀 Ovision encendido...")
    enviar_telegram("🚀 Ovision ha arrancado en modo 24/7.")
    acc = mt5.account_info()
    balance_inicio_dia = acc.balance if acc else 1000

    while True:
        try:
            if not mt5.initialize():
                time.sleep(10)
                continue
            run_ovision(balance_inicio_dia)
            gestionar_trailing_y_parciales()
            time.sleep(SEGUNDOS_TRAILING)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}. Reintentando...")
            time.sleep(10)

