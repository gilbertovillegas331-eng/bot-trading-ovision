import re

with open("app/main.py", "r", encoding="utf-8") as f:
    codigo = f.read()

# Reemplaza el initialize vacío por el que tiene la ruta al MT5 original
patron = r"mt5\.initialize\(\)"
reemplazo = 'mt5.initialize(path="C:\\\\Program Files\\\\MetaTrader 5\\\\terminal64.exe")'

codigo_nuevo = re.sub(patron, reemplazo, codigo)

with open("app/main.py", "w", encoding="utf-8") as f:
    f.write(codigo_nuevo)

print("✅ ¡Listo! Ruta del MetaTrader original inyectada.")