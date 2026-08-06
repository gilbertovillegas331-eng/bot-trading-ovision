"""Coordinador inicial del motor de estructura."""

from __future__ import annotations

from engines.structure.swing_detector import SwingDetector
from engines.structure.trend_detector import Trend, TrendDetector
from models.market_data import MarketData


class StructureEngine:
    """Coordina la detección de swings y tendencia."""

    def __init__(self) -> None:
        self.swing_detector = SwingDetector()
        self.trend_detector = TrendDetector()

    def analyze(self, candles: list[MarketData]) -> dict:
        swings = self.swing_detector.detect(candles)
        trend = self.trend_detector.detect(swings)
        return {
            "trend": trend.value,
            "swings": swings,
        }
