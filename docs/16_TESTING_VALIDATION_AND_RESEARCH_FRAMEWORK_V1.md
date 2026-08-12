# Testing, Validation & Research Framework v1

## Test types

UNIT, INTEGRATION, CONTRACT, PROPERTY, REGRESSION, REPLAY, SYSTEM, CHAOS, SECURITY, PERFORMANCE, RESEARCH.

## Reglas

- Bugs críticos generan regression tests.
- Golden datasets versionados.
- Backtest usa el mismo core.
- No look-ahead.
- OOS obligatorio.
- Walk-forward.
- Parameter robustness.
- Costs/slippage realistas.
- Negative results se conservan.
- Paper antes de live.

## Promotion states

RESEARCH, VALIDATED, PAPER_ELIGIBLE, PAPER_ACTIVE, LIVE_CANDIDATE, LIVE_APPROVED, RETIRED.

## Principio

OVISION no debe optimizarse para “verse bien” en el pasado.
