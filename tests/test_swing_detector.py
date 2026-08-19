import pytest
from engines.structure.swing_detector import SwingDetector, SwingType
from models.market_data import MarketData


def candle(index: int, high: float, low: float) -> MarketData:
    return MarketData(
        symbol="TEST",
        timeframe="M1",
        time=index,
        open=(high + low) / 2,
        high=high,
        low=low,
        close=(high + low) / 2,
        bid=1.0,
        ask=1.1,
        tick_volume=1,
    )


def test_detects_swing_high():
    candles = [
        candle(0, 2, 1),
        candle(1, 3, 1),
        candle(2, 5, 1),
        candle(3, 3, 1),
        candle(4, 2, 1),
    ]
    swings = SwingDetector().detect(candles)
    assert any(s.kind == SwingType.HIGH and s.index == 2 for s in swings)
def test_detects_swing_low():
    candles = [
        candle(0, 5, 3),
        candle(1, 5, 2),
        candle(2, 5, 1),
        candle(3, 5, 2),
        candle(4, 5, 3),
    ]

    swings = SwingDetector().detect(candles)

    assert any(
        s.kind == SwingType.LOW and s.index == 2 and s.price == 1
        for s in swings
    )


def test_returns_empty_when_candles_are_insufficient():
    candles = [
        candle(0, 2, 1),
        candle(1, 3, 1),
        candle(2, 4, 1),
        candle(3, 3, 1),
    ]

    swings = SwingDetector().detect(candles)

    assert swings == []


def test_equal_high_is_not_confirmed_as_swing_high():
    candles = [
        candle(0, 2, 1),
        candle(1, 5, 1),
        candle(2, 5, 1),
        candle(3, 3, 1),
        candle(4, 2, 1),
    ]

    swings = SwingDetector().detect(candles)

    assert not any(
        s.kind == SwingType.HIGH and s.index == 2
        for s in swings
    )


def test_rejects_invalid_confirmation_window():
    with pytest.raises(ValueError):
        SwingDetector(left_bars=0, right_bars=2)

    with pytest.raises(ValueError):
        SwingDetector(left_bars=2, right_bars=0)
