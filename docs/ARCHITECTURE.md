# Arquitectura de OVISION

```text
MetaTrader 5
    ↓
MT5 Service
    ↓
Vision Engine
    ↓
MarketData
    ↓
Structure Engine
    ↓
Liquidity / Institutional / Context Engines
    ↓
OVI MIND
    ↓
Confidence / Decision / Explain Engines
    ↓
Usuario
```

## Responsabilidades

- **OVI CORE:** coordina; no analiza.
- **Vision Engine:** observa y normaliza.
- **Structure Engine:** detecta Swings, tendencia, BOS, CHOCH y MSS.
- **Liquidity Engine:** administra BSL, SSL, EQH, EQL y barridos.
- **Institutional Engine:** administra OB, FVG, Breakers e Imbalances.
- **OVI MIND:** construye y compara hipótesis.
- **Explain Engine:** comunica el razonamiento sin reinterpretar datos.
