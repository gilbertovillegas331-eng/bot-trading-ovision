# Alpha 0.1.1 — Domain & Data Foundation

**Estado:** READY FOR IMPLEMENTATION

## Objetivo

Introducir contratos neutrales al proveedor y MarketBuffer sin romper Alpha 0.1.0.

## Scope IN

- MarketType
- Timeframe
- InstrumentId / InstrumentSpec
- InstrumentCapabilities
- VolumeType
- CandleData
- TickData
- MarketStreamKey
- DataQuality
- MarketBuffer
- MT5 Timeframe Mapper
- MT5 normalizers
- tests

## Scope OUT

No implementar aún:
- event bus;
- replay completo;
- structure state completo;
- liquidity;
- context;
- signals;
- risk;
- execution;
- API;
- AI.

## Orden de commits

1. Test scaffold
2. MarketType + Timeframe
3. InstrumentSpec + capabilities
4. CandleData
5. TickData
6. MarketStreamKey + DataQuality
7. MarketBuffer
8. MT5 Timeframe Mapper
9. MT5 normalizers
10. Regression + docs

## Regla

Test first:
failing test -> minimum implementation -> green -> refactor.

## Backward compatibility

No borrar `MarketData` aún. Legacy tests deben seguir verdes.

## Definition of Done

- contratos nuevos existen;
- Candle/Tick separados;
- Timeframe provider-neutral;
- MarketBuffer determinista;
- tests cubren edge cases;
- no live;
- docs actualizadas.
