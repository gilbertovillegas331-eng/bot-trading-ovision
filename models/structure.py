"""Contratos de dominio para la estructura de mercado de OVISION."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class SwingType(str, Enum):
    """Tipo de pivote estructural confirmado."""

    HIGH = "SWING_HIGH"
    LOW = "SWING_LOW"


@dataclass(frozen=True, slots=True)
class Swing:
    """Pivote estructural confirmado del mercado."""

    kind: SwingType
    index: int
    price: float
    time: int


class StructureType(str, Enum):
    """Clasificación estructural de un swing confirmado."""

    HH = "HH"
    HL = "HL"
    LH = "LH"
    LL = "LL"


class Trend(str, Enum):
    """Dirección estructural
 vigente."""

    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"

@dataclass(frozen=True,
slots=True)
class StructureAnalysis:
    """Resultado del análisis 
de estructura de mercado."""

    trend: Trend
    swings: list[Swing]
    bos: bool = False
    choch: bool = False