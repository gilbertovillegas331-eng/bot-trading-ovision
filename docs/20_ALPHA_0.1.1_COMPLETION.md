# OVISION Alpha 0.1.1 — Completion Record

## Status

Alpha 0.1.1 completes the provider-neutral market-data foundation planned for OVISION.

The release introduces canonical domain contracts, bounded in-memory market storage, and the first MetaTrader 5 translation layer without coupling the core domain to MT5.

This release does not add live trading, order execution, signal generation, risk management, or AI decision-making.

---

## Objectives Completed

Alpha 0.1.1 establishes a stable foundation for future market-data and strategy components.

Implemented capabilities include:

- Provider-neutral market types.
- Provider-neutral timeframes.
- Canonical instrument identity and specifications.
- Instrument capabilities.
- Canonical candle data.
- Canonical tick data.
- Explicit volume semantics.
- Market stream identity.
- Data-quality representation.
- Bounded market-data buffer.
- MetaTrader 5 timeframe mapping.
- MetaTrader 5 candle normalization.
- MetaTrader 5 tick normalization.
- UTC-normalized timestamps.
- Regression coverage for the new domain contracts.

---

## Architectural Boundary

The OVISION domain remains independent from MetaTrader 5.

The intended dependency direction is:

Provider data
-> Provider adapter
-> Canonical OVISION domain contracts
-> Data storage / analysis
-> Future strategy components

MetaTrader 5 constants and provider-specific record formats are contained inside:

`providers/mt5/`

The domain layer does not import MetaTrader 5.

---

## Canonical Domain Components

Alpha 0.1.1 introduces or strengthens the following domain concepts:

### MarketType

Canonical classification for supported market families, including:

- Forex
- Index
- Synthetic index
- Futures

### Timeframe

Timeframes are represented by fixed duration rather than provider-specific constants.

Example:

`Timeframe.from_minutes(15)`

is a domain concept independent of:

`mt5.TIMEFRAME_M15`

Provider mappings are handled by adapters.

Calendar-month timeframes are not forced into a fixed-second representation because month duration is variable.

### InstrumentId

Provides stable instrument identity independent of broker/provider symbol formatting.

### InstrumentSpec

Describes canonical instrument characteristics.

### InstrumentCapabilities

Represents what an instrument supports without assuming all market types behave identically.

### CandleData

Canonical OHLC market-data contract containing:

- Instrument identity
- Timeframe
- UTC open time
- UTC close time
- Open
- High
- Low
- Close
- Volume
- Volume semantics
- Closed/forming state
- Source

### TickData

Canonical tick contract containing:

- Instrument identity
- UTC timestamp
- Bid
- Ask
- Last
- Volume
- Volume semantics
- Source

### VolumeType

Volume meaning is explicit rather than inferred.

Supported semantics include:

- NONE
- TICK
- REAL
- CONTRACTS

### MarketStreamKey

Provides a canonical key for identifying a market-data stream.

### DataQuality

Allows data quality to be represented explicitly instead of being silently assumed.

---

## MarketBuffer

Alpha 0.1.1 adds a bounded in-memory market-data buffer.

The buffer is designed to:

- Keep recent market data available for downstream analysis.
- Prevent unbounded memory growth.
- Preserve stream separation.
- Provide deterministic behavior suitable for testing.
- Remain independent from network/provider concerns.

Persistent historical storage is outside the scope of this release.

---

## MetaTrader 5 Adapter Layer

### Timeframe Mapper

The MT5 timeframe mapper translates between:

OVISION `Timeframe`

and:

MetaTrader 5 `TIMEFRAME_*` constants.

The mapper does not require a live terminal connection for pure translation.

Unsupported mappings fail explicitly instead of silently producing incorrect values.

### Market-Data Normalizers

MT5 normalizers translate provider records into canonical OVISION contracts.

Rate normalization produces:

`CandleData`

Tick normalization produces:

`TickData`

Responsibilities include:

- UTC timestamp normalization.
- OHLC translation.
- Tick price translation.
- Explicit volume semantics.
- Provider source tagging.
- Canonical instrument identity.
- Canonical timeframe assignment.

Provider-specific field names do not leak into the domain layer.

---

## Testing

Alpha 0.1.1 was developed incrementally with regression tests.

At the completion stage, the full automated test suite reports:

`156 passed`

The suite covers the original OVISION behavior together with the new Alpha 0.1.1 contracts, buffer, mappings, and normalizers.

Final acceptance requires the full suite to remain green after this documentation update.

---

## Compatibility

Alpha 0.1.1 is additive.

Existing Alpha 0.1.0 behavior is preserved while the new provider-neutral architecture is introduced alongside it.

Migration of older components onto the canonical contracts can therefore occur incrementally instead of through a destructive rewrite.

---

## Explicit Non-Goals

Alpha 0.1.1 does not implement:

- Trading signals
- Strategy execution
- Order placement
- Position management
- Risk engine
- Liquidity engine
- AI decision engine
- Broker-account orchestration
- Live automated trading
- Production deployment

Those capabilities must build on top of the canonical contracts rather than bypass them.

---

## Acceptance Criteria

Alpha 0.1.1 is considered complete when:

1. Canonical market-data contracts exist.
2. Provider-specific MT5 concepts remain outside the domain.
3. Candle and tick timestamps use UTC.
4. Volume semantics are explicit.
5. Market streams can be identified canonically.
6. Market-data buffering is bounded.
7. MT5 timeframes can be translated explicitly.
8. MT5 rates can be normalized into CandleData.
9. MT5 ticks can be normalized into TickData.
10. Existing behavior remains regression-safe.
11. The complete automated test suite passes.
12. The Git working tree is clean after the final commit.

---

## Result

Alpha 0.1.1 establishes the first reusable market-data foundation for OVISION.

The project now has a clear separation between:

- Domain
- Data
- Provider adapters

This separation allows future integrations and trading intelligence to depend on stable canonical contracts instead of directly depending on MetaTrader 5.

The next development phase should build on these boundaries rather than introduce provider dependencies into the core.