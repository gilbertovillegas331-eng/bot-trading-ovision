"""
Detector de eventos estructurales de OVISION.

Responsabilidad:
Detectar BOS y CHOCH sobre estructura confirmada.
"""

from dataclasses import dataclass
from enum import Enum

from models.structure import Trend, StructureType


class StructureEvent(str, Enum):
    BOS = "BOS"
    CHOCH = "CHOCH"


@dataclass(frozen=True)
class StructureEventResult:
    event: StructureEvent
    previous_trend: Trend
    new_trend: Trend
    structure: StructureType


class StructureEventDetector:

    def detect(
        self,
        trend: Trend,
        structure: StructureType
    ) -> StructureEventResult | None:

        if trend == Trend.BULLISH and structure == StructureType.HH:
            return StructureEventResult(
                event=StructureEvent.BOS,
                previous_trend=Trend.BULLISH,
                new_trend=Trend.BULLISH,
                structure=structure,
            )

        if trend == Trend.BEARISH and structure == StructureType.LL:
            return StructureEventResult(
                event=StructureEvent.BOS,
                previous_trend=Trend.BEARISH,
                new_trend=Trend.BEARISH,
                structure=structure,
            )

        if trend == Trend.BULLISH and structure == StructureType.LL:
            return StructureEventResult(
                event=StructureEvent.CHOCH,
                previous_trend=Trend.BULLISH,
                new_trend=Trend.BEARISH,
                structure=structure,
            )

        if trend == Trend.BEARISH and structure == StructureType.HH:
            return StructureEventResult(
                event=StructureEvent.CHOCH,
                previous_trend=Trend.BEARISH,
                new_trend=Trend.BULLISH,
                structure=structure,
            )

        return None