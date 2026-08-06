"""Detección inicial de Break of Structure (BOS)."""

from __future__ import annotations

from dataclasses import dataclass

from engines.structure.swing_detector import Swing
from engines.structure.trend_detector import Trend
from models.market_data import MarketData


@dataclass(frozen=True, slots=True)
class BosEvent:
    direction: Trend
    broken_level: float
    candle_time: int
    close_price: float


class BosDetector:
    """Confirma BOS por cierre sobre/bajo el swing relevante."""

    def detect(
        self,
        trend: Trend,
        closed_candle: MarketData,
        last_swing_high: Swing | None,
        last_swing_low: Swing | None,
    ) -> BosEvent | None:
        if (
            trend == Trend.BULLISH
            and last_swing_high is not None
            and closed_candle.close > last_swing_high.price
        ):
            return BosEvent(
                direction=Trend.BULLISH,
                broken_level=last_swing_high.price,
                candle_time=closed_candle.time,
                close_price=closed_candle.close,
            )

        if (
            trend == Trend.BEARISH
            and last_swing_low is not None
            and closed_candle.close < last_swing_low.price
        ):
            return BosEvent(
                direction=Trend.BEARISH,
                broken_level=last_swing_low.price,
                candle_time=closed_candle.time,
                close_price=closed_candle.close,
            )

        return None
