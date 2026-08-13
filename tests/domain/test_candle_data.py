from datetime import datetime, timezone

import pytest

from domain.candle import CandleData
from domain.instrument import InstrumentId, VolumeType
from domain.timeframe import Timeframe


def make_candle(**overrides):
    values = {
        "instrument_id": InstrumentId("EURUSD"),
        "timeframe": Timeframe.from_minutes(15),
        "open_time": datetime(
            2026, 1, 1, 12, 0,
            tzinfo=timezone.utc,
        ),
        "close_time": datetime(
            2026, 1, 1, 12, 15,
            tzinfo=timezone.utc,
        ),
        "open": 1.1000,
        "high": 1.1050,
        "low": 1.0950,
        "close": 1.1020,
        "volume": 1200,
        "volume_type": VolumeType.TICK,
        "is_closed": True,
        "source": "test",
    }

    values.update(overrides)
    return CandleData(**values)


def test_valid_candle_can_be_created():
    candle = make_candle()

    assert candle.open == 1.1000
    assert candle.high == 1.1050
    assert candle.low == 1.0950
    assert candle.close == 1.1020
    assert candle.is_closed is True


def test_rejects_open_above_high():
    with pytest.raises(ValueError):
        make_candle(open=1.1100)


def test_rejects_close_above_high():
    with pytest.raises(ValueError):
        make_candle(close=1.1100)


def test_rejects_open_below_low():
    with pytest.raises(ValueError):
        make_candle(open=1.0900)


def test_rejects_close_below_low():
    with pytest.raises(ValueError):
        make_candle(close=1.0900)


def test_rejects_high_below_low():
    with pytest.raises(ValueError):
        make_candle(high=1.0900)


def test_rejects_naive_open_time():
    with pytest.raises(ValueError):
        make_candle(
            open_time=datetime(2026, 1, 1, 12, 0)
        )


def test_close_time_must_be_after_open_time():
    timestamp = datetime(
        2026, 1, 1, 12, 0,
        tzinfo=timezone.utc,
    )

    with pytest.raises(ValueError):
        make_candle(
            open_time=timestamp,
            close_time=timestamp,
        )

@pytest.mark.parametrize(
    "field",
    ["open", "high", "low", "close"],
)
@pytest.mark.parametrize(
    "invalid_value",
    [
        float("nan"),
        float("inf"),
        float("-inf"),
    ],
)
def test_rejects_non_finite_prices(field, invalid_value):
    with pytest.raises(ValueError):
        make_candle(**{field: invalid_value})


def test_rejects_naive_close_time():
    with pytest.raises(ValueError):
        make_candle(
            close_time=datetime(2026, 1, 1, 12, 15)
        )


def test_candle_can_have_no_volume():
    candle = make_candle(
        volume=None,
        volume_type=VolumeType.NONE,
    )

    assert candle.volume is None


def test_volume_cannot_be_negative():
    with pytest.raises(ValueError):
        make_candle(
            volume=-1,
            volume_type=VolumeType.TICK,
        )


def test_volume_must_be_finite():
    with pytest.raises(ValueError):
        make_candle(
            volume=float("nan"),
            volume_type=VolumeType.TICK,
        )


def test_volume_type_none_requires_no_volume():
    with pytest.raises(ValueError):
        make_candle(
            volume=100,
            volume_type=VolumeType.NONE,
        )


def test_missing_volume_requires_none_volume_type():
    with pytest.raises(ValueError):
        make_candle(
            volume=None,
            volume_type=VolumeType.TICK,
        )


def test_source_cannot_be_empty():
    with pytest.raises(ValueError):
        make_candle(source="   ")


def test_source_whitespace_is_normalized():
    candle = make_candle(source="  mt5  ")

    assert candle.source == "mt5"


def test_forming_candle_is_valid():
    candle = make_candle(is_closed=False)

    assert candle.is_closed is False


def test_negative_prices_are_allowed_when_ohlc_is_valid():
    candle = make_candle(
        open=-1.0,
        high=0.0,
        low=-2.0,
        close=-0.5,
    )

    assert candle.close == -0.5