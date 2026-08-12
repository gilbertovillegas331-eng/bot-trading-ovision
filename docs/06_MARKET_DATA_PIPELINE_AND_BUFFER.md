# Market Data Pipeline & Buffer v1

## Pipeline

Provider -> Raw -> Adapter -> Normalizer -> Validator -> Stream Guard -> MarketBuffer -> CandleClosed -> Engines

## Bootstrap

Cada engine declara historia mínima. El sistema calcula `max(required_history) + margin`.

## Buffer

Uno por MarketStreamKey:
- ordenado;
- idempotente;
- detecta duplicados;
- detecta correcciones;
- maneja out-of-order explícitamente.

## Lifecycle de vela

FORMING, CLOSED, CORRECTED, INVALID.

## Reconnect

Reconnect -> RESYNC con overlap -> deduplicación -> watermark actualizado.

## Replay

Live/replay/backtest usan el mismo pipeline y un logical clock. No look-ahead.
