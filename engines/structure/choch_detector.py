"""Detección inicial de Change of Character (CHOCH)."""

from __future__ import annotations

from dataclasses import dataclass

from engines.structure.swing_detector import Swing
from engines.structure.trend_detector import Trend
from models.market_data import MarketData


@dataclass(frozen=True, slots=True)
class ChochEvent:
    prior_trend: Trend
    new_direction: Trend
    broken_level: float
    candle_time: int
    close_price: float


class ChochDetector:
    """Detecta ruptura confirmada contra la tendencia previa."""

    def detect(
        self,
        prior_trend: Trend,
        closed_candle: MarketData,
        protected_high: Swing | None,
        protected_low: Swing | None,
    ) -> ChochEvent | None:
        if (
            prior_trend == Trend.BULLISH
            and protected_low is not None
            and closed_candle.close < protected_low.price
        ):
            return ChochEvent(
                prior_trend=Trend.BULLISH,
                new_direction=Trend.BEARISH,
                broken_level=protected_low.price,
                candle_time=closed_candle.time,
                close_price=closed_candle.close,
            )

        if (
            prior_trend == Trend.BEARISH
            and protected_high is not None
            and closed_candle.close > protected_high.price
        ):
            return ChochEvent(
                prior_trend=Trend.BEARISH,
                new_direction=Trend.BULLISH,
                broken_level=protected_high.price,
                candle_time=closed_candle.time,
                close_price=closed_candle.close,
            )

        return None
