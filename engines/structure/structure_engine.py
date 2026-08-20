from models.market_data import MarketData
from models.structure import StructureAnalysis

from engines.structure.swing_detector import SwingDetector
from engines.structure.trend_detector import TrendDetector


class StructureEngine:
    """Coordina la detección de swings y tendencia."""

    def __init__(self) -> None:
        self.swing_detector = SwingDetector()
        self.trend_detector = TrendDetector()

    def analyze(self, candles: list[MarketData]) -> StructureAnalysis:
        swings = self.swing_detector.detect(candles)
        trend = self.trend_detector.detect(swings)

        return StructureAnalysis(
            trend=trend,
            swings=swings,
        )

