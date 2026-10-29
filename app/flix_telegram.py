import re

with open("app/main.py", "r", encoding="utf-8") as f:
    codigo = f.read()

# 1. Poner el Token Original (el que sirve)
codigo = re.sub(r'TELEGRAM_TOKEN\s*=\s*".*?"', 'TELEGRAM_TOKEN = "8597898994:AAFsT2LqmBtw1b2YWHvYruoUMHUsNSfbhSc"', codigo)

# 2. Agregar la etiqueta [MODELO 1] al inicio de cada mensaje
if 'mensaje = f"[MODELO 1] {mensaje}"' not in codigo:
    codigo = codigo.replace(
        'def enviar_telegram(mensaje):\n    url =', 
        'def enviar_telegram(mensaje):\n    mensaje = f"[MODELO 1] {mensaje}"\n    url ='
    )

with open("app/main.py", "w", encoding="utf-8") as f:
    f.write(codigo)

print("✅ ¡Listo! Token arreglado y etiqueta [MODELO 1] agregada.")