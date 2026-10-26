ruta = "engines/confluence_engine.py"

print("Leyendo el archivo...")
with open(ruta, "r", encoding="utf-8") as f:
    lineas = f.readlines()

lineas_nuevas = []
for linea in lineas:
    # Si encontramos la línea del ATR, insertamos la definición de direction justo antes
    if "atr = self.ltf.df['ATR'].iloc[-1]" in linea:
        # Insertamos la línea asegurando la misma sangría
        linea_direction = '        direction = "LONG" if htf_bias == "bull" else "SHORT"\n'
        # Evitamos duplicar si ya existe en la línea anterior
        if len(lineas_nuevas) == 0 or "direction =" not in lineas_nuevas[-1]:
            lineas_nuevas.append(linea_direction)
    
    lineas_nuevas.append(linea)

with open(ruta, "w", encoding="utf-8") as f:
    f.writelines(lineas_nuevas)

print("✅ ¡Listo! La variable 'direction' ha sido asegurada.")