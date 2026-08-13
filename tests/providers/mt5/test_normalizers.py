from datetime import datetime, timezone

import pytest

from domain.candle import CandleData, VolumeType
from domain.instrument import InstrumentId
from domain.tick import TickData
from domain.timeframe import Timeframe
from providers.mt5.normalizers import (
    normalize_mt5_rate,
    normalize_mt5_tick,
)


def test_normalize_mt5_rate_returns_candle_data():
    rate = {
        "time": 1767268800,
        "open": 1.1000,
        "high": 1.1050,
        "low": 1.0950,
        "close": 1.1020,
        "tick_volume": 125,
        "real_volume": 0,
    }

    candle = normalize_mt5_rate(
        rate,
        instrument_id=InstrumentId("EURUSD"),
        timeframe=Timeframe.from_minutes(15),
    )

    assert isinstance(candle, CandleData)
    assert candle.instrument_id == InstrumentId("EURUSD")
    assert candle.timeframe == Timeframe.from_minutes(15)


def test_normalize_mt5_rate_maps_ohlc():
    rate = {
        "time": 1767268800,
        "open": 1.1000,
        "high": 1.1050,
        "low": 1.0950,
        "close": 1.1020,
        "tick_volume": 125,
        "real_volume": 0,
    }

    candle = normalize_mt5_rate(
        rate,
        instrument_id=InstrumentId("EURUSD"),
        timeframe=Timeframe.from_minutes(15),
    )

    assert candle.open == 1.1000
    assert candle.high == 1.1050
    assert candle.low == 1.0950
    assert candle.close == 1.1020


def test_normalize_mt5_rate_uses_utc():
    rate = {
        "time": 1767268800,
        "open": 1.1000,
        "high": 1.1050,
        "low": 1.0950,
        "close": 1.1020,
        "tick_volume": 125,
        "real_volume": 0,
    }

    candle = normalize_mt5_rate(
        rate,
        instrument_id=InstrumentId("EURUSD"),
        timeframe=Timeframe.from_minutes(15),
    )

    assert candle.open_time.tzinfo == timezone.utc
    assert candle.close_time.tzinfo == timezone.utc


def test_normalize_mt5_rate_derives_close_time_from_timeframe():
    rate = {
        "time": 1767268800,
        "open": 1.1000,
        "high": 1.1050,
        "low": 1.0950,
        "close": 1.1020,
        "tick_volume": 125,
        "real_volume": 0,
    }

    candle = normalize_mt5_rate(
        rate,
        instrument_id=InstrumentId("EURUSD"),
        timeframe=Timeframe.from_minutes(15),
    )

    assert (
        candle.close_time - candle.open_time
    ).total_seconds() == 900


def test_normalize_mt5_rate_uses_tick_volume_when_real_is_zero():
    rate = {
        "time": 1767268800,
        "open": 1.1000,
        "high": 1.1050,
        "low": 1.0950,
        "close": 1.1020,
        "tick_volume": 125,
        "real_volume": 0,
    }

    candle = normalize_mt5_rate(
        rate,
        instrument_id=InstrumentId("EURUSD"),
        timeframe=Timeframe.from_minutes(15),
    )

    assert candle.volume == 125.0
    assert candle.volume_type is VolumeType.TICK


def test_normalize_mt5_rate_prefers_real_volume_when_available():
    rate = {
        "time": 1767268800,
        "open": 100.0,
        "high": 105.0,
        "low": 95.0,
        "close": 102.0,
        "tick_volume": 125,
        "real_volume": 42,
    }

    candle = normalize_mt5_rate(
        rate,
        instrument_id=InstrumentId("NQ"),
        timeframe=Timeframe.from_minutes(15),
    )

    assert candle.volume == 42.0
    assert candle.volume_type is VolumeType.REAL


def test_normalize_mt5_rate_marks_closed_by_default():
    rate = {
        "time": 1767268800,
        "open": 1.1000,
        "high": 1.1050,
        "low": 1.0950,
        "close": 1.1020,
        "tick_volume": 125,
        "real_volume": 0,
    }

    candle = normalize_mt5_rate(
        rate,
        instrument_id=InstrumentId("EURUSD"),
        timeframe=Timeframe.from_minutes(15),
    )

    assert candle.is_closed is True


def test_normalize_mt5_rate_can_mark_forming_candle():
    rate = {
        "time": 1767268800,
        "open": 1.1000,
        "high": 1.1050,
        "low": 1.0950,
        "close": 1.1020,
        "tick_volume": 125,
        "real_volume": 0,
    }

    candle = normalize_mt5_rate(
        rate,
        instrument_id=InstrumentId("EURUSD"),
        timeframe=Timeframe.from_minutes(15),
        is_closed=False,
    )

    assert candle.is_closed is False


def test_normalize_mt5_rate_sets_mt5_source():
    rate = {
        "time": 1767268800,
        "open": 1.1000,
        "high": 1.1050,
        "low": 1.0950,
        "close": 1.1020,
        "tick_volume": 125,
        "real_volume": 0,
    }

    candle = normalize_mt5_rate(
        rate,
        instrument_id=InstrumentId("EURUSD"),
        timeframe=Timeframe.from_minutes(15),
    )

    assert candle.source == "mt5"


def test_normalize_mt5_tick_returns_tick_data():
    tick = {
        "time": 1767268800,
        "time_msc": 1767268800123,
        "bid": 1.1019,
        "ask": 1.1021,
        "last": 1.1020,
        "volume": 0,
        "volume_real": 0.0,
    }

    result = normalize_mt5_tick(
        tick,
        instrument_id=InstrumentId("EURUSD"),
    )

    assert isinstance(result, TickData)
    assert result.instrument_id == InstrumentId("EURUSD")


def test_normalize_mt5_tick_maps_prices():
    tick = {
        "time": 1767268800,
        "time_msc": 1767268800123,
        "bid": 1.1019,
        "ask": 1.1021,
        "last": 1.1020,
        "volume": 0,
        "volume_real": 0.0,
    }

    result = normalize_mt5_tick(
        tick,
        instrument_id=InstrumentId("EURUSD"),
    )

    assert result.bid == 1.1019
    assert result.ask == 1.1021
    assert result.last == 1.1020


def test_normalize_mt5_tick_uses_millisecond_timestamp():
    tick = {
        "time": 1767268800,
        "time_msc": 1767268800123,
        "bid": 1.1019,
        "ask": 1.1021,
        "last": 1.1020,
        "volume": 0,
        "volume_real": 0.0,
    }

    result = normalize_mt5_tick(
        tick,
        instrument_id=InstrumentId("EURUSD"),
    )

    expected = datetime.fromtimestamp(
        1767268800.123,
        tz=timezone.utc,
    )

    assert result.timestamp == expected


def test_normalize_mt5_tick_falls_back_to_seconds_timestamp():
    tick = {
        "time": 1767268800,
        "bid": 1.1019,
        "ask": 1.1021,
        "last": 1.1020,
        "volume": 0,
        "volume_real": 0.0,
    }

    result = normalize_mt5_tick(
        tick,
        instrument_id=InstrumentId("EURUSD"),
    )

    expected = datetime.fromtimestamp(
        1767268800,
        tz=timezone.utc,
    )

    assert result.timestamp == expected


def test_normalize_mt5_tick_without_volume_uses_none():
    tick = {
        "time": 1767268800,
        "bid": 1.1019,
        "ask": 1.1021,
        "last": 1.1020,
        "volume": 0,
        "volume_real": 0.0,
    }

    result = normalize_mt5_tick(
        tick,
        instrument_id=InstrumentId("EURUSD"),
    )

    assert result.volume is None
    assert result.volume_type is VolumeType.NONE


def test_normalize_mt5_tick_uses_real_volume_when_available():
    tick = {
        "time": 1767268800,
        "bid": 100.0,
        "ask": 100.25,
        "last": 100.25,
        "volume": 5,
        "volume_real": 5.0,
    }

    result = normalize_mt5_tick(
        tick,
        instrument_id=InstrumentId("NQ"),
    )

    assert result.volume == 5.0
    assert result.volume_type is VolumeType.REAL


def test_normalize_mt5_tick_sets_mt5_source():
    tick = {
        "time": 1767268800,
        "bid": 1.1019,
        "ask": 1.1021,
        "last": 1.1020,
        "volume": 0,
        "volume_real": 0.0,
    }

    result = normalize_mt5_tick(
        tick,
        instrument_id=InstrumentId("EURUSD"),
    )

    assert result.source == "mt5"


def test_rate_normalizer_requires_instrument_id():
    rate = {
        "time": 1767268800,
        "open": 1.1000,
        "high": 1.1050,
        "low": 1.0950,
        "close": 1.1020,
        "tick_volume": 125,
        "real_volume": 0,
    }

    with pytest.raises(TypeError):
        normalize_mt5_rate(
            rate,
            instrument_id="EURUSD",
            timeframe=Timeframe.from_minutes(15),
        )


def test_rate_normalizer_requires_timeframe():
    rate = {
        "time": 1767268800,
        "open": 1.1000,
        "high": 1.1050,
        "low": 1.0950,
        "close": 1.1020,
        "tick_volume": 125,
        "real_volume": 0,
    }

    with pytest.raises(TypeError):
        normalize_mt5_rate(
            rate,
            instrument_id=InstrumentId("EURUSD"),
            timeframe="M15",
        )


def test_tick_normalizer_requires_instrument_id():
    tick = {
        "time": 1767268800,
        "bid": 1.1019,
        "ask": 1.1021,
        "last": 1.1020,
        "volume": 0,
        "volume_real": 0.0,
    }

    with pytest.raises(TypeError):
        normalize_mt5_tick(
            tick,
            instrument_id="EURUSD",
        )