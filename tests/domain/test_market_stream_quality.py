from domain.instrument import InstrumentId
from domain.market_stream import DataQuality, MarketStreamKey
from domain.timeframe import Timeframe


def test_candle_stream_key_can_be_created():
    key = MarketStreamKey(
        instrument_id=InstrumentId("EURUSD"),
        timeframe=Timeframe.from_minutes(15),
    )

    assert key.instrument_id == InstrumentId("EURUSD")
    assert key.timeframe == Timeframe.from_minutes(15)


def test_tick_stream_key_can_have_no_timeframe():
    key = MarketStreamKey(
        instrument_id=InstrumentId("EURUSD"),
        timeframe=None,
    )

    assert key.timeframe is None


def test_equivalent_stream_keys_compare_equal():
    first = MarketStreamKey(
        instrument_id=InstrumentId("EURUSD"),
        timeframe=Timeframe.from_minutes(15),
    )

    second = MarketStreamKey(
        instrument_id=InstrumentId("EURUSD"),
        timeframe=Timeframe(seconds=900),
    )

    assert first == second


def test_stream_key_is_hashable():
    first = MarketStreamKey(
        instrument_id=InstrumentId("EURUSD"),
        timeframe=Timeframe.from_minutes(15),
    )

    second = MarketStreamKey(
        instrument_id=InstrumentId("EURUSD"),
        timeframe=Timeframe(seconds=900),
    )

    values = {first, second}

    assert len(values) == 1


def test_different_timeframes_produce_different_stream_keys():
    m5 = MarketStreamKey(
        instrument_id=InstrumentId("EURUSD"),
        timeframe=Timeframe.from_minutes(5),
    )

    m15 = MarketStreamKey(
        instrument_id=InstrumentId("EURUSD"),
        timeframe=Timeframe.from_minutes(15),
    )

    assert m5 != m15


def test_different_instruments_produce_different_stream_keys():
    eurusd = MarketStreamKey(
        instrument_id=InstrumentId("EURUSD"),
        timeframe=Timeframe.from_minutes(15),
    )

    gbpusd = MarketStreamKey(
        instrument_id=InstrumentId("GBPUSD"),
        timeframe=Timeframe.from_minutes(15),
    )

    assert eurusd != gbpusd


def test_data_quality_has_stable_canonical_values():
    assert DataQuality.GOOD.value == "good"
    assert DataQuality.STALE.value == "stale"
    assert DataQuality.GAP.value == "gap"
    assert DataQuality.INVALID.value == "invalid"


def test_data_quality_contains_expected_states():
    assert set(DataQuality) == {
        DataQuality.GOOD,
        DataQuality.STALE,
        DataQuality.GAP,
        DataQuality.INVALID,
    }


def test_stream_key_does_not_depend_on_provider_symbol():
    key = MarketStreamKey(
        instrument_id=InstrumentId("EURUSD"),
        timeframe=Timeframe.from_minutes(15),
    )

    assert not hasattr(key, "provider_symbol")
    assert not hasattr(key, "provider")