OVISION Alpha 0.2.0 — Structure Engine

Estado del proyecto

Versión actual: Alpha 0.2.0
Objetivo: construcción del Structure Engine.

Rama de desarrollo: "alpha-0.2.0"

La rama se encuentra respaldada en GitHub y vinculada con:

"origin/alpha-0.2.0"

Baseline confirmado

Antes de comenzar modificaciones en Alpha 0.2.0 se ejecutó la suite completa de pruebas.

Resultado:

"156 passed"

Este resultado constituye el baseline oficial de Alpha 0.2.0.

Cualquier regresión posterior deberá ser identificada con respecto a este punto.

---

Principio de diseño

OVISION no debe limitarse a detectar rupturas de máximos o mínimos.

El Structure Engine debe interpretar la estructura de mercado de forma secuencial, trazable y explicable.

La detección de BOS y CHOCH dependerá de la estructura válida previamente identificada y del nivel estructural protegido.

No se acepta como regla:

"rompió máximo = BOS"

o:

"rompió mínimo = CHOCH"

sin contexto estructural previo.

---

Nomenclatura estructural confirmada

La nomenclatura oficial de OVISION para Alpha 0.2.0 es:

- "a+a = HH" — Higher High
- "b+a = HL" — Higher Low
- "a+b = LH" — Lower High
- "b+b = LL" — Lower Low

Estas relaciones deberán transformarse en reglas deterministas dentro del Structure Engine.

---

BOS

BOS — Break of Structure

Representa una ruptura que confirma la continuación de una estructura válida existente.

Un BOS no se determina únicamente porque el precio supere un máximo o un mínimo.

Debe conocerse previamente:

1. La estructura vigente.
2. Los swings confirmados.
3. La clasificación estructural.
4. El nivel relevante de continuación.
5. La dirección de la estructura.

---

CHOCH

CHOCH — Change of Character

Representa la ruptura de la estructura protegida en sentido contrario a la estructura vigente.

Para detectar un CHOCH debe existir previamente una estructura válida y un nivel protegido identificable.

El CHOCH representa una señal de cambio estructural y no una simple ruptura aislada.

---

Auditoría realizada

Se revisaron los siguientes componentes:

- "engines/structure_engine.py"
- "engines/structure/swing_detector.py"
- "engines/structure/trend_detector.py"
- "engines/structure/bos_detector.py"
- "engines/structure/choch_detector.py"
- "tests/test_swing_detector.py"
- "models/market_data.py"

Hallazgos principales

La arquitectura existente contiene:

Swing

"SwingType"

"Swing"

"SwingDetector"

Actualmente los objetos de dominio "SwingType" y "Swing" están definidos dentro de "swing_detector.py".

Trend

"Trend"

"TrendDetector"

Actualmente "trend_detector.py" depende directamente de los objetos definidos en "swing_detector.py".

BOS

"BosEvent"

"BosDetector"

CHOCH

"ChochEvent"

"ChochDetector"

Structure Engine

"StructureEngine"

Actualmente actúa como orquestador básico de componentes estructurales.

---

Cobertura de pruebas encontrada

Existe una prueba específica para:

"SwingDetector"

Archivo:

"tests/test_swing_detector.py"

La prueba actual confirma principalmente la detección de un Swing High sencillo.

No se encontraron pruebas específicas equivalentes para:

- TrendDetector
- BosDetector
- ChochDetector
- StructureEngine

Alpha 0.2.0 deberá ampliar esta cobertura antes de considerar estable el Structure Engine.

---

Arquitectura objetivo

La arquitectura propuesta para Alpha 0.2.0 deberá separar claramente:

Dominio estructural

Conceptos que representan qué ES la estructura:

- Swing
- SwingType
- StructureType
- Trend
- BreakType
- ProtectedLevel
- StructureEvent
- StructureState

Motores estructurales

Componentes responsables de determinar CÓMO se obtiene la estructura:

- SwingDetector
- StructureClassifier
- TrendDetector
- BosDetector
- ChochDetector

Orquestación

"StructureEngine"

Será responsable de coordinar todo el proceso y producir un resultado estructural trazable.

---

Flujo estructural objetivo

"MarketData"

↓

"SwingDetector"

↓

Swings confirmados

↓

"StructureClassifier"

↓

HH / HL / LH / LL

↓

"TrendDetector"

↓

Estructura vigente

↓

Nivel estructural protegido

↓

"BosDetector / ChochDetector"

↓

Eventos estructurales

↓

"StructureState"

↓

"StructureEngine"

---

Requisito de explicabilidad

Cada decisión importante del Structure Engine deberá poder responder:

- Qué ocurrió.
- Qué swing fue relevante.
- Qué estructura existía antes.
- Qué nivel estaba protegido.
- Qué nivel fue roto.
- Por qué la ruptura se clasificó como BOS o CHOCH.
- Qué estructura queda válida después del evento.

OVISION debe poder explicar sus conclusiones y no limitarse a devolver señales.

---

Orden de implementación Alpha 0.2.0

1. Formalizar contratos del dominio estructural.
2. Crear pruebas de clasificación HH / HL / LH / LL.
3. Implementar StructureClassifier.
4. Fortalecer pruebas de SwingDetector.
5. Formalizar TrendDetector sobre estructura clasificada.
6. Definir ProtectedLevel.
7. Crear pruebas deterministas de BOS.
8. Crear pruebas deterministas de CHOCH.
9. Integrar componentes en StructureEngine.
10. Añadir trazabilidad y explicación estructural.
11. Ejecutar suite completa de regresión.
12. Documentar y cerrar Alpha 0.2.0.

---

Criterio de finalización

Alpha 0.2.0 no se considerará terminada únicamente porque el código ejecute.

Debe cumplirse:

- Reglas estructurales formalizadas.
- HH / HL / LH / LL correctamente clasificados.
- BOS correctamente diferenciado de CHOCH.
- Nivel protegido explícito.
- Resultados trazables.
- Cobertura de pruebas adecuada.
- Sin regresiones respecto al baseline.
- Suite completa en verde.
- Documentación actualizada.

---

Checkpoint

Estado actual: auditoría del código existente terminada.

Baseline: 156 pruebas aprobadas.

Siguiente fase: formalización del dominio estructural y creación de las primeras pruebas contractuales de Alpha 0.2.0.