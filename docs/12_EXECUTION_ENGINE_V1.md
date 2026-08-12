# Execution Engine v1

## Flujo

Approved RiskDecision -> OrderIntent -> ExecutionEngine -> BrokerAdapter -> Orders/Fills/Positions -> Reconciliation

## OrderIntent

Inmutable e idempotente. Incluye client_order_id/idempotency key.

## Estados

Debe existir UNKNOWN para incertidumbre real.

## Reconciliation

En live, el broker es fuente final de verdad. Startup/reconnect/timeout requieren reconciliación.

## Paper

Comparte contratos con live e incluye costos/slippage.

## Seguridad

- kill switch;
- account allowlist;
- stale intent checks;
- hard caps;
- stop protection critical;
- live flags explícitos.
