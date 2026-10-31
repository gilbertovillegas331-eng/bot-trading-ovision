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
        # 1. ESCUDO DE DATOS
        if self.df_htf is None or self.df_ltf is None or len(self.df_ltf) < 20:
            return None

        # 2. FILTRO DE SESIÓN (Londres/NY)
        es_sintetico = any(x in self.symbol for x in ["STEP", "BOOM", "CRASH", "BULL", "BEAR"])
        if not es_sintetico:
            if not (8 <= datetime.now().hour < 17): return None

        # 3. FILTRO ATR (Volatilidad)
        self.df_ltf['TR'] = np.maximum(self.df_ltf['high'] - self.df_ltf['low'], 
                            np.maximum(abs(self.df_ltf['high'] - self.df_ltf['close'].shift()), 
                                       abs(self.df_ltf['low'] - self.df_ltf['close'].shift())))
        atr_actual = self.df_ltf['TR'].rolling(14).mean().iloc[-1]
        atr_promedio = self.df_ltf['TR'].rolling(50).mean().iloc[-1]
        if pd.isna(atr_actual) or atr_actual < (atr_promedio * 0.7): return None

        # 4. REGLAS Y PUNTAJE
        precio_actual = self.df_ltf['close'].iloc[-1]
        es_alcista = self.df_htf['close'].iloc[-1] > self.df_htf['close'].iloc[-10]
        direccion = "LONG" if es_alcista else "SHORT"
        
        # Protección Boom/Crash
        if "BOOM" in self.symbol or "BULL" in self.symbol:
            if direccion != "LONG": return None
        if "CRASH" in self.symbol or "BEAR" in self.symbol:
            if direccion != "SHORT": return None

        # Simulación de confluencias (para prueba)
        confs = [
            Confluence("Sesgo Macro", "Tendencia HTF", 2),
            Confluence("Rompimiento", "BOS", 2),
            Confluence("Fair Value Gap", "FVG", 2),
            Confluence("Order Block", "OB", 2),
            Confluence("Liquidez", "Sweep", 1)
        ]
        
        puntaje = sum(c.weight for c in confs)
        if puntaje < 9: return None

        # 5. CÁLCULO DE SL Y TP
        if direccion == "LONG":
            sl = precio_actual - (atr_actual * 1.5)
            tp = precio_actual + (atr_actual * 3.0)
        else:
            sl = precio_actual + (atr_actual * 1.5)
            tp = precio_actual - (atr_actual * 3.0)

        # 6. RETORNAR OBJETO VÁLIDO
        return TradeSignal(
            symbol=self.symbol, direction=direccion,
            entry_price=precio_actual, stop_loss=sl, take_profit=tp,
            risk_percent=1.0, timestamp=datetime.now(), confluences=confs
        )
