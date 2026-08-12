# Structure Engine v1

## Flujo

Closed Candles -> Pivot Detection -> Swing Classification -> StructureState -> Protected Levels -> BOS/CHoCH -> Updated State

## Pivotes

SwingDetector detecta HIGH/LOW. Clasificación separada:
HH, HL, LH, LL, EQH, EQL.

## Tolerancia

Comparaciones en ticks con tolerancia configurable.

## Protected Levels

Lifecycle:
CANDIDATE, ACTIVE, BROKEN, RETIRED, INVALIDATED.

## BOS

Ruptura de continuación confirmada por cierre y tolerancia.

## CHoCH

Ruptura del protected level activo por cierre. Lleva a TRANSITION, no cambia tendencia confirmada inmediatamente.

## Reglas

- Wick sweep no es BOS/CHoCH.
- Estado independiente por timeframe.
- Eventos idempotentes.
- `pivot_time != confirmed_at`.
