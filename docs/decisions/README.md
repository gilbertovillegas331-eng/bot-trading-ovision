# ADR Index — OVISION

**Estado:** ACTIVE

| ADR | Decisión | Estado |
|---:|---|---|
| 001 | Núcleo multi-mercado | APPROVED |
| 002 | Independencia del proveedor de datos | APPROVED |
| 003 | Separar CandleData y TickData | APPROVED |
| 004 | Rupturas estructurales confirmadas por cierre | APPROVED |
| 005 | Risk Engine obligatorio antes de ejecución | APPROVED |
| 006 | UTC como tiempo interno | APPROVED |
| 007 | Capacidades en lugar de condicionales por mercado | APPROVED |
| 008 | Eventos de dominio inmutables y trazables | APPROVED |
| 009 | Timeframe neutral al proveedor | APPROVED |
| 010 | Semántica explícita del volumen | APPROVED |
| 011 | Velas cerradas para estructura | APPROVED |
| 012 | Mismos motores para live y replay | APPROVED |
| 013 | Procesamiento idempotente | APPROVED |
| 014 | Resync obligatorio tras reconexión | APPROVED |
| 015 | Reloj lógico para replay y backtest | APPROVED |
| 016 | Separar pivote y clasificación estructural | APPROVED |
| 017 | Protected levels con lifecycle explícito | APPROVED |
| 018 | CHoCH inicia transición, no reversión instantánea | APPROVED |
| 019 | Comparaciones estructurales cuantizadas en ticks | APPROVED |
| 020 | Mecha puede ser sweep sin ser ruptura estructural | APPROVED |
| 021 | Estado estructural independiente por timeframe | APPROVED |
| 022 | Liquidity pools con lifecycle | APPROVED |
| 023 | Sweep requiere penetración y reclaim | APPROVED |
| 024 | FVG es imbalance, no pool de liquidez | APPROVED |
| 025 | No Order Blocks sin definición canónica | APPROVED |
| 026 | Liquidity score no es probabilidad | APPROVED |
| 027 | Separar observación e inferencia | APPROVED |
| 028 | Roles de timeframe, no timeframes fijos | APPROVED |
| 029 | El conflicto entre timeframes es información | APPROVED |
| 030 | ContextScore no representa probabilidad de éxito | APPROVED |
| 031 | Separar score y confidence | APPROVED |
| 032 | Calendarios y sesiones específicos por mercado | APPROVED |
| 033 | No double counting de evidencia correlacionada | APPROVED |
| 034 | Escenario antes de señal | APPROVED |
| 035 | No señal operativa sin invalidación | APPROVED |
| 036 | NO_TRADE es una salida de primera clase | APPROVED |
| 037 | SignalScore no es probabilidad | APPROVED |
| 038 | Toda señal tiene expiración | APPROVED |
| 039 | Paper trading obligatorio antes de ejecución real | APPROVED |
| 040 | Risk Engine autoriza capital | APPROVED |
| 041 | Ejecución live desactivada por defecto | APPROVED |
| 042 | Reserva de riesgo antes de enviar orden | APPROVED |
| 043 | No ampliar stop sin nueva autorización | APPROVED |
| 044 | Kill switch obligatorio | APPROVED |
| 045 | Paper y live usan el mismo Risk Engine | APPROVED |
| 046 | Redondeo conservador de tamaño | APPROVED |
| 047 | OrderIntent idempotente | APPROVED |
| 048 | El broker es fuente final de verdad en live | APPROVED |
| 049 | UNKNOWN requiere reconciliación | APPROVED |
| 050 | Paper y live comparten contrato de ejecución | APPROVED |
| 051 | Live requiere múltiples salvaguardas | APPROVED |
| 052 | Fallo de protección de stop es incidente crítico | APPROVED |
| 053 | Paper trading incluye costos y slippage | APPROVED |
| 054 | Explicación determinista antes de IA | APPROVED |
| 055 | IA no crea eventos de mercado | APPROVED |
| 056 | Grounding validation obligatoria | APPROVED |
| 057 | Proveedor de IA desacoplado | APPROVED |
| 058 | Fallo de IA no bloquea el núcleo | APPROVED |
| 059 | Observación, inferencia e hipótesis separadas | APPROVED |
| 060 | IA no modifica lógica productiva por sí sola | APPROVED |
| 061 | Números críticos se renderizan determinísticamente | APPROVED |
| 062 | Domain events append-only | APPROVED |
| 063 | Snapshots + event replay | APPROVED |
| 064 | Storage detrás de repositories | APPROVED |
| 065 | Replay datasets versionados e inmutables | APPROVED |
| 066 | Outcomes no modifican señales históricas | APPROVED |
| 067 | Cambios de schema requieren migraciones | APPROVED |
| 068 | Aislamiento de datos por ambiente | APPROVED |
| 069 | SQLite primero, no como compromiso final | APPROVED |
| 070 | Health y Readiness son conceptos distintos | APPROVED |
| 071 | Readiness basada en capacidades | APPROVED |
| 072 | Logging estructurado obligatorio | APPROVED |
| 073 | Modular monolith primero | APPROVED |
| 074 | Releases live requieren gates adicionales | APPROVED |
| 075 | Secretos nunca en configuración versionada | APPROVED |
| 076 | RBAC y mínimo privilegio | APPROVED |
| 077 | CI y release gates obligatorios | APPROVED |
| 078 | Observabilidad no depende de IA | APPROVED |
| 079 | Backtest utiliza el mismo core que producción | APPROVED |
| 080 | Out-of-sample obligatorio para validación | APPROVED |
| 081 | Research reproducible y versionado | APPROVED |
| 082 | Resultados negativos se conservan | APPROVED |
| 083 | Paper obligatorio antes de live | APPROVED |
| 084 | Promoción de estrategias como state machine | APPROVED |
| 085 | Costos y slippage obligatorios en validación | APPROVED |
| 086 | Bugs críticos se convierten en regression tests | APPROVED |
| 087 | Escenario y señal tienen UX distinta | APPROVED |
| 088 | NO_TRADE es visible en producto | APPROVED |
| 089 | PAPER y LIVE deben ser inequívocos | APPROVED |
| 090 | Warnings de riesgo no se ocultan por plan | APPROVED |
| 091 | APIs separadas por privilegio | APPROVED |
| 092 | Alertas event-driven y deduplicadas | APPROVED |
| 093 | Product tiers no cambian la verdad del mercado | APPROVED |
| 094 | Roadmap por capacidades completas | APPROVED |
| 095 | Live execution tiene roadmap independiente | APPROVED |
| 096 | Forex primero para validación, no como límite arquitectónico | APPROVED |
| 097 | Milestones avanzan por gates, no calendario | APPROVED |
| 098 | Decisiones arquitectónicas no se reescriben silenciosamente | APPROVED |
| 099 | Monetización no reduce seguridad | APPROVED |
| 100 | Pricing permanece hipótesis hasta tener datos | APPROVED |
| 101 | Core modular antes de expansión de producto | APPROVED |

Los ADR aprobados no se borran; un cambio requiere un ADR posterior que los superseda.
