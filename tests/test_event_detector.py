from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from engines.structure.event_detector import (
    StructureEventDetector,
    StructureEvent,
)

from models.structure import Trend, StructureType


def test_bullish_bos():
    detector = StructureEventDetector()

    result = detector.detect(
        Trend.BULLISH,
        StructureType.HH
    )

    assert result.event == StructureEvent.BOS
    assert result.new_trend == Trend.BULLISH


def test_bearish_bos():
    detector = StructureEventDetector()

    result = detector.detect(
        Trend.BEARISH,
        StructureType.LL
    )

    assert result.event == StructureEvent.BOS
    assert result.new_trend == Trend.BEARISH


def test_bullish_choch():
    detector = StructureEventDetector()

    result = detector.detect(
        Trend.BULLISH,
        StructureType.LL
    )

    assert result.event == StructureEvent.CHOCH
    assert result.new_trend == Trend.BEARISH


def test_bearish_choch():
    detector = StructureEventDetector()

    result = detector.detect(
        Trend.BEARISH,
        StructureType.HH
    )

    assert result.event == StructureEvent.CHOCH
    assert result.new_trend == Trend.BULLISH