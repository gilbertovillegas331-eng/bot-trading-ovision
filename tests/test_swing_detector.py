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
