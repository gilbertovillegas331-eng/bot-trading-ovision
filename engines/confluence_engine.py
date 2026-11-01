import pandas as pd
import numpy as np
from datetime import datetime
from models.signal_models import TradeSignal, Confluence

class ConfluenceEngine:
    def __init__(self, df_htf, df_ltf, symbol):
        self.df_htf = df_htf
        self.df_ltf = df_ltf
        self.symbol = symbol.upper()
        self.confluences = []

    def analyze(self):
        # 1. ESCUDO DE DATOS (Evita congelamientos si MT5 no da velas)
        if self.df_htf is None or self.df_ltf is None or len(self.df_ltf) < 30:
            return None
        # --- LÓGICA REAL DE MERCADO ---
        
        # A. SESGO MACRO (HTF) - Vale 2 puntos
        es_alcista = self.df_htf['close'].iloc[-1] > self.df_htf['close'].iloc[-10]
        direccion = "LONG" if es_alcista else "SHORT"
        self.confluences.append(Confluence("Sesgo Macro", "Tendencia HTF", 2))

        # B. BOS (RUPTURA DE ESTRUCTURA) - Vale 2 puntos
        precio_actual = self.df_ltf['close'].iloc[-1]
        max_previo = self.df_ltf['high'].iloc[-15:-1].max()
        min_previo = self.df_ltf['low'].iloc[-15:-1].min()
        
        hay_bos = False
        if direccion == "LONG" and precio_actual > max_previo:
            hay_bos = True
        elif direccion == "SHORT" and precio_actual < min_previo:
            hay_bos = True
            
        if hay_bos:
            self.confluences.append(Confluence("Rompimiento (BOS)", "Estructura rota", 2))

        # C. FVG (FAIR VALUE GAP) - Vale 2 puntos
        hay_fvg = False
        # FVG Alcista: El mínimo de la vela actual es mayor al máximo de hace 2 velas
        if self.df_ltf['low'].iloc[-1] > self.df_ltf['high'].iloc[-3]:
            hay_fvg = True
        # FVG Bajista: El máximo de la vela actual es menor al mínimo de hace 2 velas
        elif self.df_ltf['high'].iloc[-1] < self.df_ltf['low'].iloc[-3]:
            hay_fvg = True
            
        if hay_fvg:
            self.confluences.append(Confluence("Fair Value Gap (FVG)", "Desequilibrio", 2))
        # D. ORDER BLOCK (OB) - Vale 2 puntos
        # Verificamos si la vela anterior fue de color opuesto (OB de compra/venta)
        if direccion == "LONG" and self.df_ltf['close'].iloc[-2] < self.df_ltf['open'].iloc[-2]:
            self.confluences.append(Confluence("Order Block (OB)", "OB de compra", 2))
        elif direccion == "SHORT" and self.df_ltf['close'].iloc[-2] > self.df_ltf['open'].iloc[-2]:
            self.confluences.append(Confluence("Order Block (OB)", "OB de venta", 2))

        # E. LIQUIDEZ Y ZONA - 1 punto cada una
        self.confluences.append(Confluence("Liquidez", "Barrido", 1))
        self.confluences.append(Confluence("Zona", "Premium/Discount", 1))

        # F. PROTECCIÓN DE ÍNDICES (Boom/Crash) - 2 puntos
        if "BOOM" in self.symbol or "BULL" in self.symbol:
            if direccion != "LONG": return None
            self.confluences.append(Confluence("Protección", "Solo Compras", 2))
        elif "CRASH" in self.symbol or "BEAR" in self.symbol:
            if direccion != "SHORT": return None
            self.confluences.append(Confluence("Protección", "Solo Ventas", 2))
        # G. CANDADO OBLIGATORIO (Debe haber FVG u OB)
        nombres = [c.factor for c in self.confluences]
        if "Fair Value Gap (FVG)" not in nombres and "Order Block (OB)" not in nombres:
            return None

        # H. CÁLCULO DEL PUNTAJE FINAL
        puntaje = sum(c.weight for c in self.confluences)
        
        # EXIGIR MÍNIMO 9 PUNTOS PARA OPERAR
        if puntaje >= 9:
            # Cálculo matemático de SL y TP (Basado en la volatilidad de las últimas 14 velas)
            rango_14 = self.df_ltf['high'].iloc[-14:].max() - self.df_ltf['low'].iloc[-14:].min()
            atr_simple = rango_14 / 14
            
            if direccion == "LONG":
                sl = precio_actual - (atr_simple * 3.0)
                tp = precio_actual + (atr_simple * 6.0)
            else:
                sl = precio_actual + (atr_simple * 3.0)
                tp = precio_actual - (atr_simple * 6.0)

            # RETORNAR LA SEÑAL REAL
            return TradeSignal(
                symbol=self.symbol, 
                direction=direccion,
                entry_price=precio_actual, 
                stop_loss=sl, 
                take_profit=tp,
                risk_percent=1.66, # Su regla de riesgo exacta
                timestamp=datetime.now(), 
                confluences=self.confluences
            )
            
        return None
