from datetime import datetime, timezone

import pytest

from domain.instrument import InstrumentId, VolumeType
from domain.tick import TickData


def make_tick(**overrides):
    values = {
        "instrument_id": InstrumentId("EURUSD"),
        "timestamp": datetime(
            2026, 1, 1, 12, 0,
            tzinfo=timezone.utc,
        ),
        "bid": 1.1019,
        "ask": 1.1021,
        "last": 1.1020,
        "volume": 100,
        "volume_type": VolumeType.TICK,
        "source": "test",
    }

    values.update(overrides)
    return TickData(**values)


def test_valid_tick_can_be_created():
    tick = make_tick()

    assert tick.bid == 1.1019
    assert tick.ask == 1.1021
    assert tick.last == 1.1020


def test_timestamp_must_be_utc():
    with pytest.raises(ValueError):
        make_tick(
            timestamp=datetime(2026, 1, 1, 12, 0)
        )


def test_at_least_one_price_is_required():
    with pytest.raises(ValueError):
        make_tick(
            bid=None,
            ask=None,
            last=None,
        )


def test_bid_only_tick_is_valid():
    tick = make_tick(
        ask=None,
        last=None,
    )

    assert tick.bid == 1.1019


def test_ask_only_tick_is_valid():
    tick = make_tick(
        bid=None,
        last=None,
    )

    assert tick.ask == 1.1021


def test_last_only_tick_is_valid():
    tick = make_tick(
        bid=None,
        ask=None,
        last=4500.25,
    )

    assert tick.last == 4500.25


def test_bid_cannot_be_above_ask():
    with pytest.raises(ValueError):
        make_tick(
            bid=1.1030,
            ask=1.1020,
        )


def test_equal_bid_and_ask_are_allowed():
    tick = make_tick(
        bid=1.1020,
        ask=1.1020,
    )

    assert tick.bid == tick.ask


@pytest.mark.parametrize(
    "field",
    ["bid", "ask", "last"],
)
@pytest.mark.parametrize(
    "invalid_value",
    [
        float("nan"),
        float("inf"),
        float("-inf"),
    ],
)
def test_prices_must_be_finite(field, invalid_value):
    with pytest.raises(ValueError):
        make_tick(**{field: invalid_value})


def test_negative_prices_are_allowed():
    tick = make_tick(
        bid=-2.0,
        ask=-1.0,
        last=-1.5,
    )

    assert tick.last == -1.5


def test_tick_can_have_no_volume():
    tick = make_tick(
        volume=None,
        volume_type=VolumeType.NONE,
    )

    assert tick.volume is None


def test_volume_cannot_be_negative():
    with pytest.raises(ValueError):
        make_tick(
            volume=-1,
            volume_type=VolumeType.TICK,
        )


def test_volume_must_be_finite():
    with pytest.raises(ValueError):
        make_tick(
            volume=float("nan"),
            volume_type=VolumeType.TICK,
        )


def test_volume_type_none_requires_no_volume():
    with pytest.raises(ValueError):
        make_tick(
            volume=100,
            volume_type=VolumeType.NONE,
        )


def test_missing_volume_requires_none_volume_type():
    with pytest.raises(ValueError):
        make_tick(
            volume=None,
            volume_type=VolumeType.TICK,
        )


def test_source_cannot_be_empty():
    with pytest.raises(ValueError):
        make_tick(source="   ")


def test_source_whitespace_is_normalized():
    tick = make_tick(source="  mt5  ")

    assert tick.source == "mt5"


def test_source_must_be_string():
    with pytest.raises(TypeError):
        make_tick(source=123)