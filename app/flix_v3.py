with open("app/main.py", "r", encoding="utf-8") as f:
    lineas = f.readlines()

nuevas = []
for linea in lineas:
    if "len(mt5.positions_get())" in linea and ">=" in linea:
        linea = '        if mt5.positions_get() is not None and len(mt5.positions_get()) >= 3:\n'
    nuevas.append(linea)

with open("app/main.py", "w", encoding="utf-8") as f:
    f.writelines(nuevas)

print("✅ ¡Límite cambiado a 3 operaciones en el main.py!")