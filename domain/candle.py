from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from math import isfinite

from domain.instrument import InstrumentId, VolumeType
from domain.timeframe import Timeframe


def _is_utc(value: datetime) -> bool:
    return (
        value.tzinfo is not None
        and value.utcoffset() == timedelta(0)
    )


@dataclass(frozen=True, slots=True)
class CandleData:
    instrument_id: InstrumentId
    timeframe: Timeframe

    open_time: datetime
    close_time: datetime

    open: float
    high: float
    low: float
    close: float

    volume: float | None
    volume_type: VolumeType

    is_closed: bool
    source: str

    def __post_init__(self) -> None:
        if not _is_utc(self.open_time):
            raise ValueError("open_time must be UTC")

        if not _is_utc(self.close_time):
            raise ValueError("close_time must be UTC")

        if self.close_time <= self.open_time:
            raise ValueError(
                "close_time must be after open_time"
            )

        for price in (
            self.open,
            self.high,
            self.low,
            self.close,
        ):
            if not isfinite(price):
                raise ValueError(
                    "OHLC prices must be finite"
                )

        if self.high < self.low:
            raise ValueError(
                "high cannot be below low"
            )

        if not self.low <= self.open <= self.high:
            raise ValueError(
                "open must be between low and high"
            )

        if not self.low <= self.close <= self.high:
            raise ValueError(
                "close must be between low and high"
            )
        if self.volume is None:
            if self.volume_type is not VolumeType.NONE:
                raise ValueError(
                    "missing volume requires VolumeType.NONE"
                )
        else:
            if not isfinite(self.volume):
                raise ValueError(
                    "volume must be finite"
                )

            if self.volume < 0:
                raise ValueError(
                    "volume cannot be negative"
                )

            if self.volume_type is VolumeType.NONE:
                raise ValueError(
                    "VolumeType.NONE requires no volume"
                )

        if not isinstance(self.is_closed, bool):
            raise TypeError(
                "is_closed must be a boolean"
            )

        if not isinstance(self.source, str):
            raise TypeError(
                "source must be a string"
            )

        source = self.source.strip()

        if not source:
            raise ValueError(
                "source cannot be empty"
            )

        object.__setattr__(
            self,
            "source",
            source,
        )