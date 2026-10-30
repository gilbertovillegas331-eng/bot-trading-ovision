import os

file_path = 'engines/smc_engine.py'

if not os.path.exists(file_path):
    print("❌ Error: No se encuentra engines/smc_engine.py")
else:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # El bloque de código actual que falla
    viejo_bloque = '''    def init(self, df: pd.DataFrame):
        self.df = df.copy()
        self.df['ATR'] = self._calculate_atr()'''

    # El nuevo bloque con la protección
    nuevo_bloque = '''    def init(self, df: pd.DataFrame):
        if df is None or len(df) == 0:
            self.df = None
            return
            
        self.df = df.copy()
        self.df['ATR'] = self._calculate_atr()'''

    if viejo_bloque in content:
        content = content.replace(viejo_bloque, nuevo_bloque)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ ¡ESCUDO APLICADO! El motor SMC ya no colapsará si no hay datos.")
    else:
        # Si la sintaxis es diferente, usamos un parche más flexible
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'def init(self, df: pd.DataFrame):' in line:
                lines.insert(i+1, "        if df is None or len(df) == 0:\n            self.df = None\n            return\n")
                break
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        print("✅ ¡ESCUDO APLICADO (Método flexible)! Revise el archivo.")