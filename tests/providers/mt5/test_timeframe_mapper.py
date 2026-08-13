import pytest
import MetaTrader5 as mt5

from domain.timeframe import Timeframe
from providers.mt5.timeframe_mapper import (
    from_mt5_timeframe,
    to_mt5_timeframe,
)


@pytest.mark.parametrize(
    ("timeframe", "mt5_timeframe"),
    [
        (Timeframe.from_minutes(1), mt5.TIMEFRAME_M1),
        (Timeframe.from_minutes(5), mt5.TIMEFRAME_M5),
        (Timeframe.from_minutes(15), mt5.TIMEFRAME_M15),
        (Timeframe.from_minutes(30), mt5.TIMEFRAME_M30),
        (Timeframe.from_hours(1), mt5.TIMEFRAME_H1),
        (Timeframe.from_hours(4), mt5.TIMEFRAME_H4),
        (Timeframe.from_days(1), mt5.TIMEFRAME_D1),
        (Timeframe.from_days(7), mt5.TIMEFRAME_W1),
    ],
)
def test_maps_domain_timeframe_to_mt5(
    timeframe,
    mt5_timeframe,
):
    assert to_mt5_timeframe(timeframe) == mt5_timeframe


@pytest.mark.parametrize(
    ("mt5_timeframe", "timeframe"),
    [
        (mt5.TIMEFRAME_M1, Timeframe.from_minutes(1)),
        (mt5.TIMEFRAME_M5, Timeframe.from_minutes(5)),
        (mt5.TIMEFRAME_M15, Timeframe.from_minutes(15)),
        (mt5.TIMEFRAME_M30, Timeframe.from_minutes(30)),
        (mt5.TIMEFRAME_H1, Timeframe.from_hours(1)),
        (mt5.TIMEFRAME_H4, Timeframe.from_hours(4)),
        (mt5.TIMEFRAME_D1, Timeframe.from_days(1)),
        (mt5.TIMEFRAME_W1, Timeframe.from_days(7)),
    ],
)
def test_maps_mt5_timeframe_to_domain(
    mt5_timeframe,
    timeframe,
):
    assert from_mt5_timeframe(mt5_timeframe) == timeframe


def test_round_trip_preserves_timeframe():
    original = Timeframe.from_minutes(15)

    mapped = to_mt5_timeframe(original)
    restored = from_mt5_timeframe(mapped)

    assert restored == original


def test_rejects_domain_timeframe_not_supported_by_mt5_mapper():
    with pytest.raises(ValueError):
        to_mt5_timeframe(Timeframe.from_minutes(7))


def test_rejects_unknown_mt5_timeframe():
    with pytest.raises(ValueError):
        from_mt5_timeframe(999999)


def test_monthly_mt5_timeframe_is_not_forced_into_fixed_seconds():
    with pytest.raises(ValueError):
        from_mt5_timeframe(mt5.TIMEFRAME_MN1)


def test_to_mt5_requires_timeframe_object():
    with pytest.raises(TypeError):
        to_mt5_timeframe("M15")


def test_mapper_does_not_require_mt5_terminal_connection():
    result = to_mt5_timeframe(
        Timeframe.from_minutes(15)
    )

    assert result == mt5.TIMEFRAME_M15