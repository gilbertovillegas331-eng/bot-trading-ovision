# Audit Alpha 0.1.0

## Estado actual

La Alpha 0.1.0 es una base de ingeniería, no un bot operativo continuo.

Flujo actual:
`app/main.py -> OviCore -> config/logger -> mensaje de espera -> exit`

## Hallazgos principales

- MT5Service existe, pero Core no lo integra.
- VisionEngine obtiene una vela cerrada y un tick actual, mezclando momentos distintos en MarketData.
- SwingDetector requiere historial; VisionEngine entrega una sola vela.
- BOS/CHoCH existen, pero StructureEngine no los integra.
- No existe lifecycle de protected levels.
- LiquidityEngine es skeleton.
- No hay buffer histórico ni resync.
- No hay estado persistente de estructura.
- No existe Risk Engine ni Execution Engine real.
- Config flags de MT5/engines no gobiernan runtime.
- Tests mínimos.
- `system_ready=True` no representa readiness real.
- Secrets no deben vivir en settings versionados.

## Conclusión

La base es válida como fundación, pero requiere evolución incremental antes de señales fiables o ejecución.
