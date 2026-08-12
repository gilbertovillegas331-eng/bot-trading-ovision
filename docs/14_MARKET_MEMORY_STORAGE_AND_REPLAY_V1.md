# Market Memory, Storage & Replay v1

## Storage domains

MARKET_DATA, DOMAIN_EVENTS, STATE_SNAPSHOTS, SIGNALS, OUTCOMES, EXECUTION, AUDIT, USER_PRODUCT, CONFIGURATION, RESEARCH.

## Eventos

Append-only con envelope versionado.

## Snapshots

Structure/Liquidity/Context/Risk/Execution snapshots + replay de eventos para recuperación.

## Repositories

Engines no escriben SQL directamente.

## Inicial

SQLite local está permitido; arquitectura preparada para evolucionar.

## Replay

ReplayDataset y ReplayManifest versionados con checksum, code version, engine/profile versions, logical clock y seed.

Mismo manifest + diferente output hash = fallo de reproducibilidad.
