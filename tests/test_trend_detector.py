import pytest

from engines.structure.trend_detector import TrendDetector
from models.structure import Swing, SwingType, Trend


def test_detect_bullish_trend():
    swings = [
        Swing(
            kind=SwingType.HIGH,
            index=0,
            price=100.0,
            time=0,
        ),
        Swing(
            kind=SwingType.LOW,
            index=1,
            price=90.0,
            time=1,
        ),
        Swing(
            kind=SwingType.HIGH,
            index=2,
            price=110.0,
            time=2,
        ),
        Swing(
            kind=SwingType.LOW,
            index=3,
            price=95.0,
            time=3,
        ),
    ]

    trend = TrendDetector().detect(swings)

    assert trend == Trend.BULLISH


def test_detect_bearish_trend():
    swings = [
        Swing(
            kind=SwingType.HIGH,
            index=0,
            price=100.0,
            time=0,
        ),
        Swing(
            kind=SwingType.LOW,
            index=1,
            price=90.0,
            time=1,
        ),
        Swing(
            kind=SwingType.HIGH,
            index=2,
            price=95.0,
            time=2,
        ),
        Swing(
            kind=SwingType.LOW,
            index=3,
            price=80.0,
            time=3,
        ),
    ]

    trend = TrendDetector().detect(swings)

    assert trend == Trend.BEARISH


def test_detect_neutral_without_enough_swings():
    swings = [
        Swing(
            kind=SwingType.HIGH,
            index=0,
            price=100.0,
            time=0,
        ),
        Swing(
            kind=SwingType.LOW,
            index=1,
            price=90.0,
            time=1,
        ),
    ]

    trend = TrendDetector().detect(swings)

    assert trend == Trend.NEUTRAL