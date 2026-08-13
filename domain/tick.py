from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from math import isfinite

from domain.instrument import InstrumentId, VolumeType


def _is_utc(value: datetime) -> bool:
    return (
        value.tzinfo is not None
        and value.utcoffset() == timedelta(0)
    )


@dataclass(frozen=True, slots=True)
class TickData:
    instrument_id: InstrumentId
    timestamp: datetime

    bid: float | None
    ask: float | None
    last: float | None

    volume: float | None
    volume_type: VolumeType

    source: str

    def __post_init__(self) -> None:
        if not _is_utc(self.timestamp):
            raise ValueError("timestamp must be UTC")

        if (
            self.bid is None
            and self.ask is None
            and self.last is None
        ):
            raise ValueError(
                "at least one price is required"
            )

        for price in (
            self.bid,
            self.ask,
            self.last,
        ):
            if price is not None and not isfinite(price):
                raise ValueError(
                    "prices must be finite"
                )

        if (
            self.bid is not None
            and self.ask is not None
            and self.bid > self.ask
        ):
            raise ValueError(
                "bid cannot be above ask"
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