# Risk Engine v1

## Flujo

Signal -> RiskEvaluation -> RiskDecision -> Execution

Decisiones:
APPROVED, APPROVED_REDUCED, REJECTED, BLOCKED, ERROR.

## Controles

- per trade;
- daily/weekly;
- max open risk;
- symbol/market exposure;
- correlation groups;
- spread/slippage;
- session/event;
- drawdown;
- kill switch;
- sizing.

## Position sizing

Basado en invalidación + InstrumentSpec. Si faltan specs esenciales, no dimensionar.

## Live

Desactivado por defecto.

## Reservation

RESERVED, COMMITTED, RELEASED para evitar race conditions.

## Regla

No ampliar un stop sin nueva RiskDecision.
