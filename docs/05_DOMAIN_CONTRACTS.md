# Domain Contracts v1

## Contratos

### MarketType
FOREX, INDEX, SYNTHETIC_INDEX, FUTURES.

### InstrumentSpec
Incluye identidad canónica, símbolo de proveedor, market_type, tick_size, tick_value cuando aplique, contract_size, timezone, exchange, expiry y capabilities.

### InstrumentCapabilities
Bid/ask, last, tick volume, real volume, open interest, depth, prints, execution.

### Timeframe
Objeto neutral al proveedor.

### CandleData
OHLC, volumen con semántica explícita, open_time/close_time, estado cerrado/forming, source.

### TickData
Timestamp, bid, ask, last opcional, volume opcional, source.

### VolumeType
NONE, TICK, REAL, CONTRACTS.

### DataQuality
GOOD, DEGRADED, INVALID.

### DomainEvent
event_id, occurred_at, observed_at, instrument, timeframe, source/engine/version, correlation_id, causation_id.

## Reglas

- UTC interno.
- Datos inmutables una vez confirmados.
- Missing no equivale a cero.
- Finite values.
- Cuantización según tick_size.
