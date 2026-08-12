# OVISION Architecture v1

## Estilo

**Modular monolith** inicialmente.

Áreas objetivo:
- domain/
- providers/
- data/
- engines/
- memory/
- risk/
- execution/
- storage/
- platform/
- observability/
- security/
- tests/
- research/

## Reglas de dependencia

- `domain` no depende de providers, DB, red ni IA.
- providers traducen datos externos a contratos canónicos.
- engines consumen dominio.
- Risk decide si capital puede usarse.
- Execution solo consume decisiones de riesgo aprobadas.
- UI/API nunca contienen lógica de mercado canónica.

## Migración

Incremental, testeable y reversible. No reescritura total.
