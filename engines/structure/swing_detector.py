"""Detección inicial de Swing High y Swing Low."""

from __future__ import annotations

from typing import Sequence

from models.market_data import MarketData

from models.structure import Swing, SwingType

class SwingDetector:
    """Detecta pivotes confirmados mediante una ventana simétrica."""

    def __init__(self, left_bars: int = 2, right_bars: int = 2) -> None:
        if left_bars < 1 or right_bars < 1:
            raise ValueError("left_bars y right_bars deben ser mayores que cero")
        self.left_bars = left_bars
        self.right_bars = right_bars

    def detect(self, candles: Sequence[MarketData]) -> list[Swing]:
        required = self.left_bars + self.right_bars + 1
        if len(candles) < required:
            return []

        swings: list[Swing] = []
        start = self.left_bars
        stop = len(candles) - self.right_bars

        for index in range(start, stop):
            candidate = candles[index]
            left = candles[index - self.left_bars:index]
            right = candles[index + 1:index + 1 + self.right_bars]

            if all(candidate.high > candle.high for candle in (*left, *right)):
                swings.append(
                    Swing(SwingType.HIGH, index, candidate.high, candidate.time)
                )

            if all(candidate.low < candle.low for candle in (*left, *right)):
                swings.append(
                    Swing(SwingType.LOW, index, candidate.low, candidate.time)
                )

        return swings
