import os

# --- PARTE 1: BLINDAJE DEL MOTOR SMC ---
file_smc = 'engines/smc_engine.py'
if os.path.exists(file_smc):
    with open(file_smc, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Escudo para detect_swings
    if 'def detect_swings_and_structure(self, lookback=3):' in content:
        if 'if self.df is None: return None, None' not in content:
            content = content.replace(
                'def detect_swings_and_structure(self, lookback=3):',
                'def detect_swings_and_structure(self, lookback=3):\n        if self.df is None: return None, None'
            )
    with open(file_smc, 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Motor SMC blindado.")
else:
    print("⚠️ No se encontró smc_engine.py")

# --- PARTE 2: BLINDAJE DEL MAIN.PY ---
file_main = 'app/main.py'
if os.path.exists(file_main):
    with open(file_main, 'r', encoding='utf-8') as f:
        content = f.read()

    viejo_bloque = '''        engine = ConfluenceEngine(df_htf, df_ltf, sym)
        signal = engine.analyze()'''

    nuevo_bloque = '''        try:
            engine = ConfluenceEngine(df_htf, df_ltf, sym)
            signal = engine.analyze()
        except Exception as e:
            print(f"⚠️ Error analizando {sym}. Saltando...")
            continue'''

    if viejo_bloque in content:
        content = content.replace(viejo_bloque, nuevo_bloque)
        with open(file_main, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Main.py blindado contra congelamientos.")
    else:
        print("⚠️ No se encontró el bloque exacto en main.py (revise espacios).")
else:
    print("⚠️ No se encontró main.py")