import urllib.request
import os
import shutil

# 1. Descargar el smc_engine original de GitHub
url = "https://raw.githubusercontent.com/gilbertovillegas331-eng/bot-trading-ovision/main/engines/smc_engine.py"
try:
    urllib.request.urlretrieve(url, "engines/smc_engine.py")
    print("✅ smc_engine.py descargado de GitHub.")
except Exception as e:
    print(f"❌ Error al descargar: {e}")
    exit()

# 2. Añadir las funciones nuevas (StepRise/StepDrop y Patrones)
codigo_extra = '''
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
    f.write(codigo_extra)
print("✅ Funciones extra añadidas.")

# 3. Borrar la memoria basura (pycache)
for root, dirs, files in os.walk("."):
    if "pycache" in dirs:
        shutil.rmtree(os.path.join(root, "pycache"))
print("✅ Memoria basura eliminada.")

# 4. Encender el bot automáticamente
print("🚀 Encendiendo Ovision...")
os.system(".venv\\Scripts\\python.exe -B -m app.main")