from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from domain.instrument import InstrumentId
from domain.timeframe import Timeframe


class DataQuality(str, Enum):
    GOOD = "good"
    STALE = "stale"
    GAP = "gap"
    INVALID = "invalid"


@dataclass(frozen=True, slots=True)
class MarketStreamKey:
    instrument_id: InstrumentId
    timeframe: Timeframe | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.instrument_id, InstrumentId):
            raise TypeError(
                "instrument_id must be an InstrumentId"
            )

        if (
            self.timeframe is not None
            and not isinstance(self.timeframe, Timeframe)
        ):
            raise TypeError(
                "timeframe must be a Timeframe or None"
            )