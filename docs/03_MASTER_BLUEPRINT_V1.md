# OVISION Master Blueprint v1

## Capas

1. Boot & Configuration
2. Provider/Broker Adapters
3. Market Data
4. Market State & Buffer
5. Structure Engine
6. Liquidity Engine
7. Volatility & Session
8. Market Context / MTF
9. Market Memory
10. Scenario Engine
11. Signal Engine
12. Risk Engine
13. Explain Engine
14. AI Layer
15. Platform / Observability

Execution es downstream de Risk y permanece separada.

## Flujo conceptual

Provider -> Normalize -> Validate -> Buffer -> Domain Events -> Structure -> Liquidity -> Context -> Scenario -> Signal -> Risk -> Execution

## Principios

- Domain sin imports de MT5.
- Mismos engines en live/replay/backtest.
- Multi-market por capacidades.
- No large rewrite.
- Evidencia trazable.
- IA nunca crea hechos de mercado.
