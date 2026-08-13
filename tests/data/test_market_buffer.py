import pytest

from data.market_buffer import MarketBuffer
from domain.instrument import InstrumentId
from domain.market_stream import MarketStreamKey
from domain.timeframe import Timeframe


def make_candle_key(
    symbol="EURUSD",
    minutes=15,
):
    return MarketStreamKey(
        instrument_id=InstrumentId(symbol),
        timeframe=Timeframe.from_minutes(minutes),
    )


def make_tick_key(symbol="EURUSD"):
    return MarketStreamKey(
        instrument_id=InstrumentId(symbol),
        timeframe=None,
    )


def test_buffer_can_be_created():
    buffer = MarketBuffer(capacity=3)

    assert buffer.capacity == 3


@pytest.mark.parametrize(
    "capacity",
    [0, -1, -10],
)
def test_capacity_must_be_positive(capacity):
    with pytest.raises(ValueError):
        MarketBuffer(capacity=capacity)


@pytest.mark.parametrize(
    "capacity",
    [True, 1.5, "3", None],
)
def test_capacity_must_be_integer(capacity):
    with pytest.raises(TypeError):
        MarketBuffer(capacity=capacity)


def test_append_preserves_order():
    buffer = MarketBuffer(capacity=3)
    key = make_candle_key()

    buffer.append(key, "first")
    buffer.append(key, "second")
    buffer.append(key, "third")

    assert buffer.snapshot(key) == (
        "first",
        "second",
        "third",
    )


def test_latest_returns_most_recent_item():
    buffer = MarketBuffer(capacity=3)
    key = make_candle_key()

    buffer.append(key, "first")
    buffer.append(key, "second")

    assert buffer.latest(key) == "second"


def test_unknown_stream_has_empty_snapshot():
    buffer = MarketBuffer(capacity=3)
    key = make_candle_key()

    assert buffer.snapshot(key) == ()


def test_unknown_stream_has_no_latest_item():
    buffer = MarketBuffer(capacity=3)
    key = make_candle_key()

    assert buffer.latest(key) is None


def test_capacity_discards_oldest_item():
    buffer = MarketBuffer(capacity=3)
    key = make_candle_key()

    buffer.append(key, "one")
    buffer.append(key, "two")
    buffer.append(key, "three")
    buffer.append(key, "four")

    assert buffer.snapshot(key) == (
        "two",
        "three",
        "four",
    )


def test_different_instruments_are_isolated():
    buffer = MarketBuffer(capacity=3)

    eurusd = make_candle_key("EURUSD")
    gbpusd = make_candle_key("GBPUSD")

    buffer.append(eurusd, "eurusd-data")
    buffer.append(gbpusd, "gbpusd-data")

    assert buffer.snapshot(eurusd) == (
        "eurusd-data",
    )
    assert buffer.snapshot(gbpusd) == (
        "gbpusd-data",
    )


def test_different_timeframes_are_isolated():
    buffer = MarketBuffer(capacity=3)

    m5 = make_candle_key(minutes=5)
    m15 = make_candle_key(minutes=15)

    buffer.append(m5, "m5-data")
    buffer.append(m15, "m15-data")

    assert buffer.snapshot(m5) == ("m5-data",)
    assert buffer.snapshot(m15) == ("m15-data",)


def test_tick_and_candle_streams_are_isolated():
    buffer = MarketBuffer(capacity=3)

    tick_key = make_tick_key()
    candle_key = make_candle_key()

    buffer.append(tick_key, "tick-data")
    buffer.append(candle_key, "candle-data")

    assert buffer.snapshot(tick_key) == (
        "tick-data",
    )
    assert buffer.snapshot(candle_key) == (
        "candle-data",
    )


def test_snapshot_is_immutable_tuple():
    buffer = MarketBuffer(capacity=3)
    key = make_candle_key()

    buffer.append(key, "data")

    snapshot = buffer.snapshot(key)

    assert isinstance(snapshot, tuple)


def test_clear_removes_only_selected_stream():
    buffer = MarketBuffer(capacity=3)

    eurusd = make_candle_key("EURUSD")
    gbpusd = make_candle_key("GBPUSD")

    buffer.append(eurusd, "eurusd-data")
    buffer.append(gbpusd, "gbpusd-data")

    buffer.clear(eurusd)

    assert buffer.snapshot(eurusd) == ()
    assert buffer.snapshot(gbpusd) == (
        "gbpusd-data",
    )


def test_clear_without_key_removes_all_streams():
    buffer = MarketBuffer(capacity=3)

    eurusd = make_candle_key("EURUSD")
    gbpusd = make_candle_key("GBPUSD")

    buffer.append(eurusd, "eurusd-data")
    buffer.append(gbpusd, "gbpusd-data")

    buffer.clear()

    assert buffer.snapshot(eurusd) == ()
    assert buffer.snapshot(gbpusd) == ()


def test_append_requires_market_stream_key():
    buffer = MarketBuffer(capacity=3)

    with pytest.raises(TypeError):
        buffer.append("EURUSD-M15", "data")