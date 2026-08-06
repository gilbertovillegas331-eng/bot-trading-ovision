# OVISION

**Versión:** Alpha 0.1.0  
**Estado:** En desarrollo  
**Fundador y director del proyecto:** Gilberto Villegas

## Propósito

OVISION es una plataforma profesional de inteligencia para el análisis de mercados. Su objetivo es organizar evidencias, construir escenarios y explicar el razonamiento del sistema con transparencia.

> **OVISION no intenta adivinar el mercado. OVISION ayuda a comprenderlo.**

## Alcance de Alpha 0.1.0

- Iniciar OVI CORE.
- Cargar configuración.
- Crear registros del sistema.
- Preparar la conexión con MetaTrader 5.
- Obtener y validar datos OHLC.
- Establecer la base del Vision Engine.
- Preparar la estructura para Swings, tendencia, BOS y CHOCH.

## Estructura

```text
OVISION/
├── app/                 Punto de entrada
├── core/                OVI CORE y registros
├── config/              Configuración
├── engines/             Motores de análisis
├── models/              Objetos de datos
├── services/            Integraciones externas
├── tests/               Pruebas automáticas
├── docs/                Documentación oficial
├── logs/                Registros locales
└── assets/              Recursos visuales
```

## Requisitos

- Python 3.11 o superior.
- Windows.
- MetaTrader 5 instalado para la integración en vivo.

## Inicio rápido

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m app.main
```

## Estado documental

- Hito 1: Arquitectura y Fundación — cerrado.
- Hito 2: Ingeniería e Implementación — cerrado.
- Hito 3: Alpha 0.1.0 Foundation — activo.

## Propiedad intelectual

Proyecto privado. Todos los derechos reservados hasta que el titular defina otra licencia.
