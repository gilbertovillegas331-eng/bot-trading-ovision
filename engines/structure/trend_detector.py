"""Clasificación inicial de tendencia mediante swings confirmados."""

from __future__ import annotations

from typing import Sequence

from models.structure import Swing, SwingType, Trend


class TrendDetector:

    """Determina tendencia con los dos últimos highs y lows confirmados."""

    def detect(self, swings: Sequence[Swing]) -> Trend:
        highs = [s for s in swings if s.kind == SwingType.HIGH]
        lows = [s for s in swings if s.kind == SwingType.LOW]

        if len(highs) < 2 or len(lows) < 2:
            return Trend.NEUTRAL

        previous_high, current_high = highs[-2], highs[-1]
        previous_low, current_low = lows[-2], lows[-1]

        if current_high.price > previous_high.price and current_low.price > previous_low.price:
            return Trend.BULLISH

        if current_high.price < previous_high.price and current_low.price < previous_low.price:
            return Trend.BEARISH

        return Trend.NEUTRAL
