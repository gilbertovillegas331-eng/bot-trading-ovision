"""Modelos de datos del mercado utilizados por OVISION."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True, slots=True)
class MarketData:
    symbol: str
    timeframe: str
    time: int
    open: float
    high: float
    low: float
    close: float
    bid: float
    ask: float
    tick_volume: int

    @property
    def timestamp(self) -> datetime:
        return datetime.fromtimestamp(self.time, tz=timezone.utc)

    def is_valid(self) -> bool:
        prices_positive = all(
            value > 0
            for value in (
                self.open,
                self.high,
                self.low,
                self.close,
                self.bid,
                self.ask,
            )
        )
        ohlc_consistent = (
            self.high >= max(self.open, self.close)
            and self.low <= min(self.open, self.close)
            and self.high >= self.low
        )
        spread_valid = self.ask >= self.bid
        return prices_positive and ohlc_consistent and spread_valid
