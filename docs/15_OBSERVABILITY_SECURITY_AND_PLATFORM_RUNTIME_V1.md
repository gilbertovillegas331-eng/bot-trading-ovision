# Observability, Security & Platform Runtime v1

## Lifecycle

BOOTING, CONFIGURED, INITIALIZING, CONNECTING, CONNECTED, DATA_READY, ENGINES_READY, RUNNING, DEGRADED, BLOCKED, STOPPING, STOPPED, ERROR.

## Health vs Readiness

Health: HEALTHY, DEGRADED, UNHEALTHY.  
Readiness: READY, NOT_READY, BLOCKED.

Capacidades:
ANALYSIS_READY, SIGNALS_READY, PAPER_READY, LIVE_READY, AI_READY.

## Observability

- structured logs;
- metrics;
- correlation IDs;
- tracing;
- incidents;
- alerts.

## Security

- RBAC;
- least privilege;
- secrets fuera del repo;
- auth/authz separados;
- privileged-action audit;
- rate limits.

## Deployment

Modular monolith primero. CI/release gates obligatorios.
