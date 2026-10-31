with open("app/main.py", "r", encoding="utf-8") as f:
    lineas = f.readlines()

nuevas_lineas = []
saltar = False

for i, linea in enumerate(lineas):
    if 'if signal:' in linea:
        indent = " " * (len(linea) - len(linea.lstrip()))
        nuevas_lineas.append(f"{indent}if signal:\n")
        nuevas_lineas.append(f"{indent}    tarjeta = signal.build_explanation()\n")
        nuevas_lineas.append(f"{indent}    print(tarjeta)\n")
        nuevas_lineas.append(f"{indent}    print(\"-\" * 60)\n")
        nuevas_lineas.append(f"\n")
        nuevas_lineas.append(f"{indent}    puntaje = getattr(signal, 'total_score', 0)\n")
        nuevas_lineas.append(f"\n")
        nuevas_lineas.append(f"{indent}    if puntaje >= 6:\n")
        nuevas_lineas.append(f"{indent}        enviar_telegram(tarjeta)\n")
        nuevas_lineas.append(f"{indent}        exito_orden = ejecutar_orden(signal, balance_dia)\n")
        nuevas_lineas.append(f"{indent}        if exito_orden:\n")
        nuevas_lineas.append(f"{indent}            enviar_telegram(f\"🚀 ¡Orden Ejecutada! {{signal.direction}} {{sym}}\")\n")
        nuevas_lineas.append(f"{indent}        else:\n")
        nuevas_lineas.append(f"{indent}            print(f\"🔍 {{sym}}: Error al ejecutar.\")\n")
        nuevas_lineas.append(f"{indent}    else:\n")
        nuevas_lineas.append(f"{indent}        enviar_telegram(f\"⚠️ SEÑAL OBSERVADA ({{puntaje}}/10):\\n{{tarjeta}}\")\n")
        nuevas_lineas.append(f"{indent}        print(f\"🔍 {{sym}}: Observada ({{puntaje}}/10 < 6).\")\n")
        
        saltar = True
        continue
    
    if saltar:
        # Saltamos el código viejo hasta llegar al final de la función
        if linea.strip().startswith('return True') or linea.strip().startswith('def '):
            saltar = False
            nuevas_lineas.append(linea)
        continue
        
    nuevas_lineas.append(linea)

with open("app/main.py", "w", encoding="utf-8") as f:
    f.writelines(nuevas_lineas)

print("✅ ¡Listo! Bloque de ejecución reconstruido perfectamente.")