import os

file_path = 'app/main.py'

if not os.path.exists(file_path):
    print("❌ No se encontró main.py")
else:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Buscamos el mensaje genérico y le inyectamos la variable 'e' (el error real)
    viejo = 'print(f"⚠️ Error analizando {sym}. Saltando...")'
    nuevo = 'print(f"⚠️ Error analizando {sym}: {e}. Saltando...")'

    if viejo in content:
        content = content.replace(viejo, nuevo)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ ¡LISTO! Ahora el bot nos dirá el error exacto.")
    else:
        print("⚠️ No se encontró el mensaje exacto. Revisar a mano.")
        