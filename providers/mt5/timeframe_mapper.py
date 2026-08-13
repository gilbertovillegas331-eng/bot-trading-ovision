from __future__ import annotations

import MetaTrader5 as mt5

from domain.timeframe import Timeframe


_DOMAIN_TO_MT5 = {
    Timeframe.from_minutes(1): mt5.TIMEFRAME_M1,
    Timeframe.from_minutes(5): mt5.TIMEFRAME_M5,
    Timeframe.from_minutes(15): mt5.TIMEFRAME_M15,
    Timeframe.from_minutes(30): mt5.TIMEFRAME_M30,
    Timeframe.from_hours(1): mt5.TIMEFRAME_H1,
    Timeframe.from_hours(4): mt5.TIMEFRAME_H4,
    Timeframe.from_days(1): mt5.TIMEFRAME_D1,
    Timeframe.from_days(7): mt5.TIMEFRAME_W1,
}

_MT5_TO_DOMAIN = {
    mt5_timeframe: timeframe
    for timeframe, mt5_timeframe in _DOMAIN_TO_MT5.items()
}


def to_mt5_timeframe(timeframe: Timeframe) -> int:
    if not isinstance(timeframe, Timeframe):
        raise TypeError(
            "timeframe must be a Timeframe"
        )

    try:
        return _DOMAIN_TO_MT5[timeframe]
    except KeyError as exc:
        raise ValueError(
            f"unsupported domain timeframe: "
            f"{timeframe.seconds} seconds"
        ) from exc


def from_mt5_timeframe(mt5_timeframe: int) -> Timeframe:
    if isinstance(mt5_timeframe, bool):
        raise TypeError(
            "mt5_timeframe must be an integer"
        )

    if not isinstance(mt5_timeframe, int):
        raise TypeError(
            "mt5_timeframe must be an integer"
        )

    try:
        return _MT5_TO_DOMAIN[mt5_timeframe]
    except KeyError as exc:
        raise ValueError(
            f"unsupported MT5 timeframe: "
            f"{mt5_timeframe}"
        ) from exc