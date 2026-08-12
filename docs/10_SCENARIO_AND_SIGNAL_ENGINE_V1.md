# Scenario & Signal Engine v1

## Flujo

Context -> Scenario -> Signal Eligibility -> Signal -> Risk

## Scenario lifecycle

DRAFT, WATCHING, ARMED, CONFIRMED, INVALIDATED, EXPIRED, COMPLETED, CANCELLED.

## Signal

Debe contener:
- direction;
- entry model/zone;
- invalidation;
- targets;
- score;
- confidence;
- evidence;
- risks;
- data quality;
- profile versions;
- expiration.

## Regla central

No existe señal operativa sin invalidación objetiva.

## NO_TRADE

Salida de primera clase con razones explícitas.

## Outcome

Se registra después; nunca reescribe la señal histórica.
