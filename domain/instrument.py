from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from math import isfinite

from domain.market_type import MarketType


class VolumeType(str, Enum):
    NONE = "none"
    TICK = "tick"
    REAL = "real"
    CONTRACTS = "contracts"


@dataclass(frozen=True, slots=True)
class InstrumentId:
    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str):
            raise TypeError("instrument id must be a string")

        cleaned = self.value.strip()

        if not cleaned:
            raise ValueError("instrument id cannot be empty")

        object.__setattr__(self, "value", cleaned)


@dataclass(frozen=True, slots=True)
class InstrumentCapabilities:
    bid_ask: bool = False
    last_price: bool = False
    tick_volume: bool = False
    real_volume: bool = False
    open_interest: bool = False
    market_depth: bool = False
    trade_prints: bool = False
    execution: bool = False


@dataclass(frozen=True, slots=True)
class InstrumentSpec:
    instrument_id: InstrumentId
    market_type: MarketType
    tick_size: float
    digits: int
    capabilities: InstrumentCapabilities

    tick_value: float | None = None
    contract_size: float | None = None

    base_currency: str | None = None
    quote_currency: str | None = None

    exchange: str | None = None
    timezone: str | None = None

    provider_symbol: str | None = None
    expiry: datetime | None = None

    def __post_init__(self) -> None:
        if not isfinite(self.tick_size) or self.tick_size <= 0:
            raise ValueError(
                "tick_size must be finite and greater than zero"
            )

        if isinstance(self.digits, bool) or not isinstance(self.digits, int):
            raise TypeError("digits must be an integer")

        if self.digits < 0:
            raise ValueError("digits cannot be negative")

        if self.tick_value is not None:
            if not isfinite(self.tick_value) or self.tick_value <= 0:
                raise ValueError(
                    "tick_value must be finite and greater than zero"
                )

        if self.contract_size is not None:
            if (
                not isfinite(self.contract_size)
                or self.contract_size <= 0
            ):
                raise ValueError(
                    "contract_size must be finite and greater than zero"
                )

        if self.provider_symbol is not None:
            provider_symbol = self.provider_symbol.strip()

            if not provider_symbol:
                raise ValueError(
                    "provider_symbol cannot be empty"
                )

            object.__setattr__(
                self,
                "provider_symbol",
                provider_symbol,
            )