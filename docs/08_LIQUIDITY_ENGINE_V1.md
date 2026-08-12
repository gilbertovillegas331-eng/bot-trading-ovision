# Liquidity Engine v1

## Conceptos

- Buy-side liquidity sobre referencia.
- Sell-side liquidity bajo referencia.
- Pools son zonas, no precios mágicos.

## LiquidityPool lifecycle

CANDIDATE, ACTIVE, TOUCHED, SWEPT, PARTIALLY_CONSUMED, CONSUMED, INVALIDATED, RETIRED.

## Sweep

Requiere penetración + reclaim. Si el cierre confirma ruptura estructural, no se etiqueta como simple sweep.

## Fuentes

Swings, EQH/EQL, range highs/lows, session/day/week highs/lows.

## FVG

Imbalance de tres velas; no es liquidity pool por definición.

## Disciplina semántica

No afirmar “instituciones cazaron stops” como hecho observable.
