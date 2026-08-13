from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from domain.candle import CandleData, VolumeType
from domain.instrument import InstrumentId
from domain.tick import TickData
from domain.timeframe import Timeframe


_MISSING = object()


def _get_field(
    record: Any,
    name: str,
    default: Any = _MISSING,
) -> Any:
    try:
        return record[name]
    except (KeyError, IndexError, TypeError):
        pass

    try:
        return getattr(record, name)
    except AttributeError:
        if default is _MISSING:
            raise KeyError(
                f"missing MT5 field: {name}"
            )

        return default


def normalize_mt5_rate(
    rate: Any,
    *,
    instrument_id: InstrumentId,
    timeframe: Timeframe,
    is_closed: bool = True,
) -> CandleData:
    if not isinstance(instrument_id, InstrumentId):
        raise TypeError(
            "instrument_id must be an InstrumentId"
        )

    if not isinstance(timeframe, Timeframe):
        raise TypeError(
            "timeframe must be a Timeframe"
        )

    if not isinstance(is_closed, bool):
        raise TypeError(
            "is_closed must be a boolean"
        )

    open_time = datetime.fromtimestamp(
        float(_get_field(rate, "time")),
        tz=timezone.utc,
    )

    close_time = open_time + timeframe.duration

    real_volume = float(
        _get_field(rate, "real_volume", 0) or 0
    )

    tick_volume = _get_field(
        rate,
        "tick_volume",
        None,
    )

    if real_volume > 0:
        volume = real_volume
        volume_type = VolumeType.REAL

    elif tick_volume is not None:
        volume = float(tick_volume)
        volume_type = VolumeType.TICK

    else:
        volume = None
        volume_type = VolumeType.NONE

    return CandleData(
        instrument_id=instrument_id,
        timeframe=timeframe,
        open_time=open_time,
        close_time=close_time,
        open=float(_get_field(rate, "open")),
        high=float(_get_field(rate, "high")),
        low=float(_get_field(rate, "low")),
        close=float(_get_field(rate, "close")),
        volume=volume,
        volume_type=volume_type,
        is_closed=is_closed,
        source="mt5",
    )


def normalize_mt5_tick(
    tick: Any,
    *,
    instrument_id: InstrumentId,
) -> TickData:
    if not isinstance(instrument_id, InstrumentId):
        raise TypeError(
            "instrument_id must be an InstrumentId"
        )

    time_msc = _get_field(
        tick,
        "time_msc",
        None,
    )

    if time_msc is not None and float(time_msc) > 0:
        timestamp_value = float(time_msc) / 1000.0
    else:
        timestamp_value = float(
            _get_field(tick, "time")
        )

    timestamp = datetime.fromtimestamp(
        timestamp_value,
        tz=timezone.utc,
    )

    real_volume = float(
        _get_field(tick, "volume_real", 0) or 0
    )

    integer_volume = _get_field(
        tick,
        "volume",
        None,
    )

    if real_volume > 0:
        volume = real_volume
        volume_type = VolumeType.REAL

    elif (
        integer_volume is not None
        and float(integer_volume) > 0
    ):
        volume = float(integer_volume)
        volume_type = VolumeType.CONTRACTS

    else:
        volume = None
        volume_type = VolumeType.NONE

    return TickData(
        instrument_id=instrument_id,
        timestamp=timestamp,
        bid=float(_get_field(tick, "bid")),
        ask=float(_get_field(tick, "ask")),
        last=float(_get_field(tick, "last")),
        volume=volume,
        volume_type=volume_type,
        source="mt5",
    )