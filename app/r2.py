codigo = '''
    def detect_fvgs(self, atr_multiplier=0.15):
        fvgs = []
        for i in range(2, len(self.df)):
            if self.df['low'].iloc[i] > self.df['high'].iloc[i-2]:
                gap = self.df['low'].iloc[i] - self.df['high'].iloc[i-2]
                if gap > (self.df['ATR'].iloc[i] * atr_multiplier):
                    fvgs.append({"type": "bull", "top": self.df['low'].iloc[i], "bottom": self.df['high'].iloc[i-2], "idx": i})
            if self.df['high'].iloc[i] < self.df['low'].iloc[i-2]:
                gap = self.df['low'].iloc[i-2] - self.df['high'].iloc[i]
                if gap > (self.df['ATR'].iloc[i] * atr_multiplier):
                    fvgs.append({"type": "bear", "top": self.df['low'].iloc[i-2], "bottom": self.df['high'].iloc[i], "idx": i})
        return fvgs

    def detect_order_blocks(self, events, lookback=10):
        obs = []
        for event_type, direction, idx in events:
            for j in range(idx-1, max(idx-lookback, 0), -1):
                is_bearish_candle = self.df['close'].iloc[j] < self.df['open'].iloc[j]
                if direction == "bull" and is_bearish_candle:
                    obs.append({"type": "bull", "top": self.df['high'].iloc[j], "bottom": self.df['low'].iloc[j], "idx": j})
                    break
                elif direction == "bear" and not is_bearish_candle:
                    obs.append({"type": "bear", "top": self.df['high'].iloc[j], "bottom": self.df['low'].iloc[j], "idx": j})
                    break
        return obs

    def detect_liquidity_sweep(self, lookback=10):
        sweeps = []
        for i in range(lookback, len(self.df)):
            high_previo = self.df['high'].iloc[i-lookback:i].max()
            if self.df['high'].iloc[i] > high_previo and self.df['close'].iloc[i] < high_previo:
                sweeps.append({"type": "bear", "idx": i})
            low_previo = self.df['low'].iloc[i-lookback:i].min()
            if self.df['low'].iloc[i] < low_previo and self.df['close'].iloc[i] > low_previo:
                sweeps.append({"type": "bull", "idx": i})
        return sweeps

    def detect_candle_patterns(self, idx):
        if idx < 2: return None
        o, c, h, l = self.df['open'].iloc[idx], self.df['close'].iloc[idx], self.df['high'].iloc[idx], self.df['low'].iloc[idx]
        po, pc = self.df['open'].iloc[idx-1], self.df['close'].iloc[idx-1]
        cuerpo = abs(c - o)
        rango = h - l
        if rango == 0: return None
        if c > o and pc < po and c > po and o < pc: return "bull_engulf"
        if c < o and pc > po and c < po and o > pc: return "bear_engulf"
        mecha_inf = min(o, c) - l
        mecha_sup = h - max(o, c)
        if mecha_inf > 2 * cuerpo and mecha_inf > mecha_sup: return "bull_pin"
        if mecha_sup > 2 * cuerpo and mecha_sup > mecha_inf: return "bear_pin"
        return None
'''
with open("engines/smc_engine.py", "a", encoding="utf-8") as f:
    f.write(codigo)
print("✅ Parte 2 guardada. Archivo completo.")
