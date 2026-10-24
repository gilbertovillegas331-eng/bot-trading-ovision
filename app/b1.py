codigo = '''import pandas as pd
import numpy as np

class SMCEngine:
    def init(self, df: pd.DataFrame):
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
        self.df['Swing_High'] = self.df['high'] == self.df['high'].rolling(lookback*2+1, center=True).max()
        self.df['Swing_Low'] = self.df['low'] == self.df['low'].rolling(lookback*2+1, center=True).min()
        bias = None
        events = []
        last_high, last_low = None, None
        for i in range(len(self.df)):
            if self.df['Swing_High'].iloc[i]: last_high = self.df['high'].iloc[i]
            if self.df['Swing_Low'].iloc[i]: last_low = self.df['low'].iloc[i]
            if last_high and self.df['close'].iloc[i] > last_high:
                events.append(("CHoCH" if bias != "bull" else "BOS", "bull", i))
                bias = "bull"
                last_high = None
            if last_low and self.df['close'].iloc[i] < last_low:
                events.append(("CHoCH" if bias != "bear" else "BOS", "bear", i))
                bias = "bear"
                last_low = None
        return events, bias
'''

with open("engines/smc_engine.py", "w", encoding="utf-8") as f:
    f.write(codigo)

print("✅ PARTE 1 escrita. Ahora ejecuta el paso 2.")