# engines/smc_engine.py
import pandas as pd
import numpy as np

class SMCEngine:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.df['ATR'] = self._calculate_atr()

    def _calculate_atr(self, period=14):
        tr = pd.concat([
            self.df["high"] - self.df["low"],
            (self.df["high"] - self.df["close"].shift()).abs(),
            (self.df["low"] - self.df["close"].shift()).abs(),
        ], axis=1).max(axis=1)
        return tr.rolling(period).mean()

    def detect_swings_and_structure(self, lookback=3):
        """Detecta BOS/CHoCH basados en máximos y mínimos locales."""
        self.df['Swing_High'] = self.df['high'] == self.df['high'].rolling(lookback*2+1, center=True).max()
        self.df['Swing_Low'] = self.df['low'] == self.df['low'].rolling(lookback*2+1, center=True).min()
        
        bias = None
        events = []
        last_high, last_low = None, None

        for i in range(len(self.df)):
            if self.df['Swing_High'].iloc[i]: last_high = self.df['high'].iloc[i]
            if self.df['Swing_Low'].iloc[i]: last_low = self.df['low'].iloc[i]
            
            # Ruptura de estructura
            if last_high and self.df['close'].iloc[i] > last_high:
                events.append(("CHoCH" if bias != "bull" else "BOS", "bull", i))
                bias = "bull"
                last_high = None
            if last_low and self.df['close'].iloc[i] < last_low:
                events.append(("CHoCH" if bias != "bear" else "BOS", "bear", i))
                bias = "bear"
                last_low = None
                
        return events, bias

    def detect_fvgs(self, atr_multiplier=0.15):
        """Detecta Fair Value Gaps (FVG) filtrados por volatilidad (ATR)."""
        fvgs = []
        for i in range(2, len(self.df)):
            # FVG Alcista
            if self.df['low'].iloc[i] > self.df['high'].iloc[i-2]:
                gap = self.df['low'].iloc[i] - self.df['high'].iloc[i-2]
                if gap > (self.df['ATR'].iloc[i] * atr_multiplier):
                    fvgs.append({"type": "bull", "top": self.df['low'].iloc[i], "bottom": self.df['high'].iloc[i-2], "idx": i})
            # FVG Bajista
            if self.df['high'].iloc[i] < self.df['low'].iloc[i-2]:
                gap = self.df['low'].iloc[i-2] - self.df['high'].iloc[i]
                if gap > (self.df['ATR'].iloc[i] * atr_multiplier):
                    fvgs.append({"type": "bear", "top": self.df['low'].iloc[i-2], "bottom": self.df['high'].iloc[i], "idx": i})
        return fvgs

    def detect_order_blocks(self, events, lookback=10):
        """Detecta el Order Block (OB) previo al BOS/CHoCH."""
        obs = []
        for event_type, direction, idx in events:
            for j in range(idx-1, max(idx-lookback, 0), -1):
                is_bearish_candle = self.df['close'].iloc[j] < self.df['open'].iloc[j]
                # Si el impulso es alcista, buscamos la última vela bajista
                if direction == "bull" and is_bearish_candle:
                    obs.append({"type": "bull", "top": self.df['high'].iloc[j], "bottom": self.df['low'].iloc[j], "idx": j})
                    break
                # Si el impulso es bajista, buscamos la última vela alcista
                elif direction == "bear" and not is_bearish_candle:
                    obs.append({"type": "bear", "top": self.df['high'].iloc[j], "bottom": self.df['low'].iloc[j], "idx": j})
                    break
        return obs