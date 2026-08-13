from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True, slots=True, order=True)
class Timeframe:
    seconds: int

    def __post_init__(self) -> None:
        if isinstance(self.seconds, bool):
            raise TypeError("seconds must be an integer")

        if not isinstance(self.seconds, int):
            raise TypeError("seconds must be an integer")

        if self.seconds <= 0:
            raise ValueError("seconds must be greater than zero")

    @classmethod
    def from_minutes(cls, minutes: int) -> "Timeframe":
        return cls(seconds=minutes * 60)

    @classmethod
    def from_hours(cls, hours: int) -> "Timeframe":
        return cls(seconds=hours * 60 * 60)

    @classmethod
    def from_days(cls, days: int) -> "Timeframe":
        return cls(seconds=days * 24 * 60 * 60)

    @property
    def duration(self) -> timedelta:
        return timedelta(seconds=self.seconds)