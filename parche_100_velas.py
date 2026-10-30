import os

file_path = 'app/main.py'

if not os.path.exists(file_path):
    print("❌ Error: No se encuentra app/main.py")
else:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Buscamos la función get_mt5_data y le bajamos el count a 100
    if 'def get_mt5_data(symbol, timeframe, count=300):' in content:
        content = content.replace('def get_mt5_data(symbol, timeframe, count=300):', 'def get_mt5_data(symbol, timeframe, count=100):')
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ ¡SEGUNDA BALA APLICADA! Ahora solo se piden 100 velas.")
    else:
        print("⚠️ No se encontró la función exacta. Revise a mano.")