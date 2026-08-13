import pytest

from domain.market_type import MarketType
from domain.timeframe import Timeframe


def test_market_type_contains_supported_markets():
    assert set(MarketType) == {
        MarketType.FOREX,
        MarketType.INDEX,
        MarketType.SYNTHETIC_INDEX,
        MarketType.FUTURES,
    }


def test_market_type_has_stable_canonical_values():
    assert MarketType.FOREX.value == "forex"
    assert MarketType.INDEX.value == "index"
    assert MarketType.SYNTHETIC_INDEX.value == "synthetic_index"
    assert MarketType.FUTURES.value == "futures"


def test_timeframe_can_be_created_from_minutes():
    timeframe = Timeframe.from_minutes(15)

    assert timeframe.seconds == 900


def test_equivalent_timeframes_compare_equal():
    assert Timeframe.from_minutes(60) == Timeframe.from_hours(1)


def test_timeframe_rejects_zero_duration():
    with pytest.raises(ValueError):
        Timeframe(seconds=0)


def test_timeframe_rejects_negative_duration():
    with pytest.raises(ValueError):
        Timeframe(seconds=-60)


def test_timeframe_is_hashable():
    values = {
        Timeframe.from_minutes(15),
        Timeframe(seconds=900),
    }

    assert len(values) == 1


def test_timeframes_can_be_ordered():
    m5 = Timeframe.from_minutes(5)
    m15 = Timeframe.from_minutes(15)
    h1 = Timeframe.from_hours(1)

    assert m5 < m15 < h1


def test_timeframe_exposes_timedelta_duration():
    timeframe = Timeframe.from_minutes(15)

    assert timeframe.duration.total_seconds() == 900